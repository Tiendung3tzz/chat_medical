from copyreg import pickle

import numpy as np
import onnxruntime as ort
import os
from pathlib import Path

try:
    import onnxruntime as ort
    from transformers import AutoTokenizer
except Exception:  # pragma: no cover - optional dependency
    ort = None
    AutoTokenizer = None

from pathlib import Path
import pickle


class BM25Encoder:
    def __init__(self, model_path: str | Path):
        if model_path is None:
            BASE_DIR = Path(__file__).resolve().parents[2]  # project/
            model_path = BASE_DIR / "models" 
        
        self.model_path = Path(model_path) / "bm25_encoder.pkl"
        self.model = self._load()

    def _load(self):
        if not self.model_path.exists():
            raise FileNotFoundError(f"BM25 model not found: {self.model_path}")

        with open(self.model_path, "rb") as f:
            return pickle.load(f)

    def encode(self, text: str):
        return self.model.encode_queries([text])

class ONNXEmbeddingModel:
    def __init__(self, model_path: str | None = None):
        if AutoTokenizer is None or ort is None:
            raise ImportError("onnxruntime and transformers are required for ONNXEmbedding")

        self.tokenizer = AutoTokenizer.from_pretrained("BAAI/bge-m3")
        if model_path is None:
            BASE_DIR = Path(__file__).resolve().parents[2]  # project/
            model_path = BASE_DIR / "models" 
        model_file = Path(model_path) / "bge_m3.onnx"
        
        if not os.path.exists(model_file):
            raise FileNotFoundError(f"bge_m3.onnx not found in {model_path}")

        self.session = self._create_session(model_file)

    def _create_session(self, model_path):
        providers = []
        available = ort.get_available_providers()

        if "CUDAExecutionProvider" in available:
            providers.append("CUDAExecutionProvider")
            print("Using GPU (CUDA)")
        else:
            providers.append("CPUExecutionProvider")
            print("Using CPU")

        return ort.InferenceSession(model_path, providers=providers)

    @staticmethod
    def mean_pooling(token_embeddings, attention_mask):
        mask = attention_mask[..., None]
        summed = (token_embeddings * mask).sum(axis=1)
        counts = mask.sum(axis=1)
        return summed / np.clip(counts, 1e-9, None)

    def embed(self, text):
        inputs = self.tokenizer(
            text,
            padding=True,
            truncation=True,
            return_tensors="np"
        )

        ort_inputs = {
            "input_ids": inputs["input_ids"].astype(np.int64),
            "attention_mask": inputs["attention_mask"].astype(np.int64),
        }

        output_name = self.session.get_outputs()[0].name
        outputs = self.session.run([output_name], ort_inputs)

        sentence_embeddings = self.mean_pooling(
            outputs[0],
            inputs["attention_mask"]
        )

        norms = np.linalg.norm(sentence_embeddings, axis=1, keepdims=True)
        return (sentence_embeddings / norms).tolist()