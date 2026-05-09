"""ResearchMind 测试"""

import os
import sys
import unittest
from unittest.mock import patch, MagicMock

# 添加父目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from agentmind.config import Config
from agentmind.tools import search_web, fetch_page, summarize_text


class TestConfig(unittest.TestCase):
    def test_from_env_defaults(self):
        """测试默认配置"""
        cfg = Config.from_env()
        self.assertEqual(cfg.api_base, "https://api.openai.com/v1")
        self.assertEqual(cfg.model, "gpt-4o")

    def test_validate_empty_key(self):
        """测试空 API key 验证"""
        cfg = Config()
        errors = cfg.validate()
        self.assertIn("LLM_API_KEY 未设置", errors)

    def test_validate_ok(self):
        """测试有效配置"""
        cfg = Config(api_key="sk-test123")
        errors = cfg.validate()
        self.assertEqual(len(errors), 0)


class TestTools(unittest.TestCase):
    def test_summarize_text_short(self):
        """测试短文本"""
        text = "Hello World"
        self.assertEqual(summarize_text(text, 20), text)

    def test_summarize_text_long(self):
        """测试长文本截断"""
        text = "This is a very long text that should be truncated"
        result = summarize_text(text, 20)
        self.assertLessEqual(len(result), 20)

    def test_search_web_handles_error(self):
        """测试搜索错误处理"""
        # duckduckgo_search 可能因网络失败但不会抛异常
        results = search_web("test query", max_results=1)
        self.assertIsInstance(results, list)
        if results:
            self.assertIn("title", results[0])


if __name__ == "__main__":
    unittest.main()
