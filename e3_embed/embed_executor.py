from jina import Executor, requests, DocumentArray
from sentence_transformers import SentenceTransformer
import torch


def data_loader(docs, batch_size=10):
    for i in range(0, len(docs), batch_size):
        yield docs[i : i + batch_size]


class EmbedExecutor(Executor):
    def __init__(self, device: str = "cpu", **kwargs):
        super().__init__(**kwargs)
        self.device = device
        self.model = SentenceTransformer(
            "pritamdeka/S-Biomed-Roberta-snli-multinli-stsb"
        )
        self.model.eval()
        self.model.to(self.device)

    @requests(on="/search")
    def embed_query(self, docs: DocumentArray, **kwargs):
        with torch.inference_mode():
            docs.embeddings = self.model.encode(docs.texts)

    @requests(on="/index")
    def embed_docs(self, docs: DocumentArray, **kwargs):
        if self.device == "cpu":
            # Embed each chunk individually
            with torch.inference_mode():
                for doc in docs:
                    for chunk in doc.chunks:
                        chunk.embedding = self.model.encode(chunk.text)
        else:
            # Sort chunks by length to process in batches
            all_chunks = docs["@c"]
            all_chunks.sort(
                key=lambda chunk: len(chunk.text)
            )  # proxy for sequence length
            with torch.inference_mode():
                for batch in data_loader(all_chunks):
                    batch.embeddings = self.model.encode(batch.texts)
        print("Embedded docs")
