#!/usr/bin/env python3

import argparse
import os
import sys
from typing import List, Optional

from pynput import keyboard
from rich.console import Console
from rich.live import Live
from rich.panel import Panel
from rich.progress import (
    BarColumn, Progress, SpinnerColumn,
    TaskProgressColumn, TextColumn
)
from rich.prompt import Confirm
from rich.table import Table
from rich.text import Text
from rich.layout import Layout

from saavn.models.album import Album
from saavn.models.artist import Artist
from saavn.models.playlist import Playlist
from .client import HttpClient
from .models import Track
from .saavn import Saavn

# Initialize global objects
console = Console()
saavn = Saavn()
http_client = HttpClient()


def print_banner():
    """Display the application banner and help information."""
    banner = """
         ██╗██╗ ██████╗ ███████╗ █████╗  █████╗ ██╗   ██╗███╗   ██╗      ██████╗██╗     ██╗
         ██║██║██╔═══██╗██╔════╝██╔══██╗██╔══██╗██║   ██║████╗  ██║     ██╔════╝██║     ██║
         ██║██║██║   ██║███████╗███████║███████║██║   ██║██╔██╗ ██║     ██║     ██║     ██║
    ██   ██║██║██║   ██║╚════██║██╔══██║██╔══██║╚██╗ ██╔╝██║╚██╗██║     ██║     ██║     ██║
    ╚█████╔╝██║╚██████╔╝███████║██║  ██║██║  ██║ ╚████╔╝ ██║ ╚████║     ╚██████╗███████╗██║
    ╚════╝ ╚═╝ ╚═════╝ ╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝  ╚═══╝  ╚═╝  ╚═══╝      ╚═════╝╚══════╝╚═╝
    """
    console.print(Panel.fit(banner, style="cyan"), justify="center")
    console.print(
        "━━━━━━━━━━━━━━━━━━━━━━━ Welcome to JioSaavn CLI! ━━━━━━━━━━━━━━━━━━━━━━━",
        style="magenta",
        justify="center"
    )
    
    help_text = """
    Quick Start Guide:

    [bold][cyan]saavn -s[/] [yellow]"song name"[/] [purple]-o[/] [blue]/path/to/output[/]
    [white]Example:[/] [bold][cyan]saavn -s[/] [yellow]"shape of you"[/] [purple]-o[/] [blue]~/Music[/]
    """
    console.print(help_text, style="yellow", justify="center")


def parse_args() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="🎵 JioSaavn CLI - Your Personal Music Assistant",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument("-s", "--search", type=str, help="Search using song name or url")
    parser.add_argument("-o", "--outdir", help="Output directory for downloaded songs", default=".")
    return parser.parse_args()

def render_track_list(results: List[Track], current_selection: int, selected_indices: set) -> Table:
    """Create a pretty table showing track search results."""
    table = Table(
        show_header=True,
        header_style="bold cyan",
        box=None
    )
    
    # Set up columns
    table.add_column("#", justify="right", style="dim")
    table.add_column("Selected", justify="center")
    table.add_column("Title", justify="left")
    table.add_column("Artist", justify="left") 
    table.add_column("Duration", justify="right")

    # Add each track as a row
    for i, track in enumerate(results):
        duration = f"{int(track.duration)//60}:{int(track.duration)%60:02d}"
        selected = "✓" if i in selected_indices else " "
        
        row_style = "reverse" if i == current_selection else ""
        table.add_row(
            str(i + 1),
            selected,
            track.title[:40],
            track.author.name[:20],
            duration,
            style=row_style
        )

    table.caption = "⌨️ Use ↑/↓ to navigate, [bold]Space[/] to select/deselect, [bold]Enter[/] to download, [bold]Q[/] to quit"
    return table


