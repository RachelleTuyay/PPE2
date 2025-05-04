from bertopic import BERTopic
from sklearn.datasets import fetch_20newsgroups
from sentence_transformers import SentenceTransformer 
from umap import UMAP  # reduce dimension
from hdbscan import HDBSCAN  # clustering
from sklearn.feature_extraction.text import CountVectorizer
from bertopic.vectorizers import ClassTfidfTransformer
from bertopic.representation import KeyBERTInspired
from datastructures import Corpus, Article
import argparse
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
import json

# Load JSON file and prepare data
with open("lefigaro_analyzed.json", "r", encoding="utf-8") as f:
    data = json.load(f)

docs = []
classes = []

for item in data:
    if item.get("title") and item.get("description") and item.get("categories"):
        doc = item["title"] + " " + item["description"]
        docs.append(doc)
        classes.append(item["categories"][0])


# Step 1 - Extract embeddings
embedding_model = SentenceTransformer('sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2')

# Step 2 - Reduce dimensionality
umap_model = UMAP(n_neighbors=15, n_components=5, min_dist=0.0, metric='cosine')

# Step 3 - Cluster reduced embeddings
hdbscan_model = HDBSCAN(min_cluster_size=5, metric='euclidean', cluster_selection_method='eom', prediction_data=True)

# Step 4 - Tokenize topics
french_stopwords = stopwords.words("french")
vectorizer_model = CountVectorizer(stop_words=french_stopwords)

# Step 5 - Create topic representation
ctfidf_model = ClassTfidfTransformer()

# Step 6 - (Optional) Fine-tune topic representations
representation_model = KeyBERTInspired()

# Step 7 - Assemble BERTopic
topic_model = BERTopic(
    language="multilingual",
    embedding_model=embedding_model,
    umap_model=umap_model,
    hdbscan_model=hdbscan_model,
    vectorizer_model=vectorizer_model,
    ctfidf_model=ctfidf_model,
    representation_model=representation_model
)

embeddings = embedding_model.encode(docs, show_progress_bar=True)

# Step 8 - Fit model
topics, probs = topic_model.fit_transform(docs, embeddings=embeddings)

# Step 9 - Visualizations
print(topic_model.get_topic_info()[1:31])

topics_per_class = topic_model.topics_per_class(docs, classes=classes)

fig = topic_model.visualize_topics_per_class(topics_per_class)
fig.write_html("topics_per_class.html")

fig = topic_model.visualize_topics()
fig.write_html("topics.html")

fig = topic_model.visualize_heatmap()
fig.write_html("topics_heatmap.html")

fig = topic_model.visualize_documents(docs, embeddings=embeddings)
fig.write_html("topics_embeddings.html")
