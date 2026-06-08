#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CLI Entry Point - 命令行入口模块

Main command-line interface for TermNexus with all subcommands.
"""

import os
import sys
import argparse
import textwrap
from typing import Optional

from .workspace import WorkspaceManager
from .session import SessionManager
from .router import AgentRouter
from .tui import Dashboard, Colors


def print_error(msg: str):
    """Print error message."""
    print(f"{Colors.RED}✗ {msg}{Colors.RESET}", file=sys.stderr)


def print_success(msg: str):
    """Print success message."""
    print(f"{Colors.GREEN}✓ {msg}{Colors.RESET}")


def print_info(msg: str):
    """Print info message."""
    print(f"{Colors.CYAN}ℹ {msg}{Colors.RESET}")


def print_warning(msg: str):
    """Print warning message."""
    print(f"{Colors.YELLOW}⚠ {msg}{Colors.RESET}")


def create_parser() -> argparse.ArgumentParser:
    """Create argument parser."""
    parser = argparse.ArgumentParser(
        prog="termnexus",
        description="🧠 TermNexus - AI Terminal Workspace Intelligence Engine",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent("""
            Examples:
              termnexus create my-project           # Create workspace
              termnexus list                        # List workspaces
              termnexus switch my-project           # Switch workspace
              termnexus dashboard                   # Show dashboard
              termnexus agents                      # Show AI agents
              
            Aliases: tnx (same as termnexus)
        """),
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Create workspace
    create_parser = subparsers.add_parser(
        "create", aliases=["c", "new"],
        help="Create a new workspace"
    )
    create_parser.add_argument("name", help="Workspace name")
    create_parser.add_argument("--path", "-p", default="", help="Workspace path")
    create_parser.add_argument("--type", "-t", default="auto", 
                               choices=["auto", "general", "project", "agent", "python", "node", "docker"],
                               help="Workspace type")
    create_parser.add_argument("--tag", action="append", default=[], help="Add tags")
    
    # List workspaces
    list_parser = subparsers.add_parser(
        "list", aliases=["ls", "l"],
        help="List all workspaces"
    )
    list_parser.add_argument("--type", help="Filter by type")
    list_parser.add_argument("--tag", help="Filter by tag")
    
    # Switch workspace
    switch_parser = subparsers.add_parser(
        "switch", aliases=["sw", "s"],
        help="Switch to a workspace"
    )
    switch_parser.add_argument("name", help="Workspace name or ID")
    
    # Delete workspace
    delete_parser = subparsers.add_parser(
        "delete", aliases=["del", "rm"],
        help="Delete a workspace"
    )
    delete_parser.add_argument("name", help="Workspace name or ID")
    delete_parser.add_argument("--force", "-f", action="store_true", help="Force delete")
    
    # Rename workspace
    rename_parser = subparsers.add_parser(
        "rename", aliases=["mv"],
        help="Rename a workspace"
    )
    rename_parser.add_argument("old_name", help="Current name")
    rename_parser.add_argument("new_name", help="New name")
    
    # Show workspace info
    info_parser = subparsers.add_parser(
        "info", aliases=["show", "i"],
        help="Show workspace details"
    )
    info_parser.add_argument("name", nargs="?", help="Workspace name or ID")
    
    # Sessions
    sessions_parser = subparsers.add_parser(
        "sessions", aliases=["sess"],
        help="List sessions"
    )
    sessions_parser.add_argument("--type", help="Filter by type")
    sessions_parser.add_argument("--agent", action="store_true", help="Show only agent sessions")
    
    # Agents
    subparsers.add_parser(
        "agents", aliases=["agent", "ai"],
        help="Show AI Agent summary"
    )
    
    # Stats
    subparsers.add_parser(
        "stats", aliases=["stat", "st"],
        help="Show workspace statistics"
    )
    
    # Dashboard
    subparsers.add_parser(
        "dashboard", aliases=["dash", "d"],
        help="Show full dashboard"
    )
    
    # Context
    subparsers.add_parser(
        "context", aliases=["ctx"],
        help="Show current context"
    )
    
    # Recommendations
    subparsers.add_parser(
        "recommend", aliases=["rec", "r"],
        help="Get workspace recommendations"
    )
    
    # Route
    route_parser = subparsers.add_parser(
        "route", aliases=["ro"],
        help="Routing commands"
    )
    route_sub = route_parser.add_subparsers(dest="route_command")
    
    route_rules = route_sub.add_parser("rules", help="List routing rules")
    route_add = route_sub.add_parser("add", help="Add routing rule")
    route_add.add_argument("name", help="Rule name")
    route_add.add_argument("pattern", help="Match pattern")
    route_add.add_argument("target", help="Target workspace")
    route_add.add_argument("--priority", type=int, default=0, help="Priority")
    
    route_del = route_sub.add_parser("remove", help="Remove routing rule")
    route_del.add_argument("name", help="Rule name")
    
    route_sub.add_parser("history", help="Show routing history")
    route_sub.add_parser("patterns", help="Show switch patterns")
    
    # Help
    subparsers.add_parser(
        "help", aliases=["h"],
        help="Show help"
    )
    
    # Version
    parser.add_argument("--version", "-v", action="version", version="%(prog)s 1.0.0")
    
    return parser


def cmd_create(args, wm: WorkspaceManager, dashboard: Dashboard):
    """Handle create command."""
    ws_type = args.type if args.type != "auto" else "general"
    auto_detect = args.type == "auto"
    
    ws = wm.create_workspace(args.name, args.path, ws_type, auto_detect)
    
    # Add custom tags
    for tag in args.tag:
        ws.add_tag(tag)
    
    wm.save_workspaces()
    
    print_success(f"Created workspace '{args.name}' ({ws.id})")
    print_info(f"  Path: {ws.path}")
    print_info(f"  Type: {ws.workspace_type}")
    if ws.tags:
        print_info(f"  Tags: {', '.join(ws.tags)}")
    
    # Show detected metadata
    if ws.metadata:
        if "framework" in ws.metadata:
            print_info(f"  Framework: {ws.metadata['framework']}")
        if "git_branch" in ws.metadata:
            print_info(f"  Git Branch: {ws.metadata['git_branch']}")


def cmd_list(args, wm: WorkspaceManager, dashboard: Dashboard):
    """Handle list command."""
    workspaces = wm.list_workspaces(args.type, args.tag)
    
    if not workspaces:
        print_info("No workspaces found")
        return
    
    print(dashboard.render_workspace_list(workspaces))
    print(f"\n  Total: {len(workspaces)} workspace(s)")


def cmd_switch(args, wm: WorkspaceManager, dashboard: Dashboard):
    """Handle switch command."""
    # Try exact match first
    ws = wm.find_workspace_by_name(args.name)
    
    # Try by ID prefix
    if not ws:
        for wid, w in wm.workspaces.items():
            if wid.startswith(args.name):
                ws = w
                break
    
    if not ws:
        print_error(f"Workspace '{args.name}' not found")
        print_info("Run 'termnexus list' to see available workspaces")
        return
    
    if wm.switch_to_workspace(ws.id):
        print_success(f"Switched to workspace '{ws.name}'")
        print_info(f"  Path: {ws.path}")
        
        # Show active sessions
        if ws.sessions:
            print_info(f"  Active sessions: {ws.get_active_sessions_count()}")
        
        # Show detected agents
        agents = wm.detect_agent_sessions(ws.id)
        if agents:
            print_info(f"  Detected AI Agents:")
            for agent in agents[:3]:
                print_info(f"    🤖 {agent['agent']} (PID {agent['pid']})")
    else:
        print_error(f"Failed to switch to workspace '{ws.name}'")


def cmd_delete(args, wm: WorkspaceManager, dashboard: Dashboard):
    """Handle delete command."""
    ws = wm.find_workspace_by_name(args.name)
    
    if not ws:
        # Try by ID prefix
        for wid, w in wm.workspaces.items():
            if wid.startswith(args.name):
                ws = w
                break
    
    if not ws:
        print_error(f"Workspace '{args.name}' not found")
        return
    
    if not args.force:
        response = input(f"Delete workspace '{ws.name}'? [y/N]: ")
        if response.lower() != "y":
            print_info("Cancelled")
            return
    
    if wm.delete_workspace(ws.id):
        print_success(f"Deleted workspace '{ws.name}'")
    else:
        print_error("Failed to delete workspace")


def cmd_rename(args, wm: WorkspaceManager, dashboard: Dashboard):
    """Handle rename command."""
    ws = wm.find_workspace_by_name(args.old_name)
    
    if not ws:
        print_error(f"Workspace '{args.old_name}' not found")
        return
    
    if wm.rename_workspace(ws.id, args.new_name):
        print_success(f"Renamed workspace to '{args.new_name}'")
    else:
        print_error("Failed to rename workspace")


def cmd_info(args, wm: WorkspaceManager, dashboard: Dashboard):
    """Handle info command."""
    if args.name:
        ws = wm.find_workspace_by_name(args.name)
        if not ws:
            for wid, w in wm.workspaces.items():
                if wid.startswith(args.name):
                    ws = w
                    break
    else:
        # Show current workspace info
        ws_id = os.environ.get("TERM_NEXUS_WORKSPACE_ID", "")
        ws = wm.get_workspace(ws_id) if ws_id else None
    
    if not ws:
        print_info("No workspace selected")
        return
    
    print(f"\n{Colors.BOLD}📁 Workspace: {ws.name}{Colors.RESET}")
    print(f"  ID: {ws.id}")
    print(f"  Path: {ws.path}")
    print(f"  Type: {ws.workspace_type}")
    print(f"  Tags: {', '.join(ws.tags) if ws.tags else 'None'}")
    print(f"  Sessions: {len(ws.sessions)} ({ws.get_active_sessions_count()} active)")
    
    if ws.metadata:
        print(f"\n{Colors.BOLD}Metadata:{Colors.RESET}")
        for key, value in ws.metadata.items():
            if isinstance(value, dict):
                print(f"  {key}:")
                for k, v in value.items():
                    print(f"    {k}: {v}")
            else:
                print(f"  {key}: {value}")
    
    if ws.sessions:
        print(f"\n{Colors.BOLD}Sessions:{Colors.RESET}")
        for s in ws.sessions:
            status_icon = "🟢" if s["status"] == "running" else "🔴"
            print(f"  {status_icon} {s['type']} ({s['id']}) - {s.get('agent_name', 'N/A')}")


def cmd_sessions(args, sm: SessionManager, dashboard: Dashboard):
    """Handle sessions command."""
    sessions = sm.list_sessions(
        session_type=args.type,
        agent_only=args.agent
    )
    print(dashboard.render_session_list(sessions))


def cmd_agents(args, sm: SessionManager, dashboard: Dashboard):
    """Handle agents command."""
    agents = sm.get_agent_summary()
    print(dashboard.render_agent_summary(agents))
    
    if not agents:
        print_info("No AI Agents currently running")
        print_info("Start an agent (e.g., claude, codex, aider) to see it here")


def cmd_stats(args, wm: WorkspaceManager, dashboard: Dashboard):
    """Handle stats command."""
    stats = wm.get_workspace_stats()
    print(dashboard.render_stats(stats))


def cmd_dashboard(args, wm: WorkspaceManager, sm: SessionManager, dashboard: Dashboard):
    """Handle dashboard command."""
    current_ws = os.environ.get("TERM_NEXUS_WORKSPACE_ID", "")
    print(dashboard.render_dashboard(current_ws))


def cmd_context(args, router: AgentRouter, dashboard: Dashboard):
    """Handle context command."""
    context = router.capture_context()
    print(dashboard.render_context(context))
    
    # Show recommendation
    rec = router.get_recommendation(context)
    if rec:
        print(f"\n{Colors.BOLD}💡 Recommendation:{Colors.RESET}")
        print(f"  Workspace: {rec['workspace']}")
        print(f"  Confidence: {rec['confidence']}")
        print(f"  Reason: {rec['reason']}")


def cmd_recommend(args, wm: WorkspaceManager, sm: SessionManager, 
                   router: AgentRouter, dashboard: Dashboard):
    """Handle recommend command."""
    context = router.capture_context()
    
    # Get session-based recommendations
    if sm:
        recs = sm.get_recommended_sessions(context.cwd)
        if recs:
            print(dashboard.render_recommendations(recs))
    
    # Get routing recommendation
    rec = router.get_recommendation(context)
    if rec:
        print(f"\n{Colors.BOLD}🎯 Smart Routing:{Colors.RESET}")
        print(f"  Suggested: {rec['workspace']}")
        print(f"  Confidence: {rec['confidence']}")
        print(f"  Based on: {rec['reason']}")
        
        if rec.get('alternatives'):
            print(f"\n  Alternatives:")
            for alt in rec['alternatives']:
                print(f"    • {alt['workspace']} (score: {alt['score']})")


def cmd_route(args, router: AgentRouter):
    """Handle route subcommands."""
    if args.route_command == "rules":
        print(f"\n{Colors.BOLD}📋 Routing Rules:{Colors.RESET}")
        for rule in router.rules:
            status = "✓" if rule.enabled else "✗"
            auto = "auto" if rule.auto_switch else "manual"
            print(f"  [{status}] {rule.name}")
            print(f"      Pattern: {rule.pattern}")
            print(f"      Target: {rule.target_workspace}")
            print(f"      Priority: {rule.priority} | Switch: {auto}")
    
    elif args.route_command == "add":
        from .router import RouteRule
        rule = RouteRule(
            name=args.name,
            pattern=args.pattern,
            target_workspace=args.target,
            priority=args.priority,
        )
        if router.add_rule(rule):
            print_success(f"Added routing rule '{args.name}'")
        else:
            print_error(f"Rule '{args.name}' already exists")
    
    elif args.route_command == "remove":
        if router.remove_rule(args.name):
            print_success(f"Removed routing rule '{args.name}'")
        else:
            print_error(f"Rule '{args.name}' not found")
    
    elif args.route_command == "history":
        patterns = router.get_switch_patterns()
        print(f"\n{Colors.BOLD}📊 Switch Patterns:{Colors.RESET}")
        for key, value in patterns.items():
            if isinstance(value, dict):
                print(f"\n  {key}:")
                for k, v in value.items():
                    print(f"    {k}: {v}")
            else:
                print(f"  {key}: {value}")
    
    elif args.route_command == "patterns":
        patterns = router.get_switch_patterns()
        print(f"\n{Colors.BOLD}🔄 Switch Analysis:{Colors.RESET}")
        if "top_switches" in patterns:
            print("\n  Most Common Switches:")
            for switch, count in patterns["top_switches"].items():
                print(f"    {switch}: {count} times")


def cmd_help(args, dashboard: Dashboard):
    """Handle help command."""
    print(dashboard.render_help())


def main():
    """Main entry point."""
    parser = create_parser()
    args = parser.parse_args()
    
    # Initialize managers
    wm = WorkspaceManager()
    sm = SessionManager()
    router = AgentRouter()
    dashboard = Dashboard(wm, sm)
    
    # Handle no command
    if not args.command:
        print(dashboard.render_dashboard())
        print(dashboard.render_help())
        return
    
    # Route commands
    try:
        if args.command in ("create", "c", "new"):
            cmd_create(args, wm, dashboard)
        
        elif args.command in ("list", "ls", "l"):
            cmd_list(args, wm, dashboard)
        
        elif args.command in ("switch", "sw", "s"):
            cmd_switch(args, wm, dashboard)
        
        elif args.command in ("delete", "del", "rm"):
            cmd_delete(args, wm, dashboard)
        
        elif args.command in ("rename", "mv"):
            cmd_rename(args, wm, dashboard)
        
        elif args.command in ("info", "show", "i"):
            cmd_info(args, wm, dashboard)
        
        elif args.command in ("sessions", "sess"):
            cmd_sessions(args, sm, dashboard)
        
        elif args.command in ("agents", "agent", "ai"):
            cmd_agents(args, sm, dashboard)
        
        elif args.command in ("stats", "stat", "st"):
            cmd_stats(args, wm, dashboard)
        
        elif args.command in ("dashboard", "dash", "d"):
            cmd_dashboard(args, wm, sm, dashboard)
        
        elif args.command in ("context", "ctx"):
            cmd_context(args, router, dashboard)
        
        elif args.command in ("recommend", "rec", "r"):
            cmd_recommend(args, wm, sm, router, dashboard)
        
        elif args.command == "route":
            cmd_route(args, router)
        
        elif args.command in ("help", "h"):
            cmd_help(args, dashboard)
        
        else:
            print_error(f"Unknown command: {args.command}")
            print_info("Run 'termnexus help' for usage information")
    
    except KeyboardInterrupt:
        print("\n")
        print_info("Interrupted by user")
        sys.exit(0)
    except Exception as e:
        print_error(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
