"""FastAPI entry point for govt-customer-support (Self-Hosted on Azure Container Apps)."""

import os
import logging
from contextlib import asynccontextmanager
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

load_dotenv()

# --- Azure Monitor / OpenTelemetry Instrumentation ---
from azure.monitor.opentelemetry import configure_azure_monitor
from opentelemetry import trace

connection_string = os.environ.get("APPLICATIONINSIGHTS_CONNECTION_STRING", "")
if connection_string:
    configure_azure_monitor(connection_string=connection_string)
    logging.info("Azure Monitor telemetry enabled")
else:
    logging.warning("APPLICATIONINSIGHTS_CONNECTION_STRING not set - telemetry disabled")

tracer = trace.get_tracer("govt-customer-support")
# --- End Instrumentation ---

from .agent_runtime import run_agent

# Business Rules:
# Always greet the customer by name. Escalate if unresolved after 3 attempts. Never share internal ticket IDs with customers.

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting govt-customer-support...")
    yield
    print("Shutting down govt-customer-support...")


app = FastAPI(
    title="govt-customer-support",
    description="A customer support agent for government services",
    version="1.0.0",
    lifespan=lifespan,
)


class InvokeRequest(BaseModel):
    message: str
    session_id: str | None = None


class InvokeResponse(BaseModel):
    response: str
    session_id: str | None = None


@app.get("/health")
async def health():
    return {"status": "healthy", "agent": "govt-customer-support"}


@app.post("/invoke", response_model=InvokeResponse)
async def invoke(req: InvokeRequest):
    """Invoke the agent with a message."""
    with tracer.start_as_current_span("agent_invoke") as span:
        span.set_attribute("agent.name", "govt-customer-support")
        span.set_attribute("agent.session_id", req.session_id or "none")
        span.set_attribute("agent.message_length", len(req.message))
        try:
            result = await run_agent(req.message)
            span.set_attribute("agent.response_length", len(result))
            span.set_attribute("agent.status", "success")
            return InvokeResponse(response=result, session_id=req.session_id)
        except Exception as e:
            span.set_attribute("agent.status", "error")
            span.set_attribute("agent.error", str(e))
            span.record_exception(e)
            raise HTTPException(status_code=500, detail=str(e))