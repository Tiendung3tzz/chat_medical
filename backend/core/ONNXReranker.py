from huggingface_hub import hf_hub_download, snapshot_download
import onnxruntime as ort
from transformers import AutoTokenizer
from pathlib import Path
import os
class ONNXReranker:
    def __init__(
            self,
            model_path: str | None = None, 
            repo_id: str = "tiendung3t/bge-m3-reranker",
            filename: str = "bge_m3_rerank.onnx",
            top_k=5
        ):
        if AutoTokenizer is None or ort is None:
            raise ImportError("onnxruntime and transformers are required for ONNXEmbedding")

        self.tokenizer = AutoTokenizer.from_pretrained("BAAI/bge-reranker-v2-m3")
        if model_path is None:
            self.model_path = Path("backend/models") / filename
        else:
            self.model_path = Path(model_path)
        model_dir = self.model_path.parent
        if not self.model_path.exists():
            model_dir.mkdir(parents=True, exist_ok=True)

            snapshot_download(
                repo_id=repo_id,
                local_dir=model_dir,
                local_dir_use_symlinks=False, 
                allow_patterns=["*.onnx", "*.onnx.data"],
            )

        # Kiểm tra external data
        data_file = self.model_path.with_suffix(".onnx.data")
        if not data_file.exists():
            raise RuntimeError(f"Missing ONNX external data file: {data_file}")

        self.session = self._create_session(self.model_path)
        self.top_k = top_k

    def _create_session(self, model_path):
        providers = []
        available = ort.get_available_providers()

        if "CUDAExecutionProvider" in available:
            providers.append("CUDAExecutionProvider")
        else:
            providers.append("CPUExecutionProvider")

        return ort.InferenceSession(model_path, providers=providers)

    def rerank(self,query, document, top_k=None):
        pairs = [(query, doc.metadata['enriched_content']) for doc in document]
        inputs = self.tokenizer(
            pairs,
            padding=True,
            truncation=True,
            return_tensors="np"
        )

        ort_inputs = {k: v.astype("int64") for k, v in inputs.items()}
        outputs = self.session.run(
            [self.session.get_outputs()[0].name],
            ort_inputs
        )[0]

        scores = outputs.squeeze().astype(float)
        if scores.ndim == 0:
            scores = [scores]

        ranked = sorted(enumerate(scores), key=lambda x: x[1], reverse=True)
        retrieval_topks = [document[i[0]] for i in ranked[:self.top_k if top_k is None else top_k]]
        return retrieval_topks