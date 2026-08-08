from fastapi import FastAPI

from app.agents.planner import PlannerAgent
from app.agents.search_agent import SearchAgent
from app.models.schemas import ResearchRequest


app = FastAPI(
    title="Research & Search Agent",
    description="Agentic AI system for multi-source research",
    version="1.0.0"
)


planner = PlannerAgent()
search_agent = SearchAgent()


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "research-search-agent"
    }


@app.post("/research")
def research(request: ResearchRequest):

    plan = planner.create_plan(request.question)

    search_results = search_agent.search_queries(
        plan.queries
    )

    return {
        "question": request.question,
        "search_queries": plan.queries,
        "results": search_results
    }