import os
from typing import List, Dict

# AGMIDI Lead Generation Agent Configuration

CONFIG = {
    "company": {
        "name": "AGMIDI",
        "website": "https://www.agmidi.com",
        "tagline": "EdTech Growth Partner India",
        "core_services": [
            "Branded Mobile App & Website Platform Setup",
            "Performance Marketing (Meta & Google Ads)",
            "YouTube Channel Growth & Creative Strategy",
            "Course Creation, Pricing Architecture & Funnels",
            "Sales Automation & Admission Conversion Systems"
        ]
    },
    
    # Priority Coaching Hubs across India
    "target_locations": [
        {"city": "Kota", "state": "Rajasthan", "tier": "Tier-1 Hub"},
        {"city": "Delhi NCR", "state": "Delhi", "tier": "Metro Hub"},
        {"city": "Patna", "state": "Bihar", "tier": "Tier-1 Hub"},
        {"city": "Pune", "state": "Maharashtra", "tier": "Metro Hub"},
        {"city": "Hyderabad", "state": "Telangana", "tier": "Metro Hub"},
        {"city": "Jaipur", "state": "Rajasthan", "tier": "Tier-1 Hub"},
        {"city": "Sikar", "state": "Rajasthan", "tier": "Tier-1 Hub"},
        {"city": "Lucknow", "state": "Uttar Pradesh", "tier": "Tier-1 Hub"},
        {"city": "Bengaluru", "state": "Karnataka", "tier": "Metro Hub"},
        {"city": "Ahmedabad", "state": "Gujarat", "tier": "Tier-1 Hub"},
        {"city": "Indore", "state": "Madhya Pradesh", "tier": "Tier-1 Hub"},
        {"city": "Prayagraj", "state": "Uttar Pradesh", "tier": "Tier-1 Hub"},
        {"city": "Bhopal", "state": "Madhya Pradesh", "tier": "Tier-2 Hub"},
        {"city": "Chandigarh", "state": "Punjab/Haryana", "tier": "Tier-2 Hub"},
        {"city": "Kolkata", "state": "West Bengal", "tier": "Metro Hub"}
    ],

    # High-ticket educational categories ideal for AGMIDI
    "target_categories": [
        "NEET & JEE Coaching Institutes",
        "UPSC & State PSC Civil Services Academies",
        "SSC & Banking Exam Preparation Classes",
        "Stock Market & Trading Mentors",
        "Digital Marketing & Coding Training Bootcamps",
        "Spoken English & IELTS / Study Abroad Centers",
        "Independent Online Educators & YouTube Teachers"
    ],

    # Target search queries constructed programmatically
    "search_queries": [
        "coaching institute NEET JEE {city}",
        "UPSC civil services academy {city}",
        "SSC banking competitive exam coaching {city}",
        "best coaching classes {city} contact phone",
        "trading mentor stock market classes {city}",
        "ielts spoken english coaching institute {city}"
    ],

    # YouTube creator search tags (pan-India)
    "youtube_creator_keywords": [
        "UPSC preparation tips",
        "SSC CGL strategy Hindi",
        "NEET biology lecture class",
        "JEE chemistry preparation",
        "share market trading course Hindi",
        "spoken english classes online",
        "State PSC exam strategy",
        "Class 10 12 board preparation Hindi"
    ],

    # Output file settings
    "excel_file_path": "AGMIDI_India_Leads.xlsx",
    
    # Daily automation settings
    "daily_run_time": "09:30", # Runs daily at 9:30 AM
    "max_leads_per_batch": 30
}
