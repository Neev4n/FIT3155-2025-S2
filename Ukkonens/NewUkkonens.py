import string

ASCII_START = 37
ASCII_END = 126
ENDING_CHAR = "!"

class SuffixTreeLeaf():

    def __init__(self, start : int, end: int):
        self.start = start
        self. end = end

class SuffixTreeNode():

    def __init__(self, start: int, end: int):
        self. children : list[SuffixTreeNode | SuffixTreeLeaf | None] = [None] * (ASCII_END - ASCII_START)
        self.start = start
        self.end = end

class SuffixTree():

    def __init__(self, input_str : string):
        self.str = input_str
        self.root = SuffixTreeNode(-1,-1)

    def _get_char_index(self, input_char: str):

        return ord(input_char) - ASCII_START if input_char != ENDING_CHAR else -1

    def createSuffixTree(self):

        n = len(self.str)

        for i in range(n):
            j = 0

            while j <= i:

                curr: SuffixTreeNode = self.root

                char = self.str[j]
                char_idx = self._get_char_index(char)
                jump = 0

                traversing_node: SuffixTreeNode | SuffixTreeLeaf = curr.children[char_idx]

                # move through to node
                if traversing_node:
                    start = traversing_node.start
                    end = traversing_node.end
                    k = 0

                    while k + j <= i:

                        # rule 1 or move through node
                        if k + start == end:

                            # move through node
                            if j + k >= end and i > end + 1:

                                if j + k + 1 >= n:
                                    break

                                k += 1
                                curr = traversing_node

                                char = self.str[j+k]
                                char_ind = self._get_char_index(char)
                                prev_end = end

                                traversing_node: SuffixTreeNode | SuffixTreeLeaf = curr.children[char_ind]

                                if not traversing_node:
                                    new_node = SuffixTreeLeaf(j+k, j+k)
                                    curr.children[char_ind] = new_node

                                start = traversing_node.start
                                end = traversing_node.end

                                jump += start - prev_end

                                k = 0
                                continue

                            # rule 1
                            traversing_node.end += 1
                            break

                # rule 2 extension
                else:
                    new_node = SuffixTreeLeaf(j, i)
                    curr.children[char_idx] = new_node

                j += 1




test = "xyzx" + ENDING_CHAR

suffix_tree  = SuffixTree(test)

print(suffix_tree.createSuffixTree())






