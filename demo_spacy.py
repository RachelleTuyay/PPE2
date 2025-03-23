import spacy

def analyser_texte(texte):
    nlp = spacy.load("fr_core_news_sm")
    doc = nlp(texte)

    print("Analyse du texte :\n")
    for token in doc:
        print(f"Forme : {token.text}\tLemme : {token.lemma_}\tPOS : {token.pos_}")

if __name__ == "__main__":
    exemple = "Les étudiants lisent un livre intéressant à la bibliothèque."
    analyser_texte(exemple)