import textwrap
from typing import Any, Dict, List, Optional, Set, Union
from rich.console import Console, Group
from rich.live import Live
from rich.panel import Panel
from rich.status import Status
from rich.text import Text
from rich.markdown import Markdown
import time


class StreamingResponseHandler:
    """Handler for streaming team responses with rich console output"""

    def __init__(
            self,
            console: Optional[Console] = None,
            show_message: bool = True,
            show_reasoning: bool = True,
            show_tool_calls: bool = True,
            show_member_responses: bool = True,
            markdown: bool = False,
    ):
        self.console = console or Console()
        self.show_message = show_message
        self.show_reasoning = show_reasoning
        self.show_tool_calls = show_tool_calls
        self.show_member_responses = show_member_responses
        self.markdown = markdown

        # Content trackers
        self.response_content = ""
        self.reasoning_content = ""
        self.reasoning_steps = []
        self.processed_reasoning_steps = set()  # Track processed reasoning steps
        self.input_content = ""

        # Tool call trackers
        self.team_tool_calls = []
        self.member_tool_calls = {}
        self.processed_tool_calls = set()

        # Member response trackers
        self.member_responses = {}

        # Timing
        self.start_time = time.time()

    def _get_elapsed_time(self) -> float:
        """Get elapsed time since start"""
        return time.time() - self.start_time

    def _create_panel(
            self,
            content: Union[str, Text, Markdown],
            title: str,
            border_style: str = "blue"
    ) -> Panel:
        """Create a styled panel"""
        return Panel(
            content,
            title=title,
            border_style=border_style,
            padding=(1, 2),
        )

    def _add_reasoning_step(self, step: Any):
        """Add a reasoning step, avoiding duplicates"""
        if step is None:
            return

        # Create a unique identifier for the reasoning step
        # Use multiple attributes to create a more robust ID
        step_id = None

        # Try to create ID from step attributes
        if hasattr(step, 'title') and hasattr(step, 'reasoning'):
            title = getattr(step, 'title', '')
            reasoning = getattr(step, 'reasoning', '')
            # Use a hash of title + reasoning content (first 100 chars to avoid huge IDs)
            step_id = hash(f"{title}:{reasoning[:100] if reasoning else ''}")
        else:
            # Fallback to hash of string representation
            step_id = hash(str(step)[:200])

        # Only add if we haven't seen this step before
        if step_id not in self.processed_reasoning_steps:
            self.processed_reasoning_steps.add(step_id)
            self.reasoning_steps.append(step)

    def _format_reasoning_step(self, step: Any) -> str:
        """Format a reasoning step for display"""
        if isinstance(step, str):
            return step

        # Try to extract content from ReasoningStep object
        content = getattr(step, 'content', None)
        if content:
            return str(content)

        # Try to extract text or message
        text = getattr(step, 'text', None) or getattr(step, 'message', None)
        if text:
            return str(text)

        # Fallback to string representation
        return str(step)

    def _format_tool_call(self, tool: Any) -> str:
        """Format a tool call for display"""
        if tool is None:
            return "Unknown Tool"

        tool_name = getattr(tool, 'tool_name', None) or getattr(tool, 'name', str(tool))
        tool_args = getattr(tool, 'tool_args', None) or getattr(tool, 'arguments', {})

        if tool_args and isinstance(tool_args, dict):
            try:
                args_str = ", ".join(f"{k}={v}" for k, v in tool_args.items())
                return f"{tool_name}({args_str})"
            except Exception:
                return f"{tool_name}()"
        return f"{tool_name}()"

    def _add_tool_call(self, tool: Any, member_id: Optional[str] = None):
        """Add a tool call, avoiding duplicates"""
        if tool is None:
            return

        # Generate unique ID for this tool call
        tool_id = getattr(tool, 'tool_call_id', None) or str(hash(str(tool)))

        if tool_id not in self.processed_tool_calls:
            self.processed_tool_calls.add(tool_id)

            if member_id:
                if member_id not in self.member_tool_calls:
                    self.member_tool_calls[member_id] = []
                self.member_tool_calls[member_id].append(tool)
            else:
                self.team_tool_calls.append(tool)

    def _build_panels(self) -> List[Panel]:
        """Build all panels for current state"""
        panels = []
        elapsed = self._get_elapsed_time()

        # Message panel
        if self.input_content and self.show_message:
            message_panel = self._create_panel(
                Text(self.input_content, style="green"),
                "Message",
                border_style="cyan"
            )
            panels.append(message_panel)

        # Reasoning steps panels
        if self.reasoning_steps and self.show_reasoning:
            for i, step in enumerate(self.reasoning_steps, 1):
                reasoning_text = self._format_reasoning_step(step)
                reasoning_panel = self._create_panel(
                    Text(reasoning_text),
                    f"Reasoning Step {i}",
                    border_style="green"
                )
                panels.append(reasoning_panel)

        # Reasoning content panel (for string-based reasoning)
        if self.reasoning_content and self.show_reasoning:
            thinking_panel = self._create_panel(
                Text(self.reasoning_content),
                f"Thinking ({elapsed:.1f}s)",
                border_style="green"
            )
            panels.append(thinking_panel)

        # Member tool calls and responses
        for member_id in sorted(self.member_tool_calls.keys()):
            # Member tool calls panel
            if self.show_tool_calls and self.member_tool_calls[member_id]:
                tool_calls_text = self._format_tool_calls_list(
                    self.member_tool_calls[member_id]
                )
                member_name = member_id  # You can map this to actual names

                tool_panel = self._create_panel(
                    tool_calls_text,
                    f"{member_name} Tool Calls",
                    border_style="yellow"
                )
                panels.append(tool_panel)

            # Member response panel
            if self.show_member_responses and member_id in self.member_responses:
                response_content = self.member_responses[member_id]
                if self.markdown:
                    response_content = Markdown(response_content)
                else:
                    response_content = Text(response_content)

                member_panel = self._create_panel(
                    response_content,
                    f"{member_id} Response",
                    border_style="magenta"
                )
                panels.append(member_panel)

        # Team tool calls panel
        if self.show_tool_calls and self.team_tool_calls:
            tool_calls_text = self._format_tool_calls_list(self.team_tool_calls)
            team_tool_panel = self._create_panel(
                tool_calls_text,
                "Team Tool Calls",
                border_style="yellow"
            )
            panels.append(team_tool_panel)

        # Team response panel
        if self.response_content:
            response_content = self.response_content
            if self.markdown:
                response_content = Markdown(response_content)
            else:
                response_content = Text(response_content)

            response_panel = self._create_panel(
                response_content,
                f"Response ({elapsed:.1f}s)",
                border_style="blue"
            )
            panels.append(response_panel)

        return panels

    def _format_tool_calls_list(self, tool_calls: List[Any]) -> str:
        """Format a list of tool calls with wrapping"""
        console_width = self.console.width
        panel_width = console_width - 10  # Account for panel borders

        lines = []
        for tool in tool_calls:
            formatted = self._format_tool_call(tool)
            wrapped = textwrap.fill(
                f"• {formatted}",
                width=panel_width,
                subsequent_indent="  "
            )
            lines.append(wrapped)

        return "\n\n".join(lines)

    def handle_stream(
            self,
            team: Any,
            input: str,
            **kwargs
    ):
        """Handle streaming response from team"""
        self.input_content = input
        self.start_time = time.time()

        with Live(console=self.console, refresh_per_second=10) as live:
            # Initial status
            status = Status(
                "Thinking...",
                spinner="aesthetic",
                speed=0.4
            )
            live.update(status)

            # Get streaming response
            response_stream = team.run(
                input=input,
                stream=True,
                stream_intermediate_steps=True,
                **kwargs
            )

            # Process events
            for event in response_stream:
                try:
                    event_type = getattr(event, 'event', None)

                    # Handle different event types
                    if event_type == "TeamRunContent":
                        # Main response content
                        content = getattr(event, 'content', '')
                        if isinstance(content, str):
                            self.response_content += content

                    elif event_type == "run_content":
                        # Alternative content event
                        content = getattr(event, 'content', '')
                        if isinstance(content, str):
                            self.response_content += content

                    elif event_type == "TeamReasoningStep":
                        # Reasoning content - could be string or ReasoningStep object
                        reasoning = getattr(event, 'content', '')
                        if reasoning:
                            if isinstance(reasoning, str):
                                self.reasoning_content += reasoning
                            else:
                                # It's a ReasoningStep object - deduplicate
                                self._add_reasoning_step(reasoning)

                    elif event_type == "reasoning_content":
                        # Alternative reasoning event
                        reasoning = getattr(event, 'reasoning_content', '')
                        if reasoning:
                            if isinstance(reasoning, str):
                                self.reasoning_content += reasoning
                            else:
                                self._add_reasoning_step(reasoning)

                    # Handle reasoning_steps attribute - deduplicate each step
                    if hasattr(event, 'reasoning_steps') and event.reasoning_steps:
                        if isinstance(event.reasoning_steps, list):
                            for step in event.reasoning_steps:
                                self._add_reasoning_step(step)
                        else:
                            self._add_reasoning_step(event.reasoning_steps)

                    elif event_type == "TeamToolCallStarted":
                        # Team tool call started
                        tool = getattr(event, 'tool', None)
                        if tool:
                            self._add_tool_call(tool)

                    elif event_type == "tool_call_completed":
                        # Team tool call completed
                        tool = getattr(event, 'tool', None)
                        if tool:
                            self._add_tool_call(tool)

                    elif event_type == "ToolCallStarted":
                        # Member tool call started
                        tool = getattr(event, 'tool', None)
                        member_id = getattr(event, 'member_id', 'unknown')
                        if tool:
                            self._add_tool_call(tool, member_id)

                    elif event_type == "ToolCallCompleted":
                        # Member tool call completed
                        tool = getattr(event, 'tool', None)
                        member_id = getattr(event, 'member_id', 'unknown')
                        if tool:
                            self._add_tool_call(tool, member_id)

                    # Handle member responses
                    if hasattr(event, 'member_responses') and event.member_responses:
                        for member_response in event.member_responses:
                            member_id = getattr(
                                member_response,
                                'agent_id',
                                getattr(member_response, 'team_id', None)
                            )

                            if member_id:
                                # Extract member content
                                content = getattr(member_response, 'content', '')
                                if content and member_id not in self.member_responses:
                                    self.member_responses[member_id] = content
                                elif content:
                                    self.member_responses[member_id] += content

                                # Extract member tools
                                tools = getattr(member_response, 'tools', None)
                                if tools is not None:
                                    for tool in tools:
                                        self._add_tool_call(tool, member_id)

                    # Update display
                    panels = self._build_panels()
                    if panels:
                        live.update(Group(*panels))
                    else:
                        live.update(status)

                except Exception as e:
                    # Log error but continue processing
                    self.console.print(f"[red]Error processing event: {e}[/red]")
                    continue

            # Final update without status
            panels = self._build_panels()
            if panels:
                live.update(Group(*panels))