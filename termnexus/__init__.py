#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🧠 TermNexus - AI Terminal Workspace Intelligence Engine
AI终端工作区智能引擎

A zero-dependency Python CLI tool for intelligent terminal workspace management
with AI Agent session awareness, smart routing, and TUI dashboard.

Version: 1.0.0
License: MIT
"""

__version__ = "1.0.0"
__author__ = "TermNexus Team"
__license__ = "MIT"

from .workspace import WorkspaceManager
from .session import SessionManager
from .router import AgentRouter
from .tui import Dashboard

__all__ = [
    "WorkspaceManager",
    "SessionManager", 
    "AgentRouter",
    "Dashboard",
]
