"""Agent runtime – setup and run loop for govt-customer-support."""

import os
from openai import AzureOpenAI
from .tools import web_search


SYSTEM_PROMPT = """\
A customer support agent that can search a knowledge base, create support tickets, track ticket status, and escalate complex issues to human agents when needed. It responds politely, provides step-by-step troubleshooting, and always confirms resolution before closing a case.
"""


def _get_client() -> AzureOpenAI:
    return AzureOpenAI(
        azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
        api_key=os.environ["AZURE_OPENAI_API_KEY"],
        api_version="2024-06-01",
    )


async def run_agent() -> None:
    client = _get_client()
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]

    print("Agent ready. Type 'exit' to quit.")
    while True:
        user_input = input("You: ").strip()
        if user_input.lower() in ("exit", "quit"):
            break

        messages.append({"role": "user", "content": user_input})

        response = client.chat.completions.create(
            model=os.environ.get("AZURE_OPENAI_DEPLOYMENT", "gpt-4o"),
            messages=messages,
        )

        assistant_msg = response.choices[0].message.content or ""
        messages.append({"role": "assistant", "content": assistant_msg})
        print(f"Agent: {assistant_msg}")
