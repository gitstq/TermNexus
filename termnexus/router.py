#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI Agent Router Module - AI Agent智能路由模块

Intelligently routes between AI Agent sessions, manages context switching,
and provides smart recommendations for workspace transitions.
"""

import os
import re
import time
import json
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field


@dataclass
class RouteRule:
    """A routing rule for AI Agent sessions."""
    name: str
    pattern: str  # Regex pattern or keyword
    target_workspace: str
    priority: int = 0
    auto_switch: bool = False
    description: str = ""
    enabled: bool = True


@dataclass
class ContextSnapshot:
    """Snapshot of terminal context for intelligent routing."""
    timestamp: float
    cwd: str
    git_branch: str = ""
    env_vars: Dict[str, str] = field(default_factory=dict)
    recent_commands: List[str] = field(default_factory=list)
    active_agents: List[str] = field(default_factory=list)
    file_context: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "timestamp": self.timestamp,
            "cwd": self.cwd,
            "git_branch": self.git_branch,
            "env_vars": self.env_vars,
            "recent_commands": self.recent_commands,
            "active_agents": self.active_agents,
            "file_context": self.file_context,
        }


class AgentRouter:
    """Intelligent router for AI Agent sessions and workspace switching."""
    
    DEFAULT_RULES = [
        RouteRule("claude-project", r"claude|anthropic", "claude-workspace", 10),
        RouteRule("codex-project", r"codex|openai-codex", "codex-workspace", 10),
        RouteRule("cursor-project", r"cursor", "cursor-workspace", 10),
        RouteRule("gemini-project", r"gemini|google-gemini", "gemini-workspace", 10),
        RouteRule("aider-project", r"aider", "aider-workspace", 10),
        RouteRule("python-dev", r"python|\.py$", "python-workspace", 5),
        RouteRule("node-dev", r"node|npm|yarn|\.js$|\.ts$", "node-workspace", 5),
        RouteRule("rust-dev", r"rust|cargo|\.rs$", "rust-workspace", 5),
        RouteRule("go-dev", r"go|\.go$", "go-workspace", 5),
    ]
    
    def __init__(self, config_dir: Optional[str] = None):
        self.config_dir = Path(config_dir or self._get_default_config_dir())
        self.config_dir.mkdir(parents=True, exist_ok=True)
        self.rules_file = self.config_dir / "router_rules.json"
        self.history_file = self.config_dir / "route_history.json"
        self.rules: List[RouteRule] = []
        self.history: List[Dict[str, Any]] = []
        self._load_rules()
        self._load_history()
    
    def _get_default_config_dir(self) -> str:
        """Get default configuration directory."""
        if os.name == "nt":
            return os.path.join(os.environ.get("APPDATA", ""), "TermNexus")
        else:
            return os.path.join(os.path.expanduser("~"), ".config", "termnexus")
    
    def _load_rules(self):
        """Load routing rules from disk."""
        if self.rules_file.exists():
            try:
                with open(self.rules_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                self.rules = [
                    RouteRule(**rule_data) for rule_data in data.get("rules", [])
                ]
            except (json.JSONDecodeError, KeyError, TypeError):
                self.rules = list(self.DEFAULT_RULES)
        else:
            self.rules = list(self.DEFAULT_RULES)
            self._save_rules()
    
    def _save_rules(self):
        """Save routing rules to disk."""
        data = {
            "version": "1.0.0",
            "updated_at": time.time(),
            "rules": [
                {
                    "name": r.name,
                    "pattern": r.pattern,
                    "target_workspace": r.target_workspace,
                    "priority": r.priority,
                    "auto_switch": r.auto_switch,
                    "description": r.description,
                    "enabled": r.enabled,
                }
                for r in self.rules
            ],
        }
        with open(self.rules_file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def _load_history(self):
        """Load routing history."""
        if self.history_file.exists():
            try:
                with open(self.history_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                self.history = data.get("history", [])[-100:]  # Keep last 100
            except (json.JSONDecodeError, KeyError, TypeError):
                self.history = []
    
    def _save_history(self):
        """Save routing history."""
        data = {
            "version": "1.0.0",
            "updated_at": time.time(),
            "history": self.history[-100:],
        }
        with open(self.history_file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def add_rule(self, rule: RouteRule) -> bool:
        """Add a new routing rule."""
        # Check for duplicate names
        for existing in self.rules:
            if existing.name == rule.name:
                return False
        
        self.rules.append(rule)
        # Sort by priority descending
        self.rules.sort(key=lambda r: r.priority, reverse=True)
        self._save_rules()
        return True
    
    def remove_rule(self, name: str) -> bool:
        """Remove a routing rule by name."""
        for i, rule in enumerate(self.rules):
            if rule.name == name:
                self.rules.pop(i)
                self._save_rules()
                return True
        return False
    
    def match_context(self, context: ContextSnapshot) -> List[Tuple[RouteRule, int]]:
        """Match context against routing rules and return matches with scores."""
        matches = []
        
        for rule in self.rules:
            if not rule.enabled:
                continue
            
            score = 0
            
            # Check recent commands
            for cmd in context.recent_commands:
                if re.search(rule.pattern, cmd, re.IGNORECASE):
                    score += rule.priority * 2
            
            # Check active agents
            for agent in context.active_agents:
                if re.search(rule.pattern, agent, re.IGNORECASE):
                    score += rule.priority * 3
            
            # Check file context
            for file in context.file_context:
                if re.search(rule.pattern, file, re.IGNORECASE):
                    score += rule.priority
            
            # Check cwd
            if re.search(rule.pattern, context.cwd, re.IGNORECASE):
                score += rule.priority
            
            if score > 0:
                matches.append((rule, score))
        
        # Sort by score descending
        matches.sort(key=lambda x: x[1], reverse=True)
        return matches
    
    def get_recommendation(self, context: ContextSnapshot) -> Optional[Dict[str, Any]]:
        """Get workspace recommendation based on current context."""
        matches = self.match_context(context)
        
        if not matches:
            return None
        
        best_rule, score = matches[0]
        
        # Check history for similar contexts
        similar_switches = [
            h for h in self.history
            if h.get("target_workspace") == best_rule.target_workspace
        ]
        
        confidence = min(score / 50.0, 1.0)
        if similar_switches:
            confidence = min(confidence + 0.1, 1.0)
        
        return {
            "workspace": best_rule.target_workspace,
            "rule": best_rule.name,
            "score": score,
            "confidence": round(confidence, 2),
            "auto_switch": best_rule.auto_switch,
            "reason": f"Matched pattern '{best_rule.pattern}' in context",
            "alternatives": [
                {"workspace": r.target_workspace, "score": s}
                for r, s in matches[1:3]
            ],
        }
    
    def record_switch(self, from_workspace: str, to_workspace: str, 
                      context: ContextSnapshot, triggered_by: str = "manual"):
        """Record a workspace switch in history."""
        entry = {
            "timestamp": time.time(),
            "from": from_workspace,
            "to": to_workspace,
            "context": context.to_dict(),
            "triggered_by": triggered_by,
        }
        self.history.append(entry)
        self._save_history()
    
    def get_switch_patterns(self) -> Dict[str, Any]:
        """Analyze switch history for patterns."""
        if not self.history:
            return {"message": "No switch history available"}
        
        # Most common switches
        switch_counts = {}
        for entry in self.history:
            key = f"{entry['from']} -> {entry['to']}"
            switch_counts[key] = switch_counts.get(key, 0) + 1
        
        # Most frequent workspaces
        workspace_counts = {}
        for entry in self.history:
            workspace_counts[entry["to"]] = workspace_counts.get(entry["to"], 0) + 1
        
        # Time-based patterns
        hour_distribution = {}
        for entry in self.history:
            hour = time.localtime(entry["timestamp"]).tm_hour
            hour_distribution[hour] = hour_distribution.get(hour, 0) + 1
        
        return {
            "total_switches": len(self.history),
            "top_switches": dict(sorted(switch_counts.items(), 
                                        key=lambda x: x[1], reverse=True)[:5]),
            "top_workspaces": dict(sorted(workspace_counts.items(),
                                          key=lambda x: x[1], reverse=True)[:5]),
            "hour_distribution": hour_distribution,
        }
    
    def capture_context(self) -> ContextSnapshot:
        """Capture current terminal context."""
        ctx = ContextSnapshot(
            timestamp=time.time(),
            cwd=os.getcwd(),
        )
        
        # Detect git branch
        try:
            git_dir = os.path.join(ctx.cwd, ".git")
            if os.path.isdir(git_dir):
                head_file = os.path.join(git_dir, "HEAD")
                if os.path.exists(head_file):
                    with open(head_file, "r") as f:
                        ref = f.read().strip()
                    if ref.startswith("ref: "):
                        ctx.git_branch = ref[5:].replace("refs/heads/", "")
        except Exception:
            pass
        
        # Capture relevant env vars
        relevant_env = [
            "TERM_NEXUS_WORKSPACE", "TERM_NEXUS_WORKSPACE_ID",
            "ANTHROPIC_API_KEY", "OPENAI_API_KEY", "GEMINI_API_KEY",
            "OLLAMA_HOST", "VIRTUAL_ENV", "CONDA_DEFAULT_ENV",
        ]
        for key in relevant_env:
            if key in os.environ:
                ctx.env_vars[key] = os.environ[key]
        
        # Get recent commands from shell history (if available)
        ctx.recent_commands = self._get_recent_commands()
        
        # Detect active agents
        ctx.active_agents = self._detect_active_agents()
        
        # Get recent file context
        ctx.file_context = self._get_file_context()
        
        return ctx
    
    def _get_recent_commands(self, count: int = 10) -> List[str]:
        """Get recent commands from shell history."""
        commands = []
        
        # Try to read bash/zsh history
        history_files = [
            os.path.expanduser("~/.bash_history"),
            os.path.expanduser("~/.zsh_history"),
        ]
        
        for hist_file in history_files:
            if os.path.exists(hist_file):
                try:
                    with open(hist_file, "r", errors="ignore") as f:
                        lines = f.readlines()
                    # Get last N non-empty lines
                    for line in reversed(lines):
                        line = line.strip()
                        if line and not line.startswith("#"):
                            commands.append(line)
                            if len(commands) >= count:
                                break
                except Exception:
                    pass
                break
        
        return commands
    
    def _detect_active_agents(self) -> List[str]:
        """Detect currently active AI Agents."""
        agents = []
        
        try:
            if os.name == "posix":
                import subprocess
                result = subprocess.run(
                    ["ps", "-eo", "cmd"],
                    capture_output=True, text=True, timeout=5
                )
                
                agent_patterns = {
                    "claude": "claude",
                    "codex": "codex",
                    "cursor": "cursor",
                    "gemini": "gemini",
                    "aider": "aider",
                    "continue": "continue",
                    "copilot": "copilot",
                    "ollama": "ollama",
                }
                
                for line in result.stdout.split("\n"):
                    line_lower = line.lower()
                    for agent, pattern in agent_patterns.items():
                        if pattern in line_lower and agent not in agents:
                            agents.append(agent)
        except Exception:
            pass
        
        return agents
    
    def _get_file_context(self, count: int = 5) -> List[str]:
        """Get recent file context from current directory."""
        files = []
        cwd = os.getcwd()
        
        try:
            # List files modified recently
            all_files = []
            for f in os.listdir(cwd):
                if os.path.isfile(os.path.join(cwd, f)) and not f.startswith("."):
                    mtime = os.path.getmtime(os.path.join(cwd, f))
                    all_files.append((f, mtime))
            
            # Sort by modification time
            all_files.sort(key=lambda x: x[1], reverse=True)
            files = [f[0] for f in all_files[:count]]
        except Exception:
            pass
        
        return files
    
    def suggest_next_workspace(self, current_workspace: str = "") -> Optional[Dict[str, Any]]:
        """Suggest next workspace based on patterns."""
        if not self.history:
            return None
        
        # Find what users typically switch to after current workspace
        next_workspaces = {}
        for entry in self.history:
            if entry["from"] == current_workspace:
                to = entry["to"]
                next_workspaces[to] = next_workspaces.get(to, 0) + 1
        
        if not next_workspaces:
            return None
        
        best = max(next_workspaces.items(), key=lambda x: x[1])
        total = sum(next_workspaces.values())
        
        return {
            "workspace": best[0],
            "probability": round(best[1] / total, 2),
            "based_on": f"{best[1]} out of {total} switches from {current_workspace}",
        }
