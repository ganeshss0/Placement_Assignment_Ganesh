##############################
###### Python Answer 10 ######
##############################

# A program to count the number of verbs, nouns, pronouns and adjectives in a given 
# sentense or paragraph and return respective count as dictionary.





##############################
########## Solution ##########
##############################

# importing nltk library for tokenizing and tagging the sentense

from nltk import word_tokenize, pos_tag



def count_grammer(sentence: str) -> dict:
    '''Return a dictionary contains number of nouns, pronouns, verbs and adjective in sentense.'''

    # default return dictionary
    Dict = {'nouns':0, 'pronouns':0, 'verbs':0, 'adjectives':0}
    # tokenizing the sentence
    tokens = word_tokenize(sentence)
    # tagging the tokenized words
    tagged_words = [tag[1] for tag in pos_tag(tokens)]

    tags = {
        'nouns': ['NN', 'NNS', 'NNP', 'NNPS'],
        'verbs': ['VB', 'VBD', 'VBG', 'VBN' 'VBP' 'VBZ'],
        'adjectives': ['JJ', 'JJS', 'JJR'],
        'pronouns': ['PRP', 'PRP$']
    }
    # tag counting function
    counter = lambda x: tagged_words.count(x)
    for tag in Dict:
        Dict[tag] = sum(map(counter, tags[tag]))

    return Dict

#########################
##### TESTING ###########
#########################

if __name__ == "__main__":
    sentences = (
        'Today is very nice weather, it sunny outside. Yesterday was raining.',
        'You have to write at least two additional cases.',
        'The quick brown fox jumps over the lazy dog.')
    
    for sentence in sentences:
        print('\nINPUT:', sentence)
        print('OUTPUT:', count_grammer(sentence))
    
