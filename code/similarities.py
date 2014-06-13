from numpy import sqrt, concatenate
import networkx as nx
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from collections import Counter

stemmer = PorterStemmer()


def remove_stopwords(v):
    """
    Given a vector of words, removes stopwords from the English language, and returns the remaining words.
    """
    return [i for i in v if i not in stopwords.words('english')]


def stem(v):
    """
    Given a vector of words, removes stopwords, does stemming and returns the remaining words.
    """
    return [stemmer.stem(i) for i in remove_stopwords(v)]


def get_similarity(v1, v2):
    """
    Computes the similarity between the two given vectors of words.
    """
    v1 = set(v1)
    v2 = set(v2)
    return len(v1.intersection(v2)) / (sqrt(len(v1) * len(v2)))


def build_graph(data, similarity_threshold=0.3):
    """
    doc
    """
    vectors = {}
    for d in data:
        vectors[d['id']] = stem(d['tags'])

    g = nx.Graph()
    ids = vectors.keys()
    for i in xrange(len(ids)):
        for j in xrange(i, len(ids)):
            similarity = get_similarity(vectors[ids[i]], vectors[ids[j]])
            if similarity >= similarity_threshold:
                g.add_edge(ids[i], ids[j], {'weight': similarity})

    return g

def rank_relevance(g):
    """
    doc
    """
    pageranks = nx.pagerank(g, weight='weight')
    pageranks = sorted(pageranks.items(), key=lambda x: x[1], reverse=True)
    return [id for id, val in pageranks]


def select_tags(data, id):
    """
    data is a dictionary of id: tags format, and id is the id of the entity the user selected.
    """
    print data.values()
    if len(data.values()) > 1:
        values = concatenate(data.values())
    else:
        values = data.values()[0]

    tag_counter = Counter(values)
    theme_tags = [t[0] for t in tag_counter.most_common(2)]

    picked_tags = data[id]
    data.pop(id)
    if len(data.values()) > 1:
        values = concatenate(data.values())
    else:
        values = data.values()[0]
    picked_tags = set(picked_tags) - set(values)

    if picked_tags:
        theme_tags.extend(picked_tags)
    return theme_tags
