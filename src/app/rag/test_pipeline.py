from app.rag.pipeline import retrieve_knowledge

query = "PaymentService is repeatedly failing " "to connect to the database"

result = retrieve_knowledge(
    query=query,
    dense_k=10,
    sparse_k=10,
    rerank_k=8,
    final_k=5,
    relevance_threshold=0.50,
)

print("\n================================")
print("RAG PIPELINE")
print("================================")

print("\nQuery:")
print(result["query"])

print("\nRetrieved Results:")
print("--------------------------------")

for index, item in enumerate(result["results"], start=1):

    print(f"\nResult {index}")

    print("Source:", item["metadata"].get("source"))

    print("Chunk:", item["metadata"].get("chunk_id"))

    print("Relevance:", round(item.get("relevance_score", 0), 3))

    print("Text:", item["text"][:300])

print("\n================================")
print("FINAL CONTEXT")
print("================================")

print(result["context"])

print("\n================================")
print("CITATIONS")
print("================================")

for citation in result["citations"]:
    print(citation)
