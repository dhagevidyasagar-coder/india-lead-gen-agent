import time
import random
from datetime import datetime
from typing import List, Dict, Any, Optional
from rich.console import Console
from rich.table import Table
from rich.progress import track

from lead_agent.config import CONFIG
from lead_agent.collectors.web_collector import WebCollector
from lead_agent.collectors.youtube_collector import YouTubeEducatorCollector
from lead_agent.collectors.seed_database import SEED_INSTITUTES
from lead_agent.enrichers.lead_enricher import LeadEnricher
from lead_agent.storage.excel_manager import ExcelManager

console = Console()

class LeadGenAgent:
    """AGMIDI Autonomous Pan-India Lead Generation Agent."""

    def __init__(self, excel_path: Optional[str] = None):
        self.excel_path = excel_path or CONFIG.get("excel_file_path", "AGMIDI_India_Leads.xlsx")
        self.storage = ExcelManager(self.excel_path)
        self.web_collector = WebCollector()
        self.yt_collector = YouTubeEducatorCollector()
        self.enricher = LeadEnricher()

    def run_discovery(self, mode: str = "quick", target_city: Optional[str] = None, target_category: Optional[str] = None) -> Dict[str, Any]:
        """
        Executes a lead discovery run across India.
        mode: 'quick' (10-20 leads), 'full' (broad pan-India scan)
        """
        console.print(f"\n[bold blue]🚀 Starting AGMIDI Pan-India Lead Discovery Agent[/bold blue]")
        console.print(f"[dim]Company: AGMIDI (EdTech Growth Partner) | Target: Educators & Coaching Centers[/dim]\n")

        raw_leads: List[Dict[str, Any]] = []
        today_str = datetime.now().strftime("%Y-%m-%d")

        # 1. Load curated verified seeds (if not already added)
        for seed in SEED_INSTITUTES:
            if target_city and target_city.lower() not in seed.get("city", "").lower():
                continue
            if target_category and target_category.lower() not in seed.get("category", "").lower():
                continue
            seed_copy = dict(seed)
            seed_copy["date_added"] = today_str
            raw_leads.append(seed_copy)

        # 2. Select target locations
        locations = CONFIG["target_locations"]
        if target_city:
            locations = [loc for loc in locations if target_city.lower() in loc["city"].lower()]
            if not locations:
                locations = [{"city": target_city, "state": "India", "tier": "Custom Target"}]
        elif mode == "quick":
            # For quick runs, pick 3 major hubs
            locations = locations[:3]

        # 3. Web Discovery across coaching hubs
        console.print(f"[cyan]🔍 Scanning coaching institutes across {len(locations)} hubs...[/cyan]")
        for loc in locations:
            city_name = loc["city"]
            queries = [
                f"best coaching institute NEET JEE {city_name} contact phone",
                f"UPSC civil services academy {city_name} phone email",
                f"SSC banking exam coaching classes {city_name}"
            ]
            if mode == "quick":
                queries = queries[:1]

            for q in queries:
                try:
                    results = self.web_collector.collect(q, limit=5)
                    for r in results:
                        r["city"] = city_name
                        r["state"] = loc.get("state", "India")
                        r["category"] = "Coaching Institute"
                        r["date_added"] = today_str
                        raw_leads.append(r)
                except Exception as e:
                    console.print(f"[yellow]Web scan note: {e}[/yellow]")
                time.sleep(0.5)

        # 4. YouTube Educator & Creator Discovery
        yt_keywords = CONFIG["youtube_creator_keywords"]
        if mode == "quick":
            yt_keywords = yt_keywords[:2]

        console.print(f"[cyan]📺 Discovering educational creators on YouTube across India...[/cyan]")
        for kw in yt_keywords:
            try:
                yt_results = self.yt_collector.collect(kw, limit=4)
                for r in yt_results:
                    r["city"] = "Online / Pan-India"
                    r["state"] = "India"
                    r["date_added"] = today_str
                    raw_leads.append(r)
            except Exception as e:
                console.print(f"[yellow]YouTube scan note: {e}[/yellow]")
            time.sleep(0.5)

        # 5. Enrich & Score Leads
        console.print(f"[magenta]⚡ Normalizing numbers, verifying emails & scoring leads for AGMIDI...[/magenta]")
        enriched_leads = []
        for raw in raw_leads:
            enriched = self.enricher.enrich(raw)
            enriched_leads.append(enriched)

        # 6. Save & Deduplicate into Excel
        save_stats = self.storage.update_excel(enriched_leads)

        # 7. Print summary table
        self._display_summary_table(enriched_leads, save_stats)

        return {
            "leads_processed": len(enriched_leads),
            "new_leads_saved": save_stats["new_added"],
            "total_leads_in_excel": save_stats["total_leads_in_file"],
            "excel_path": save_stats["file_path"]
        }

    def _display_summary_table(self, leads: List[Dict[str, Any]], stats: Dict[str, Any]):
        table = Table(title="🎯 AGMIDI Lead Generation Run - Results", show_header=True, header_style="bold green")
        table.add_column("Business / Creator Name", style="bold")
        table.add_column("Category")
        table.add_column("City")
        table.add_column("Phone")
        table.add_column("Score", justify="right")
        table.add_column("Priority")

        # Show top 8 leads
        top_leads = sorted(leads, key=lambda x: x.get("lead_score", 0), reverse=True)[:8]
        for l in top_leads:
            phone_disp = l.get("phone") or "[dim]N/A[/dim]"
            score = str(l.get("lead_score", 0))
            priority = l.get("priority_tier", "Tier B")
            table.add_row(
                l.get("business_name", "")[:28],
                l.get("category", "")[:20],
                l.get("city", "")[:12],
                phone_disp,
                score,
                priority
            )

        console.print("\n")
        console.print(table)
        console.print(f"\n[bold green]✅ Excel Database Updated Successfully![/bold green]")
        console.print(f"📁 [bold underline]{stats['file_path']}[/bold underline]")
        console.print(f"📊 [cyan]New Leads Added Today:[/cyan] [bold]{stats['new_added']}[/bold] | [dim]Duplicates Skipped: {stats['skipped_duplicates']}[/dim] | [green]Total Leads in Pipeline: {stats['total_leads_in_file']}[/green]\n")
