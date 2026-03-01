class HybridRetriever:
    def __init__(self, index_manager, embedding_model, bm25, alpha=0.7):
        self.index = index_manager
        self.embedding_model = embedding_model
        self.bm25 = bm25
        self.alpha = alpha

    def retrieve(self, query, top_k=10):
        dense = self.embedding_model.embed(query)[0]
        sparse = self.bm25.encode_queries([query])[0]

        scaled_dense = [v * self.alpha for v in dense]
        scaled_sparse = {
            "indices": sparse["indices"],
            "values": [v * (1 - self.alpha) for v in sparse["values"]]
        }

        return self.index.query(
            vector=scaled_dense,
            sparse_vector=scaled_sparse,
            top_k=top_k,
            include_metadata=True
        )