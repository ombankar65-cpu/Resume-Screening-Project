from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def get_ats_score(resume, jd):

    tfidf = TfidfVectorizer()

    data = [resume, jd]

    vectors = tfidf.fit_transform(data)

    score = cosine_similarity(vectors[0], vectors[1])

    final_score = score[0][0] * 100

    return round(final_score, 2)
