from app.graph.workflow import research_graph


if __name__ == "__main__":
    result = research_graph.invoke({
        "question": "What are the major challenges facing India's oil and gas industry?"
    })

    print("\nSEARCH QUERIES:")
    for query in result["search_queries"]:
        print("-", query)

    print("\nRAW RESULTS:")
    print(len(result["search_results"]))

    print("\nUNIQUE RESULTS:")
    print(len(result["unique_results"]))

    print("\nVERIFICATION:")
    print(result["verification"])
