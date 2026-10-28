import time
import schedule
from datetime import datetime
from rich.console import Console

from lead_agent.config import CONFIG
from lead_agent.engine import LeadGenAgent

console = Console()

class DailyLeadScheduler:
    """Manages scheduled daily updates to the AGMIDI Excel database."""

    def __init__(self):
        self.agent = LeadGenAgent()
        self.run_time = CONFIG.get("daily_run_time", "09:30")

    def daily_job(self):
        console.print(f"\n[bold yellow]⏰ Triggering Scheduled Daily Lead Run: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}[/bold yellow]")
        try:
            result = self.agent.run_discovery(mode="full")
            console.print(f"[bold green]✨ Scheduled daily run complete: {result['new_leads_saved']} new leads added![/bold green]")
        except Exception as e:
            console.print(f"[bold red]❌ Daily job error: {e}[/bold red]")

    def start_scheduler(self):
        console.print(f"[bold green]📅 AGMIDI Daily Lead Agent Scheduler Activated[/bold green]")
        console.print(f"⏰ Daily trigger scheduled for: [bold cyan]{self.run_time}[/bold cyan] every day.")
        console.print("[dim]Press Ctrl+C to exit scheduler anytime.[/dim]\n")

        # Run immediately on start once so the user doesn't have to wait until tomorrow 9:30 AM to see data
        console.print("[blue]▶️ Executing initial bootstrap run now...[/blue]")
        self.daily_job()

        schedule.every().day.at(self.run_time).do(self.daily_job)

        while True:
            schedule.run_pending()
            time.sleep(30)
