import random
import word_generation
import crossword_generation
from puzzle import Puzzle

def is_valid(word):
    '''Check that each letter is alpha'''
    return all([ord('A') <= ord(c) <= ord('Z') for c in word])

def encode_dictionary_as_set(filename):
    word_set = set([])
    words_by_length = {}
    with open(filename) as file:
        for line in file:
            word = line.rstrip().upper()
            if is_valid(word):
                word_set.add(word)
                word_length = len(word)
                if word_length not in words_by_length:
                    words_by_length[word_length] = []
                words_by_length[word_length].append(word)

    return word_set, words_by_length

if __name__ == '__main__':
    dictionary, words_by_length = encode_dictionary_as_set('small_words.txt')

    while True:
        # Pick a random 7 letter word
        word = random.choice(words_by_length[7]).upper()
        # Debug
        word = "DISEASE"
        word_list = word_generation.generate_word_list(word, dictionary)

        print(word_list)

        crossword = crossword_generation.generate_crossword(word_list)
        puzzle = Puzzle(crossword, word)

        # Main Loop
        while not puzzle.is_solved():
            print(puzzle)
            word = input().upper()
            if not is_valid(word):
                print("Invalid Input! {}".format(word))
            else:
                puzzle.try_word(word)
        print('Solved!')
