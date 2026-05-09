"""报告生成"""

import os
from datetime import datetime
from typing import Optional

from .config import Config


def generate_report(
    topic: str,
    questions: list[str],
    gathered_data: list[dict],
    synthesis: str,
    config: Config,
) -> str:
    """生成 Markdown 格式研究报告"""

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    safe_topic = "".join(c if c.isalnum() or c in " _-" else "_" for c in topic)[:40]

    lines = [
        f"# {topic}",
        "",
        f"> **生成时间**: {timestamp}",
        f"> **模型**: {config.model}",
        "",
        "---",
        "",
        "## 目录",
        "",
        "1. [研究概述](#1-研究概述)",
        "2. [子问题研究](#2-子问题研究)",
        "3. [综合结论](#3-综合结论)",
        "4. [参考来源](#4-参考来源)",
        "",
        "---",
        "",
        "## 1. 研究概述",
        "",
        f"本报告针对「{topic}」进行了系统性研究。",
        f"研究过程采用 AI Agent 工作流：**规划 → 搜索 → 综合**，",
        f"共覆盖 {len(questions)} 个子问题，查阅 {sum(len(d.get('search_results',[])) for d in gathered_data)} 个信息来源。",
        "",
        "### 子问题列表",
        "",
    ]

    for i, q in enumerate(questions, 1):
        lines.append(f"- **问题 {i}**: {q}")

    lines += [
        "",
        "---",
        "",
        "## 2. 子问题研究",
        "",
    ]

    for i, (q, data) in enumerate(zip(questions, gathered_data), 1):
        lines += [
            f"### 2.{i} {q}",
            "",
            "#### 搜索结果",
            "",
        ]
        for sr in data.get("search_results", []):
            title = sr.get("title", "")
            url = sr.get("url", "")
            snippet = sr.get("snippet", "")
            lines.append(f"- **[{title}]({url})**")
            if snippet:
                lines.append(f"  - {snippet}")
            lines.append("")

        lines += [
            "#### 抓取的页面内容摘要",
            "",
        ]
        for pg in data.get("pages", []):
            title = pg.get("title", "")
            url = pg.get("url", "")
            content = pg.get("content", "")[:500]
            lines.append(f"- **[{title}]({url})**:")
            lines.append(f"  {content[:200]}...")
            lines.append("")

        lines.append("")

    lines += [
        "---",
        "",
        "## 3. 综合结论",
        "",
        synthesis,
        "",
        "---",
        "",
        "## 4. 参考来源",
        "",
    ]

    seen_urls = set()
    for data in gathered_data:
        for sr in data.get("search_results", []):
            url = sr.get("url", "")
            title = sr.get("title", "")
            if url and url not in seen_urls:
                seen_urls.add(url)
                lines.append(f"- [{title}]({url})")

    lines += [
        "",
        "---",
        "",
        f"*本报告由 ResearchMind AI Agent 自动生成 | {timestamp}*",
        "",
    ]

    # 确保输出目录存在
    output_dir = os.path.join(os.getcwd(), "output")
    os.makedirs(output_dir, exist_ok=True)

    report_path = os.path.join(output_dir, f"report_{safe_topic}.md")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    return report_path
