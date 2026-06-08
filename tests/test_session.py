#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Session Module Tests - 会话模块测试
"""

import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from termnexus.session import SessionInfo, SessionManager


class TestSessionInfo(unittest.TestCase):
    """Test SessionInfo dataclass."""
    
    def test_create_session(self):
        """Test session creation."""
        session = SessionInfo(
            session_id="test123",
            name="test-session",
            session_type="shell",
            pid=1234,
            command="bash",
            cwd="/tmp",
            env={},
            status="running",
            created_at=0,
            last_active=0,
            metadata={},
        )
        self.assertEqual(session.name, "test-session")
        self.assertTrue(session.is_agent is False)
    
    def test_agent_session(self):
        """Test agent session detection."""
        session = SessionInfo(
            session_id="agent123",
            name="claude-session",
            session_type="agent",
            pid=5678,
            command="claude",
            cwd="/project",
            env={},
            status="running",
            created_at=0,
            last_active=0,
            metadata={},
        )
        self.assertTrue(session.is_agent)


class TestSessionManager(unittest.TestCase):
    """Test SessionManager class."""
    
    def setUp(self):
        """Set up test environment."""
        self.temp_dir = tempfile.mkdtemp()
        self.sm = SessionManager(self.temp_dir)
    
    def tearDown(self):
        """Clean up test environment."""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_create_session(self):
        """Test creating session."""
        session = self.sm.create_session("test", "bash", "shell")
        self.assertEqual(session.name, "test")
        self.assertEqual(session.session_type, "shell")
        self.assertIn(session.session_id, self.sm.sessions)
    
    def test_list_sessions(self):
        """Test listing sessions."""
        self.sm.create_session("s1", "bash", "shell")
        self.sm.create_session("s2", "claude", "agent")
        sessions = self.sm.list_sessions()
        self.assertEqual(len(sessions), 2)
    
    def test_list_agent_sessions(self):
        """Test filtering agent sessions."""
        self.sm.create_session("s1", "bash", "shell")
        self.sm.create_session("s2", "claude", "agent")
        agents = self.sm.list_sessions(agent_only=True)
        self.assertEqual(len(agents), 1)
        self.assertEqual(agents[0].name, "s2")
    
    def test_get_session(self):
        """Test getting session by ID."""
        session = self.sm.create_session("test", "bash")
        found = self.sm.get_session(session.session_id)
        self.assertIsNotNone(found)
        self.assertEqual(found.name, "test")
    
    def test_remove_session(self):
        """Test removing session."""
        session = self.sm.create_session("test", "bash")
        result = self.sm.remove_session(session.session_id)
        self.assertTrue(result)
        self.assertNotIn(session.session_id, self.sm.sessions)
    
    def test_detect_agent(self):
        """Test agent detection from command."""
        agent = self.sm._detect_agent_from_command("claude-code", "")
        self.assertEqual(agent, "claude")
        
        agent = self.sm._detect_agent_from_command("python script.py", "")
        self.assertIsNone(agent)
    
    def test_get_stats(self):
        """Test session statistics."""
        self.sm.create_session("s1", "bash", "shell")
        self.sm.create_session("s2", "claude", "agent")
        stats = self.sm.get_session_stats()
        self.assertEqual(stats["total_sessions"], 2)
        self.assertEqual(stats["agent_sessions"], 1)
    
    def test_persistence(self):
        """Test session persistence."""
        session = self.sm.create_session("persist", "bash")
        self.sm.save_sessions()
        
        sm2 = SessionManager(self.temp_dir)
        self.assertIn(session.session_id, sm2.sessions)


if __name__ == "__main__":
    unittest.main()
