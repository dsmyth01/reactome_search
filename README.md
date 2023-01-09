# reactome_search

### Install Requirements
`pip3 install -r requirements.txt`

### Ensure SQLite Db in Root Directory
Sqlite db `reactome` contains searchable documents.

### Run Index/Query App

`python3 app.py --index_docs=0 --query="[Your Query Here]"`

Usage:
- `index_docs` is used only for indexing new documents into the search database. Set to a number greater than 0 to index that number of documents.
- `query` a query string to find closest matches in the document database.

### Models
- Sentence tokenization using `nltk`'s `punkt` tokenizer.
- Embeddings generated using `pritamdeka/S-Biomed-Roberta-snli-multinli-stsb`. See https://huggingface.co/pritamdeka/S-Biomed-Roberta-snli-multinli-stsb for more documentation.