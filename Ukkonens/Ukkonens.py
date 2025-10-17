import string

import pdb, traceback, sys

ASCII_START = 37
ASCII_END = 126
ENDING_CHAR = "!"

# input_string = "xyzxyaxyz!"
input_string = "xyxzxa!"
node_number = 0

class GlobalEnd:
    def __init__(self, val=-1):
        self.val = val

global_end = GlobalEnd()

class SuffixTreeNode:

    def __init__(self, start: int, end: int, is_leaf : bool, suffix_link = None):
        global node_number
        node_number += 1

        self.is_leaf = is_leaf
        self.node_val = node_number
        self.children : list[SuffixTreeNode | None] = [None] * (ASCII_END - ASCII_START + 1)
        self.start = start
        self.end = global_end if is_leaf else end
        self.suffix_link : SuffixTreeNode | None = suffix_link

    def __str__(self):
        has_children = not all(x is None for x in self.children)
        children_arr_str = ", ".join(str(node) for node in self.children if node is not None) if has_children else ""
        children_str = f", children : [{children_arr_str}]" if has_children else ""
        type_str = "Leaf" if self.is_leaf else "Internal"
        substring_str = input_string[self.start:self.end + 1] if not self.is_leaf else input_string[self.start:self.end.val + 1]
        suffix_link_str = ", suffix link: Node " + str(self.suffix_link.node_val) if  self.suffix_link else ""
        return f"Node ({type_str}) {self.node_val}: {substring_str}{children_str}{suffix_link_str}"

    def convert_to_internal_node(self, end: int):
        self.end = end
        self.is_leaf = False

    def add_suffix_link(self, to_node):
        self.suffix_link = to_node

    def get_end(self):
        return self.end if not self.is_leaf else self.end.val

class SuffixTree:

    def __init__(self, input_str : string):
        self.str = input_str
        self.root = SuffixTreeNode(-1,-1, False)
        self.suffix_array = [0] * len(input_str)

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
            prev_internal_node = None
            remaining += 1

            global global_end
            global_end.val += 1

            # loop through extensions
            while remaining > 0:

                char_to_check = self.str[i]

                if active_length > 0:
                    active_char = self.str[active_edge]
                    active_char_ind = self._get_char_index(active_char)
                    edge = active_node.children[active_char_ind]

                else:
                    char = self.str[i]
                    char_ind = self._get_char_index(char)

                    edge: SuffixTreeNode = active_node.children[char_ind]

                if edge:

                    while edge.start + active_length > edge.get_end():
                        next_edge_ind = self._get_char_index(self.str[edge.get_end() + 1])
                        active_length -= (edge.start + active_length - edge.get_end() + 1)
                        active_node = edge
                        edge = active_node.children[next_edge_ind]

                    next_char = self.str[edge.start + active_length] if edge is not None else ""

                    if char_to_check == next_char:
                        active_edge = edge.start
                        active_length += 1
                        break

                    else:
                        middle_edge = SuffixTreeNode(edge.start, edge.start + active_length - 1, False)
                        middle_edge_char_ind = self._get_char_index(self.str[edge.start])

                        edge.start = edge.start + active_length

                        new_edge = SuffixTreeNode(i,i,True)

                        edge_char_ind = self._get_char_index(self.str[edge.start])
                        new_edge_char_ind = self._get_char_index(self.str[i])

                        active_node.children[middle_edge_char_ind] = middle_edge
                        middle_edge.children[edge_char_ind] = edge
                        middle_edge.children[new_edge_char_ind] = new_edge

                        if prev_internal_node:
                            prev_internal_node.add_suffix_link(middle_edge)

                        prev_internal_node = middle_edge
                        prev_internal_node.add_suffix_link(self.root)



                        remaining -= 1

                        # root
                        if active_node.node_val == 1:
                            active_length -= 1
                            active_edge += 1
                        else:
                            active_node = active_node.suffix_link


                else:
                    new_node = SuffixTreeNode(i, i, True)

                    active_node.children[self._get_char_index(char_to_check)] = new_node
                    remaining -= 1

    # def create_suffix_array(self):



if __name__ == '__main__':
    suffix_tree  = SuffixTree(input_string)
    suffix_tree.createSuffixTree()









