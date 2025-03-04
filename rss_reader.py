import re

def rss_reader_re(chemin_fichier):
    with open(chemin_fichier, 'r', encoding='utf-8') as fichier:
        contenu = fichier.read()
    
    metadonnees = []
    pattern = re.compile(
        r'<item>.*?<id>(.*?)</id>.*?<source>(.*?)</source>.*?<title>(.*?)</title>.*?<description>(.*?)</description>.*?<date>(.*?)</date>.*?<category>(.*?)</category>',
        re.DOTALL
    )
    
    for match in pattern.finditer(contenu):
        id, source, titre, description, date, category = match.groups()
        metadonnees.append({
            'id': id,
            'source': source,
            'title': titre,
            'content': description,
            'date': date,
            'category': category
        })
    
    return metadonnees