#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Session Management Module - 会话管理模块

Manages terminal sessions with AI Agent detection, process tracking,
and intelligent session lifecycle management.
"""

import os
import re
import time
import json
import signal
import subprocess
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict


@dataclass
class SessionInfo:
    """Information about a terminal session."""
    session_id: str
    name: str
    session_type: str  # shell, agent, server, task
    pid: int
    command: str
    cwd: str
    env: Dict[str, str]
    status: str  # running, suspended, stopped
    created_at: float
    last_active: float
    metadata: Dict[str, Any]
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
    
    @property
    def is_agent(self) -> bool:
        """Check if this is an AI Agent session."""
        return self.session_type in ("agent", "ai", "copilot", "claude", "codex")
    
    @property
    def duration(self) -> float:
        """Get session duration in seconds."""
        return time.time() - self.created_at
    
    @property
    def idle_time(self) -> float:
        """Get idle time in seconds."""
        return time.time() - self.last_active


class SessionManager:
    """Manages terminal sessions with process tracking."""
    
    AGENT_SIGNATURES = {
        "claude": {
            "commands": ["claude", "claude-code", "anthropic"],
            "env_vars": ["ANTHROPIC_API_KEY", "CLAUDE_CODE"],
            "files": [".claude", "CLAUDE.md"],
        },
        "codex": {
            "commands": ["codex", "openai-codex"],
            "env_vars": ["OPENAI_API_KEY", "CODEX_API_KEY"],
            "files": [".codex"],
        },
        "cursor": {
            "commands": ["cursor", "cursor-agent"],
            "env_vars": ["CURSOR_API_KEY"],
            "files": [".cursorrules", ".cursor"],
        },
        "gemini": {
            "commands": ["gemini", "gemini-cli", "google-gemini"],
            "env_vars": ["GEMINI_API_KEY", "GOOGLE_API_KEY"],
            "files": [".gemini"],
        },
        "aider": {
            "commands": ["aider"],
            "env_vars": ["OPENAI_API_KEY", "ANTHROPIC_API_KEY"],
            "files": [".aider", ".aider.conf.yml"],
        },
        "continue": {
            "commands": ["continue"],
            "env_vars": [],
            "files": [".continue"],
        },
        "copilot": {
            "commands": ["github-copilot", "copilot-cli", "gh copilot"],
            "env_vars": ["GITHUB_TOKEN", "GITHUB_COPILOT_TOKEN"],
            "files": [],
        },
        "ollama": {
            "commands": ["ollama"],
            "env_vars": ["OLLAMA_HOST"],
            "files": [],
        },
    }
    
    def __init__(self, config_dir: Optional[str] = None):
        self.config_dir = Path(config_dir or self._get_default_config_dir())
        self.config_dir.mkdir(parents=True, exist_ok=True)
        self.sessions_file = self.config_dir / "sessions.json"
        self.sessions: Dict[str, SessionInfo] = {}
        self._load_sessions()
    
    def _get_default_config_dir(self) -> str:
        """Get default configuration directory."""
        if os.name == "nt":
            return os.path.join(os.environ.get("APPDATA", ""), "TermNexus")
        else:
            return os.path.join(os.path.expanduser("~"), ".config", "termnexus")
    
    def _load_sessions(self):
        """Load sessions from disk."""
        if self.sessions_file.exists():
            try:
                with open(self.sessions_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                for s_data in data.get("sessions", []):
                    session = SessionInfo(**s_data)
                    self.sessions[session.session_id] = session
            except (json.JSONDecodeError, KeyError, TypeError):
                self.sessions = {}
    
    def save_sessions(self):
        """Save sessions to disk."""
        data = {
            "version": "1.0.0",
            "updated_at": time.time(),
            "sessions": [s.to_dict() for s in self.sessions.values()],
        }
        with open(self.sessions_file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def create_session(self, name: str, command: str, 
                       session_type: str = "shell",
                       cwd: str = "",
                       env: Optional[Dict[str, str]] = None) -> SessionInfo:
        """Create and start a new session."""
        import hashlib
        
        session_id = hashlib.md5(f"{name}:{time.time()}".encode()).hexdigest()[:10]
        
        if not cwd:
            cwd = os.getcwd()
        
        # Detect if this is an agent session
        if session_type == "shell":
            detected_agent = self._detect_agent_from_command(command, cwd)
            if detected_agent:
                session_type = "agent"
        
        session = SessionInfo(
            session_id=session_id,
            name=name,
            session_type=session_type,
            pid=0,  # Will be set if we start the process
            command=command,
            cwd=cwd,
            env=env or {},
            status="running",
            created_at=time.time(),
            last_active=time.time(),
            metadata={"agent_detected": session_type == "agent"},
        )
        
        self.sessions[session_id] = session
        self.save_sessions()
        return session
    
    def _detect_agent_from_command(self, command: str, cwd: str) -> Optional[str]:
        """Detect AI Agent from command string and working directory."""
        cmd_lower = command.lower()
        
        # Check command patterns
        for agent, sig in self.AGENT_SIGNATURES.items():
            for pattern in sig["commands"]:
                if pattern in cmd_lower:
                    return agent
        
        # Check environment variables
        for agent, sig in self.AGENT_SIGNATURES.items():
            for env_var in sig["env_vars"]:
                if os.environ.get(env_var):
                    return agent
        
        # Check workspace files
        if cwd and os.path.isdir(cwd):
            for agent, sig in self.AGENT_SIGNATURES.items():
                for file_pattern in sig["files"]:
                    if os.path.exists(os.path.join(cwd, file_pattern)):
                        return agent
        
        return None
    
    def detect_all_agents(self) -> List[Dict[str, Any]]:
        """Scan system for all running AI Agent processes."""
        agents = []
        
        try:
            if os.name == "posix":
                result = subprocess.run(
                    ["ps", "-eo", "pid,ppid,cmd"],
                    capture_output=True, text=True, timeout=10
                )
                for line in result.stdout.split("\n")[1:]:
                    parts = line.strip().split(None, 2)
                    if len(parts) >= 3:
                        try:
                            pid = int(parts[0])
                        except ValueError:
                            continue
                        
                        cmd = parts[2]
                        agent = self._detect_agent_from_command(cmd, "")
                        
                        if agent:
                            # Try to get cwd
                            cwd = ""
                            try:
                                cwd = os.readlink(f"/proc/{pid}/cwd")
                            except (OSError, PermissionError):
                                pass
                            
                            agents.append({
                                "pid": pid,
                                "agent": agent,
                                "command": cmd[:100],
                                "cwd": cwd,
                            })
        except Exception:
            pass
        
        return agents
    
    def get_session(self, session_id: str) -> Optional[SessionInfo]:
        """Get session by ID."""
        return self.sessions.get(session_id)
    
    def list_sessions(self, session_type: Optional[str] = None,
                      status: Optional[str] = None,
                      agent_only: bool = False) -> List[SessionInfo]:
        """List sessions with filtering."""
        result = list(self.sessions.values())
        
        if session_type:
            result = [s for s in result if s.session_type == session_type]
        
        if status:
            result = [s for s in result if s.status == status]
        
        if agent_only:
            result = [s for s in result if s.is_agent]
        
        # Sort by last_active descending
        result.sort(key=lambda s: s.last_active, reverse=True)
        return result
    
    def update_session(self, session_id: str, **kwargs) -> bool:
        """Update session attributes."""
        session = self.sessions.get(session_id)
        if not session:
            return False
        
        for key, value in kwargs.items():
            if hasattr(session, key):
                setattr(session, key, value)
        
        session.last_active = time.time()
        self.save_sessions()
        return True
    
    def kill_session(self, session_id: str, force: bool = False) -> bool:
        """Kill a session by sending signal to its process."""
        session = self.sessions.get(session_id)
        if not session or session.pid == 0:
            return False
        
        try:
            sig = signal.SIGKILL if force else signal.SIGTERM
            os.kill(session.pid, sig)
            session.status = "stopped"
            self.save_sessions()
            return True
        except (OSError, ProcessLookupError):
            session.status = "stopped"
            self.save_sessions()
            return False
    
    def remove_session(self, session_id: str) -> bool:
        """Remove a session from tracking."""
        if session_id in self.sessions:
            del self.sessions[session_id]
            self.save_sessions()
            return True
        return False
    
    def get_session_stats(self) -> Dict[str, Any]:
        """Get session statistics."""
        total = len(self.sessions)
        type_counts = {}
        status_counts = {}
        agent_count = 0
        total_duration = 0.0
        
        for s in self.sessions.values():
            type_counts[s.session_type] = type_counts.get(s.session_type, 0) + 1
            status_counts[s.status] = status_counts.get(s.status, 0) + 1
            if s.is_agent:
                agent_count += 1
            total_duration += s.duration
        
        return {
            "total_sessions": total,
            "type_distribution": type_counts,
            "status_distribution": status_counts,
            "agent_sessions": agent_count,
            "total_duration_hours": round(total_duration / 3600, 2),
            "avg_session_duration_min": round(total_duration / max(total, 1) / 60, 2),
        }
    
    def get_agent_summary(self) -> List[Dict[str, Any]]:
        """Get summary of all detected AI Agents."""
        agents = self.detect_all_agents()
        
        # Group by agent type
        summary = {}
        for agent in agents:
            agent_type = agent["agent"]
            if agent_type not in summary:
                summary[agent_type] = {
                    "type": agent_type,
                    "count": 0,
                    "processes": [],
                }
            summary[agent_type]["count"] += 1
            summary[agent_type]["processes"].append(agent)
        
        return list(summary.values())
    
    def attach_to_session(self, session_id: str) -> Tuple[bool, str]:
        """Attach to an existing session (if supported by platform)."""
        session = self.sessions.get(session_id)
        if not session:
            return False, "Session not found"
        
        # For shell sessions, we can try to resume
        if session.session_type == "shell" and session.pid > 0:
            try:
                # Check if process is still running
                os.kill(session.pid, 0)
                session.last_active = time.time()
                self.save_sessions()
                return True, f"Attached to session {session.name}"
            except OSError:
                session.status = "stopped"
                self.save_sessions()
                return False, "Session process no longer running"
        
        return False, "Session type does not support attach"
    
    def get_recommended_sessions(self, cwd: str = "") -> List[Dict[str, Any]]:
        """Get recommended sessions based on current context."""
        if not cwd:
            cwd = os.getcwd()
        
        recommendations = []
        
        # Find sessions in same directory
        for session in self.sessions.values():
            score = 0
            reasons = []
            
            if session.cwd == cwd:
                score += 50
                reasons.append("Same directory")
            elif cwd.startswith(session.cwd + "/"):
                score += 30
                reasons.append("Parent directory")
            
            if session.is_agent:
                score += 20
                reasons.append("AI Agent")
            
            if session.status == "running":
                score += 10
                reasons.append("Active")
            
            if score > 0:
                recommendations.append({
                    "session": session.to_dict(),
                    "score": score,
                    "reasons": reasons,
                })
        
        # Sort by score
        recommendations.sort(key=lambda x: x["score"], reverse=True)
        return recommendations[:10]
