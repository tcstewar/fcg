import fcg

class Cat(fcg.Construction):
    def produce(cat):
        cat.meaning.animal_type='CAT'
    def comprehend(cat):
        cat.form = 'cat'
    def contribute(cat):
        cat.referent = cat.meaning.object
        cat.sem_category = 'ANIMATE'
        cat.lex_category = 'NOUN'
        cat.number = 'SINGULAR'

class The(fcg.Construction):
    def produce(the):
        the.meaning.definite='TRUE'
    def comprehend(the):
        the.form = 'the'
    def contribute(the):
        the.referent = the.meaning.object
        the.lex_category = 'ARTICLE'

class NounPhrase(fcg.Construction):
    def produce(article, noun):
        article.referent = noun.referent
        article.lex_category = 'ARTICLE'
        noun.lex_category = 'NOUN'
    def comprehend(article, noun):
        article.lex_category = 'ARTICLE'
        noun.lex_category = 'NOUN'
        article.left_of = noun
        noun.right_of = article
    def contribute(article, noun, phrase):
        article.number = noun.number
        noun.syn_func.head = phrase
        article.syn_func.determiner = noun
        phrase.referent = noun.referent
        phrase.category = 'NP'
        phrase.constituents = [article, noun]
        phrase.agreement = noun.number

world = fcg.FCG()
s1 = world.make_structure()
s1.meaning.animal_type = 'CAT'
s1.meaning.object = 'obj-1'
s2 = world.make_structure()
s2.meaning.definite = 'TRUE'
s2.meaning.object = 'obj-1'

world.add_construction(Cat)
world.add_construction(The)
world.add_construction(NounPhrase)

world.display()
world.step('produce')
world.display()
world.step('produce')
world.display()
world.step('produce')
world.display()




world = fcg.FCG()
s1 = world.make_structure()
s1.form = 'the'
s2 = world.make_structure()
s2.form = 'cat'
s1.left_of = s2
s2.right_of = s1

world.add_construction(Cat)
world.add_construction(The)
world.add_construction(NounPhrase)

world.display()
world.step('comprehend')
world.display()
world.step('comprehend')
world.display()
world.step('comprehend')
world.display()

