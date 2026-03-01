import onnxruntime as ort
from transformers import AutoTokenizer
from pathlib import Path
import os
class ONNXReranker:
    def __init__(self, model_path: str | None = None):
        if AutoTokenizer is None or ort is None:
            raise ImportError("onnxruntime and transformers are required for ONNXEmbedding")

        self.tokenizer = AutoTokenizer.from_pretrained("BAAI/bge-reranker-v2-m3")
        if model_path is None:
            BASE_DIR = Path(__file__).resolve().parents[2]  # project/
            model_path = BASE_DIR / "models" 
        model_file = Path(model_path) / "bge_m3_rerank.onnx"
        
        if not os.path.exists(model_file):
            raise FileNotFoundError(f"bge_m3_rerank.onnx not found in {model_path}")
        self.session = self._create_session(model_file)

    def _create_session(self, model_path):
        providers = []
        available = ort.get_available_providers()

        if "CUDAExecutionProvider" in available:
            providers.append("CUDAExecutionProvider")
        else:
            providers.append("CPUExecutionProvider")

        return ort.InferenceSession(model_path, providers=providers)

    def rerank(self, pairs):
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

        return sorted(
            enumerate(scores),
            key=lambda x: x[1],
            reverse=True
        )