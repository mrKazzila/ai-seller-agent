from collections.abc import Sequence

import numpy as np
from scipy.sparse import csr_matrix
from sklearn.feature_extraction.text import TfidfVectorizer


class ProductSearchIndex:
    def __init__(self, documents: Sequence[str]) -> None:
        self._vectorizer = TfidfVectorizer(
            analyzer="char_wb",
            ngram_range=(2, 5),
            lowercase=False,
        )
        self._matrix: csr_matrix = self._vectorizer.fit_transform(
            documents,
        )

    def search(self, query: str) -> np.ndarray:
        query_vector = self._vectorizer.transform([query])
        scores = query_vector @ self._matrix.T

        return scores.toarray()[0]
