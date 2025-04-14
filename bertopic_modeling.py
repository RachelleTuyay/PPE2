from bertopic import BERTopic
from umap import UMAP
from hdbscan import HDBSCAN
from sentence_transformers import SentenceTransformer
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer
from bertopic.representation import KeyBERTInspired
from bertopic.vectorizers import ClassTfidfTransformer
import json

# Charger le fichier JSON
with open("corpusBFMTV_json.json", "r", encoding="utf-8") as f:
    data = json.load(f)
#notes : rajouter xml et pickle pour la lecture et ouverture du corpus

# Extraire title + description pour chaque article
docs = [f"{item['title']}. {item['description']}" for item in data]
classes = [f"{item['categories']}" for item in data]

# Step 1 - Extract embeddings
embedding_model = SentenceTransformer("sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")

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

# Assemble BERTopic
topic_model = BERTopic(
    language="multilingual",
    embedding_model=embedding_model,
    umap_model=umap_model,
    hdbscan_model=hdbscan_model,
    vectorizer_model=vectorizer_model,
    ctfidf_model=ctfidf_model,
    representation_model=representation_model
)

# Fit the model
#embeddings = embedding_model.encode(docs, show_progress_bar=False)
topics, probs = topic_model.fit_transform(docs)
#topics, probs = topic_model.fit_transform(docs, embeddings) #ligne pour la visualisation des embeddings


#Visualisation :
#print(topic_model.get_topic_info()[1:31]) #Afficher les 30 premiers résultats

#topics en fonction des catégories
topics_per_class = topic_model.topics_per_class(docs, classes=classes)
#fig = topic_model.visualize_topics_per_class(topics_per_class)
#fig.write_html("topics_per_class.html")

#fig = topic_model.visualize_topics()
#fig.write_html("topics.html")

#Affiche dans une map de chaleur
#fig = topic_model.visualize_heatmap()
#fig.write_html("topics_heatmap.html")

#Affiche les embeddings
#fig = topic_model.visualize_documents(docs, embeddings=embeddings)
#fig.write_html("topics_embeddings.html")
