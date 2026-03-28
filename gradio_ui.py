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

with gr.Blocks() as ui:
    gr.Markdown("# 🔍 Analyse Concurrentielle")
    query_textbox = gr.Textbox(
        label="Saisissez le nom d'une entreprise pour l'analyse :",
        placeholder="Ex: Tesla, Apple, OpenAI..."
    )
    run_button = gr.Button("Lancer l'analyse", variant="primary")
    report = gr.Markdown(label="Rapport d'analyse")

    run_button.click(fn=run, inputs=query_textbox, outputs=report)
    query_textbox.submit(fn=run, inputs=query_textbox, outputs=report)

ui.launch(inbrowser=True, theme=gr.themes.Default(primary_hue="sky"))