def select_with_arrows(results: List[Track]) -> List[Track]:
    """Let user select tracks using keyboard navigation."""
    current_selection = 0
    selected_indices = set()
    running = True
    
    def on_press(key):
        nonlocal current_selection, selected_indices, running
        
        try:
            if key == keyboard.Key.up and current_selection > 0:
                current_selection -= 1
            elif key == keyboard.Key.down and current_selection < len(results) - 1:
                current_selection += 1
            elif key == keyboard.Key.space:
                if current_selection in selected_indices:
                    selected_indices.remove(current_selection)
                else:
                    selected_indices.add(current_selection)
            elif key == keyboard.Key.enter:
                running = False
            elif hasattr(key, 'char') and key.char == 'q':
                console.print("Thanks for using JioSaavn CLI! 👋", style="yellow")
                sys.exit(0)
        except AttributeError:
            pass
            
    # Start keyboard listener
    listener = keyboard.Listener(on_press=on_press)
    listener.start()
    
    # Show live track list
    with Live(
        render_track_list(results, current_selection, selected_indices),
        refresh_per_second=4,
        auto_refresh=True,
        screen=True
    ) as live:
        while running:
            live.update(render_track_list(results, current_selection, selected_indices))
    
    listener.stop()
    return [results[i] for i in selected_indices]


def download(tracks: List[Track]) -> None:
    """Download selected tracks with progress bar."""
    if not tracks:
        return

    args = parse_args()
    os.makedirs(args.outdir, exist_ok=True)

    console.print("Preparing downloads...", style="cyan")
    for track in tracks:
        try:
            # Create safe filename
            filename = "".join(
                c for c in f"{track.title} - {track.author.name}.mp3"
                if c.isalnum() or c in (' ', '-', '_', '.')
            )
            filepath = os.path.join(args.outdir, filename)
            
            # Check for existing file
            if os.path.exists(filepath):
                if not Confirm.ask(f"[yellow]File {filename} already exists. Overwrite?[/]"):
                    continue

            # Download with progress bar
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                BarColumn(),
                TaskProgressColumn()
            ) as progress:
                task = progress.add_task(f"Downloading {filename}", total=100)
                buffer = http_client.get_buffer(track.media_url)
                chunk_size = len(buffer) // 100
                
                with open(filepath, 'wb') as f:
                    for i in range(0, len(buffer), chunk_size):
                        f.write(buffer[i:i + chunk_size])
                        progress.update(task, advance=1)
                        
            console.print(f"✅ Successfully downloaded: {filename}", style="green")
        
        except Exception as e:
            console.print(f"❌ Failed to download {filename}: {str(e)}", style="red")
            if Confirm.ask("[yellow]Would you like to retry?[/]"):
                try:
                    download([track])
                except:
                    console.print("Failed to download after retry. Skipping...", style="red")


def search(query: str) -> Optional[List[Track]]:
    """Search for tracks and handle different result types."""
    console.print(f"\n🔍 Searching for: {query}", style="cyan")
    
    try:
        # Handle URLs vs search terms
        results = saavn.search(query) if "https://" in query else saavn._search_tracks(query, count=5, pages=1)

        if not results:
            console.print("😕 No matches found! Try different keywords?", style="red")
            return None

        # Handle different result types
        if isinstance(results, (Playlist, Album, Artist)):
            console.print(f"Found {len(results.tracks)} tracks in {results.__class__.__name__.lower()}", style="green")
            return select_with_arrows(results.tracks)
        elif isinstance(results, list):
            console.print(f"Found {len(results)} matches", style="green")
            return select_with_arrows(results)
        elif isinstance(results, Track):
            console.print(f"\nFound this track: {results.title} by {results.author.name}", style="cyan")
            if Confirm.ask("\n[yellow]Would you like to download this track?[/]"):
                download([results])
            return None
            
    except Exception as e:
        console.print(f"❌ Search failed: {str(e)}", style="red")
        if Confirm.ask("[yellow]Would you like to retry?[/]"):
            return search(query)
    return None


def main():
    """Main entry point for the CLI app."""
    try:
        args = parse_args()
        if args.search:
            if tracks := search(args.search):
                download(tracks)
        else:
            print_banner()
            
    except KeyboardInterrupt:
        console.print("\n👋 Thanks for using JioSaavn CLI! Come back soon!", style="yellow")
    except Exception as e:
        console.print(f"Unexpected error: {e}", style="red")
        sys.exit(1)


if __name__ == "__main__":
    main()
