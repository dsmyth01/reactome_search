from jina import Flow, Document


def run(num_docs_to_index, query_string):
    f = (
        Flow(restful=True)
        .add(name="e0_pull", uses="e0_pull/config.yml")
        .add(name="e1_cleanup", uses="e1_cleanup/config.yml")
        .add(name="e2_split", uses="e2_split/config.yml")
        .add(
            name="e3_embed",
            uses="e3_embed/config.yml",
            replicas=5,
            uses_with={"device": "cpu"},
        )
        .add(name="e4_search", uses="e4_search/config.yml")
    )

    f.save_config("flow.yml")

    with f:
        if num_docs_to_index > 0:
            all_docs = f.post(on="/pull", inputs=[])
            all_docs = all_docs[:num_docs_to_index]
            print(all_docs.summary())

            indexed_docs = f.post(on="/index", inputs=all_docs, request_size=10)
            print(indexed_docs.summary())

        results = f.post("/search", [Document(text=query_string)])

        return results


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser("reactome_app")
    parser.add_argument("--index_docs", help="Whether to perform index.", type=int)
    parser.add_argument("--query", help="Query String", type=str)
    args = parser.parse_args()

    results = run(args.index_docs, args.query)
    print("=" * 100)
    print(f"Query: '{args.query}'")
    print("=" * 100)
    print("Results")
    print("=" * 100)
    for result in results:
        print(f"Parent Doc: {result.parent_id}")
        print(f"Score: {result.scores['cosine'].value}")
        print(f"Text: {result.text}")
        print("\n")
