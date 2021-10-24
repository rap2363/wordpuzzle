from collections import namedtuple

# A crossword is built up incrementally, where words are added in an alternating pattern of
# horizontal and vertical ways. We try to place the word according to a convolution score, which 
# prioritizes placing the words within the bounds of the existing puzzle as well as reusing letters. 
class Crossword:
    def __init__(self):
        self.min_x = 0
        self.max_x = 0
        self.min_y = 0
        self.max_y = 0
        self.horizontal_words = []
        self.vertical_words = []
        self.horizontal = True
        # Indexed by (x,y) tuples.
        self.grid = {}
        self.word_map = {}

    def place_horizontal(self, word, x, y):
        self.word_map[word] = (x,y)
        print('horizon')
        print(self.word_map[word])
        for c in word:
            self.grid[(x, y)] = (c, True)
            self.min_x = min(self.min_x, x)
            self.max_x = max(self.max_x, x)
            x += 1
        print("x: ", self.min_x, self.max_x)
        self.horizontal_words.append(word)

    def place_vertical(self, word, x, y):
        self.word_map[word] = (x,y)
        print(self.word_map[word])
        for c in word:
            self.grid[(x, y)] = (c, False)
            self.min_y = min(self.min_y, y)
            self.max_y = max(self.max_y, y)
            y += 1
        print("y: ", self.min_y, self.max_y)
        self.vertical_words.append(word)

    def get_word_indexes(self, word, horizontal):
        x,y = self.word_map[word]
        print('Word Indexes: {}, {},{}'.format(word, x, y))
        for _ in range(len(word)):
            yield x,y
            if horizontal:
                x += 1
            else:
                y += 1

    def inside_bounds(self, x, y):
        return self.min_x <= x <= self.max_x and self.min_y <= y <= self.max_y

    def calculate_convolution_score(self, word, shift, start_x, start_y, horizontal):
        '''The convolution is calculated based on:
        1. Each character that occupies a space outside of the current bounds gets a penalty of -1.
        2. Each character that is inside the bounds recieves a penalty of 0.
        3. A character that is shared with the letter of another word is given a bonus of +2.
        4. If characters do not match with an existing word or letter we immediately return -inf.
        '''
        x = start_x
        y = start_y
        if horizontal:
            x -= shift
        else:
            y -= shift
        print('CALC CONV SCORE FOR {} at {},{},{}'.format(word, x, y, horizontal))
        score = 0
        for i,c in enumerate(word):
            score += -1 if not self.inside_bounds(x, y) else 0
            if (x,y) in self.grid and self.grid[(x,y)][0] != c:
                print("DIFF CHAR {},{},{},{}".format(x, y, self.grid[(x,y)][0], c))
                return float('-inf')
            if (x,y) in self.grid and self.grid[(x,y)] == (c,horizontal):
                # Character must be in a different direction.
                print("SAME DIR {},{},{},{}".format(x, y, horizontal, c))
                return float('-inf')
            letter_matches = (x,y) in self.grid and self.grid[(x,y)][0] == c

            if letter_matches:
                score += 2
            else:
                # Check that no words exist on the sides if the letter doesn't match.
                if horizontal or i == 0 or i == len(word) - 1:
                    # Check up and down.
                    if (x, y - 1) in self.grid or (x, y + 1) in self.grid:
                        print("UP AND DOWN {},{},{}".format(x, y, c))
                        return float('-inf')
                if not horizontal or i == 0 or i == len(word) - 1:
                    # Check left and right
                    if (x + 1, y) in self.grid or (x - 1, y) in self.grid:
                        print("LEFT AND RIGHT {},{},{}".format(x, y, c))
                        return float('-inf')

            if horizontal:
                x += 1
            else:
                y += 1
        return score

    def add_word(self, word):
        self.horizontal = not self.horizontal
        if len(self.grid) == 0:
            # First word, place it into the grid at the origin horizontally.
            self.place_horizontal(word, x=0, y=0)
            print(self)
            return

        # Otherwise, we loop through our existing set of words to figure out where we can place the
        # new one.
        best_score = float('-inf')
        Placement = namedtuple('Placement', ['x', 'y', 'i'])
        best_placement = None
        for anchor in self.vertical_words if self.horizontal else self.horizontal_words:
            for x,y in self.get_word_indexes(anchor, horizontal=not self.horizontal):
                print('ANCHOR:{} -{},{}'.format(anchor, x, y))
                for i,c in enumerate(word):
                    score = self.calculate_convolution_score(word, shift=i, start_x=x, start_y=y, horizontal=self.horizontal)
                    print('score: {} and placement ({}, {}, {}, {})'.format(score, x, y, i, self.horizontal))
                    if score > best_score:
                        best_score = score
                        best_placement = Placement(x, y, i)
                        print('BestScore {} and placement: {}'.format(best_score, best_placement))

        if best_placement is None:
            return
        
        if self.horizontal:
            self.place_horizontal(word, best_placement.x - best_placement.i, best_placement.y)
        else:
            self.place_vertical(word, best_placement.x, best_placement.y - best_placement.i)
        print(self)

    def __repr__(self):
        print(self.min_x, self.min_y, self.max_x, self.max_y)
        print(self.word_map)
        print(self.grid)
        s = ''
        for y in range(self.min_y - 1, self.max_y + 2):
            for x in range(self.min_x - 1, self.max_x + 2):
                s += self.grid.get((x,y), ('-',False))[0].upper()
            s += '\n'

        return s

def generate_crossword(word_list, max_words=10):
    crossword = Crossword()
    i = 0
    for word in word_list:
        i += 1
        crossword.add_word(word)
        if i > max_words:
            break
    return crossword