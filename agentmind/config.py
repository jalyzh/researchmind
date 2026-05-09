"""配置管理 - 支持 OpenAI / MiMo 等兼容 API"""

import os
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Config:
    """AI API 配置"""
    api_key: str = ""
    api_base: str = "https://api.openai.com/v1"
    model: str = "gpt-4o"
    max_tokens: int = 4096
    temperature: float = 0.7

    # 搜索配置
    max_search_results: int = 5
    max_concurrent_searches: int = 3

    # 报告配置
    report_language: str = "zh"  # zh / en

    @classmethod
    def from_env(cls) -> "Config":
        """从环境变量加载配置"""
        return cls(
            api_key=os.getenv("LLM_API_KEY", ""),
            api_base=os.getenv("LLM_API_BASE", "https://api.openai.com/v1"),
            model=os.getenv("LLM_MODEL", "gpt-4o"),
            max_tokens=int(os.getenv("LLM_MAX_TOKENS", "4096")),
            temperature=float(os.getenv("LLM_TEMPERATURE", "0.7")),
            max_search_results=int(os.getenv("MAX_SEARCH_RESULTS", "5")),
            report_language=os.getenv("REPORT_LANGUAGE", "zh"),
        )

    def validate(self) -> list[str]:
        """检查配置，返回缺少的配置项"""
        errors = []
        if not self.api_key:
            errors.append("LLM_API_KEY 未设置")
        if not self.api_base:
            errors.append("LLM_API_BASE 未设置")
        return errors
