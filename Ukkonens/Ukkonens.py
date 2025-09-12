import string

class SuffixTreeLeaf():

    def __init__(self, start : int, end: int):
        self.start = start
        self. end = end

class SuffixTreeNode():

    def __init__(self, start: int, end: int):
        self. children : list[SuffixTreeNode | SuffixTreeLeaf | None] = [None] * 27
        self.start = start
        self.end = end

class SuffixTree():

    def __init__(self, str : string):
        self.str = str
        self.root = SuffixTreeNode(-1,-1)

    def _get_char_index(self, char: str):
        char_ind = ord(char) - ord('a')

        return char_ind if char_ind >= 0 else -1

    def createSuffixTree(self):

        n = len(self.str)

        # loop through phases
        for i in range(n):

            j = 0

            # loop through extensions
            while j <= i:

                curr: SuffixTreeNode = self.root

                char = self.str[j]
                char_ind = self._get_char_index(char)
                jump = 0\

                traversing_node : SuffixTreeNode | SuffixTreeLeaf = curr.children[char_ind]

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

                        # rule 2
                        elif self.str[k + j + jump] != self.str[start + k]:
                            traversing_node_char_ind = self._get_char_index(self.str[start + k])
                            new_node_char_ind = self._get_char_index(self.str[k+j])

                            middle_node = SuffixTreeNode(start, start + k - 1)

                            traversing_node.start = start + k

                            new_node = SuffixTreeLeaf(k+j, k+j)

                            curr.children[char_ind] = middle_node

                            middle_node.children[traversing_node_char_ind] = traversing_node
                            middle_node.children[new_node_char_ind] = new_node

                        k += 1

                # rule 2
                else:
                    new_node = SuffixTreeLeaf(j, i)
                    curr.children[char_ind] = new_node

                j += 1

test = "xyzx$x"

suffix_tree  = SuffixTree(test)

print(suffix_tree.createSuffixTree())






