import re
import urllib.parse
from typing import List, Dict, Any
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from lead_agent.collectors.base import BaseCollector

class WebCollector(BaseCollector):
    """Gathers educational institute leads by web discovery across Indian cities."""

    def __init__(self):
        try:
            self.ua = UserAgent()
        except Exception:
            self.ua = None

    def _get_headers(self) -> Dict[str, str]:
        user_agent = self.ua.random if self.ua else "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        return {
            "User-Agent": user_agent,
            "Accept-Language": "en-IN,en-US;q=0.9,en;q=0.8,hi;q=0.7",
            "Referer": "https://www.google.com/"
        }

    def collect(self, query: str, limit: int = 15) -> List[Dict[str, Any]]:
        leads = []
        try:
            url = f"https://html.duckduckgo.com/html/?q={urllib.parse.quote_plus(query)}"
            headers = self._get_headers()
            resp = requests.post(url, data={"q": query}, headers=headers, timeout=4)
            
            if resp.status_code == 200:
                soup = BeautifulSoup(resp.text, "lxml")
                results = soup.select(".result")

                for res in results[:limit]:
                    title_elem = res.select_one(".result__title a")
                    snippet_elem = res.select_one(".result__snippet")
                    url_elem = res.select_one(".result__url")

                    if not title_elem:
                        continue

                    title = title_elem.get_text(strip=True)
                    snippet = snippet_elem.get_text(strip=True) if snippet_elem else ""
                    raw_url = title_elem.get("href", "")
                    
                    # Clean DuckDuckGo redirect url if needed
                    match_url = re.search(r"uddg=([^&]+)", raw_url)
                    clean_url = urllib.parse.unquote(match_url.group(1)) if match_url else raw_url

                    # Extract potential phone numbers in snippet or title
                    combined_text = f"{title} {snippet}"
                    phone_match = re.search(r"(?:\+91[\s-]?)?[6789]\d{9}\b", combined_text)
                    phone = phone_match.group(0) if phone_match else ""

                    # Extract email if present
                    email_match = re.search(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", combined_text)
                    email = email_match.group(0) if email_match else ""

                    # Deep contact fetch if phone is missing and clean_url is valid
                    if not phone and clean_url.startswith("http") and not any(x in clean_url for x in ["youtube.com", "facebook.com", "instagram.com", "wikipedia.org"]):
                        try:
                            site_resp = requests.get(clean_url, headers=headers, timeout=4)
                            if site_resp.status_code == 200:
                                site_text = site_resp.text
                                p_match = re.search(r"(?:\+91[\s-]?)?[6789]\d{9}\b", site_text)
                                if p_match:
                                    phone = p_match.group(0)
                                if not email:
                                    e_match = re.search(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", site_text)
                                    if e_match:
                                        found_e = e_match.group(0)
                                        if not any(found_e.endswith(ext) for ext in [".png", ".jpg", ".webp", ".svg"]):
                                            email = found_e
                        except Exception:
                            pass

                    leads.append({
                        "business_name": title.split(" - ")[0].split(" | ")[0].strip(),
                        "full_title": title,
                        "description": snippet,
                        "website": clean_url,
                        "phone": phone,
                        "email": email,
                        "source": "Web Search Discovery",
                        "raw_query": query
                    })
        except Exception as e:
            # Silently degrade gracefully on network drops
            pass

        return leads
