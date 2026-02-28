import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import List, Dict, Optional, Any
import os
import signal
import subprocess

from app.core.manager import Agent
from app.core.ollama_provider import OllamaProvider
from app.core.gemini_provider import GeminiProvider
from app.core.memory import Memory
from app.utils.config import Config

app = FastAPI(title="AI Agent Brain")
config = Config()
memory = Memory()

# LLM Provider Setup
def get_provider():
    provider_name = config.get("provider", "ollama")
    model_name = config.get("model", "llama3")

    if provider_name == "ollama":
        return OllamaProvider(model_name=model_name)
    elif provider_name == "gemini":
        api_key = config.get("gemini_api_key", "")
        return GeminiProvider(api_key=api_key, model_name=model_name)
    else:
        raise ValueError(f"Unknown provider: {provider_name}")

# Use the advanced Agent instead of simple Manager
agent = Agent(get_provider(), memory)

@app.on_event("startup")
async def startup_event():
    """Ensure the selected Ollama model is available on startup."""
    provider_name = config.get("provider", "ollama")
    if provider_name == "ollama":
        model_name = config.get("model", "llama3")
        print(f"Startup: Checking Ollama model '{model_name}'...")
        try:
            subprocess.run(["ollama", "pull", model_name], check=True)
        except Exception as e:
            print(f"Startup warning: Could not verify Ollama model '{model_name}': {e}")

class ChatRequest(BaseModel):
    message: str
    system_prompt: Optional[str] = None

class ChatResponse(BaseModel):
    response: str

@app.get("/status")
def get_status():
    return {
        "status": "online",
        "provider": config.get("provider"),
        "model": config.get("model")
    }

@app.post("/chat")
async def chat(request: ChatRequest):
    """
    Refactored to support streaming for better performance/latency.
    """
    try:
        # Load default prompt from file if not specified in request
        try:
            with open("app/utils/default_system_prompt.txt", "r") as f:
                default_prompt = f.read()
        except:
            default_prompt = config.get("system_prompt")

        base_prompt = request.system_prompt or default_prompt

        # Generator for streaming the response
        def generate():
            for chunk in agent.stream(request.message, base_prompt):
                yield chunk

        return StreamingResponse(generate(), media_type="text/plain")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

import asyncio

def restart_service():
    """Restarts the service after a short delay to allow the response to be sent."""
    os.kill(os.getpid(), signal.SIGTERM)

@app.post("/update")
async def update():
    """
    Triggers a git pull and a self-restart.
    In a systemd context, we might rely on the restart policy.
    """
    repo_path = config.get("repo_path", os.getcwd())
    try:
        # 1. Git Pull
        subprocess.check_call(["git", "-C", repo_path, "pull"])

        # 2. Restart (self-kill after delay, systemd should pick it up)
        loop = asyncio.get_event_loop()
        loop.call_later(1, restart_service)
        return {"status": "Update started, restarting service in 1s..."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Update failed: {str(e)}")

@app.post("/restart")
async def restart():
    loop = asyncio.get_event_loop()
    loop.call_later(1, restart_service)
    return {"status": "Restarting in 1s..."}

@app.post("/clear")
def clear_history():
    agent.clear_history()
    return {"status": "History cleared"}

def start_server():
    host = config.get("api_host", "127.0.0.1")
    port = config.get("api_port", 8000)
    uvicorn.run(app, host=host, port=port)

if __name__ == "__main__":
    start_server()
