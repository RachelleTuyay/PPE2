from trankit import Pipeline

p = Pipeline('english', gpu=False)
p.add('chinese')
p.add('french')

#doc = '''Before using any function of Trankit, we need to initialize a pipeline. Here is how we can do it for English.'''
doc = '''bouge pas, reste-là! 看看tankit这个outil能不能进行mixed分词'''
all = p(doc)

for sentence in all['sentences']:
	for token in sentence['tokens']:
		print(f"form: {token['text']}\tlemma: {token['lemma']}\tpos: {token['upos']}")