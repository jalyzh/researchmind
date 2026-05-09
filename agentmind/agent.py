"""Agent 核心 - 规划-搜索-写作 的多步骤 Agent 工作流"""

import json
from typing import Optional

from openai import OpenAI

from .config import Config
from .tools import search_web, fetch_page
from .report import generate_report


class ResearchAgent:
    """研究助手 Agent，展示了多步骤 Agent 工作流"""

    def __init__(self, config: Config):
        self.config = config
        self.client = OpenAI(
            api_key=config.api_key,
            base_url=config.api_base,
        )
        self.history: list[dict] = []  # 记录每一步的中间结果

    def _call_llm(self, system: str, prompt: str, response_format: Optional[dict] = None) -> str:
        """调用 LLM"""
        kwargs = {
            "model": self.config.model,
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": prompt},
            ],
            "temperature": self.config.temperature,
            "max_tokens": self.config.max_tokens,
        }
        if response_format:
            kwargs["response_format"] = response_format

        resp = self.client.chat.completions.create(**kwargs)
        return resp.choices[0].message.content or ""

    def plan_research(self, topic: str) -> list[str]:
        """
        步骤 1: 规划 - Agent 将研究主题分解为子问题
        """
        lang = "中文" if self.config.report_language == "zh" else "English"
        system = f"你是一个研究规划专家。将研究主题分解为 3-5 个关键子问题。用{lang}回答。"
        prompt = f"""研究主题: {topic}

请将以上主题分解为 3-5 个关键子问题，以便全面深入地研究该主题。
每个子问题应该具体、可搜索、能独立回答。

输出格式: 每行一个子问题，不要编号以外的额外格式。"""

        result = self._call_llm(system, prompt)
        questions = [
            line.strip().lstrip("0123456789.）。) ")
            for line in result.strip().split("\n")
            if line.strip()
        ]
        self.history.append({"step": "plan", "topic": topic, "questions": questions})
        return questions[:5]

    def search_and_gather(self, question: str) -> dict:
        """
        步骤 2: 搜索与收集 - Agent 调用搜索工具获取信息
        """
        # 2a. 搜索
        results = search_web(question, max_results=self.config.max_search_results)

        # 2b. 阅读前几个结果
        fetched = []
        for r in results[:3]:
            url = r.get("url", "")
            if url:
                content = fetch_page(url)
                fetched.append({
                    "url": url,
                    "title": r.get("title", ""),
                    "content": content[:3000],
                })

        return {"question": question, "search_results": results, "pages": fetched}

    def synthesize(self, topic: str, gathered_data: list[dict]) -> str:
        """
        步骤 3: 综合 - Agent 综合所有收集到的信息
        """
        lang = "中文" if self.config.report_language == "zh" else "English"
        system = f"""你是一个研究分析师。根据收集到的信息，对每个子问题给出全面准确的回答。
引用信息来源。用{lang}回答。"""

        context_parts = []
        for item in gathered_data:
            context_parts.append(f"## 问题: {item['question']}\n")
            for sr in item.get("search_results", []):
                context_parts.append(f"- [{sr.get('title','')}]({sr.get('url','')}): {sr.get('snippet','')}")
            for pg in item.get("pages", []):
                context_parts.append(f"\n[页面内容 - {pg.get('title','')}]({pg.get('url','')}):\n{pg.get('content','')[:2000]}")

        context = "\n".join(context_parts)[:30000]

        prompt = f"""研究主题: {topic}

以下是针对该主题各子问题收集到的信息:

{context}

请综合以上信息，对每个子问题给出有深度、有见解的回答。
回答要基于收集到的信息，并标注信息来源。"""

        synthesis = self._call_llm(system, prompt)
        self.history.append({"step": "synthesize", "synthesis": synthesis})
        return synthesis

    def run(self, topic: str) -> str:
        """
        运行完整的研究工作流

        步骤:
        1. 规划 (Plan)    - 将主题分解为子问题
        2. 搜索 (Search)  - 对每个子问题联网搜索
        3. 综合 (Synthesize) - 综合信息生成报告
        """
        print(f"\n🔍 研究主题: {topic}")
        print("=" * 60)

        # Step 1: Plan
        print("\n📋 [步骤 1/3] 规划研究路径...")
        questions = self.plan_research(topic)
        for i, q in enumerate(questions, 1):
            print(f"   {i}. {q}")

        # Step 2: Search & Gather
        print(f"\n🌐 [步骤 2/3] 联网搜索信息 ({len(questions)} 个子问题)...")
        gathered = []
        for i, q in enumerate(questions, 1):
            print(f"   [{i}/{len(questions)}] 搜索: {q[:50]}...")
            data = self.search_and_gather(q)
            gathered.append(data)
            print(f"      → 找到 {len(data['search_results'])} 条结果")

        # Step 3: Synthesize
        print("\n✍️  [步骤 3/3] 综合信息生成报告...")
        synthesis = self.synthesize(topic, gathered)

        # Generate final report
        print("\n📄 生成最终报告...")
        report_path = generate_report(topic, questions, gathered, synthesis, self.config)
        print(f"\n✅ 报告已生成: {report_path}")
        return report_path
