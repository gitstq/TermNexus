#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Workspace Module Tests - 工作区模块测试
"""

import os
import sys
import tempfile
import unittest
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from termnexus.workspace import Workspace, WorkspaceManager


class TestWorkspace(unittest.TestCase):
    """Test Workspace class."""
    
    def test_create_workspace(self):
        """Test workspace creation."""
        ws = Workspace("test-project", "/tmp/test", "project")
        self.assertEqual(ws.name, "test-project")
        self.assertEqual(ws.path, "/tmp/test")
        self.assertEqual(ws.workspace_type, "project")
        self.assertTrue(len(ws.id) > 0)
    
    def test_add_session(self):
        """Test adding session to workspace."""
        ws = Workspace("test")
        session = ws.add_session("shell", 1234, "bash")
        self.assertEqual(session["type"], "shell")
        self.assertEqual(session["pid"], 1234)
        self.assertEqual(len(ws.sessions), 1)
    
    def test_remove_session(self):
        """Test removing session."""
        ws = Workspace("test")
        session = ws.add_session("shell", 1234, "bash")
        result = ws.remove_session(session["id"])
        self.assertTrue(result)
        self.assertEqual(len(ws.sessions), 0)
    
    def test_to_dict(self):
        """Test serialization."""
        ws = Workspace("test", "/tmp", "general")
        data = ws.to_dict()
        self.assertEqual(data["name"], "test")
        self.assertEqual(data["path"], "/tmp")
        self.assertIn("id", data)
    
    def test_from_dict(self):
        """Test deserialization."""
        ws = Workspace("test", "/tmp", "general")
        data = ws.to_dict()
        ws2 = Workspace.from_dict(data)
        self.assertEqual(ws2.name, ws.name)
        self.assertEqual(ws2.id, ws.id)


class TestWorkspaceManager(unittest.TestCase):
    """Test WorkspaceManager class."""
    
    def setUp(self):
        """Set up test environment."""
        self.temp_dir = tempfile.mkdtemp()
        self.wm = WorkspaceManager(self.temp_dir)
    
    def tearDown(self):
        """Clean up test environment."""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_create_workspace(self):
        """Test creating workspace."""
        ws = self.wm.create_workspace("my-project", auto_detect=False)
        self.assertEqual(ws.name, "my-project")
        self.assertIn(ws.id, self.wm.workspaces)
    
    def test_list_workspaces(self):
        """Test listing workspaces."""
        self.wm.create_workspace("ws1", auto_detect=False)
        self.wm.create_workspace("ws2", auto_detect=False)
        workspaces = self.wm.list_workspaces()
        self.assertEqual(len(workspaces), 2)
    
    def test_find_workspace(self):
        """Test finding workspace by name."""
        ws = self.wm.create_workspace("find-me", auto_detect=False)
        found = self.wm.find_workspace_by_name("find-me")
        self.assertIsNotNone(found)
        self.assertEqual(found.id, ws.id)
    
    def test_delete_workspace(self):
        """Test deleting workspace."""
        ws = self.wm.create_workspace("delete-me", auto_detect=False)
        result = self.wm.delete_workspace(ws.id)
        self.assertTrue(result)
        self.assertNotIn(ws.id, self.wm.workspaces)
    
    def test_rename_workspace(self):
        """Test renaming workspace."""
        ws = self.wm.create_workspace("old-name", auto_detect=False)
        result = self.wm.rename_workspace(ws.id, "new-name")
        self.assertTrue(result)
        self.assertEqual(self.wm.workspaces[ws.id].name, "new-name")
    
    def test_get_stats(self):
        """Test getting statistics."""
        self.wm.create_workspace("ws1", auto_detect=False)
        self.wm.create_workspace("ws2", auto_detect=False)
        stats = self.wm.get_workspace_stats()
        self.assertEqual(stats["total_workspaces"], 2)
    
    def test_detect_workspace_type(self):
        """Test workspace type detection."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create a Python project
            Path(tmpdir, "requirements.txt").touch()
            ws_type = self.wm._detect_workspace_type(tmpdir)
            self.assertEqual(ws_type, "python")
    
    def test_persistence(self):
        """Test workspace persistence."""
        ws = self.wm.create_workspace("persist", auto_detect=False)
        self.wm.save_workspaces()
        
        # Create new manager pointing to same directory
        wm2 = WorkspaceManager(self.temp_dir)
        self.assertIn(ws.id, wm2.workspaces)
        self.assertEqual(wm2.workspaces[ws.id].name, "persist")


if __name__ == "__main__":
    unittest.main()
