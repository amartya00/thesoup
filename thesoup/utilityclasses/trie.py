class TrieNode:
    """
    This class implements a node in a trie. It's usage outside of a trie is not recommended although no one is
    stopping you.

    NOTE: This supports ASCII character set only.

    Structurally, it contains a fixed size list internally, initialized to all Nones. Whenever a character in inserted,
    it creates another TrieNode object at the index corresponding to the ascii character.
    """
    ASCII_CHARSET_SIZE = 128

    def __init__(self):
        """
        Constructor. Needs no parameters
        """
        self.storage = [None] * TrieNode.ASCII_CHARSET_SIZE
        self.end_marker = False

    def __contains__(self, char: str) -> bool:
        """
        Implements the contains functionality. You can do `'a' in trie_node_object`.
        :param char: The character to test
        :return: Boolean
        """
        if len(char) > 1:
            raise ValueError("'{}' is not a single character.".format(char))
        return self.storage[ord(char)] is not None

    def __getitem__(self, char: str) -> 'TrieNode':
        """
        This implements the index into the object. It returns the trie node object in the index corresponding to
        the ASCII value of the character. `None` would indicate absence of that character in the node object.
        :param char:
        :return:
        """
        if len(char) > 1:
            raise ValueError("'{}' is not a single character.".format(char))
        return self.storage[ord(char)]

    def __iter__(self):
        """
        Implements the iter functionality. It iterates over the internal storage.
        :return: An iterator.
        """
        return iter(self.storage)

    def set_char(self, char: str, end_marker: bool = False):
        """
        This sets a character inside a trie. If the character already existed at that position, a end marker is installed
        if needed.
        :param char:
        :param end_marker:
        :return:
        """
        if len(char) > 1:
            raise ValueError("'{}' is not a single character.".format(char))

        if char not in self:
            self.storage[ord(char)] = TrieNode()
        node = self.storage[ord(char)]
        node.end_marker = end_marker or node.end_marker


class Trie:
    """
    This class is the implement of a Trie data structure, for the ASCII character set. The contents are case sensitive.
    """

    def __init__(self):
        """
        Constructor. This takes no arguments
        """
        self.root = TrieNode()

    @staticmethod
    def _insert_callback(word: str, start_pos: int, node: TrieNode):
        if start_pos == len(word) - 1:
            node.set_char(word[start_pos], True)
        else:
            node.set_char(word[start_pos])
            Trie._insert_callback(word, start_pos + 1, node[word[start_pos]])

    @staticmethod
    def _search_callback(word: str, pos: int, node: TrieNode) -> bool:
        if pos == len(word):
            return node
        else:
            return Trie._search_callback(word, pos + 1, node[word[pos]]) if (word[pos] in node) else None

    @staticmethod
    def _collect_branches(node: TrieNode) -> list:
        if node is None:
            return ['']
        sub_strings = []
        valid_next_nodes = filter(lambda elem: elem[1] is not None, enumerate(node))
        for enum, nxt in valid_next_nodes:
            char = chr(enum)
            end_marker = nxt.end_marker
            if end_marker:
                sub_strings.append(char)

            more_substrings = ["{}{}".format(char, s) for s in Trie._collect_branches(nxt)]
            sub_strings.extend(more_substrings)
        return sub_strings

    def insert(self, word: str):
        """
        This function inserts a word into the trie
        :param word: The word to insert into the trie
        :return
        """
        Trie._insert_callback(word, 0, self.root)

    def __contains__(self, word: str) -> bool:
        """
        This implements the contains method. Use it like "word" in my_trie_struct
        :param word:
        :return: `boolean` whether the trie contains the word
        """
        terminal_node = Trie._search_callback(word, 0, self.root)
        return False if terminal_node is None else terminal_node.end_marker

    def __getitem__(self, word: str) -> list:
        """
        This returns the tree under the passed index. This is useful for implementing type-ahead.
        :param word: The index
        :return: A list of words under the index
        """
        terminal_node = Trie._search_callback(word, 0, self.root)
        entries = []
        if terminal_node.end_marker:
            entries.append(word)
        entries.extend(["{}{}".format(word, s) for s in Trie._collect_branches(terminal_node)])
        return entries
