import re

from jina import Executor, requests, DocumentArray


def clean_doc(doc):
    doc.text = re.sub(r"<.+?>", "", doc.tags["summation"])


class CleanupExecutor(Executor):
    @requests(on="/index")
    def clean_docs(self, docs: DocumentArray, **kwargs):
        for doc in docs:
            clean_doc(doc)
        print("Cleaned docs")
