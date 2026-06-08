#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Workspace Management Module - 工作区管理模块

Manages terminal workspaces with project context, environment variables,
and AI Agent session bindings.
"""

import os
import json
import time
import hashlib
from pathlib import Path
from typing import Dict, List, Optional, Any


class Workspace:
    """Represents a single terminal workspace with full context."""
    
    def __init__(self, name: str, path: str = "", workspace_type: str = "general"):
        self.name = name
        self.path = path or os.getcwd()
        self.workspace_type = workspace_type  # general, project, agent, remote
        self.created_at = time.time()
        self.updated_at = time.time()
        self.sessions: List[Dict[str, Any]] = []
        self.env_vars: Dict[str, str] = {}
        self.tags: List[str] = []
        self.metadata: Dict[str, Any] = {}
        self._id = hashlib.md5(f"{name}:{path}:{time.time()}".encode()).hexdigest()[:12]
    
    @property
    def id(self) -> str:
        return self._id
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self._id,
            "name": self.name,
            "path": self.path,
            "type": self.workspace_type,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "sessions": self.sessions,
            "env_vars": self.env_vars,
            "tags": self.tags,
            "metadata": self.metadata,
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Workspace":
        ws = cls(data["name"], data["path"], data.get("type", "general"))
        ws._id = data["id"]
        ws.created_at = data["created_at"]
        ws.updated_at = data["updated_at"]
        ws.sessions = data.get("sessions", [])
        ws.env_vars = data.get("env_vars", {})
        ws.tags = data.get("tags", [])
        ws.metadata = data.get("metadata", {})
        return ws
    
    def add_session(self, session_type: str, pid: int, cmd: str, 
                    agent_name: str = "", status: str = "running") -> Dict[str, Any]:
        """Add a new session to this workspace."""
        session = {
            "id": hashlib.md5(f"{pid}:{time.time()}".encode()).hexdigest()[:8],
            "type": session_type,
            "pid": pid,
            "command": cmd,
            "agent_name": agent_name,
            "status": status,
            "started_at": time.time(),
            "last_active": time.time(),
        }
        self.sessions.append(session)
        self.updated_at = time.time()
        return session
    
    def remove_session(self, session_id: str) -> bool:
        """Remove a session by ID."""
        for i, s in enumerate(self.sessions):
            if s["id"] == session_id:
                self.sessions.pop(i)
                self.updated_at = time.time()
                return True
        return False
    
    def update_session_status(self, session_id: str, status: str) -> bool:
        """Update session status."""
        for s in self.sessions:
            if s["id"] == session_id:
                s["status"] = status
                s["last_active"] = time.time()
                self.updated_at = time.time()
                return True
        return False
    
    def set_env_var(self, key: str, value: str):
        """Set environment variable for this workspace."""
        self.env_vars[key] = value
        self.updated_at = time.time()
    
    def add_tag(self, tag: str):
        """Add a tag to this workspace."""
        if tag not in self.tags:
            self.tags.append(tag)
            self.updated_at = time.time()
    
    def get_active_sessions_count(self) -> int:
        """Get count of active sessions."""
        return sum(1 for s in self.sessions if s["status"] == "running")
    
    def get_agent_sessions(self) -> List[Dict[str, Any]]:
        """Get all AI Agent sessions in this workspace."""
        return [s for s in self.sessions if s["type"] in ("agent", "ai")]


class WorkspaceManager:
    """Manages all workspaces with persistence."""
    
    AGENT_PATTERNS = {
        "claude": ["claude", "claude-code", "anthropic"],
        "codex": ["codex", "openai-codex"],
        "cursor": ["cursor", "cursor-agent"],
        "gemini": ["gemini", "gemini-cli"],
        "aider": ["aider"],
        "continue": ["continue"],
        "copilot": ["github-copilot", "copilot-cli"],
        "ollama": ["ollama"],
        "generic": ["python", "node", "npm", "yarn"],
    }
    
    def __init__(self, config_dir: Optional[str] = None):
        self.config_dir = Path(config_dir or self._get_default_config_dir())
        self.config_dir.mkdir(parents=True, exist_ok=True)
        self.workspaces_file = self.config_dir / "workspaces.json"
        self.workspaces: Dict[str, Workspace] = {}
        self._load_workspaces()
    
    def _get_default_config_dir(self) -> str:
        """Get default configuration directory."""
        if os.name == "nt":
            return os.path.join(os.environ.get("APPDATA", ""), "TermNexus")
        else:
            return os.path.join(os.path.expanduser("~"), ".config", "termnexus")
    
    def _load_workspaces(self):
        """Load workspaces from disk."""
        if self.workspaces_file.exists():
            try:
                with open(self.workspaces_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                for ws_data in data.get("workspaces", []):
                    ws = Workspace.from_dict(ws_data)
                    self.workspaces[ws.id] = ws
            except (json.JSONDecodeError, KeyError, TypeError):
                self.workspaces = {}
    
    def save_workspaces(self):
        """Save workspaces to disk."""
        data = {
            "version": "1.0.0",
            "updated_at": time.time(),
            "workspaces": [ws.to_dict() for ws in self.workspaces.values()],
        }
        with open(self.workspaces_file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def create_workspace(self, name: str, path: str = "", 
                         workspace_type: str = "general",
                         auto_detect: bool = True) -> Workspace:
        """Create a new workspace."""
        if not path:
            path = os.getcwd()
        
        path = os.path.abspath(path)
        
        # Auto-detect workspace type from directory contents
        if auto_detect:
            workspace_type = self._detect_workspace_type(path)
        
        ws = Workspace(name, path, workspace_type)
        
        # Auto-detect project metadata
        if auto_detect:
            ws.metadata = self._detect_project_metadata(path)
            ws.tags = self._detect_tags(path, workspace_type)
        
        self.workspaces[ws.id] = ws
        self.save_workspaces()
        return ws
    
    def _detect_workspace_type(self, path: str) -> str:
        """Auto-detect workspace type from directory."""
        if not os.path.isdir(path):
            return "general"
        
        files = os.listdir(path)
        
        # Check for AI agent project markers
        agent_markers = [".claude", ".aider", ".cursorrules", ".continue"]
        if any(os.path.exists(os.path.join(path, m)) for m in agent_markers):
            return "agent"
        
        # Check for project types
        if any(f in files for f in ["package.json", "yarn.lock", "pnpm-lock.yaml"]):
            return "node"
        elif any(f in files for f in ["requirements.txt", "setup.py", "pyproject.toml", "Pipfile"]):
            return "python"
        elif any(f in files for f in ["Cargo.toml", "go.mod", "pom.xml", "build.gradle"]):
            return "project"
        elif any(f in files for f in ["Dockerfile", "docker-compose.yml", ".dockerignore"]):
            return "docker"
        elif any(f in files for f in [".git", ".github"]):
            return "project"
        
        return "general"
    
    def _detect_project_metadata(self, path: str) -> Dict[str, Any]:
        """Detect project metadata from directory."""
        metadata = {}
        
        if not os.path.isdir(path):
            return metadata
        
        # Detect Git info
        git_dir = os.path.join(path, ".git")
        if os.path.isdir(git_dir):
            metadata["git"] = True
            try:
                head_file = os.path.join(git_dir, "HEAD")
                if os.path.exists(head_file):
                    with open(head_file, "r") as f:
                        ref = f.read().strip()
                    if ref.startswith("ref: "):
                        metadata["git_branch"] = ref[5:].replace("refs/heads/", "")
            except Exception:
                pass
        
        # Detect language/framework
        files = os.listdir(path)
        if "package.json" in files:
            try:
                with open(os.path.join(path, "package.json"), "r") as f:
                    pkg = json.load(f)
                metadata["framework"] = "node"
                metadata["project_name"] = pkg.get("name", "")
                metadata["scripts"] = list(pkg.get("scripts", {}).keys())
            except Exception:
                pass
        elif "requirements.txt" in files:
            metadata["framework"] = "python"
        elif "Cargo.toml" in files:
            metadata["framework"] = "rust"
        elif "go.mod" in files:
            metadata["framework"] = "go"
        
        # Count files by type
        file_counts = {}
        for root, dirs, filenames in os.walk(path):
            # Skip common non-project dirs
            dirs[:] = [d for d in dirs if d not in 
                       ["node_modules", ".git", "__pycache__", ".venv", 
                        "venv", "target", "build", "dist", ".idea", ".vscode"]]
            for f in filenames:
                ext = os.path.splitext(f)[1].lower()
                if ext:
                    file_counts[ext] = file_counts.get(ext, 0) + 1
        
        metadata["file_counts"] = dict(sorted(file_counts.items(), 
                                               key=lambda x: x[1], reverse=True)[:10])
        
        return metadata
    
    def _detect_tags(self, path: str, workspace_type: str) -> List[str]:
        """Auto-detect tags for workspace."""
        tags = [workspace_type]
        
        if not os.path.isdir(path):
            return tags
        
        files = os.listdir(path)
        
        # Language tags
        lang_map = {
            "python": [".py", "requirements.txt", "setup.py", "pyproject.toml"],
            "javascript": [".js", "package.json"],
            "typescript": [".ts", ".tsx", "tsconfig.json"],
            "rust": [".rs", "Cargo.toml"],
            "go": [".go", "go.mod"],
            "java": [".java", "pom.xml", "build.gradle"],
        }
        
        for lang, markers in lang_map.items():
            if any(any(f.endswith(m) or f == m for f in files) for m in markers):
                if lang not in tags:
                    tags.append(lang)
        
        # Framework tags
        if "package.json" in files:
            try:
                with open(os.path.join(path, "package.json"), "r") as f:
                    pkg = json.load(f)
                deps = {**pkg.get("dependencies", {}), **pkg.get("devDependencies", {})}
                fw_map = {
                    "react": "react", "vue": "vue", "angular": "angular",
                    "next": "nextjs", "nuxt": "nuxtjs", "svelte": "svelte",
                    "express": "express", "fastapi": "fastapi", "django": "django",
                    "flask": "flask", "spring": "spring",
                }
                for dep, tag in fw_map.items():
                    if dep in deps and tag not in tags:
                        tags.append(tag)
            except Exception:
                pass
        
        # AI Agent tags
        agent_markers = {
            "claude": [".claude", "CLAUDE.md", ".claudeignore"],
            "cursor": [".cursorrules", ".cursor"],
            "aider": [".aider", ".aider.conf.yml"],
            "continue": [".continue", ".continueignore"],
        }
        for agent, markers in agent_markers.items():
            if any(os.path.exists(os.path.join(path, m)) for m in markers):
                if agent not in tags:
                    tags.append(agent)
        
        return tags
    
    def get_workspace(self, workspace_id: str) -> Optional[Workspace]:
        """Get workspace by ID."""
        return self.workspaces.get(workspace_id)
    
    def find_workspace_by_name(self, name: str) -> Optional[Workspace]:
        """Find workspace by name (exact or partial match)."""
        # Exact match first
        for ws in self.workspaces.values():
            if ws.name == name:
                return ws
        # Partial match
        for ws in self.workspaces.values():
            if name.lower() in ws.name.lower():
                return ws
        return None
    
    def list_workspaces(self, workspace_type: Optional[str] = None,
                        tag: Optional[str] = None) -> List[Workspace]:
        """List workspaces with optional filtering."""
        result = list(self.workspaces.values())
        
        if workspace_type:
            result = [ws for ws in result if ws.workspace_type == workspace_type]
        
        if tag:
            result = [ws for ws in result if tag in ws.tags]
        
        # Sort by updated_at descending
        result.sort(key=lambda ws: ws.updated_at, reverse=True)
        return result
    
    def delete_workspace(self, workspace_id: str) -> bool:
        """Delete a workspace."""
        if workspace_id in self.workspaces:
            del self.workspaces[workspace_id]
            self.save_workspaces()
            return True
        return False
    
    def rename_workspace(self, workspace_id: str, new_name: str) -> bool:
        """Rename a workspace."""
        ws = self.workspaces.get(workspace_id)
        if ws:
            ws.name = new_name
            ws.updated_at = time.time()
            self.save_workspaces()
            return True
        return False
    
    def get_workspace_stats(self) -> Dict[str, Any]:
        """Get overall workspace statistics."""
        total = len(self.workspaces)
        type_counts = {}
        tag_counts = {}
        total_sessions = 0
        active_sessions = 0
        agent_sessions = 0
        
        for ws in self.workspaces.values():
            type_counts[ws.workspace_type] = type_counts.get(ws.workspace_type, 0) + 1
            for tag in ws.tags:
                tag_counts[tag] = tag_counts.get(tag, 0) + 1
            total_sessions += len(ws.sessions)
            active_sessions += ws.get_active_sessions_count()
            agent_sessions += len(ws.get_agent_sessions())
        
        return {
            "total_workspaces": total,
            "type_distribution": type_counts,
            "top_tags": dict(sorted(tag_counts.items(), key=lambda x: x[1], reverse=True)[:10]),
            "total_sessions": total_sessions,
            "active_sessions": active_sessions,
            "agent_sessions": agent_sessions,
        }
    
    def detect_agent_sessions(self, workspace_id: str) -> List[Dict[str, Any]]:
        """Detect AI Agent sessions in a workspace by scanning processes."""
        ws = self.workspaces.get(workspace_id)
        if not ws:
            return []
        
        detected = []
        
        # Try to detect running processes (platform-specific)
        try:
            if os.name == "posix":
                import subprocess
                # Get processes with cwd matching workspace path
                result = subprocess.run(
                    ["ps", "-eo", "pid,ppid,cmd"],
                    capture_output=True, text=True, timeout=5
                )
                for line in result.stdout.split("\n")[1:]:
                    parts = line.strip().split(None, 2)
                    if len(parts) >= 3:
                        pid_str, _, cmd = parts
                        try:
                            pid = int(pid_str)
                        except ValueError:
                            continue
                        
                        # Check if process belongs to this workspace
                        try:
                            proc_cwd = os.readlink(f"/proc/{pid}/cwd")
                            if proc_cwd == ws.path or proc_cwd.startswith(ws.path + "/"):
                                agent_name = self._classify_agent(cmd)
                                if agent_name:
                                    detected.append({
                                        "pid": pid,
                                        "command": cmd[:80],
                                        "agent": agent_name,
                                        "cwd": proc_cwd,
                                    })
                        except (OSError, PermissionError):
                            continue
        except Exception:
            pass
        
        return detected
    
    def _classify_agent(self, cmd: str) -> str:
        """Classify a command line as an AI Agent type."""
        cmd_lower = cmd.lower()
        for agent, patterns in self.AGENT_PATTERNS.items():
            for pattern in patterns:
                if pattern in cmd_lower:
                    return agent
        return ""
    
    def switch_to_workspace(self, workspace_id: str) -> bool:
        """Switch to a workspace (change directory and set env vars)."""
        ws = self.workspaces.get(workspace_id)
        if not ws:
            return False
        
        if os.path.isdir(ws.path):
            os.chdir(ws.path)
            # Set workspace env vars
            for key, value in ws.env_vars.items():
                os.environ[key] = value
            os.environ["TERM_NEXUS_WORKSPACE"] = ws.name
            os.environ["TERM_NEXUS_WORKSPACE_ID"] = ws.id
            ws.updated_at = time.time()
            self.save_workspaces()
            return True
        return False
