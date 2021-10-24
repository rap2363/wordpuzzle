# A Data structure to efficiently encode (and lookup) words in O(M) time where M is the character 
# length of a word. The idea of the trie is to encode characters of words as nodes in the trie, 
# where each node contains pointers to other characters.
class TrieNode:
    def __init__(self, is_word=False):
        self.is_word = is_word
        self.nodes = [None for i in range(26)]

    def get_node_for_letter(self, letter):
        return self.nodes[ord(letter) - ord('a')]

    def add_node_for_letter(self, letter):
        node = self.get_node_for_letter(letter)
        if node is None:
            node = TrieNode()
            self.nodes[ord(letter) - ord('a')] = node
        return node

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def encode_word(self, word):
        '''For each character, add a new node in our trie.'''
        curr_node = self.root
        for i,c in enumerate(word):
            curr_node = curr_node.add_node_for_letter(c)
            if i == len(word) - 1:
                curr_node.is_word = True

    def find(self, word):
        '''For each character, see if we have a node corresponding to it and look up the word.'''
        curr_node = self.root
        for c in word:
            curr_node = curr_node.get_node_for_letter(c)
            if curr_node is None:
                return False
        return curr_node.is_word

def is_valid(word):
    '''Check that each letter is alpha'''
    for c in word:
        if ord(c) > ord('z') or ord(c) < ord('a'):
            return False
    return True

def run(filename):
    trie = Trie()
    some_words = ['hello', 'whatsup', 'box', 'dictionary', 'dictionar', 'diction']
    with open(filename) as file:
        for line in file:
            word = line.rstrip()
            if word in some_words:
                print(word)
            if is_valid(word): 
                trie.encode_word(word)
    for word in some_words:
        print('\'{0}\' in the dictionary? {1}'.format(word, 'yes' if trie.find(word) else 'no'))

if __name__ == '__main__':
    filename = 'words_50k.txt'
    run(filename)
