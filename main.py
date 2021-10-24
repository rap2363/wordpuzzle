from trie import Trie
import word_generation

def is_valid(word):
    '''Check that each letter is alpha'''
    for c in word:
        if ord(c) > ord('z') or ord(c) < ord('a'):
            return False
    return True

def encode_dictionary_as_trie(filename):
    trie = Trie()
    with open(filename) as file:
        for line in file:
            word = line.rstrip()
            if is_valid(word): 
                trie.encode_word(word)

    return trie

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
    dictionary = encode_dictionary_as_set('words_50k.txt')
    print('Dictionary Encoded!')

    print(word_generation.generate_word_list('raven', dictionary))
