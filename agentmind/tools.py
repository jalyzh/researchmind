"""工具层 - Agent 可调用的工具集合"""

import re
import textwrap
from typing import Optional

import requests
from duckduckgo_search import DDGS


def search_web(query: str, max_results: int = 5) -> list[dict]:
    """
    DuckDuckGo 搜索，返回搜索结果列表。
    每条结果包含: title, url, snippet
    """
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=max_results))
        return [
            {
                "title": r.get("title", ""),
                "url": r.get("href", ""),
                "snippet": r.get("body", ""),
            }
            for r in results
        ]
    except Exception as e:
        return [{"title": f"[搜索出错]", "url": "", "snippet": f"搜索失败: {e}"}]


def fetch_page(url: str, timeout: int = 15) -> str:
    """
    抓取网页内容，返回纯文本。
    限制最大长度避免 token 爆炸。
    """
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        )
    }
    try:
        resp = requests.get(url, headers=headers, timeout=timeout)
        resp.raise_for_status()
        text = resp.text

        # 简单清理 HTML 标签
        text = re.sub(r"<script[^>]*>.*?</script>", "", text, flags=re.DOTALL)
        text = re.sub(r"<style[^>]*>.*?</style>", "", text, flags=re.DOTALL)
        text = re.sub(r"<[^>]+>", " ", text)
        text = re.sub(r"\s+", " ", text).strip()

        # 限制长度
        max_chars = 8000
        if len(text) > max_chars:
            text = text[:max_chars] + "\n\n[...内容已截断...]"

        return text
    except Exception as e:
        return f"[抓取失败] {url}: {e}"


def summarize_text(text: str, max_length: int = 200) -> str:
    """简单截断文本到指定长度"""
    if len(text) <= max_length:
        return text
    return text[:max_length].rsplit(" ", 1)[0] + "..."
