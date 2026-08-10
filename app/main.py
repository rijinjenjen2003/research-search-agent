from uuid import uuid4

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

    "total_results": len(
        result.get("search_results", [])
    ),

    "unique_results": len(
        result.get("unique_results", [])
    ),

    "approved_sources": [
        {
            "title": source.get("title"),
            "url": source.get("url")
        }
        for source in result.get("approved_sources", [])
    ],

    "rejected_sources": len(
        result.get("rejected_sources", [])
    ),

    "verification": result.get("verification"),

    "final_answer": result.get("final_answer")
}