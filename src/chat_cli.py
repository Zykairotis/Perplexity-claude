#!/usr/bin/env python3
"""
Perplexity CLI Chat Tool

A simple command-line interface for getting responses from Perplexity AI.
Just ask questions and get answers - no complexity, no history management.
"""

import argparse
import asyncio
import json
import sys
from typing import Dict, List

import httpx
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.live import Live
from prompt_toolkit import prompt
from prompt_toolkit.history import InMemoryHistory
from prompt_toolkit.key_binding import KeyBindings

# Configuration
DEFAULT_BASE_URL = "http://localhost:4000"
DEFAULT_MODE = "auto"
DEFAULT_MODEL = "auto"

# Available modes and their models (only working ones from s2.py)
AVAILABLE_MODES = {
    "auto": ["auto"],
    "pro": ["sonar", "claude37sonnetthinking", "grok4"]
}

# Model mapping from user-friendly names to s2.py format
MODEL_MAPPING = {
    # Auto mode - use pro-sonar as default
    "auto": "pro-sonar",

    # Pro mode models
    "sonar": "pro-sonar",
    "claude37sonnetthinking": "pro-claude37sonnetthinking",
    "grok4": "pro-grok4",

    # User-friendly aliases
    "gpt-4o": "pro-sonar",
    "claude": "pro-claude37sonnetthinking",
    "claude 3.7 sonnet": "pro-claude37sonnetthinking",
    "grok-4": "pro-grok4",
    "grok": "pro-grok4"
}

AVAILABLE_SOURCES = ["web", "scholar", "social", "edgar"]  # All sources available

