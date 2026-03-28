from agents import trace, InputGuardrailTripwireTriggered, Runner
import gradio as gr
from deep_research_manager import research_manager
from usage_tracker import has_exceeded_quota, increment_usage, get_usage, MAX_QUOTA


async def run(query: str, profile: gr.OAuthProfile | None):
    if profile is None:
        yield "⚠️ **Authentification requise**\n\nVeuillez vous connecter avec votre compte Hugging Face (bouton 'Sign in with Hugging Face') pour lancer l'analyse."
        return

    username = profile.preferred_username


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
    with gr.Row():
        gr.Markdown("# 🔍 Analyse Concurrentielle")
        gr.LoginButton()
        gr.LogoutButton()

    query_textbox = gr.Textbox(
        label="Saisissez le nom d'une entreprise pour l'analyse :",
        placeholder="Ex: Tesla, Apple, OpenAI..."
    )
    run_button = gr.Button("Lancer l'analyse", variant="primary")
    report = gr.Markdown(label="Rapport d'analyse")

    run_button.click(fn=run, inputs=query_textbox, outputs=report)
    query_textbox.submit(fn=run, inputs=query_textbox, outputs=report)

ui.launch(inbrowser=True, theme=gr.themes.Default(primary_hue="sky"))

