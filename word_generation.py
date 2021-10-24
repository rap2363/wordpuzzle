from itertools import permutations

def generate_word_list(word, dictionary, min_word_length=3):    
    word = 'raven'
    print('Generating words from {}'.format(word))
    word_set = set([])
    words_by_length = {}
    max_word_length = len(word) + 1
    for i in range(min_word_length, max_word_length):
        for candidate in permutations(word, i):
            candidate = ''.join(candidate)
            if candidate not in word_set and candidate in dictionary:
                word_set.add(candidate)
                if i not in words_by_length:
                    words_by_length[i] = []
                words_by_length[i].append(candidate)

    # Now generate a word ordering by going backwards from the max_length to the min_length until we use all the words.
    num_words = len(word_set)
    word_set = set([])
    word_list = []
    curr_length = max_word_length
    for i in range(num_words):
        if curr_length == min_word_length:
            curr_length = max_word_length - 1
        else:
            curr_length -= 1
        words = words_by_length[curr_length]
        for w in words:
                if w not in word_set:
                    word_set.add(w)
                    word_list.append(w)
                    break
    return word_list
