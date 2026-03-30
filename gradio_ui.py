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

    with trace("Deep Research Orchestration"):
        try:
            result = Runner.run_streamed(research_manager, query, max_turns=30)
            
            status_log = f"⏳ Lancement de l'analyse pour **{query}**...\n\n"
            yield status_log
            
            async for event in result.stream_events():
                # Gestion des transferts d'agents
                if type(event).__name__ == "AgentUpdatedStreamEvent":
                    agent_name = event.new_agent.name if hasattr(event, "new_agent") else "spécialisé"
                    status_log += f"- 🤝 **Transfert à l'agent :** `{agent_name}`\n"
                    yield status_log
                    continue
                    
                # Sécurité : ignorer les événements qui n'ont pas l'attribut data
                if not hasattr(event, "data"):
                    continue
                    
                # Extraire de façon robuste les informations envoyées par openai-agents (Pydantic ou dictionnaires)
                data = event.data
                tool_name = None
                
                if hasattr(data, "type") and data.type == "function":
                    tool_name = getattr(data, "name", "outil métier")
                elif isinstance(data, dict) and data.get("type") == "function":
                    tool_name = data.get("name", "outil métier")
                elif "ToolCall" in type(data).__name__:
                    tool_name = getattr(data, "name", getattr(data, "function", {}).get("name", "recherche"))

                if tool_name:
                    status_log += f"- 🛠️ **Exécution de l'outil :** `{tool_name}`\n"
                    yield status_log

            increment_usage(username)
            current_usage = get_usage(username)

            status_log += "\n✅ **Analyse terminée, assemblage du rapport final...**\n"
            yield status_log
            
            # Au cas où final_output serait formaté comme un objet Pydantic de type Response
            final_report = getattr(result.final_output, "content", result.final_output)
            if not final_report:
                final_report = "L'analyse a été complétée et l'e-mail expédié, mais l'affichage du rapport complet a été omis par l'agent Email."

            yield f"{final_report}\n\n---\n*Recherche effectuée par {username} ({current_usage}/{MAX_QUOTA} requêtes utilisées)*"
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

