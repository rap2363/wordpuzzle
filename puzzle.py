import random

# A Puzzle is comprised of a crossword and some state keeping to figure out what words need to be
# inputted for the puzzle to be considered solved.
class Puzzle:
    def __init__(self, crossword, word):
        self.crossword = crossword
        self.solved_words = set([])
        self.letters = [c.upper() for c in word]
        self.shuffle()

    def shuffle(self):
        random.shuffle(self.letters)

    def try_word(self, word):
        if word not in self.crossword.word_map:
            return False

        self.solved_words.add(word)
        return True

    def is_solved(self):
        return len(self.crossword.word_map) == len(self.solved_words)

    def __repr__(self):
        s = self.crossword.repr_with_words(self.solved_words)
        # Display characters
        s += '\n'
        for c in self.letters:
            s += ' {} '.format(c)
        s += '\n'
        return s