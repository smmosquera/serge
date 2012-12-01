"""Implements a class to help with randomized text generation"""


import random
import re

class TextGenerator(object):
    """Generate text from forms
    
    A form gives the possible values for something, for example the
    form for colour might give [red, green, blue].
    
    You can then convert sentences like 'the @colour@ book'
    
    Conversion can be heirarchical like:
        objects are [book, table, @colour@ cat]
        
    Sentence 'the @object@' would give a "book" or a "red cat".
    
    """
    
    def __init__(self):
        """Initialise the generator"""
        self.forms = {}
        
    def addExample(self, name, conversion):
        """Add a new form"""
        try:
            the_form = self.forms[name]
        except KeyError:
            the_form = set()
            self.forms[name] = the_form
        #
        the_form.add(conversion)

    def addExampleFromText(self, text):
        """Add an example from text - the name is ':' separated from the conversion"""
        parts = [i.strip() for i in text.strip().split(':', 1)]
        if len(parts) != 2:
            raise ValueError('Need ":" separated name and then conversion. Got [%s]' % (parts,))
        self.addExample(*parts)
    
    def addExamplesFromText(self, text):
        """Add a number of examples from text"""
        for line in text.splitlines():
            if line.strip() and not line.strip().startswith('#'):
                self.addExampleFromText(line)
    
    def addExamplesFromFile(self, filename):
        """Add multiple examples from a file"""
        text = file(filename, 'r').read()
        self.addExamplesFromText(text)
                
    def getRandomFormCompletion(self, name):
        """Return the comletion of a form randomly"""
        return random.choice(list(self.forms[name]))
        
    def getRandomSentence(self, text, properties=None):
        """Return a random sentence from the text"""
        if properties is None:
            properties = {}
        match = re.match('(.*?)@(.*?)@(.*)', text, re.DOTALL+re.M)
        if match:
            name = match.groups()[1]
            try:
                replacement = properties[name]
            except KeyError:
                replacement = self.getRandomFormCompletion(name)
                if '@' not in replacement:
                    properties[name] = replacement
            #
            return self.getRandomSentence(
                match.groups()[0] + 
                replacement + 
                match.groups()[2], properties)
        else:
            return text
            
            
if __name__ == '__main__':
    t = TextGenerator()
    t.addExample('colour', 'red')
    t.addExample('colour', 'green')
    t.addExample('colour', 'blue')
    t.addExample('object', '@thing@')
    t.addExample('object', 'a @colour@ @thing@')
    t.addExample('object', 'a @colour@ @thing@')    
    t.addExample('thing', 'cat')
    t.addExample('thing', 'dog')
    t.addExample('thing', 'book')
    t.addExample('size', 'small')
    t.addExample('size', 'tiny')
    t.addExample('size', 'large')
    t.addExample('thing', '@size@ @thing@')
    
    for i in range(10):
        print t.getRandomSentence('@object@')

    n = TextGenerator()
    n.addExamplesFromText(
    """
     colour:  red
    colour:  blue
    colour:  green 
    colour:  yellow
    colour:  purple 
    colour:  black 
    colour:  fuscia 
    #
    jewel:   diamond
    jewel:   ruby
    jewel:   emerald
    jewel:   saphire    
    #
    size: small
    size: tiny
    size: large
    size: giant
    #
    time-span: everlasting
    time-span: temporary
    time-span: nighttime
    time-span: daytime
    time-span: lifelong
    time-span: eternal
    #
    effect: wellness
    effect: charm
    effect: charisma
    effect: intellect
    #
    jewel-item:  @colour@ @jewel@
    jewel-item:  @jewel@
    #
    jewel-description: The @size@ @jewel-item@ of @property@
    jewel-description: The @jewel-item@ of @property@
    short-jewel-description: @jewel-item@
    #
    property: @time-span@ @effect@
    property: @effect@
    #
    reason: was @verb@ by @name@ in @time@
    verb: lost
    verb: placed
    verb: discarded
    verb: mislaid
    verb: recorded
    #
    name: @first-name@ @last-name@
    name: @first-name@ @last-name@ @post-name@
    first-name: Bob
    first-name: Fred
    first-name: Jim
    first-name: Bill
    first-name: Marvin
    first-name: Jill
    first-name: Alice
    first-name: Sheila
    first-name: Lemon
    last-name: Smith
    last-name: Jones
    last-name: Crimson
    last-name: Little
    last-name: Jenson
    last-name: Williams
    post-name: Junior
    post-name: Senior
    post-name: I
    post-name: II
    #
    time: 1900's
    time: 1800's
    time: 1950's
    time: 1960's
    time: 1970's
    time: 1980's
    time: 1990's
    #
    description: @jewel-description@ @reason@
    #
    """
    )              
    
    for i in range(20):
        print n.getRandomSentence('@description@')
