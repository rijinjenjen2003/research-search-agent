from langgraph.graph import StateGraph, START, END

from app.graph.state import ResearchState

from app.agents.planner import PlannerAgent
from app.agents.search_agent import SearchAgent
from app.agents.verifier import VerificationAgent

from app.retrieval.deduplication import DeduplicationService
from app.agents.synthesizer import SynthesizerAgent


planner = PlannerAgent()
search_agent = SearchAgent()
deduplication_service = DeduplicationService()
verifier = VerificationAgent()
synthesizer = SynthesizerAgent()
def planner_node(state: ResearchState):

    plan = planner.create_plan(
        state["question"]
    )

    return {
        "search_queries": plan.queries
    }

def search_node(state: ResearchState):

    results = search_agent.search_queries(
        state["search_queries"]
    )

    return {
        "search_results": results
    }

def deduplication_node(state: ResearchState):

    unique_results = deduplication_service.remove_duplicates(
        state["search_results"]
    )

    return {
        "unique_results": unique_results
    }

def verification_node(state: ResearchState):

    verification = verifier.verify(
        state["question"],
        state["unique_results"]
    )

    return {
        "verification": verification
    }
def route_after_verification(state: ResearchState):

    verification_text = state["verification"]["verification"]

    if "INSUFFICIENT" in verification_text:
        return "search"

    if "CONFLICTING" in verification_text:
        return "search"

    return "synthesizer"
def synthesizer_node(state: ResearchState):

    final_answer = synthesizer.synthesize(
        state["question"],
        state["unique_results"],
        state["verification"]
    )

    return {
        "final_answer": final_answer
    }
def build_graph():

    graph = StateGraph(ResearchState)

    graph.add_node("planner", planner_node)
    graph.add_node("search", search_node)
    graph.add_node("deduplicate", deduplication_node)
    graph.add_node("verify", verification_node)
    graph.add_node("synthesizer", synthesizer_node)

    graph.add_edge(START, "planner")
    graph.add_edge("planner", "search")
    graph.add_edge("search", "deduplicate")
    graph.add_edge("deduplicate", "verify")
    graph.add_edge("verify", END)

    graph.add_conditional_edges(
        "verify",
        route_after_verification,
        {
            "search": "search",
            "synthesizer": "synthesizer"
        }
    )

    graph.add_edge("synthesizer", END)

    return graph.compile()


research_graph = build_graph()
