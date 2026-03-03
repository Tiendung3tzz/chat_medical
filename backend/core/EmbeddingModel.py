from copyreg import pickle

import numpy as np
import onnxruntime as ort
import os
from pathlib import Path
from huggingface_hub import hf_hub_download, snapshot_download

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
        BASE_DIR = Path(__file__).resolve().parents[2]  # project/
        if model_path is None:
            model_path = BASE_DIR/"backend"/"models"
            model_file = Path(model_path) / "bm25_encoder.pkl"
        else:
            model_file = BASE_DIR / Path(model_path)
        
        self.model_path = model_file
        self.model = self._load()

    def _load(self):
        if not self.model_path.exists():
            raise FileNotFoundError(f"BM25 model not found: {self.model_path}")

        with open(self.model_path, "rb") as f:
            return pickle.load(f)

    def encode(self, text: str):
        return self.model.encode_queries([text])

class ONNXEmbeddingModel:
    def __init__(
            self, 
            model_path: str | None = None,  
            repo_id: str = "tiendung3t/bge-m3-onnx",
            filename: str = "bge_m3.onnx"
        ):
        if AutoTokenizer is None or ort is None:
            raise ImportError("onnxruntime and transformers are required for ONNXEmbedding")

        self.tokenizer = AutoTokenizer.from_pretrained("BAAI/bge-m3")
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