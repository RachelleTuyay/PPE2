import stanza
import argparse
import os
from pathlib import Path

def load_model_stanza() :
    stanza_dir = str(Path.home()) + "/stanza_resources/fr/"
    if not os.path.isdir(stanza_dir):
        stanza.download('fr') 
    else :
        return

def analyse_stanza(file) :

    load_model_stanza()

    nlp = stanza.Pipeline('fr', processors='tokenize,mwt,pos,lemma')

    with open(file, 'r', encoding="iso-8859-1") as f:
        texte = f.read()
    
    doc = nlp(texte)
    #forme
    #lemme
    #pos
    for i, sentence in enumerate(doc.sentences):
        print(f'Phrase numéro n°{i}:',*[f'\tid : {word.id}\tforme: {word.text}\tlemme: {word.lemma}\tPOS: {word.pos}' for word in sentence.words], sep='\n')


if __name__ == "__main__" :

    parser = argparse.ArgumentParser(description="Analyseur tokens")
    parser.add_argument("fichier_entree", help="Fichier texte d'entrée")
    args = parser.parse_args()
    file = args.fichier_entree

    analyse_stanza(file)