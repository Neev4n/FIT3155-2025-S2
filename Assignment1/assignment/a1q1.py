import sys

ASCII_START = 37
ASCII_END = 126
ENDING_CHAR = "!"

def z_algorithm(text: str):
    """
        Function description: Creates a Z array which contains the length of the prefix matched of a given index with the text itself

        Input:
            text : input text to create Z array

        Time complexity: O(S) where S is the length of the string

        Time complexity analysis : Given S is the length of the string,

            creating Z array is O(S)
            populating Z array is O(S)

            O(S)
    """
    n = len(text)
    l = 0
    r = 0
    Z = [0] * n

    # loop left to right
    for k in range(1, n):
        # out of box
        if k > r:
            l = r = k

            # fill out current Z box
            while (r < n and text[r - l] == text[r]):
                r += 1

            # store length of Z box
            Z[k] = r - l
            r -= 1


        # in box
        else:
            k1 = k - l

            # length does not exceed Z box -> copy previous Z values
            if (Z[k1] + k <= r):
                Z[k] = Z[k1]

            # length exceeds Z box -> continue pattern matching from end of Z box
            else:

                l = r = k
                while (r < n and text[r - l] == text[r]):
                    r += 1

                # store length of Z box
                Z[k] = r - l
                r -= 1

    return Z


def pattern_match_wildcard(pattern: str, text: str):
    """
        Function description: Pattern matches the pattern with the given text and accounts for wild card (#) characters which can be substituted as any character

        Approach:

            Step 1:
                -The pattern will contain components of characters that are separated by a wildcard/s
                -Separate pattern to be matched into multiple components and store the component string and index

            Step 2:
                -Create a count array which contains the number of components that can be combined from a given starting point
                -Produce a Z array for each component and use it to populate the count array

            Step 3:
                -Loop through the count array and if all components can be combined from a given start point then the pattern can be matched from that index

        Input:
            text: input text to be pattern matched with
            pattern: pattern to match with input text

        Time complexity: O(C * (T + P)) where C is the number of components, T is the length of the text and P is the length of the pattern

        Time complexity analysis: Given C is the number of components, T is the length of the text and P is the length of the pattern,

            populating components and component_indices array is O(P)
            creating count array is O(T)
            populating count array using Z algorithm on each component is O(C(T+P))
            producing return array is O(T)

            O(C(T+P))

        Space complexity: O(T + P)

            components and component_indices array is O(P)
            count array is O(T)
            Z array for each component is O(T+P) -> past Z values are not stored so it is not multiplied by C
            res array is O(T)
    """

    pat_length = len(pattern)
    text_length = len(text)
    components = []  # contains string components
    component_indices = []  # contains starting indices for string components
    curr_component = ""
    curr_index = 0
    max_start = text_length - pat_length + 1  # starting index cannot exceed max_start

    count = [0] * (max_start)  # count of number of components that can be combined from a given starting point (O(T))

    if max_start < 0 or pat_length == 0 or text_length == 0:
        return []

    # step 1:
    # collect all components and indices
    # a component is a non-wildcard section of the pattern
    for char_index in range(pat_length):    # O(P)

        # if wild card
        if pattern[char_index] == "#":

            # if component exists -> add it to components, add index and reset curr_component
            if curr_component:
                components.append(curr_component)
                component_indices.append(curr_index)
                curr_component = ""

            # move current index regardless to next index
            curr_index = char_index + 1

        # if normal character -> add char to current component
        else:
            curr_component += pattern[char_index]

    # if component still exists -> add char to components and indices
    if curr_component:
        components.append(curr_component)
        component_indices.append(curr_index)

    # edge case where its all wildcards -> return all possible indices
    if not components:
        return list(range(max_start))

    num_components = len(components)

    # step 2:
    # run the Z algorithm on each component
    # use Z values to find possible pattern matches
    for pat_pos, component in zip(component_indices, components):   # O(C)
        combined = component + ENDING_CHAR + text
        Z = z_algorithm(combined)   # O(T + P)

        # loop through z array
        for i in range(len(component), len(combined)):

            # if a full match exists with component -> update starting position
            if Z[i] >= len(component):

                text_pos = i - len(component) - 1  # find position in full text
                start_pos = text_pos - pat_pos  # find where the complete pattern to match would start in the text

                # if the starting position is valid -> increment number of components from that given start point
                if 0 <= start_pos < max_start:
                    count[start_pos] += 1

    # step 3:
    # if every component can exist from a given start point (count[i] == num_components) -> it is a full pattern match
    res = [i + 1 for i in range(max_start) if count[i] == num_components]   #O(T)
    return res

# this function reads a file and return its content
def read_file(file_path: str) -> str:
    f = open(file_path, 'r')


    line = f.readlines()
    f.close()
    return line

def write_file(output_path: str, result: list[int]):
    with open(output_path, "w") as file:
        file.write("\n".join(map(str, result)))


if __name__ == '__main__':
    print("Number of arguments passed : ", len(sys.argv))
    # this is the program name
    print("Oth argument : ", sys.argv[0])
    # first argument/file path
    # second argument/file path
    print("First argument : ", sys.argv[1])
    print("Second argument : ", sys.argv[2])

    OUTPUT_FILE_NAME = "output_a1q1.txt"

    txt = read_file(sys.argv[1])
    pat = read_file(sys.argv[2])

    res = pattern_match_wildcard("".join(pat), "".join(txt))
    write_file(OUTPUT_FILE_NAME, res)

    print("\nContent of first file : ", read_file(sys.argv[1]))
    print("\nContent of second file : ", read_file(sys.argv[2]))