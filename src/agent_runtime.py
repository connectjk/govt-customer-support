"""Agent runtime -- setup and run loop for govt-customer-support."""

import os
from openai import AzureOpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from .tools import web_search


SYSTEM_PROMPT = """\
A customer support agent that can search a knowledge base, create support tickets, track ticket status, and escalate complex issues to human agents when needed. It responds politely, provides step-by-step troubleshooting, and always confirms resolution before closing a case.
"""


def _get_client() -> AzureOpenAI:
    """Create Azure OpenAI client using managed identity (DefaultAzureCredential)."""
    token_provider = get_bearer_token_provider(
        DefaultAzureCredential(),
        "https://cognitiveservices.azure.com/.default",
    )
    return AzureOpenAI(
        azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
        azure_ad_token_provider=token_provider,
        api_version="2024-06-01",
    )


async def run_agent(message: str) -> str:
    """Process a single user message and return the assistant response."""
    client = _get_client()
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": message},
    ]

    response = client.chat.completions.create(
        model=os.environ.get("AZURE_OPENAI_DEPLOYMENT", "gpt-4o"),
        messages=messages,
    )

    return response.choices[0].message.content or ""