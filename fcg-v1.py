

class Construction(object):
    pass


class Cat(Construction):
    def produce(cat):
        cat.meaning.animal_type='CAT'
    def comprehend(cat):
        cat.form = 'cat'
    def contribute(cat):
        cat.referent = cat.meaning.object
        cat.sem_category = 'ANIMATE'
        cat.lex_category = 'NOUN'
        cat.number = 'SINGULAR'

class The(Construction):
    def produce(the):
        the.meaning.definite='TRUE'
    def comprehend(the):
        the.form = 'the'
    def contribute(the):
        the.referent = the.meaning.object
        the.lex_category = 'ARTICLE'

class NounPhrase(Construction):
    def produce(article, noun):
        article.referent = noun.referent
    def comprehend(article, noun):
        article.lex_category = 'ARTICLE'
        noun.lex_category = 'NOUN'
        article.left_of = noun
        noun.right_of = article
    def contribute(article, noun, phrase)
        article.number = noun.number
        noun.syn_func.head = noun_phrase
        article.syn_func.determiner = noun
        phrase.referent = noun.referent
        phrase.category = 'NP'
        phrase.constituents = [article, noun]
        phrase.agreement = noun.number

world = World()
s1 = world.make_structure()
s1.meaning.animal_type = 'CAT'
s1.referent = 'obj-1'
s2 = world.make_object()
s2.meaning.definite = 'TRUE'
s2.referent = 'obj-1'


