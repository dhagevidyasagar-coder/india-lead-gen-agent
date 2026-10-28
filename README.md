# AGMIDI Autonomous Pan-India Lead Generation Agent 🇮🇳
**Targeted for EdTech Growth Partnerships, Coaching Centers, Academies & Online Educators**  
Official Website: [agmidi.com](https://www.agmidi.com)

---

## 🚀 Overview

This agent is custom-engineered for **AGMIDI** to solve nationwide client acquisition across India. It systematically finds, verifies, scores, and exports high-ticket educational leads into an organized, automatically-updating Excel sheet (`AGMIDI_India_Leads.xlsx`).

### Target Client Profiles (Pan-India):
1. **Offline & Hybrid Coaching Centers**: NEET/JEE, UPSC, SSC, Banking, State PSCs in major hubs (Kota, Delhi Mukherjee Nagar/Kalu Sarai, Patna Boring Road, Hyderabad Ameerpet, Pune Sadashiv Peth, Jaipur, Sikar, Lucknow).  
   *Pitch*: Custom branded mobile app (like PhysicsWallah/Khan Sir model) + 50-100 monthly admission inquiries via Meta & Google Ads.
2. **Independent Educators & Content Creators**: YouTube educators and Instagram knowledge creators with 10k–500k followers across India.  
   *Pitch*: Launch your own digital academy & branded course platform; AGMIDI handles 100% tech, marketing, and sales funnels.
3. **High-Ticket Skill Mentors**: Stock market/trading mentors, spoken English/IELTS institutes, coding academies.

---

## 📁 System Architecture

```
india_lead_gen_agent/
├── AGMIDI_India_Leads.xlsx     <-- Generated live master Excel database
├── main.py                     <-- CLI tool to run discoveries & scheduler
├── requirements.txt            <-- Dependencies
├── lead_agent/
│   ├── config.py               <-- Target cities, niches, and daily run times
│   ├── engine.py               <-- Central orchestrator & pipeline runner
│   ├── collectors/
│   │   ├── base.py             <-- Base collector abstract class
│   │   ├── web_collector.py    <-- Multi-engine web directory scraper
│   │   ├── youtube_collector.py<-- Indian educational YouTube creator finder
│   │   └── seed_database.py    <-- Verified Pan-India seed repository
│   ├── enrichers/
│   │   └── lead_enricher.py    <-- +91 phone cleaning, wa.me links & scoring
│   ├── storage/
│   │   └── excel_manager.py    <-- Multi-sheet Excel generator & deduplicator
│   ├── scheduler/
│   │   └── cron_runner.py      <-- Automated daily execution daemon
│   └── templates/
│       └── pitch_templates.py  <-- High-converting WhatsApp & cold email scripts
```

---

## 📊 Features of the Generated Excel Workbook

The generated `AGMIDI_India_Leads.xlsx` workbook includes:

1. **Sheet 1: `All Leads (Pan-India)`**
   - **Lead ID**: Unique tracking identifier (e.g., `AGM-1002`)
   - **Discovery Date**: When the lead was found
   - **Business / Creator Name**: Institute or educator channel name
   - **Category**: NEET/JEE, UPSC, SSC/Banking, Trading, etc.
   - **City & State**: Target location across India
   - **Phone (+91)**: Normalized 10-digit Indian mobile/contact
   - **WhatsApp Direct Link**: Clickable `https://wa.me/91XXXXXXXXXX` (open in WhatsApp with 1-click)
   - **Email Address & Website**: Direct contact points
   - **Lead Score (1-100) & Priority Tier**: High-value (A-Tier), Medium (B-Tier), Nurture (C-Tier)
   - **AGMIDI Pitch Offer**: Tailored offer (App Development, Meta Ads, Funnels)
   - **Outreach Stage**: `Not Contacted`, `Meeting Booked`, etc.

2. **Sheet 2: `Daily Updates & Metrics`**
   - Keeps an audit log of every daily run with date, timestamp, and new leads added.

3. **Sheet 3: `Outreach Scripts (AGMIDI)`**
   - Ready-to-copy WhatsApp messages & Cold Email templates for sales outreach.

---

## 🛠️ Usage Instructions

### 1. Run Quick Lead Discovery
```bash
python3 main.py run --mode quick
```

### 2. Run Full Pan-India Scan
```bash
python3 main.py run --mode full
```

### 3. Target Specific City or Category
```bash
# Target Kota NEET/JEE institutes:
python3 main.py run --city Kota --category NEET

# Target Delhi UPSC academies:
python3 main.py run --city "Delhi NCR" --category UPSC

# Target Hyderabad institutes:
python3 main.py run --city Hyderabad
```

### 4. Start Daily Background Auto-Updater
To keep the sheet updated daily automatically:
```bash
python3 main.py schedule
```
*By default, runs every morning at 09:30 AM IST and appends fresh, deduplicated leads.*

### 5. Check Current Database Stats
```bash
python3 main.py stats
```

---

## ⚙️ Customization

Edit `lead_agent/config.py` to add new cities, adjust keywords, change run hours, or modify the lead scoring criteria.
