from agents import Agent, WebSearchTool, ModelSettings

INSTRUCTIONS = (
    "Vous êtes un assistant de recherche en veille concurrentielle. Pour le terme de recherche donné, "
    "cherchez sur le web et produisez un résumé concis axé sur les données tangibles. "
    "Extrayez impérativement : les noms des concurrents, les chiffres clés (revenus, parts de marché), "
    "et les stratégies notables. Rédigez de manière factuelle (les listes à puces sont encouragées). "
    "Soyez extrêmement concis (moins de 300 mots). Ne faites aucun commentaire général, concentrez-vous "
    "uniquement sur la data brute et utile pour un rapport d'intelligence économique."
)

search_agent = Agent(
    name="Search agent",
    instructions=INSTRUCTIONS,
    tools=[WebSearchTool(search_context_size="low")],
    model="gpt-4o-mini",
    model_settings=ModelSettings(tool_choice="required"),
)