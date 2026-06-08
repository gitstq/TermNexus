#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Router Module Tests - 路由模块测试
"""

import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from termnexus.router import RouteRule, ContextSnapshot, AgentRouter


class TestRouteRule(unittest.TestCase):
    """Test RouteRule dataclass."""
    
    def test_create_rule(self):
        """Test rule creation."""
        rule = RouteRule("test", "python", "py-workspace", 5)
        self.assertEqual(rule.name, "test")
        self.assertEqual(rule.pattern, "python")
        self.assertEqual(rule.target_workspace, "py-workspace")
        self.assertEqual(rule.priority, 5)


class TestContextSnapshot(unittest.TestCase):
    """Test ContextSnapshot dataclass."""
    
    def test_create_snapshot(self):
        """Test snapshot creation."""
        ctx = ContextSnapshot(
            timestamp=0,
            cwd="/tmp",
            git_branch="main",
        )
        self.assertEqual(ctx.cwd, "/tmp")
        self.assertEqual(ctx.git_branch, "main")


class TestAgentRouter(unittest.TestCase):
    """Test AgentRouter class."""
    
    def setUp(self):
        """Set up test environment."""
        self.temp_dir = tempfile.mkdtemp()
        self.router = AgentRouter(self.temp_dir)
    
    def tearDown(self):
        """Clean up test environment."""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_add_rule(self):
        """Test adding routing rule."""
        rule = RouteRule("new-rule", "test", "test-workspace", 5)
        result = self.router.add_rule(rule)
        self.assertTrue(result)
        self.assertEqual(len(self.router.rules), len(self.router.DEFAULT_RULES) + 1)
    
    def test_add_duplicate_rule(self):
        """Test adding duplicate rule."""
        rule = RouteRule("new-rule", "test", "test-workspace")
        self.router.add_rule(rule)
        result = self.router.add_rule(rule)
        self.assertFalse(result)
    
    def test_remove_rule(self):
        """Test removing rule."""
        rule = RouteRule("removable", "test", "test-workspace")
        self.router.add_rule(rule)
        result = self.router.remove_rule("removable")
        self.assertTrue(result)
    
    def test_match_context(self):
        """Test context matching."""
        ctx = ContextSnapshot(
            timestamp=0,
            cwd="/project",
            recent_commands=["python script.py", "pytest"],
        )
        matches = self.router.match_context(ctx)
        self.assertTrue(len(matches) > 0)
    
    def test_get_recommendation(self):
        """Test getting recommendation."""
        ctx = ContextSnapshot(
            timestamp=0,
            cwd="/project",
            recent_commands=["claude", "python"],
        )
        rec = self.router.get_recommendation(ctx)
        self.assertIsNotNone(rec)
        self.assertIn("workspace", rec)
        self.assertIn("confidence", rec)
    
    def test_capture_context(self):
        """Test context capture."""
        ctx = self.router.capture_context()
        self.assertIsNotNone(ctx.cwd)
        self.assertIsInstance(ctx.recent_commands, list)


if __name__ == "__main__":
    unittest.main()
