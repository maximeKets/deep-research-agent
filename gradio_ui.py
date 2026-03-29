from agents import trace, InputGuardrailTripwireTriggered, Runner
import gradio as gr
from deep_research_manager import research_manager
from usage_tracker import has_exceeded_quota, increment_usage, get_usage, MAX_QUOTA


async def run(query: str, profile: gr.OAuthProfile | None):
    if profile is None:
        yield "⚠️ **Authentification requise**\n\nVeuillez vous connecter avec votre compte Hugging Face (bouton 'Sign in with Hugging Face') pour lancer l'analyse."
        return

    username = profile.username

    if has_exceeded_quota(username):
        yield f"⚠️ **Limite de {MAX_QUOTA} recherches atteinte**\n\nVous avez utilisé tout votre quota disponible pour ce profil ({username})."
        return

    yield f"⏳ Lancement de l'analyse pour **{query}**...\n\n*Veuillez patienter, cela peut prendre quelques minutes.*"

    with trace("Deep Research Orchestration"):
        try:
            result = Runner.run_streamed(research_manager, query, max_turns=30)

            async for event in result.stream_events():
                # Gestion des transferts d'agents
                if type(event).__name__ == "AgentUpdatedStreamEvent":
                    agent_name = event.new_agent.name if hasattr(event, "new_agent") else "spécialisé"
                    gr.Info(f"🤝 Transfert à l'agent : {agent_name}...")
                    continue
                    
                # Sécurité : ignorer les événements qui n'ont pas l'attribut data
                if not hasattr(event, "data"):
                    continue
                    
                event_type = type(event.data).__name__

                if "ToolCall" in event_type or (hasattr(event.data, "type") and event.data.type == "function"):
                    tool_name = getattr(event.data, "name", "outil") if hasattr(event.data, "name") else "recherche"
                    gr.Info(f"🛠️ Exécution de l'outil : {tool_name}")
                elif "Agent" in event_type and "Transfer" in event_type:
                    gr.Info("🤝 Transfert à un autre agent spécialisé...")
                elif "RunStep" in event_type:
                    pass

            increment_usage(username)
            current_usage = get_usage(username)

            yield f"{result.final_output}\n\n---\n*Recherche effectuée par {username} ({current_usage}/{MAX_QUOTA} requêtes utilisées)*"
        except InputGuardrailTripwireTriggered:
            yield (
                "⚠️ **Requête bloquée par le guardrail de sécurité.**\n\n"
                "Votre demande a été identifiée comme ne relevant pas d'une "
                "recherche d'information légitime. Veuillez reformuler."
            )

with gr.Blocks() as ui:
    with gr.Row():
        gr.Markdown("# 🔍 Analyse Concurrentielle")
        gr.LoginButton()

    query_textbox = gr.Textbox(
        label="Saisissez le nom d'une entreprise pour l'analyse :",
        placeholder="Ex: Tesla, Apple, OpenAI..."
    )
    run_button = gr.Button("Lancer l'analyse", variant="primary")
    report = gr.Markdown(label="Rapport d'analyse")

    run_button.click(fn=run, inputs=query_textbox, outputs=report)
    query_textbox.submit(fn=run, inputs=query_textbox, outputs=report)

ui.launch(inbrowser=True, theme=gr.themes.Default(primary_hue="sky"))