class PerplexityCLI:
    def __init__(self, base_url: str, mode: str, model: str, sources: List[str]):
        self.base_url = base_url.rstrip('/')
        self.console = Console()
        self.client = httpx.AsyncClient(timeout=120.0)
        self.mode = mode
        self.model = model
        self.sources = sources

        # Key bindings
        self.kb = KeyBindings()
        self.setup_key_bindings()

    def setup_key_bindings(self):
        """Setup custom key bindings"""
        @self.kb.add('c-c')
        def _(event):
            """Handle Ctrl+C"""
            event.app.exit(exception=KeyboardInterrupt, style='class:aborting')

        @self.kb.add('c-d')
        def _(event):
            """Handle Ctrl+D (EOF)"""
            event.app.exit()

    async def check_server_health(self) -> bool:
        """Check if the server is running"""
        try:
            response = await self.client.get(f"{self.base_url}/health")
            return response.status_code == 200
        except Exception:
            return False

    async def send_message(self, message: str, stream: bool = False) -> str:
        """Send a message to the OpenAI-compatible API and return the response"""
        # Convert to OpenAI format
        messages = [{"role": "user", "content": message}]

        # Map model to s2.py format
        model_str = MODEL_MAPPING.get(self.model, f"pro-{self.model}")

        payload = {
            "model": model_str,
            "messages": messages,
            "stream": stream
        }

        try:
            if stream:
                return await self._handle_streaming_response(payload)
            else:
                response = await self.client.post(
                    f"{self.base_url}/v1/chat/completions",
                    json=payload,
                    headers={"Content-Type": "application/json"}
                )
                response.raise_for_status()
                data = response.json()
                return data["choices"][0]["message"]["content"]

        except httpx.HTTPStatusError as e:
            try:
                error_data = e.response.json()
                error_msg = error_data.get("detail", f"HTTP {e.response.status_code}")
            except:
                error_msg = f"HTTP {e.response.status_code}: {e.response.text}"
            return f"Error: {error_msg}"
        except Exception as e:
            return f"Error: {str(e)}"

    async def _handle_streaming_response(self, payload: Dict) -> str:
        """Handle streaming response from the OpenAI-compatible API"""
        full_response = ""

        try:
            # Use the OpenAI streaming endpoint
            async with self.client.stream(
                "POST",
                f"{self.base_url}/v1/chat/completions",
                json=payload,
                headers={"Content-Type": "application/json"}
            ) as response:
                response.raise_for_status()

                # Show model info
                model_display = self.model if self.mode != "auto" else "Auto"
                self.console.print(f"\n[bold blue]{model_display} ({self.mode.title()}):[/bold blue]")

                with Live(console=self.console, refresh_per_second=4) as live:
                    display_text = ""

                    async for line in response.aiter_lines():
                        if line.startswith("data: "):
                            data_str = line[6:]  # Remove "data: " prefix

                            if data_str.strip() == "[DONE]":
                                break

                            try:
                                data = json.loads(data_str)

                                # Handle OpenAI streaming format
                                if "choices" in data and len(data["choices"]) > 0:
                                    delta = data["choices"][0].get("delta", {})
                                    if "content" in delta:
                                        content = delta["content"]
                                        full_response += content
                                        display_text += content
                                        live.update(Markdown(display_text))

                            except json.JSONDecodeError:
                                continue

                self.console.print()  # Add newline after completion

        except Exception as e:
            # Fallback to non-streaming if streaming fails
            self.console.print(f"[yellow]Streaming failed, using regular request...[/yellow]")
            try:
                # Remove stream from payload for non-streaming request
                fallback_payload = payload.copy()
                fallback_payload["stream"] = False

                response = await self.client.post(
                    f"{self.base_url}/v1/chat/completions",
                    json=fallback_payload,
                    headers={"Content-Type": "application/json"}
                )
                response.raise_for_status()
                data = response.json()
                full_response = data["choices"][0]["message"]["content"]

                # Display the response
                model_display = self.model if self.mode != "auto" else "Auto"
                self.console.print(f"\n[bold blue]{model_display} ({self.mode.title()}):[/bold blue]")
                self.console.print(Markdown(full_response))
                self.console.print()

            except Exception as fallback_error:
                return f"Error: {str(fallback_error)}"

        return full_response

    def show_config(self):
        """Display current configuration"""
        self.console.print(f"[dim]Mode: {self.mode} | Model: {self.model} | Sources: {', '.join(self.sources)} | Server: {self.base_url}[/dim]")

    def show_detailed_config(self):
        """Show detailed configuration"""
        from rich.table import Table

        config_table = Table(title="Current Configuration")
        config_table.add_column("Setting", style="cyan")
        config_table.add_column("Value", style="white")

        config_table.add_row("Server URL", self.base_url)
        config_table.add_row("Mode", self.mode)
        config_table.add_row("Model", self.model)
        config_table.add_row("Sources", ", ".join(self.sources))

        self.console.print(config_table)

    def show_available_options(self):
        """Show available modes and models"""
        self.console.print("\n[bold]Available Modes and Models:[/bold]")

        for mode, models in AVAILABLE_MODES.items():
            status = "[green]Current[/green]" if mode == self.mode else ""
            self.console.print(f"\n[bold cyan]{mode.title()}[/bold cyan] {status}")

            for model in models:
                model_status = "[green]→ Current[/green]" if model == self.model and mode == self.mode else ""
                self.console.print(f"  • {model} {model_status}")

        self.console.print(f"\n[bold]Available Sources:[/bold]")
        for source in AVAILABLE_SOURCES:
            status = "[green]✓[/green]" if source in self.sources else " "
            self.console.print(f"  {status} {source}")

    def get_recommendations(self):
        """Get recommendations based on current setup"""
        recommendations = []

        if self.mode == "auto":
            recommendations.append("💡 Try [yellow]Pro mode[/yellow] for better responses: [cyan]/mode pro[/cyan]")

        if self.model == "auto":
            recommendations.append("🤖 Try specific models: [cyan]/model sonar[/cyan] or [cyan]/model grok4[/cyan]")

        if len(self.sources) == 1 and self.sources[0] == "web":
            recommendations.append("📚 Add more sources: [cyan]/sources web,scholar[/cyan]")

        if self.mode == "pro" and self.model == "grok4":
            recommendations.append("🔥 Great choice! Grok4 is excellent for conversational AI")

        return recommendations

    def show_help(self):
        """Display help information"""
        help_text = """
[bold]Perplexity CLI Chat Tool[/bold]

[bold cyan]Interactive Commands:[/bold cyan]
  [yellow]/help[/yellow]           - Show this help
  [yellow]/config[/yellow]         - Show detailed configuration
  [yellow]/options[/yellow]        - Show available modes, models, and sources
  [yellow]/mode <name>[/yellow]    - Change mode (auto, pro)
  [yellow]/model <name>[/yellow]   - Change model (sonar, grok4, claude37sonnetthinking)
  [yellow]/sources <list>[/yellow] - Set sources (web,scholar,social,edgar)
  [yellow]/recommend[/yellow]      - Get recommendations for better results
  [yellow]/quit[/yellow] or [yellow]/exit[/yellow] - Exit the chat

[bold cyan]Examples:[/bold cyan]
  [yellow]/mode pro[/yellow]                    - Switch to Pro mode
  [yellow]/model grok4[/yellow]                 - Use Grok4 model
  [yellow]/sources web,scholar[/yellow]         - Use web and scholar sources
  [yellow]/recommend[/yellow]                   - Get personalized tips

[bold cyan]Tips:[/bold cyan]
  • Use [yellow]Ctrl+C[/yellow] to cancel current input
  • Use [yellow]Ctrl+D[/yellow] to force quit
  • Commands start with [yellow]/[/yellow]
  • Type normally to chat with AI
        """
        self.console.print(Panel(help_text, title="Help", border_style="blue"))

    async def handle_command(self, command: str) -> bool:
        """Handle interactive commands. Returns True if should continue, False if should exit."""
        parts = command.strip().split(None, 1)
        cmd = parts[0].lower()
        arg = parts[1] if len(parts) > 1 else ""

        if cmd in ["/quit", "/exit", "/q"]:
            return False
        elif cmd == "/help":
            self.show_help()
        elif cmd == "/config":
            self.show_detailed_config()
        elif cmd == "/options":
            self.show_available_options()
        elif cmd == "/recommend":
            recommendations = self.get_recommendations()
            if recommendations:
                self.console.print("\n[bold green]💡 Recommendations:[/bold green]")
                for rec in recommendations:
                    self.console.print(f"  {rec}")
            else:
                self.console.print("[green]✨ Your current setup looks great![/green]")
        elif cmd == "/mode":
            if arg:
                if arg in AVAILABLE_MODES:
                    old_mode = self.mode
                    self.mode = arg
                    # Reset to first model in the new mode
                    self.model = AVAILABLE_MODES[arg][0]
                    self.console.print(f"[green]Switched from {old_mode} to {arg} mode (model: {self.model})[/green]")

                    # Show recommendations
                    recommendations = self.get_recommendations()
                    if recommendations:
                        self.console.print("\n[dim]💡 Tip: " + recommendations[0] + "[/dim]")
                else:
                    self.console.print(f"[red]Mode '{arg}' not available. Available modes: {', '.join(AVAILABLE_MODES.keys())}[/red]")
            else:
                self.console.print("[yellow]Usage: /mode <mode_name>[/yellow]")
                self.console.print(f"Available modes: {', '.join(AVAILABLE_MODES.keys())}")
        elif cmd == "/model":
            if arg:
                if arg in AVAILABLE_MODES.get(self.mode, []):
                    old_model = self.model
                    self.model = arg
                    self.console.print(f"[green]Switched from {old_model} to {arg}[/green]")

                    # Show recommendations
                    recommendations = self.get_recommendations()
                    if recommendations:
                        self.console.print("\n[dim]💡 Tip: " + recommendations[0] + "[/dim]")
                else:
                    available = AVAILABLE_MODES.get(self.mode, [])
                    self.console.print(f"[red]Model '{arg}' not available for mode '{self.mode}'. Available models: {', '.join(available)}[/red]")
            else:
                available = AVAILABLE_MODES.get(self.mode, [])
                self.console.print("[yellow]Usage: /model <model_name>[/yellow]")
                self.console.print(f"Available models for {self.mode} mode: {', '.join(available)}")
        elif cmd == "/sources":
            if arg:
                # Parse sources (handle both space and comma separated)
                sources = arg.replace(',', ' ').split()
                valid_sources = [s for s in sources if s in AVAILABLE_SOURCES]
                invalid_sources = [s for s in sources if s not in AVAILABLE_SOURCES]

                if valid_sources:
                    old_sources = self.sources.copy()
                    self.sources = valid_sources
                    self.console.print(f"[green]Sources changed from {', '.join(old_sources)} to {', '.join(valid_sources)}[/green]")
                    if invalid_sources:
                        self.console.print(f"[yellow]Invalid sources ignored: {', '.join(invalid_sources)}[/yellow]")

                    # Show recommendations
                    recommendations = self.get_recommendations()
                    if recommendations:
                        self.console.print("\n[dim]💡 Tip: " + recommendations[0] + "[/dim]")
                else:
                    self.console.print(f"[red]No valid sources provided. Available sources: {', '.join(AVAILABLE_SOURCES)}[/red]")
            else:
                self.console.print(f"[yellow]Usage: /sources <source1> <source2> ... [/yellow]")
                self.console.print(f"Available sources: {', '.join(AVAILABLE_SOURCES)}")
        else:
            self.console.print(f"[red]Unknown command: {cmd}. Type /help for available commands.[/red]")

        return True

    async def interactive_chat(self):
        """Start interactive chat mode"""
        # Check server health
        if not await self.check_server_health():
            self.console.print(f"[red]Cannot connect to Perplexity server at {self.base_url}[/red]")
            self.console.print("[yellow]Please make sure the server is running and try again.[/yellow]")
            return

        # Display welcome
        model_display = self.model if self.mode != "auto" else "Auto"
        sources_display = ", ".join(self.sources)

        welcome_text = f"""[bold green]Perplexity CLI Chat[/bold green]

[bold cyan]Configuration:[/bold cyan]
• Mode: [yellow]{self.mode.title()}[/yellow]
• Model: [yellow]{model_display}[/yellow]
• Sources: [yellow]{sources_display}[/yellow]

Type your questions and get answers from Perplexity AI.
Use [yellow]/help[/yellow] for commands, [yellow]Ctrl+C[/yellow] to cancel, [yellow]Ctrl+D[/yellow] to force quit."""

        self.console.print(Panel(welcome_text, title="Perplexity CLI", border_style="blue"))

        # Show initial recommendations
        recommendations = self.get_recommendations()
        if recommendations:
            self.console.print(f"\n[dim]💡 {recommendations[0]}[/dim]")

        # Setup history
        history = InMemoryHistory()

        while True:
            try:
                # Get user input
                user_input = await asyncio.get_event_loop().run_in_executor(
                    None,
                    lambda: prompt(
                        "Ask: ",
                        history=history,
                        key_bindings=self.kb
                    )
                )

                if not user_input or not user_input.strip():
                    continue

                # Handle commands
                if user_input.startswith('/'):
                    should_continue = await self.handle_command(user_input)
                    if not should_continue:
                        break
                    continue

                # Send message to Perplexity
                response = await self.send_message(user_input, stream=False)

                # Display the response
                if response.startswith("Error:"):
                    self.console.print(f"[red]{response}[/red]")
                else:
                    # Show successful response
                    model_display = self.model if self.mode != "auto" else "Auto"
                    self.console.print(f"\n[bold blue]{model_display} ({self.mode.title()}):[/bold blue]")
                    self.console.print(Markdown(response))
                    self.console.print()

            except KeyboardInterrupt:
                self.console.print("\n[yellow]Input cancelled. Use /quit or Ctrl+D to exit.[/yellow]")
                continue
            except EOFError:
                # Force quit on Ctrl+D
                self.console.print("\n[yellow]Force quit (Ctrl+D)[/yellow]")
                break
            except Exception as e:
                self.console.print(f"[red]Unexpected error: {e}[/red]")
                continue

        self.console.print("\n[bold blue]Goodbye! 👋[/bold blue]")

    async def single_message(self, message: str, stream: bool = False):
        """Send a single message and print response"""
        # Check server health
        if not await self.check_server_health():
            self.console.print(f"[red]Cannot connect to Perplexity server at {self.base_url}[/red]")
            return

        self.show_config()
        response = await self.send_message(message, stream=stream)

        # Show any errors or non-streamed responses
        if response and (not stream or response.startswith("Error:")):
            model_display = self.model if self.mode != "auto" else "Auto"
            self.console.print(f"\n[bold blue]{model_display} ({self.mode.title()}):[/bold blue]")
            if response.startswith("Error:"):
                self.console.print(f"[red]{response}[/red]")
            else:
                self.console.print(Markdown(response))

    async def close(self):
        """Clean up resources"""
        await self.client.aclose()

