import re
from typing import Dict, Any, Optional

class LeadEnricher:
    """Enriches and normalizes raw Indian educational leads for AGMIDI."""

    @staticmethod
    def clean_phone(raw_phone: str) -> Optional[str]:
        if not raw_phone:
            return None
        
        # Remove non-digits
        digits = re.sub(r"\D", "", str(raw_phone))
        
        # If starts with 91 and has 12 digits (standard +91)
        if len(digits) == 12 and digits.startswith("91"):
            clean = digits[2:]
        # If starts with 0 and has 11 digits
        elif len(digits) == 11 and digits.startswith("0"):
            clean = digits[1:]
        elif len(digits) == 10:
            clean = digits
        else:
            return None
        
        # Indian mobile numbers typically start with 6, 7, 8, 9
        if clean[0] in ["6", "7", "8", "9"]:
            return clean
        # Or standard Indian landline with STD (10 digits)
        return clean

    @staticmethod
    def format_whatsapp_link(phone: Optional[str]) -> str:
        if phone and len(phone) == 10:
            return f"https://wa.me/91{phone}"
        return ""

    @staticmethod
    def clean_email(raw_email: str) -> Optional[str]:
        if not raw_email:
            return None
        
        # Standard regex for email extraction
        match = re.search(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", str(raw_email))
        if match:
            email = match.group(0).lower().strip()
            # Filter out generic image/font false positives
            if not any(email.endswith(ext) for ext in [".png", ".jpg", ".jpeg", ".webp", ".svg"]):
                return email
        return None

    @classmethod
    def score_lead(cls, lead: Dict[str, Any]) -> int:
        score = 0
        phone = lead.get("phone")
        email = lead.get("email")
        website = lead.get("website")
        city = lead.get("city", "")

        # Contact availability
        if phone:
            score += 35
        if email:
            score += 20
        if website and "http" in str(website):
            score += 20
        
        # Key hubs have higher commercial willingness for app & marketing
        prime_hubs = ["Kota", "Delhi NCR", "Patna", "Pune", "Hyderabad", "Jaipur", "Lucknow", "Sikar"]
        if any(hub.lower() in city.lower() for hub in prime_hubs):
            score += 15
        else:
            score += 10

        # Description / niche presence
        if lead.get("category"):
            score += 10

        return min(score, 100)

    @classmethod
    def get_priority_tier(cls, score: int) -> str:
        if score >= 75:
            return "Tier A (High Value)"
        elif score >= 50:
            return "Tier B (Medium Value)"
        else:
            return "Tier C (Nurture)"

    @classmethod
    def enrich(cls, raw_lead: Dict[str, Any]) -> Dict[str, Any]:
        """Normalize, score, and enrich a single lead record."""
        cleaned_phone = cls.clean_phone(raw_lead.get("phone", ""))
        cleaned_email = cls.clean_email(raw_lead.get("email", ""))
        wa_link = cls.format_whatsapp_link(cleaned_phone)

        enriched = {
            **raw_lead,
            "phone": cleaned_phone or raw_lead.get("phone", ""),
            "email": cleaned_email or raw_lead.get("email", ""),
            "whatsapp_link": wa_link,
            "status": raw_lead.get("status") or "New Lead",
            "outreach_stage": "Not Contacted"
        }

        score = cls.score_lead(enriched)
        enriched["lead_score"] = score
        enriched["priority_tier"] = cls.get_priority_tier(score)

        return enriched
