from jina import Executor, requests, DocumentArray


class SearchExecutor(Executor):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._docs = DocumentArray(
            storage="sqlite",
            config={"connection": "reactome", "table_name": "documents"},
        )

    @requests(on="/index")
    def index_docs(self, docs: DocumentArray, **kwargs):
        self._docs.extend(docs)

    @requests(on="/search")
    def search_chunks(self, docs: DocumentArray, **kwargs):
        docs.match(
            self._docs["@c"],
            metric="cosine",
            limit=10,
        )
        for doc in docs[0].matches:
            doc.tags["full_text"] = self._docs[doc.parent_id].text

        return docs[0].matches
