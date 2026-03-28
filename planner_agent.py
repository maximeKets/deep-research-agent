from pydantic import BaseModel, Field
from agents import Agent

HOW_MANY_SEARCHES = 4

INSTRUCTIONS = f"Vous êtes un analyste stratégique. À partir du nom de l'entreprise cible, générez {HOW_MANY_SEARCHES} requêtes de recherche web distinctes pour explorer son marché et ses concurrents.Les requêtes doivent être  optimisées pour un moteur de recherche."


class WebSearchItem(BaseModel):
    reason: str = Field(
        description="Votre justification sur l'importance de cette recherche pour l'analyse concurrentielle.")
    query: str = Field(description="Le terme de recherche exact à utiliser sur le web.")


class WebSearchPlan(BaseModel):
    searches: list[WebSearchItem] = Field(description="La liste des recherches web à effectuer.")


planner_agent = Agent(
    name="PlannerAgent",
    instructions=INSTRUCTIONS,
    model="gpt-4o-mini",
    output_type=WebSearchPlan,
)