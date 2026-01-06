#!/usr/bin/env python3
"""Main entry point for the AI News Agent."""

import argparse
import sys
from agent import AINewsAgent
from rich.console import Console
from rich.panel import Panel
from rich.text import Text


def main():
    """Main function."""
    parser = argparse.ArgumentParser(
        description="AI News Agent - Scrapes and summarizes latest AI developments"
    )
    parser.add_argument(
        "--days",
        type=int,
        default=7,
        help="Number of days to look back for articles (default: 7)"
    )
    parser.add_argument(
        "--output",
        type=str,
        default=None,
        help="Output JSON file path (default: auto-generated)"
    )
    parser.add_argument(
        "--no-save",
        action="store_true",
        help="Don't save results to JSON file"
    )
    parser.add_argument(
        "--fast",
        action="store_true",
        help="Fast mode: Skip full content scraping and AI summarization (MVP mode)"
    )
    parser.add_argument(
        "--no-summaries",
        action="store_true",
        help="Skip AI summarization (categorization only)"
    )
    
    args = parser.parse_args()
    
    console = Console()
    
    try:
        agent = AINewsAgent()
        
        # MVP/Fast mode: skip full content and summaries
        fetch_full_content = not args.fast
        generate_summaries = not args.fast and not args.no_summaries
        
        if args.fast:
            console.print("[yellow]Fast mode enabled: Using RSS summaries only, no AI summarization[/yellow]\n")
        
        results = agent.run(
            days=args.days,
            fetch_full_content=fetch_full_content,
            generate_summaries=generate_summaries
        )
        
        # Display results
        output_text = agent.format_output(results)
        console.print(Panel(output_text, title="AI News Report", border_style="blue"))
        
        # Save results
        if not args.no_save:
            agent.save_results(results, args.output)
        
        # Summary statistics
        total_articles = sum(len(articles) for articles in results.values())
        console.print(f"\n[green]✓[/green] Processed {total_articles} articles across {len(results)} categories")
        
    except KeyboardInterrupt:
        console.print("\n[yellow]Interrupted by user[/yellow]")
        sys.exit(1)
    except Exception as e:
        console.print(f"\n[red]Error: {e}[/red]")
        import traceback
        console.print(f"[red]{traceback.format_exc()}[/red]")
        sys.exit(1)


if __name__ == "__main__":
    main()
