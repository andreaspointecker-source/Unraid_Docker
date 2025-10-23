"""Link grabber service for extracting download links - JDownloader style."""

import logging
import re
import base64
from typing import Dict, List, Optional
from urllib.parse import urlparse, urljoin

import requests
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)


class LinkGrabberService:
    """Service for extracting download links - inspired by JDownloader."""

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        })

    def extract_links(self, url: str, password: Optional[str] = None) -> Dict[str, any]:
        """
        Extract download links from a container URL - JDownloader workflow.

        Args:
            url: Container URL (FileCrypt.cc, etc.)
            password: Optional container password

        Returns:
            Dictionary with:
                - source: Container source (filecrypt, etc.)
                - name: Container name
                - links: List of download URLs
                - password: Password if found
                - requires_captcha: Boolean
                - captcha_url: URL to captcha page if required
                - captcha_type: Type of captcha (recaptcha, cutcaptcha, etc.)
                - requires_password: Boolean
        """
        parsed = urlparse(url)
        domain = parsed.netloc.lower()

        if "filecrypt" in domain:
            return self._parse_filecrypt(url, password)
        else:
            return self._parse_generic(url)

    def _parse_filecrypt(self, url: str, password: Optional[str] = None) -> Dict[str, any]:
        """
        Parse FileCrypt.cc container - JDownloader CNL/DLC approach.

        Workflow (JDownloader style):
        1. Normalize URL to .html format
        2. Fetch page and check for password/captcha requirements
        3. Extract container metadata (name, password hint)
        4. Try CNL (Click'n'Load) - best method, no external dependencies
        5. Fallback to DLC container download
        6. Last resort: crawl redirect links manually

        Args:
            url: FileCrypt.cc container URL
            password: Container password if known

        Returns:
            Dictionary with links, captcha info, and metadata
        """
        try:
            logger.info(f"Parsing FileCrypt container: {url}")

            # Normalize URL
            if not url.endswith('.html'):
                container_id = url.split('/')[-1].split('.')[0].split('?')[0]
                url = f"https://filecrypt.cc/Container/{container_id}.html"

            # Fetch the main page
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")

            result = {
                "source": "filecrypt",
                "name": "FileCrypt Container",
                "links": [],
                "password": None,
                "requires_captcha": False,
                "captcha_url": None,
                "captcha_type": None,
                "requires_password": False,
                "total_links": 0,
            }

            # Extract container name
            title_elem = soup.find("h1") or soup.find("title")
            if title_elem:
                result["name"] = title_elem.text.strip()

            # Check for password requirement
            password_input = soup.find("input", {"name": "password"})
            if password_input:
                result["requires_password"] = True
                if not password:
                    logger.info("FileCrypt container requires password")
                    return result

            # Check for captcha requirement
            # FileCrypt uses: ReCaptcha, CutCaptcha, KeyCaptcha, ClickCaptcha
            captcha_found = False

            # ReCaptcha v2
            if soup.find("div", {"class": "g-recaptcha"}):
                result["requires_captcha"] = True
                result["captcha_type"] = "recaptcha_v2"
                result["captcha_url"] = url
                captcha_found = True
                logger.info("FileCrypt container requires ReCaptcha v2")

            # CutCaptcha
            if soup.find("iframe", src=re.compile(r"cutcaptcha")):
                result["requires_captcha"] = True
                result["captcha_type"] = "cutcaptcha"
                result["captcha_url"] = url
                captcha_found = True
                logger.info("FileCrypt container requires CutCaptcha")

            # If captcha required, return early (user must solve)
            if captcha_found:
                return result

            # Try to find mirror/download links
            # FileCrypt shows links after password/captcha
            links = []

            # Method 1: Look for mirror containers
            # FileCrypt has multiple mirrors (rapidgator, uploaded, etc.)
            mirror_divs = soup.find_all("div", {"class": re.compile(r"mirror|link", re.I)})
            for div in mirror_divs:
                # Look for data attributes or hidden inputs with URLs
                for attr in ["data-href", "data-url", "data-link"]:
                    if div.has_attr(attr):
                        link_url = div[attr]
                        if link_url and link_url.startswith("http"):
                            links.append(link_url)

            # Method 2: Look for download buttons with data attributes (FileCrypt's main method)
            # FileCrypt uses: <button data-XXXX="link_id" onclick="openLink(...)">
            download_buttons = soup.find_all("button", {"class": "download"})
            for button in download_buttons:
                # Find data-* attribute containing link ID
                for attr, value in button.attrs.items():
                    if attr.startswith("data-") and value:
                        # Build /Link/ URL
                        link_id = value
                        redirect_url = f"/Link/{link_id}.html"
                        full_url = urljoin(url, redirect_url)
                        links.append(full_url)
                        logger.info(f"Found FileCrypt link: {full_url}")
                        break

            # Method 3: Look for /Link/ redirect URLs in <a> tags
            redirect_links = soup.find_all("a", href=re.compile(r"/Link/\w+"))
            for elem in redirect_links:
                href = elem.get("href", "")
                if href:
                    # Convert relative to absolute
                    if not href.startswith("http"):
                        href = urljoin(url, href)
                    links.append(href)

            # Method 3: Look for CNL (Click'n'Load) data
            # CNL is FileCrypt's preferred method - encrypted link data in page
            cnl_scripts = soup.find_all("script", text=re.compile(r"cnl|jdownloader", re.I))
            for script in cnl_scripts:
                # Look for CNL2 format
                # Usually contains: crypted, jk, source
                cnl_data = re.search(r'crypted\s*[:=]\s*["\']([^"\']+)["\']', script.string or "")
                if cnl_data:
                    try:
                        # CNL2 uses base64 encoded data
                        encrypted = cnl_data.group(1)
                        # In real implementation, would decrypt with key
                        logger.info("Found CNL2 encrypted data (decryption not implemented)")
                        # For now, mark as found
                        result["cnl_available"] = True
                    except Exception as e:
                        logger.warning(f"Failed to parse CNL data: {e}")

            # Method 4: Look for DLC container download link
            dlc_link = soup.find("a", href=re.compile(r"\.dlc$", re.I))
            if dlc_link:
                dlc_url = dlc_link.get("href", "")
                if dlc_url:
                    if not dlc_url.startswith("http"):
                        dlc_url = urljoin(url, dlc_url)
                    result["dlc_url"] = dlc_url
                    logger.info(f"Found DLC container: {dlc_url}")

            # Remove duplicates
            links = list(set(links))

            # FileCrypt /Link/ URLs need to be kept as-is
            # They redirect to the actual download hoster
            result["links"] = links
            result["total_links"] = len(links)

            logger.info(f"Extracted {len(links)} links from FileCrypt container")
            return result

        except Exception as e:
            logger.error(f"Failed to parse FileCrypt container: {e}")
            raise

    def resolve_redirect_link(self, redirect_url: str) -> Optional[str]:
        """
        Resolve FileCrypt /Link/ redirect to actual download URL.

        Args:
            redirect_url: FileCrypt redirect URL (e.g., /Link/XXXXX)

        Returns:
            Actual download URL or None
        """
        try:
            # Follow redirect
            response = self.session.head(redirect_url, allow_redirects=True, timeout=10)
            final_url = response.url

            # Check if it's a valid download URL
            hosters = ["rapidgator", "uploaded", "ddownload", "nitro", "ddl", "mega", "mediafire"]
            if any(hoster in final_url.lower() for hoster in hosters):
                logger.info(f"Resolved redirect: {redirect_url} -> {final_url}")
                return final_url

            return None
        except Exception as e:
            logger.error(f"Failed to resolve redirect {redirect_url}: {e}")
            return None

    def _parse_generic(self, url: str) -> Dict[str, any]:
        """Generic link extraction from any URL."""
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
                "requires_captcha": False,
                "requires_password": False,
                "total_links": len(links),
            }

        except Exception as e:
            logger.error(f"Failed to parse generic URL: {e}")
            raise
