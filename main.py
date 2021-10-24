from trie import Trie
import word_generation
import crossword_generation

def is_valid(word):
    '''Check that each letter is alpha'''
    return all([ord('a') <= ord(c) <= ord('z') for c in word])

def encode_dictionary_as_set(filename):
    word_set = set([])
    with open(filename) as file:
        for line in file:
            word = line.rstrip()
            if is_valid(word):
                word_set.add(word)

    return word_set

if __name__ == '__main__':
    print('Encoding Dictionary')
    dictionary = encode_dictionary_as_set('small_words.txt')
    print('Dictionary Encoded!')

    word_list = word_generation.generate_word_list('hospital', dictionary)

    print(word_list)

    crossword = crossword_generation.generate_crossword(word_list)
    print(crossword)
