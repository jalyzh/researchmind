"""ResearchMind CLI 入口"""

import os
import sys
from pathlib import Path

from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown

from .config import Config
from .agent import ResearchAgent

console = Console()

BANNER = """
╔══════════════════════════════════════════╗
║          ResearchMind  v1.0              ║
║     AI 驱动的智能研究助手                  ║
╚══════════════════════════════════════════╝
"""


def print_banner():
    console.print(Panel.fit(BANNER, style="bold cyan"))


def check_config(cfg: Config) -> bool:
    errors = cfg.validate()
    if errors:
        console.print("[red]❌ 配置检查失败:[/red]")
        for e in errors:
            console.print(f"   - {e}")
        console.print()
        console.print("请设置环境变量:")
        console.print("  set LLM_API_KEY=your_api_key")
        console.print("  set LLM_API_BASE=https://api.openai.com/v1  (或 MiMo 地址)")
        console.print("  set LLM_MODEL=gpt-4o  (或小米 MiMo 模型名)")
        return False
    return True


def show_config(cfg: Config):
    console.print("\n[bold]📋 当前配置:[/bold]")
    masked_key = cfg.api_key[:8] + "..." + cfg.api_key[-4:] if len(cfg.api_key) > 12 else "***"
    console.print(f"   API Base: {cfg.api_base}")
    console.print(f"   Model:    {cfg.model}")
    console.print(f"   API Key:  {masked_key}")
    console.print(f"   语言:     {'中文' if cfg.report_language == 'zh' else 'English'}")
    console.print()


def main():
    print_banner()

    # 加载配置
    cfg = Config.from_env()

    if "--config" in sys.argv:
        show_config(cfg)
        return

    if not check_config(cfg):
        sys.exit(1)

    # 获取研究主题
    topic = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else ""
    if not topic:
        console.print("[yellow]请输入研究主题作为参数[/yellow]")
        console.print("用法: researchmind <研究主题>")
        console.print("示例: researchmind 小米MiMo大模型的技术特点与应用场景")
        sys.exit(1)

    # 运行 Agent
    try:
        agent = ResearchAgent(cfg)
        report_path = agent.run(topic)
        console.print(f"\n[green]✅ 研究完成! 报告保存在:[/green] {report_path}")
    except KeyboardInterrupt:
        console.print("\n[yellow]⚠️ 用户中断[/yellow]")
        sys.exit(1)
    except Exception as e:
        console.print(f"\n[red]❌ 运行出错: {e}[/red]")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
