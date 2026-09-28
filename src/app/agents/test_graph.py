from app.agents.graph import build_graph

graph = build_graph()
test_state = {
    "candidates": [
        {
            "type": "repeated_error",
            "message": "Database connection failed",
            "count": 37,
        },
        {
            "type": "potential_security_issue",
            "event_id": "EVT-000021",
            "message": "Authorization: Bearer [REDACTED]",
            "detected_sensitive_data": ["bearer_token"],
        },
    ]
}

result = graph.invoke(test_state)

print("\nFINAL RESULT\n")
print(result)
