from fastapi import FastAPI

from app.agents.planner import PlannerAgent
from app.models.schemas import ResearchRequest


app = FastAPI(
    title="Research & Search Agent",
    description="Agentic AI system for multi-source research",
    version="1.0.0"
)


planner = PlannerAgent()


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "research-search-agent"
    }


@app.post("/research")
def research(request: ResearchRequest):

    plan = planner.create_plan(request.question)

    return {
        "question": request.question,
        "search_queries": plan.queries
    }