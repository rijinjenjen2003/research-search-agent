from fastapi import FastAPI

from app.models.schemas import ResearchRequest
from app.graph.workflow import research_graph


app = FastAPI(
    title="Research & Search Agent",
    description="Agentic AI system for multi-source research",
    version="1.0.0"
)


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "research-search-agent"
    }


@app.post("/research")
def research(request: ResearchRequest):

    result = research_graph.invoke({
        "question": request.question
    })

    return {
        "question": result["question"],
        "search_queries": result["search_queries"],
        "total_results": len(result["search_results"]),
        "unique_results": len(result["unique_results"]),
        "verification": result["verification"],
        "final_answer": result["final_answer"]
    }