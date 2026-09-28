from langgraph.graph import END, START, StateGraph
from app.agents.critic import evidence_critic
from app.agents.evidence import evidence_retriever
from app.agents.evaluation import ragas_evaluation_agent
from app.agents.mcp import mcp_context_agent
from app.agents.performance import performance_agent
from app.agents.rca import rca_agent
from app.agents.rag import rag_agent
from app.agents.reliability import reliability_agent
from app.agents.report import report_generator
from app.agents.security import security_agent
from app.agents.severity import severity_agent
from app.agents.state import AgentState
from app.agents.supervisor import supervisor

def build_graph():
    graph = StateGraph(AgentState)
    graph.add_node("supervisor", supervisor)
    graph.add_node("evidence", evidence_retriever)
    graph.add_node("security", security_agent)
    graph.add_node("reliability", reliability_agent)
    graph.add_node("performance", performance_agent)
    graph.add_node("rag", rag_agent)
    graph.add_node("mcp", mcp_context_agent)
    graph.add_node("rca", rca_agent)
    graph.add_node("critic", evidence_critic)
    graph.add_node("severity", severity_agent)
    graph.add_node("report", report_generator)
    graph.add_node("ragas_evaluation", ragas_evaluation_agent)
    graph.add_edge(START, "supervisor")
    graph.add_edge("supervisor", "evidence")
    graph.add_edge("evidence", "security")
    graph.add_edge("evidence", "reliability")
    graph.add_edge("evidence", "performance")
    graph.add_edge("security", "rag")
    graph.add_edge("reliability", "rag")
    graph.add_edge("performance", "rag")
    graph.add_edge("rag", "mcp")
    graph.add_edge("mcp", "rca")
    graph.add_edge("rca", "critic")
    graph.add_edge("critic", "severity")
    graph.add_edge("severity", "report")
    graph.add_edge("report", "ragas_evaluation")
    graph.add_edge("ragas_evaluation", END)
    return graph.compile()
