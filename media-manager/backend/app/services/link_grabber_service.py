"""Link grabber service for extracting download links from container sites."""

import logging
import re
from typing import Dict, List, Optional
from urllib.parse import urlparse, parse_qs

import requests
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)


class LinkGrabberService:
    """Service for extracting download links from various container sites."""

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        })

    def extract_links(self, url: str) -> Dict[str, any]:
        """
        Extract download links from a container URL.

        Args:
            url: Container URL (FileCrypt.cc, etc.)

        Returns:
            Dictionary with:
                - source: Container source (filecrypt, etc.)
                - name: Container name
                - links: List of download URLs
                - password: Password if found
        """
        parsed = urlparse(url)
        domain = parsed.netloc.lower()

        if "filecrypt" in domain:
            return self._parse_filecrypt(url)
        else:
            # Generic link extraction
            return self._parse_generic(url)

    def _parse_filecrypt(self, url: str) -> Dict[str, any]:
        """
        Parse FileCrypt.cc container.

        Args:
            url: FileCrypt.cc container URL

        Returns:
            Dictionary with extracted links and metadata
        """
        try:
            logger.info(f"Parsing FileCrypt container: {url}")

            # Fetch the page
            response = self.session.get(url, timeout=30)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, "html.parser")

            # Extract container name
            container_name = "FileCrypt Container"
            title_elem = soup.find("h1")
            if title_elem:
                container_name = title_elem.text.strip()

            # Extract password if visible
            password = None
            password_elem = soup.find("input", {"name": "password"})
            if password_elem and password_elem.get("value"):
                password = password_elem.get("value")

            # Alternative: password in text
            password_match = re.search(r"Password:\s*(\S+)", response.text, re.IGNORECASE)
            if password_match:
                password = password_match.group(1)

            # Extract download links
            links = []

            # Method 1: Look for links in the page
            # FileCrypt usually has links in <a> tags with specific classes or patterns
            link_elements = soup.find_all("a", href=re.compile(r"(rapidgator|uploaded|ddl|nitro|ddownload)", re.I))
            for elem in link_elements:
                href = elem.get("href", "")
                if href and href.startswith("http"):
                    links.append(href)

            # Method 2: Look for mirror links (FileCrypt.cc specific)
            # FileCrypt uses a mirror parameter in the URL
            mirror_links = soup.find_all("a", {"class": re.compile(r"mirror", re.I)})
            for elem in mirror_links:
                onclick = elem.get("onclick", "")
                # Extract URL from onclick
                url_match = re.search(r"['\"](https?://[^'\"]+)['\"]", onclick)
                if url_match:
                    links.append(url_match.group(1))

            # Method 3: Look in JavaScript variables
            # FileCrypt sometimes stores links in JS arrays
            script_tags = soup.find_all("script")
            for script in script_tags:
                if script.string:
                    # Look for URLs in JavaScript
                    js_urls = re.findall(r'https?://(?:rapidgator|uploaded|ddl|nitro|ddownload)[^\s"\'<>]+', script.string)
                    links.extend(js_urls)

            # Method 4: Check for redirect links
            # FileCrypt may use /Link/<id> format
            redirect_links = soup.find_all("a", href=re.compile(r"/Link/\w+"))
            for elem in redirect_links:
                href = elem.get("href", "")
                if href:
                    # Convert relative to absolute
                    if not href.startswith("http"):
                        parsed_url = urlparse(url)
                        href = f"{parsed_url.scheme}://{parsed_url.netloc}{href}"

                    # Fetch redirect target
                    try:
                        redirect_resp = self.session.head(href, allow_redirects=True, timeout=10)
                        final_url = redirect_resp.url
                        if "rapidgator" in final_url or "ddownload" in final_url or "uploaded" in final_url:
                            links.append(final_url)
                    except Exception as e:
                        logger.warning(f"Failed to follow redirect {href}: {e}")

            # Remove duplicates
            links = list(set(links))

            # Filter out invalid links
            valid_links = []
            for link in links:
                # Check if it's a valid download link
                if any(hoster in link.lower() for hoster in ["rapidgator", "uploaded", "ddownload", "nitro", "ddl"]):
                    valid_links.append(link)

            logger.info(f"Extracted {len(valid_links)} links from FileCrypt container")

            return {
                "source": "filecrypt",
                "name": container_name,
                "links": valid_links,
                "password": password,
                "total_links": len(valid_links),
            }

        except Exception as e:
            logger.error(f"Failed to parse FileCrypt container: {e}")
            raise

    def _parse_generic(self, url: str) -> Dict[str, any]:
        """
        Generic link extraction from any URL.

        Args:
            url: URL to parse

        Returns:
            Dictionary with extracted links
        """
        try:
            logger.info(f"Parsing generic URL: {url}")

            response = self.session.get(url, timeout=30)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, "html.parser")

            # Extract all links
            links = []
            for a_tag in soup.find_all("a", href=True):
                href = a_tag["href"]
                if href.startswith("http"):
                    links.append(href)

            # Filter for known file hosters
            valid_links = []
            hosters = ["rapidgator", "uploaded", "ddownload", "nitro", "ddl", "mega", "mediafire"]
            for link in links:
                if any(hoster in link.lower() for hoster in hosters):
                    valid_links.append(link)

            links = list(set(valid_links))

            return {
                "source": "generic",
                "name": "Generic Container",
                "links": links,
                "password": None,
                "total_links": len(links),
            }

        except Exception as e:
            logger.error(f"Failed to parse generic URL: {e}")
            raise