async def main():
    parser = argparse.ArgumentParser(
        description="Perplexity CLI Chat Tool - Simple AI Search Interface",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                                    # Start interactive chat
  %(prog)s "What is quantum computing?"       # Send single message
  %(prog)s --mode pro --model gpt-4o "Explain AI"  # Use specific mode and model
  chat_cli.py --sources web,scholar "Research topic"  # Use specific sources
        """
    )

    parser.add_argument(
        "message",
        nargs="?",
        help="Single message to send (if not provided, starts interactive mode)"
    )

    parser.add_argument(
        "--base-url",
        default=DEFAULT_BASE_URL,
        help=f"Base URL for the Perplexity server (default: {DEFAULT_BASE_URL})"
    )

    parser.add_argument(
        "--mode",
        choices=list(AVAILABLE_MODES.keys()),
        default=DEFAULT_MODE,
        help=f"Search mode (default: {DEFAULT_MODE})"
    )

    parser.add_argument(
        "--model",
        help="Specific model to use (must be compatible with selected mode)"
    )

    parser.add_argument(
        "--sources",
        help="Comma-separated list of sources (web,scholar,social,edgar)"
    )

    parser.add_argument(
        "--stream",
        action="store_true",
        help="Enable streaming responses"
    )

    args = parser.parse_args()

    # Set model
    model = args.model if args.model else AVAILABLE_MODES[args.mode][0]

    # Validate model for mode
    if args.model and args.model not in AVAILABLE_MODES.get(args.mode, []):
        available = AVAILABLE_MODES.get(args.mode, [])
        print(f"Error: Model '{args.model}' not available for mode '{args.mode}'")
        print(f"Available models for {args.mode}: {', '.join(available)}")
        sys.exit(1)

    # Set sources
    sources = ["web"]  # default
    if args.sources:
        sources = [s.strip() for s in args.sources.split(',')]
        valid_sources = [s for s in sources if s in AVAILABLE_SOURCES]
        invalid_sources = [s for s in sources if s not in AVAILABLE_SOURCES]

        if not valid_sources:
            print(f"Error: No valid sources provided. Available: {', '.join(AVAILABLE_SOURCES)}")
            sys.exit(1)

        if invalid_sources:
            print(f"Warning: Invalid sources ignored: {', '.join(invalid_sources)}")

        sources = valid_sources

    # Create CLI instance
    cli = PerplexityCLI(args.base_url, args.mode, model, sources)

    try:
        if args.message:
            # Single message mode
            stream_enabled = args.stream
            await cli.single_message(args.message, stream=stream_enabled)
        else:
            # Interactive mode
            await cli.interactive_chat()
    except KeyboardInterrupt:
        print("\nInterrupted by user")
    except Exception as e:
        print(f"Fatal error: {e}")
        sys.exit(1)
    finally:
        await cli.close()

if __name__ == "__main__":
    asyncio.run(main())
