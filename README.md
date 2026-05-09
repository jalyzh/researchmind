# ResearchMind 🤖✨

**AI 驱动的智能研究助手 — 展示多步骤 Agent 工作流的完整项目**

> ResearchMind 是一个展示完整 AI Agent 工作流的开源项目。
> 核心能力：Agent 自主规划 → 工具调用执行 → 信息综合生成报告。

---

## 项目概述

ResearchMind 是一个**演示 AI Agent 工作流**的命令行工具。它接收一个研究主题，自动完成以下步骤：

```
用户输入主题
     ↓
┌─────────────────────────────────────┐
│  Step 1: 规划 (Plan)                 │
│  Agent 将主题分解为 3-5 个子问题      │
├─────────────────────────────────────┤
│  Step 2: 搜索 (Search)               │
│  Agent 调用搜索工具，对每个子问题      │
│  联网搜索并抓取页面内容               │
├─────────────────────────────────────┤
│  Step 3: 综合 (Synthesize)           │
│  Agent 综合所有信息，生成结构化报告    │
└─────────────────────────────────────┘
     ↓
生成 Markdown 研究报告 📄
```

### 展示的能力

| 能力 | 说明 |
|------|------|
| 🤖 **Agent 工作流** | 多步骤推理：规划 → 执行 → 综合 |
| 🔧 **工具调用** | 联网搜索、网页抓取等外部工具 |
| 🧠 **LLM 编排** | 多次调用 LLM，每次有不同角色分工 |
| 📊 **结构化输出** | 生成格式化 Markdown 研究报告 |
| 🔌 **API 兼容** | 支持 OpenAI / MiMo 等任何兼容 API |

---

## 快速开始

### 1. 安装

```bash
# 克隆仓库
git clone https://github.com/YOUR_USERNAME/researchmind.git
cd researchmind

# 安装依赖
pip install -r requirements.txt
```

### 2. 配置

```bash
# 方式一：环境变量（推荐）
set LLM_API_KEY=sk-your-api-key-here
set LLM_API_BASE=https://api.openai.com/v1
set LLM_MODEL=gpt-4o

# 或使用任意兼容 API（如 MiMo 等）：
set LLM_API_KEY=your-api-key
set LLM_API_BASE=https://api.your-provider.com/v1
set LLM_MODEL=model-name
```

### 3. 运行

```bash
# 运行研究
python -m agentmind "大语言模型在科研领域的应用"

# 查看配置
python -m agentmind --config
```

### 输出示例

运行后会生成 `output/report_<主题>.md` 文件，内容包含：

- 📋 研究概述与子问题列表
- 🔍 每个子问题的搜索结果
- ✍️ AI 综合分析与结论
- 📚 参考来源列表

---

## 项目结构

```
researchmind/
├── agentmind/              # 核心代码
│   ├── __init__.py         # 包入口
│   ├── main.py             # CLI 命令行入口
│   ├── agent.py            # Agent 核心：规划→搜索→综合工作流
│   ├── tools.py            # 工具层：搜索、网页抓取
│   ├── report.py           # 报告生成
│   └── config.py           # API 配置管理
├── examples/
│   └── sample_report.md    # 示例报告
├── tests/
│   └── test_agent.py       # 单元测试
├── requirements.txt        # Python 依赖
└── README.md               # 本文件
```

---

## 代码亮点

### 1. Agent 工作流 (`agent.py`)

```python
class ResearchAgent:
    def run(self, topic: str) -> str:
        # Step 1: Plan - 将主题分解为子问题
        questions = self.plan_research(topic)

        # Step 2: Search - 对每个子问题联网搜索
        gathered = [self.search_and_gather(q) for q in questions]

        # Step 3: Synthesize - 综合信息生成报告
        synthesis = self.synthesize(topic, gathered)
        return generate_report(topic, questions, gathered, synthesis)
```

### 2. 工具调用 (`tools.py`)

Agent 可调用 `search_web()` 搜索互联网和 `fetch_page()` 抓取网页内容，展示 AI 与外部工具的结合。

### 3. 配置灵活 (`config.py`)

支持任意 OpenAI 兼容 API，可无缝切换不同服务商。

---

## 环境要求

- Python 3.10+
- 一个 LLM API Key（OpenAI / MiMo / 其他兼容 API）

---

## License

MIT
