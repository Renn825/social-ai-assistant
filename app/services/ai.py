import json
from typing import Any

import httpx

from app.core.config import get_settings


class LLMClient:
    def __init__(self) -> None:
        settings = get_settings()
        self.base_url = settings.llm_base_url.rstrip("/")
        self.api_key = settings.llm_api_key
        self.model = settings.llm_model

    @property
    def enabled(self) -> bool:
        return bool(self.api_key)

    def chat(
        self,
        messages: list[dict[str, str]],
        *,
        json_mode: bool = False,
        temperature: float = 0.2,
    ) -> str:
        if not self.enabled:
            return self._mock_response(messages)

        payload: dict[str, Any] = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
        }
        if json_mode:
            payload["response_format"] = {"type": "json_object"}

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        response = httpx.post(
            f"{self.base_url}/chat/completions",
            headers=headers,
            json=payload,
            timeout=60,
        )
        response.raise_for_status()
        data = response.json()
        return data["choices"][0]["message"]["content"]

    def complete_json(
        self,
        messages: list[dict[str, str]],
        *,
        fallback: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        content = self.chat(messages, json_mode=True)
        try:
            return json.loads(content)
        except json.JSONDecodeError:
            return fallback or {"summary": content}

    def _mock_response(self, messages: list[dict[str, str]]) -> str:
        user_message = messages[-1]["content"]
        if "报告" in user_message or "周报" in user_message:
            return json.dumps(
                {
                    "title": "AI 工具话题周报",
                    "summary": "本周 AI 工具相关内容热度较高，用户关注效率提升、自动化办公和内容生成。",
                    "highlights": [
                        "效率工具类内容互动量较高",
                        "自动化办公需求增长",
                        "内容生成类选题仍有空间",
                    ],
                    "suggestions": [
                        "增加真实案例拆解",
                        "制作入门到进阶的实操流程",
                        "补充成本与效果对比",
                    ],
                },
                ensure_ascii=False,
            )
        return json.dumps(
            {
                "summary": "这是未配置 LLM API Key 时的本地模拟结果。",
                "sentiment": "neutral",
                "keywords": ["AI", "效率", "自动化"],
                "topics": ["效率工具", "自动化"],
                "content_suggestions": ["增加真实案例", "制作实操教程"],
                "copy_suggestions": ["适合新手收藏", "可直接复用的效率提示词"],
            },
            ensure_ascii=False,
        )
