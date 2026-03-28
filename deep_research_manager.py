from pathlib import Path
from dotenv import load_dotenv
from planner_agent import planner_agent
from search_agent import search_agent
from writer_agent import writer_agent
from guardrails import GuardrailAgent

load_dotenv(override=True)

planner_tool = planner_agent.as_tool(
    tool_name="planner",
    tool_description=(
        "Planifier les recherches d'analyse concurrentielle. Fournissez le nom "
        "de l'entreprise et recevez une liste de requêtes ciblées (concurrents principaux, "
        "parts de marché, positionnement, actualités) avec leurs justifications."
    ),
)

search_tool = search_agent.as_tool(
    tool_name="web_search",
    tool_description=(
        "Effectuer une recherche web ciblée. Fournissez un terme de recherche "
        "et sa raison d'être, et recevez un résumé concis des données marché ou concurrentielles."
    ),
)

manager_instruction = """\
Vous êtes le Manager d'Analyse Concurrentielle (Competitive Intelligence Manager).

Votre rôle est d'orchestrer une étude de marché et une analyse concurrentielle approfondie à partir du nom d'une entreprise fourni par l'utilisateur.

Suivez ces étapes attentivement :

1. **Planification** : L'entrée utilisateur est un nom d'entreprise strict. Utilisez l'outil `planner` pour générer une stratégie de recherche. Les requêtes doivent viser à identifier : les concurrents directs et indirects, les parts de marché, les avantages compétitifs (USP), et les actualités récentes de ce secteur. Ne sautez pas cette étape.

2. **Recherche** : Pour CHAQUE requête retournée par le planner, utilisez l'outil `web_search` en lui fournissant le terme de recherche et la raison associée. Collectez méticuleusement tous les résumés et les données chiffrées trouvées.

3. **Rédaction & Envoi** : Une fois toutes les recherches terminées, transmettez (handoff) le nom de l'entreprise ET l'ensemble des résumés structurés au WriterAgent. Le WriterAgent rédigera le rapport d'analyse concurrentielle puis le transmettra automatiquement à l'Email Agent pour l'envoi.

Règles importantes :
- L'entrée que vous recevez a déjà été vérifiée : c'est un nom d'entreprise valide.
- Vous devez TOUJOURS utiliser l'outil planner avant de lancer les recherches.
- Vous devez effectuer TOUTES les recherches suggérées par le planner pour avoir une vue marché complète.
- Ne rédigez JAMAIS le rapport vous-même — transmettez les données brutes au WriterAgent via le handoff.
"""

research_manager = GuardrailAgent(
    config=Path("guardrails_config.json"),
    name="Competitive Research Manager",
    instructions=manager_instruction,
    model="gpt-4o-mini",
)