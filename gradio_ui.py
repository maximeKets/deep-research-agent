from agents import trace, InputGuardrailTripwireTriggered, Runner
import gradio as gr
from deep_research_manager import research_manager


async def run(query: str):
    with trace("Deep Research Company"):
        try:
            result = await Runner.run(research_manager, query, max_turns=10)
            return result.final_output
        except InputGuardrailTripwireTriggered:
            return (
                " **Requête bloquée par le guardrail de sécurité.**"
            )



