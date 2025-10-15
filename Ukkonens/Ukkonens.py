import string

import pdb, traceback, sys

ASCII_START = 37
ASCII_END = 126
ENDING_CHAR = "!"

input_string = "xyzxaxyz!"
node_number = 0

class GlobalEnd:
    def __init__(self, val=-1):
        self.val = val

global_end = GlobalEnd()

class SuffixTreeNode:

    def __init__(self, start: int, end: int, is_leaf : bool):
        global node_number
        node_number += 1

        self.is_leaf = is_leaf
        self.node_val = node_number
        self.children : list[SuffixTreeNode | None] = [None] * (ASCII_END - ASCII_START + 1)
        self.start = start
        self.end = global_end if is_leaf else end

    def __str__(self):
        children_str = ", ".join(str(node) for node in self.children if node is not None)
        type_str = "Leaf" if self.is_leaf else "Internal"
        substring_str = input_string[self.start:self.end + 1] if not self.is_leaf else input_string[self.start:self.end.val + 1]
        return f"Node ({type_str}) {self.node_val}: {substring_str}, children: [{children_str}]"

    def convert_to_internal_node(self, end: int):
        self.end = end
        self.is_leaf = False

class SuffixTree:

    def __init__(self, input_str : string):
        self.str = input_str
        self.root = SuffixTreeNode(-1,-1, False)

    def _get_char_index(self, input_char: str):

        return ord(input_char) - ASCII_START if input_char != ENDING_CHAR else -1

    def createSuffixTree(self):

        n = len(self.str)

        remaining = 0
        active_node = self.root
        active_edge = -1
        active_length = 0

        # loop through phases
        for i in range(n):
            remaining += 1

            global global_end
            global_end.val += 1
            j = 0

            # loop through extensions
            while remaining > 0:

                if i == 3 and j == 3:
                    pass

                curr: SuffixTreeNode = active_node

                char = self.str[i+active_length]
                char_ind = self._get_char_index(char)
                jump = 0

                traversing_node : SuffixTreeNode = curr.children[char_ind]

                if traversing_node:

                    active_edge = traversing_node.start
                    active_length += 1

                    start = traversing_node.start
                    end = traversing_node.end
                    k = 0

                    while k + j + jump <= i:

                        # rule 1 or move through node
                        if k + start == end:

                            # move through node
                            if j + k >= end and i > end + 1:

                                # rule 3
                                if j + k + 1 > i:
                                    break

                                k += 1
                                curr = traversing_node

                                char = self.str[j+k]
                                char_ind = self._get_char_index(char)

                                traversing_node: SuffixTreeNode = curr.children[char_ind]

                                if not traversing_node:
                                    new_node = SuffixTreeNode(j+k, j+k, True)
                                    curr.children[char_ind] = new_node

                                start = traversing_node.start
                                end = traversing_node.end

                                jump = start - j

                                jump = 1 if jump < 0 else jump

                                k = 0
                                continue

                            # rule 1
                            # traversing_node.end += 1
                            # break

                        # rule 2
                        elif self.str[k + j + jump] != self.str[start + k]:
                            traversing_node_char_ind = self._get_char_index(self.str[start + k])
                            new_node_char_ind = self._get_char_index(self.str[k+j+jump])

                            middle_node = SuffixTreeNode(start, start + k - 1, False)

                            traversing_node.start = start + k

                            new_node = SuffixTreeNode(k+j+jump, k+j+jump, True)

                            curr.children[char_ind] = middle_node

                            middle_node.children[traversing_node_char_ind] = traversing_node
                            middle_node.children[new_node_char_ind] = new_node

                        k += 1

                # rule 2
                else:
                    new_node = SuffixTreeNode(i, i, True)
                    curr.children[char_ind] = new_node
                    remaining -= 1

                j += 1

                # rule 3
                # if j > i:
                #     active_length += 1
                #     active_edge += 1
                #     pass

        return self.root

if __name__ == '__main__':
    suffix_tree  = SuffixTree(input_string)
    print(suffix_tree.createSuffixTree())







