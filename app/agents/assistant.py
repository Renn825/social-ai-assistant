from dataclasses import dataclass
from typing import Any, Callable

from sqlmodel import Session, select

from app.models.post import CrawlPost
from app.services.ai import LLMClient


@dataclass
class ToolResult:
    name: str
    output: Any


class AssistantAgent:
    def __init__(self, session: Session) -> None:
        self.session = session
        self.llm = LLMClient()
        self.tools: dict[str, Callable[[dict[str, Any]], Any]] = {
            "search_posts": self.search_posts,
            "summarize_posts": self.summarize_posts,
            "generate_report": self.generate_report,
        }

    def call_tool(self, name: str, arguments: dict[str, Any]) -> ToolResult:
        tool = self.tools.get(name)
        if tool is None:
            return ToolResult(name=name, output={"error": f"unknown tool: {name}"})
        return ToolResult(name=name, output=tool(arguments))

    def search_posts(self, arguments: dict[str, Any]) -> list[dict[str, Any]]:
        keyword = arguments.get("keyword", "")
        limit = min(int(arguments.get("limit", 10)), 50)
        statement = select(CrawlPost).limit(limit)
        if keyword:
            statement = statement.where(CrawlPost.title.contains(keyword))
        posts = self.session.exec(statement).all()
        return [
            {
                "id": post.id,
                "platform": post.platform,
                "title": post.title,
                "url": post.url,
            }
            for post in posts
        ]

    def summarize_posts(self, arguments: dict[str, Any]) -> dict[str, Any]:
        keyword = arguments.get("keyword", "")
        posts = self.search_posts({"keyword": keyword, "limit": 10})
        content = "\n".join(item["title"] for item in posts)
        data = self.llm.complete_json(
            [
                {
                    "role": "system",
                    "content": "你是内容分析助手，请总结社媒内容主题。",
                },
                {
                    "role": "user",
                    "content": f"请总结以下内容主题：\n{content}",
                },
            ]
        )
        return data

    def generate_report(self, arguments: dict[str, Any]) -> dict[str, Any]:
        platform = arguments.get("platform", "xiaohongshu")
        posts = self.session.exec(
            select(CrawlPost)
            .where(CrawlPost.platform == platform)
            .limit(20)
        ).all()
        samples = "\n".join(f"- {post.title}" for post in posts)
        return self.llm.complete_json(
            [
                {
                    "role": "system",
                    "content": "你是社媒数据分析师，请生成结构化分析报告。",
                },
                {
                    "role": "user",
                    "content": f"请基于以下内容生成周报：\n{samples or '暂无数据'}",
                },
            ]
        )

    def run(self, message: str) -> dict[str, Any]:
        if not self.llm.enabled:
            return self._rule_based_run(message)

        # A production version should use OpenAI function calling or
        # LangGraph. The current implementation keeps the same tool interface
        # while remaining runnable without an external LLM.
        return {
            "answer": "已调用社媒数据分析能力。",
            "tool_calls": [],
        }

    def _rule_based_run(self, message: str) -> dict[str, Any]:
        if "报告" in message:
            result = self.call_tool("generate_report", {})
            return {
                "answer": result.output.get("summary", "已生成报告"),
                "tool_calls": [{"name": result.name, "output": result.output}],
            }

        result = self.call_tool("summarize_posts", {})
        return {
            "answer": result.output.get("summary", "已完成内容总结"),
            "tool_calls": [{"name": result.name, "output": result.output}],
        }

