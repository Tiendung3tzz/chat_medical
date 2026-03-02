from pinecone import Pinecone, ServerlessSpec
from typing import Dict, List, Optional

class PineconeIndexManager:
    def __init__(self, api_key, index_name, environment: Optional[str] = None, dimension=1024, metric="dotproduct"):
        self.api_key = api_key
        self.index_name = index_name
        self.environment = environment
        self.dimension = dimension
        self.metric = metric

        self.pc = Pinecone(api_key=self.api_key)
        self._init_index()

    def _init_index(self):
        if not self.pc.has_index(self.index_name):
            self.pc.create_index(
                name=self.index_name,
                dimension=self.dimension,
                metric=self.metric,
                spec=ServerlessSpec(
                    cloud="aws",
                    region=self.environment or "us-east-1"
                )
            )
        self.index = self.pc.Index(self.index_name)

    def query(self, **kwargs):
        return self.index.query(**kwargs)