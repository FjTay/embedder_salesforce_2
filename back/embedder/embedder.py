from sentence_transformers import SentenceTransformer
from sentence_transformers import util

MODEL_NAME = "all-MiniLM-L6-v2"
_model = None


def _get_model():
    global _model
    if _model is None:
        _model = SentenceTransformer(MODEL_NAME)
    return _model


def embed(text: str):
    return _get_model().encode(text)


def _all_ngram_chunks(query: str, min_ngram: int = 4, max_ngram: int = 8):
    words = query.split()
    n = len(words)
    if n < min_ngram:
        return [query]
    chunks = [query]
    seen = {query}
    for length in range(min_ngram, min(max_ngram, n) + 1):
        for i in range(n - length + 1):
            chunk = " ".join(words[i : i + length])
            if chunk not in seen:
                seen.add(chunk)
                chunks.append(chunk)
    return chunks


def similarity_matrix(query: str, texts: list, split_query_clauses: bool = False):
    model = _get_model()
    texts_emb = model.encode(texts)
    if split_query_clauses:
        chunks = _all_ngram_chunks(query)
        query_embs = model.encode(chunks)
        return util.cos_sim(query_embs, texts_emb)
    query_emb = model.encode(query)
    return util.cos_sim(query_emb, texts_emb)


def match_objects(query: str, object_names: list, top_k: int = 5, embedding_texts: list = None, boost_objects: set = None, boost_factor: float = 1.5, split_query_clauses: bool = False):
    model = _get_model()
    to_embed = embedding_texts if embedding_texts else object_names
    objects_emb = model.encode(to_embed)
    if split_query_clauses:
        chunks = _all_ngram_chunks(query)
        query_embs = model.encode(chunks)
        sim_matrix = util.cos_sim(query_embs, objects_emb)
        scores = sim_matrix.max(dim=0)[0]
    else:
        query_emb = model.encode(query)
        scores = util.cos_sim(query_emb, objects_emb)[0]
    if boost_objects:
        boost_lower = {o.lower() for o in boost_objects}
        for i, name in enumerate(object_names):
            if name.lower() in boost_lower:
                scores[i] = scores[i] * boost_factor
    sorted_indices = scores.argsort(descending=True)
    top_indices = sorted_indices[:top_k]
    return [object_names[i] for i in top_indices]
