#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TUI Dashboard Module - 终端用户界面仪表盘模块

Provides a beautiful terminal-based dashboard for workspace and session
monitoring with zero external dependencies.
"""

import os
import sys
import time
import shutil
from typing import Dict, List, Optional, Any


class Colors:
    """ANSI color codes for terminal output."""
    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    ITALIC = "\033[3m"
    UNDERLINE = "\033[4m"
    
    # Foreground colors
    BLACK = "\033[30m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"
    
    # Bright foreground colors
    BRIGHT_BLACK = "\033[90m"
    BRIGHT_RED = "\033[91m"
    BRIGHT_GREEN = "\033[92m"
    BRIGHT_YELLOW = "\033[93m"
    BRIGHT_BLUE = "\033[94m"
    BRIGHT_MAGENTA = "\033[95m"
    BRIGHT_CYAN = "\033[96m"
    BRIGHT_WHITE = "\033[97m"
    
    # Background colors
    BG_BLACK = "\033[40m"
    BG_RED = "\033[41m"
    BG_GREEN = "\033[42m"
    BG_YELLOW = "\033[43m"
    BG_BLUE = "\033[44m"
    BG_MAGENTA = "\033[45m"
    BG_CYAN = "\033[46m"
    BG_WHITE = "\033[47m"


class Dashboard:
    """Terminal dashboard for workspace and session monitoring."""
    
    ICONS = {
        "workspace": "📁",
        "agent": "🤖",
        "shell": "💻",
        "server": "🖥️",
        "task": "📋",
        "running": "🟢",
        "stopped": "🔴",
        "suspended": "🟡",
        "python": "🐍",
        "node": "⬢",
        "rust": "🦀",
        "go": "🐹",
        "docker": "🐳",
        "git": "📦",
        "claude": "✨",
        "codex": "🔷",
        "cursor": "🖱️",
        "gemini": "♊",
        "aider": "🦞",
        "copilot": "🪶",
        "ollama": "🦙",
        "arrow": "➜",
        "star": "⭐",
        "time": "⏱️",
        "cpu": "📊",
        "memory": "💾",
        "disk": "💿",
        "network": "🌐",
        "check": "✓",
        "cross": "✗",
        "warning": "⚠️",
        "info": "ℹ️",
        "rocket": "🚀",
        "fire": "🔥",
        "sparkle": "✨",
    }
    
    def __init__(self, workspace_manager=None, session_manager=None):
        self.workspace_manager = workspace_manager
        self.session_manager = session_manager
        self.term_width = self._get_terminal_width()
        self.use_colors = self._supports_colors()
    
    def _get_terminal_width(self) -> int:
        """Get terminal width."""
        try:
            return shutil.get_terminal_size().columns
        except Exception:
            return 80
    
    def _supports_colors(self) -> bool:
        """Check if terminal supports colors."""
        if os.name == "nt":
            return True  # Windows Terminal supports colors
        return hasattr(sys.stdout, "isatty") and sys.stdout.isatty()
    
    def _color(self, text: str, color: str) -> str:
        """Apply color to text if supported."""
        if self.use_colors:
            return f"{color}{text}{Colors.RESET}"
        return text
    
    def _bold(self, text: str) -> str:
        """Make text bold."""
        return self._color(text, Colors.BOLD)
    
    def _center(self, text: str, width: Optional[int] = None, 
                fill: str = " ") -> str:
        """Center text."""
        if width is None:
            width = self.term_width
        return text.center(width, fill)
    
    def _truncate(self, text: str, max_len: int, suffix: str = "...") -> str:
        """Truncate text to max length."""
        if len(text) <= max_len:
            return text
        return text[:max_len - len(suffix)] + suffix
    
    def _format_duration(self, seconds: float) -> str:
        """Format duration in human-readable form."""
        if seconds < 60:
            return f"{int(seconds)}s"
        elif seconds < 3600:
            return f"{int(seconds / 60)}m"
        elif seconds < 86400:
            return f"{int(seconds / 3600)}h"
        else:
            return f"{int(seconds / 86400)}d"
    
    def _draw_line(self, char: str = "─", color: str = Colors.DIM) -> str:
        """Draw a horizontal line."""
        line = char * self.term_width
        return self._color(line, color)
    
    def _draw_box(self, title: str, content: List[str], 
                  width: Optional[int] = None) -> str:
        """Draw a box with title."""
        if width is None:
            width = min(60, self.term_width - 4)
        
        lines = []
        top = f"┌─ {self._bold(title)} " + "─" * (width - len(title) - 5) + "┐"
        lines.append(top)
        
        for line in content:
            padded = f"│ {self._truncate(line, width - 4)}"
            padded += " " * (width - len(padded) + 1) + "│"
            lines.append(padded)
        
        bottom = "└" + "─" * (width - 2) + "┘"
        lines.append(bottom)
        
        return "\n".join(lines)
    
    def render_header(self) -> str:
        """Render dashboard header."""
        lines = []
        lines.append("")
        title = f"{self.ICONS['sparkle']}  TermNexus - AI Terminal Workspace Intelligence Engine"
        lines.append(self._center(self._bold(title)))
        lines.append(self._center("🧠 Intelligent Workspace Management for AI Agents | v1.0.0"))
        lines.append(self._draw_line())
        return "\n".join(lines)
    
    def render_workspace_list(self, workspaces: List[Any], 
                              highlight_id: str = "") -> str:
        """Render workspace list."""
        lines = []
        lines.append(f"\n{self._bold('📁 Workspaces')}")
        lines.append(self._draw_line("─", Colors.BLUE))
        
        if not workspaces:
            lines.append(f"  {self.ICONS['info']} No workspaces found. Create one with: termnexus create <name>")
            return "\n".join(lines)
        
        # Header
        header = (f"  {'ID':<8} {'Name':<20} {'Type':<10} {'Path':<30} "
                  f"{'Sessions':<8} {'Status'}")
        lines.append(self._color(header, Colors.BOLD))
        lines.append(self._draw_line("─", Colors.DIM))
        
        for ws in workspaces:
            ws_id = ws.id[:8]
            name = self._truncate(ws.name, 18)
            ws_type = ws.workspace_type
            path = self._truncate(ws.path, 28)
            sessions = ws.get_active_sessions_count()
            
            # Type icon
            type_icon = self.ICONS.get(ws_type, "📁")
            
            # Highlight current workspace
            prefix = f"{self.ICONS['arrow']} " if ws.id == highlight_id else "  "
            color = Colors.GREEN if ws.id == highlight_id else Colors.RESET
            
            line = (f"{prefix}{ws_id:<8} {name:<20} {type_icon} {ws_type:<8} "
                    f"{path:<30} {sessions:<8} {self.ICONS['running']}")
            lines.append(self._color(line, color))
            
            # Show tags if any
            if ws.tags:
                tag_str = " ".join([f"[{t}]" for t in ws.tags[:5]])
                lines.append(f"           {self._color(tag_str, Colors.DIM)}")
        
        return "\n".join(lines)
    
    def render_session_list(self, sessions: List[Any]) -> str:
        """Render session list."""
        lines = []
        lines.append(f"\n{self._bold('💻 Sessions')}")
        lines.append(self._draw_line("─", Colors.CYAN))
        
        if not sessions:
            lines.append(f"  {self.ICONS['info']} No active sessions")
            return "\n".join(lines)
        
        # Header
        header = (f"  {'ID':<8} {'Name':<18} {'Type':<10} {'PID':<8} "
                  f"{'Duration':<10} {'Status'}")
        lines.append(self._color(header, Colors.BOLD))
        lines.append(self._draw_line("─", Colors.DIM))
        
        for s in sessions:
            sid = s.session_id[:8] if hasattr(s, 'session_id') else s.get("id", "")[:8]
            name = self._truncate(s.name if hasattr(s, 'name') else s.get("name", ""), 16)
            stype = s.session_type if hasattr(s, 'session_type') else s.get("type", "shell")
            pid = str(s.pid if hasattr(s, 'pid') else s.get("pid", 0))
            duration = self._format_duration(
                s.duration if hasattr(s, 'duration') else 
                time.time() - s.get("started_at", time.time())
            )
            status = s.status if hasattr(s, 'status') else s.get("status", "running")
            
            # Type icon
            type_icon = self.ICONS.get(stype, "💻")
            status_icon = self.ICONS.get(status, "⚪")
            
            # Color by status
            status_color = Colors.GREEN if status == "running" else Colors.RED
            
            line = (f"  {sid:<8} {name:<18} {type_icon} {stype:<8} "
                    f"{pid:<8} {duration:<10} {status_icon}")
            lines.append(self._color(line, status_color))
        
        return "\n".join(lines)
    
    def render_agent_summary(self, agents: List[Dict[str, Any]]) -> str:
        """Render AI Agent summary."""
        lines = []
        lines.append(f"\n{self._bold('🤖 AI Agents')}")
        lines.append(self._draw_line("─", Colors.MAGENTA))
        
        if not agents:
            lines.append(f"  {self.ICONS['info']} No AI Agents detected")
            return "\n".join(lines)
        
        for agent in agents:
            agent_type = agent.get("type", "unknown")
            count = agent.get("count", 0)
            icon = self.ICONS.get(agent_type, "🤖")
            
            line = f"  {icon} {self._bold(agent_type.upper())}: {count} process(es)"
            lines.append(line)
            
            # Show processes
            for proc in agent.get("processes", [])[:3]:
                cmd = self._truncate(proc.get("command", ""), 50)
                pid = proc.get("pid", 0)
                lines.append(f"     └─ PID {pid}: {self._color(cmd, Colors.DIM)}")
        
        return "\n".join(lines)
    
    def render_stats(self, stats: Dict[str, Any]) -> str:
        """Render statistics panel."""
        lines = []
        lines.append(f"\n{self._bold('📊 Statistics')}")
        lines.append(self._draw_line("─", Colors.YELLOW))
        
        content = []
        content.append(f"  {self.ICONS['workspace']} Total Workspaces: {stats.get('total_workspaces', 0)}")
        content.append(f"  {self.ICONS['shell']} Total Sessions: {stats.get('total_sessions', 0)}")
        content.append(f"  {self.ICONS['running']} Active Sessions: {stats.get('active_sessions', 0)}")
        content.append(f"  {self.ICONS['agent']} AI Agent Sessions: {stats.get('agent_sessions', 0)}")
        
        if "type_distribution" in stats:
            content.append("")
            content.append("  Workspace Types:")
            for ws_type, count in stats["type_distribution"].items():
                icon = self.ICONS.get(ws_type, "📁")
                content.append(f"    {icon} {ws_type}: {count}")
        
        if "top_tags" in stats:
            content.append("")
            content.append("  Top Tags:")
            for tag, count in list(stats["top_tags"].items())[:5]:
                content.append(f"    🏷️  {tag}: {count}")
        
        lines.extend(content)
        return "\n".join(lines)
    
    def render_recommendations(self, recommendations: List[Dict[str, Any]]) -> str:
        """Render workspace recommendations."""
        lines = []
        lines.append(f"\n{self._bold('💡 Recommendations')}")
        lines.append(self._draw_line("─", Colors.GREEN))
        
        if not recommendations:
            lines.append(f"  {self.ICONS['info']} No recommendations available")
            return "\n".join(lines)
        
        for i, rec in enumerate(recommendations[:5], 1):
            session = rec.get("session", {})
            score = rec.get("score", 0)
            reasons = rec.get("reasons", [])
            
            name = session.get("name", "Unknown")
            ws_type = session.get("type", "shell")
            icon = self.ICONS.get(ws_type, "💻")
            
            line = f"  {i}. {icon} {self._bold(name)} (score: {score})"
            lines.append(line)
            
            if reasons:
                reason_str = ", ".join(reasons)
                lines.append(f"     └─ {self._color(reason_str, Colors.DIM)}")
        
        return "\n".join(lines)
    
    def render_help(self) -> str:
        """Render help information."""
        lines = []
        lines.append("")
        lines.append(self._center(self._bold("📖 Quick Reference"), fill="═"))
        lines.append("")
        
        commands = [
            ("create <name>", "Create a new workspace"),
            ("list", "List all workspaces"),
            ("switch <name|id>", "Switch to a workspace"),
            ("delete <name|id>", "Delete a workspace"),
            ("rename <old> <new>", "Rename a workspace"),
            ("sessions", "List all sessions"),
            ("agents", "Show AI Agent summary"),
            ("stats", "Show workspace statistics"),
            ("recommend", "Get workspace recommendations"),
            ("dashboard", "Show full dashboard"),
            ("context", "Show current context"),
            ("help", "Show this help message"),
        ]
        
        for cmd, desc in commands:
            lines.append(f"  {self._color(f'tnx {cmd}', Colors.CYAN):<25} {desc}")
        
        lines.append("")
        lines.append(self._center("", fill="═"))
        return "\n".join(lines)
    
    def render_dashboard(self, highlight_workspace: str = "") -> str:
        """Render full dashboard."""
        lines = []
        lines.append(self.render_header())
        
        # Workspace list
        if self.workspace_manager:
            workspaces = self.workspace_manager.list_workspaces()
            lines.append(self.render_workspace_list(workspaces, highlight_workspace))
        
        # Session list
        if self.session_manager:
            sessions = self.session_manager.list_sessions(status="running")
            lines.append(self.render_session_list(sessions))
        
        # Agent summary
        if self.session_manager:
            agents = self.session_manager.get_agent_summary()
            lines.append(self.render_agent_summary(agents))
        
        # Stats
        if self.workspace_manager:
            stats = self.workspace_manager.get_workspace_stats()
            lines.append(self.render_stats(stats))
        
        lines.append("")
        lines.append(self._center(
            f"{self.ICONS['info']} Press 'q' to quit | 'h' for help | 'r' to refresh",
            fill="─"
        ))
        lines.append("")
        
        return "\n".join(lines)
    
    def render_context(self, context: Any) -> str:
        """Render current context information."""
        lines = []
        lines.append(f"\n{self._bold('🎯 Current Context')}")
        lines.append(self._draw_line("─", Colors.CYAN))
        
        if hasattr(context, 'to_dict'):
            ctx = context.to_dict()
        else:
            ctx = context
        
        lines.append(f"  {self.ICONS['workspace']} Directory: {ctx.get('cwd', os.getcwd())}")
        
        if ctx.get('git_branch'):
            lines.append(f"  {self.ICONS['git']} Git Branch: {ctx.get('git_branch')}")
        
        if ctx.get('active_agents'):
            agents = ", ".join(ctx['active_agents'])
            lines.append(f"  {self.ICONS['agent']} Active Agents: {agents}")
        
        if ctx.get('recent_commands'):
            lines.append(f"\n  {self._bold('Recent Commands:')}")
            for cmd in ctx['recent_commands'][:5]:
                lines.append(f"    {self.ICONS['arrow']} {cmd[:60]}")
        
        if ctx.get('file_context'):
            lines.append(f"\n  {self._bold('Recent Files:')}")
            for f in ctx['file_context'][:5]:
                lines.append(f"    📄 {f}")
        
        return "\n".join(lines)
    
    def clear_screen(self):
        """Clear terminal screen."""
        if os.name == "nt":
            os.system("cls")
        else:
            os.system("clear")
    
    def refresh(self):
        """Refresh dashboard display."""
        self.term_width = self._get_terminal_width()
        self.clear_screen()
        print(self.render_dashboard())
