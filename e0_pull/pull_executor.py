from jina import Executor, requests, DocumentArray, Document

import reactome_data_script as reactome


class PullExecutor(Executor):
    @requests(on="/pull")
    def pull_docs(self, **kwargs):
        resp = reactome.get_information_for_term("*")

        out_docs = DocumentArray()
        out_docs.extend([Document(**entry) for entry in resp["Pathway"]["pathologies"]])
        out_docs.extend(
            [Document(**entry) for entry in resp["Pathway"]["nonpathologies"]]
        )
        out_docs.extend(
            [Document(**entry) for entry in resp["Reaction"]["pathologies"]]
        )
        out_docs.extend(
            [Document(**entry) for entry in resp["Reaction"]["nonpathologies"]]
        )
        print(f"Returning {len(out_docs)} pulled docs")
        return out_docs
