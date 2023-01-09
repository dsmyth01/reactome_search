from jina import Executor, requests, DocumentArray, Document
import nltk


def load_tokenizer():
    tokenizer_path = "tokenizers/punkt/english.pickle"
    if not nltk.data.find(tokenizer_path):
        nltk.download("punkt")
    return nltk.data.load(tokenizer_path)


class SplitExecutor(Executor):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.sent_detector = load_tokenizer()

    def chunkify(self, doc):
        doc.chunks = DocumentArray(
            [
                Document(
                    id=f"{doc.id}-{i}",
                    text=doc.text[start_pos:end_pos],
                    start_pos=start_pos,
                    end_pos=end_pos,
                )
                for (i, (start_pos, end_pos)) in enumerate(
                    self.sent_detector.span_tokenize(doc.text)
                )
            ]
        )

    @requests(on="/index")
    def split_docs(self, docs: DocumentArray, **kwargs):
        for doc in docs:
            self.chunkify(doc)
        print("Chunkified docs")
