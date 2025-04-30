from bertopic import BERTopic

from sklearn.datasets import fetch_20newsgroups

from datastructures import Corpus, Article
import argparse

from sentence_transformers import SentenceTransformer
from umap import UMAP
from hdbscan import HDBSCAN
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer
from bertopic.vectorizers import ClassTfidfTransformer
from bertopic.representation import KeyBERTInspired

#import spacy

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


def main():

    parser = argparse.ArgumentParser(description="Topic modeling")
    parser.add_argument("file", help="Chemin du fichier/dossier contenant le corpus")
    parser.add_argument("format", choices=["json", "xml", "pickle"], help="Format du corpus")
    args = parser.parse_args()

    if args.format == "json" :
        docs = Corpus.load_json(args.file)
    if args.format == "xml" :
        docs = Corpus.load_xml(args.file)
    if args.format == "pickle":
        docs = Corpus.load_pickle(args.file)

    docs = [article for article in docs.articles if article.description != None]

    classes = [article.categories for article in docs if article.description != None]
    
    docs = [article.description for article in docs if article.description != None]

    classes_flat = [categorie for categories in classes for categorie in categories]

   
    #nlp = spacy.load("fr_core_news_md", exclude=['tagger', 'parser', 'ner','attribute_ruler', 'lemmatizer'])

    topic_model = BERTopic(
        language='multilingual',
        embedding_model=embedding_model,
        vectorizer_model=vectorizer_model,
        umap_model=umap_model,
        hdbscan_model=hdbscan_model,
        ctfidf_model=ctfidf_model,
        representation_model=representation_model
        )
    

    embeddings = embedding_model.encode(docs, show_progress_bar=True)
    topics, probs = topic_model.fit_transform(docs, embeddings)
    topic_model.update_topics(docs, vectorizer_model=vectorizer_model)

    print(topic_model.get_topic_info())
    #print(topic_model.get_topic(0))
    print(topic_model.get_document_info(docs))

    topics_per_class = topic_model.topics_per_class(docs, classes=classes_flat)
    topic_model.visualize_topics_per_class(topics_per_class, top_n_topics=10)

    hierarchical_topics = topic_model.hierarchical_topics(docs)
    fig = topic_model.visualize_hierarchy(hierarchical_topics=hierarchical_topics)
    fig.write_html("hierarchical_topics.html")

    fig = topic_model.visualize_topics_per_class(topics_per_class)
    fig.write_html("topics_per_class.html")

    fig = topic_model.visualize_topics()
    fig.write_html("topics.html")

    #Affiche dans une map de chaleur
    fig = topic_model.visualize_heatmap()
    fig.write_html("topics_heatmap.html")

    #Affiche les embeddings
    fig = topic_model.visualize_documents(docs, embeddings=embeddings)
    fig.write_html("topics_embeddings.html")


if __name__ == "__main__" :

    main()