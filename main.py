#!/usr/bin/env python3
import sys
import argparse
from rich.console import Console
from rich.panel import Panel

from lead_agent.config import CONFIG
from lead_agent.engine import LeadGenAgent
from lead_agent.scheduler.cron_runner import DailyLeadScheduler
from lead_agent.storage.excel_manager import ExcelManager

console = Console()

def print_banner():
    banner = (
        "[bold cyan]AGMIDI Autonomous Lead Generation Agent (Pan-India)[/bold cyan]\n"
        "[dim]Specialized for EdTech Growth Partnerships, Coaching Centers & Educational Creators[/dim]\n"
        "[link=https://www.agmidi.com]https://www.agmidi.com[/link]"
    )
    console.print(Panel(banner, border_style="blue", expand=False))

def cmd_run(args):
    agent = LeadGenAgent()
    agent.run_discovery(
        mode=args.mode,
        target_city=args.city,
        target_category=args.category
    )

def cmd_schedule(args):
    scheduler = DailyLeadScheduler()
    scheduler.start_scheduler()

def cmd_stats(args):
    storage = ExcelManager()
    count = storage.get_existing_lead_count()
    console.print(f"\n📊 [bold]AGMIDI Database Status:[/bold]")
    console.print(f"📁 Excel File: [bold cyan]{storage.file_path}[/bold cyan]")
    console.print(f"👥 Total Leads in Pipeline: [bold green]{count}[/bold green]\n")

def main():
    print_banner()

    parser = argparse.ArgumentParser(description="AGMIDI Pan-India Lead Generation Agent")
    subparsers = parser.add_subparsers(dest="command", help="Available subcommands")

    # Command: run
    run_parser = subparsers.add_parser("run", help="Run on-demand lead discovery")
    run_parser.add_argument("--mode", choices=["quick", "full"], default="quick", help="Execution mode (quick or full scan)")
    run_parser.add_argument("--city", type=str, default=None, help="Target specific city (e.g. Kota, Delhi NCR, Patna, Pune)")
    run_parser.add_argument("--category", type=str, default=None, help="Target specific category (e.g. NEET, UPSC, Trading)")

    # Command: schedule
    subparsers.add_parser("schedule", help="Start automated daily background updater")

    # Command: stats
    subparsers.add_parser("stats", help="Display current Excel lead metrics")

    args = parser.parse_args()

    if args.command == "run" or args.command is None:
        if args.command is None:
            # Default to quick run if no subcommand given
            args.mode = "quick"
            args.city = None
            args.category = None
        cmd_run(args)
    elif args.command == "schedule":
        cmd_schedule(args)
    elif args.command == "stats":
        cmd_stats(args)

if __name__ == "__main__":
    main()
