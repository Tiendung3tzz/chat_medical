class HybridRetriever:
    def __init__(self, index_manager, embedding_model, bm25, candidate = 20, alpha=0.7):
        self.index_manager = index_manager
        self.embedding_model = embedding_model
        self.bm25 = bm25
        self.candidate = candidate
        self.alpha = alpha


    def retrieve(self, query, top_k=None):
        dense = self.embedding_model.embed(query)[0]
        sparse = self.bm25.encode(query)[0]

        scaled_dense = [v * self.alpha for v in dense]
        scaled_sparse = {
            "indices": sparse["indices"],
            "values": [v * (1 - self.alpha) for v in sparse["values"]]
        }

        return self.index_manager.query(
            vector=scaled_dense,
            sparse_vector=scaled_sparse,
            top_k=self.candidate if top_k is None else top_k,
            include_metadata=True
        )