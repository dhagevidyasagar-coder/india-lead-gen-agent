import re
import urllib.parse
from typing import List, Dict, Any
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from lead_agent.collectors.base import BaseCollector

class YouTubeEducatorCollector(BaseCollector):
    """Discovers Indian educational YouTube creators and tutors looking to monetize with an app."""

    def __init__(self):
        try:
            self.ua = UserAgent()
        except Exception:
            self.ua = None

    def _get_headers(self) -> Dict[str, str]:
        user_agent = self.ua.random if self.ua else "Mozilla/5.0"
        return {
            "User-Agent": user_agent,
            "Accept-Language": "en-IN,en;q=0.9,hi;q=0.8"
        }

    def collect(self, query: str, limit: int = 15) -> List[Dict[str, Any]]:
        leads = []
        try:
            # Query DuckDuckGo specifically for site:youtube.com channel or playlist creators
            search_query = f"site:youtube.com/c/ OR site:youtube.com/@ {query} India"
            url = f"https://html.duckduckgo.com/html/?q={urllib.parse.quote_plus(search_query)}"
            headers = self._get_headers()
            resp = requests.post(url, data={"q": search_query}, headers=headers, timeout=4)

            if resp.status_code == 200:
                soup = BeautifulSoup(resp.text, "lxml")
                results = soup.select(".result")

                for res in results[:limit]:
                    title_elem = res.select_one(".result__title a")
                    snippet_elem = res.select_one(".result__snippet")

                    if not title_elem:
                        continue

                    title = title_elem.get_text(strip=True)
                    snippet = snippet_elem.get_text(strip=True) if snippet_elem else ""
                    raw_url = title_elem.get("href", "")

                    match_url = re.search(r"uddg=([^&]+)", raw_url)
                    clean_url = urllib.parse.unquote(match_url.group(1)) if match_url else raw_url

                    # Check if it is a channel link
                    if "youtube.com" not in clean_url:
                        continue

                    combined_text = f"{title} {snippet}"
                    phone_match = re.search(r"(?:\+91[\s-]?)?[6789]\d{9}\b", combined_text)
                    phone = phone_match.group(0) if phone_match else ""

                    email_match = re.search(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", combined_text)
                    email = email_match.group(0) if email_match else ""

                    channel_name = title.replace(" - YouTube", "").split(" - ")[0].strip()

                    leads.append({
                        "business_name": f"{channel_name} (YouTube)",
                        "full_title": title,
                        "description": snippet,
                        "website": clean_url,
                        "phone": phone,
                        "email": email,
                        "source": "YouTube Educator Discovery",
                        "category": "YouTube / Online Educator",
                        "raw_query": query
                    })
        except Exception:
            pass

        return leads
