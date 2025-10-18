from typing import List
import os
import numpy as np
from gensim.models import Word2Vec, FastText, KeyedVectors
from gensim.models.fasttext import load_facebook_vectors


class StaticEmbeddings:
    def __init__(self, vector_size: int = 300, window: int = 5, min_count: int = 2, workers: int = 4):
        self.vector_size = vector_size
        self.window = window
        self.min_count = min_count
        self.workers = workers
        self.w2v_model = None  # Word2Vec or KeyedVectors
        self.ft_model = None   # FastText or KeyedVectors

    def train_word2vec(self, tokenized_texts: List[List[str]]) -> Word2Vec:
        self.w2v_model = Word2Vec(
            sentences=tokenized_texts,
            vector_size=self.vector_size,
            window=self.window,
            min_count=self.min_count,
            workers=self.workers,
            sg=1,
        )
        return self.w2v_model

    def train_fasttext(self, tokenized_texts: List[List[str]]) -> FastText:
        self.ft_model = FastText(
            sentences=tokenized_texts,
            vector_size=self.vector_size,
            window=self.window,
            min_count=self.min_count,
            workers=self.workers,
            sg=1,
        )
        return self.ft_model

    def load_word2vec_kv(self, path: str, binary: bool | None = None) -> KeyedVectors:
        if binary is None:
            binary = path.endswith('.bin') or path.endswith('.bin.gz')
        self.w2v_model = KeyedVectors.load_word2vec_format(path, binary=binary)
        self.vector_size = int(self.w2v_model.vector_size)
        return self.w2v_model

    def load_fasttext_kv(self, path: str) -> KeyedVectors:
        # Loads Facebook fastText .bin/.vec into KeyedVectors
        # gensim 4.x supports load_facebook_vectors for .bin
        if path.endswith('.bin'):
            self.ft_model = load_facebook_vectors(path)
        else:
            # .vec text format
            self.ft_model = KeyedVectors.load_word2vec_format(path, binary=False)
        self.vector_size = int(self.ft_model.vector_size)
        return self.ft_model

    def _get_kv(self, kind: str) -> KeyedVectors:
        model = self.w2v_model if kind == "w2v" else self.ft_model
        if model is None:
            raise ValueError("Embeddings not available for kind=" + kind)
        return model.wv if hasattr(model, 'wv') else model

    def sentence_to_vector(self, tokens: List[str], kind: str = "w2v") -> np.ndarray:
        kv = self._get_kv(kind)
        vectors = []
        for token in tokens:
            if token in kv:
                vectors.append(kv[token])
        if not vectors:
            return np.zeros(self.vector_size, dtype=np.float32)
        return np.mean(vectors, axis=0)

    def tokens_to_sequence_matrix(self, tokens: List[str], max_len: int, kind: str = "w2v") -> np.ndarray:
        kv = self._get_kv(kind)
        seq = np.zeros((max_len, self.vector_size), dtype=np.float32)
        for i, token in enumerate(tokens[:max_len]):
            if token in kv:
                seq[i] = kv[token]
        return seq

    def save_kv(self, out_dir: str, kind: str) -> str:
        os.makedirs(out_dir, exist_ok=True)
        kv = self._get_kv(kind)
        out_path = os.path.join(out_dir, f"{kind}.kv")
        kv.save(out_path)
        return out_path
