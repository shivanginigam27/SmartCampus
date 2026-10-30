from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def recommend_events(interests, events, top_n=5):
    if not events:
        return []

    documents = [interests] + [
        f"{e['category']} {e['title']} {e['description']}"
        for e in events
    ]

    vectorizer = TfidfVectorizer(stop_words="english")
    matrix = vectorizer.fit_transform(documents)
    scores = cosine_similarity(matrix[0:1], matrix[1:]).flatten()

    ranked = sorted(
        zip(events, scores),
        key=lambda x: x[1],
        reverse=True
    )

    return [
        {**event, "score": round(float(score), 3)}
        for event, score in ranked[:top_n]
    ]
