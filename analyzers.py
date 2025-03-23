import stanza
from datastructures import Article,Corpus,Token, load_json, load_pickle, load_xml, AnalyzedArticle, save_json, save_pickle, save_xml
from pathlib import Path
import os
import argparse


def load_model_stanza() :
    stanza_dir = str(Path.home()) + "/stanza_resources/fr/"
    if not os.path.isdir(stanza_dir):
        stanza.download('fr') 
    else :
        return
    

def analyse_stanza(article:Article) -> AnalyzedArticle :
    
    load_model_stanza()
    nlp = stanza.Pipeline('fr', processors='tokenize,mwt,pos,lemma', verbose=False)


    def extraction_tokens(text:str):

        doc = nlp(text)

        tokens = []
        for sentence in doc.sentences : 
            for word in sentence.words :
                tokens.append(Token(word.text, word.lemma, word.pos))
        return tokens

    tokens_description = extraction_tokens(article.description)
    return AnalyzedArticle(article, tokens_description)
        


def main():
    parser = argparse.ArgumentParser(description="Analyseur tokens")
    parser.add_argument("fichier_entree", help="Fichier d'entrée correspondant au corpus d'articles filtrés")
    parser.add_argument("format", choices=["json","pickle","xml"], help="format du fichier d'entrée")
    parser.add_argument("analyzer", choices=["stanza","spacy","trankit"], help="choix de l'analyzer syntaxique à utiliser")
    parser.add_argument("save", choices=["json","xml","pickle"], help="format de sauvegarde pour la sortie de l'analyse")
    args = parser.parse_args()
    file = args.fichier_entree


    if args.format == "json" :
        corpus_article = load_json(Corpus, file)
    if args.format == "xml" :
        corpus_article = load_xml(file)
    if args.format == "pickle":
        corpus_article = load_pickle(file)
    if args.analyzer == "stanza" :
        articles_analyzed = []
        for article in corpus_article.articles :
            articles_analyzed.append(analyse_stanza(article))

            '''with open("output_analyse.txt", "a") as output :
                output.write(f"Titre : {res_analyse[0]}\nTokens : {res_analyse[1]}\n\n")'''
    corpus_analyse = Corpus(articles_analyzed)
    if args.save == "json" :
        corpus_article = save_json(corpus_analyse, "output_analyse.json")
    if args.save == "xml" :
        corpus_article = save_xml(corpus_analyse, "output_analyse.xml")
    if args.save == "pickle":
        corpus_article = save_pickle(corpus_analyse, "output_analyse.pickle")



if __name__ == "__main__" :
    main()

