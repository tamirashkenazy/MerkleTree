# Tom Menashe, 316429653

import hashlib

tree = None

'''
Each merkle node has min index and max index so it is in the shape of h0-7
if the min index equals the max index then it is a leaf (for example: h1-1)
'''
class Merkle:
    def __init__(self, min_index, max_index, name='', sons = []):
        self.min_index = min_index
        self.max_index = max_index
        self.sons = sons
        # if it is a leaf
        if not sons:
            self.name = name
        # if it is not a leaf, the hash is on the concatenation of the 2 sons
        else:
            string = self.sons[0].name + self.sons[1].name
            self.name = hashlib.sha256(string.encode()).hexdigest()

'''
From the input of the user we create a array of Merkle leafs
'''
def create_leafs(input_array):
    leafs = []
    index = 0
    # not including the user choice
    for my_input in input_array[1:]:
        leafs.append(Merkle(index, index, name=my_input))
        index += 1
    return leafs

'''
Create a full Merkle tree by using the leaves and going up
'''
def create_merkle_tree(splitted_input):
    # getting the leafs
    merkle_tree = create_leafs(splitted_input)

    final_index = len(merkle_tree) -1
    current_index = 0
    while current_index < final_index:
        sons = []
        sons.append(merkle_tree[current_index])
        sons.append(merkle_tree[current_index + 1])
        merkle_tree.append(Merkle(merkle_tree[current_index].min_index, merkle_tree[current_index + 1].max_index, name='', sons=sons))
        current_index += 2
        final_index += 1
    return merkle_tree

'''
Getting the path from the leaf with the index of the user
'''
def get_inclusion_way(root, index):
    min_index = root.min_index
    max_index = root.max_index
    way = ''
    if min_index != max_index or min_index != index:
        # if the index is in the right part of the subtree we go right and add the name of the left side
        if index >= (min_index + max_index +1)/2:
            string = get_inclusion_way(root.sons[1], index)
            if string !='':
                way = string + ' ' + 'l ' + root.sons[0].name +' '
            else:
                way = string + 'l ' + root.sons[0].name + ' '
        # if the index is in the left part of the subtree we go left and add the name of the right side
        elif index < (min_index + max_index +1)/2:
            string = get_inclusion_way(root.sons[0], index)
            if string != '':
                way = string +' ' + 'r ' + root.sons[1].name
            else:
                way = string + 'r ' + root.sons[1].name
    way = way.replace("  ", " ")
    return way

'''
Checking the validation of the way of inclusion we get from the user
'''
def check_path(leaf, root_hash, path_to_check):
    arg_number = 0
    result = leaf
    while arg_number < len(path_to_check):
        # if we need to add the concatenation from the left side
        if path_to_check[arg_number] == 'l':
            concatenation = path_to_check[arg_number+1] +result
            result = hashlib.sha256(concatenation.encode()).hexdigest()

        # if we need to add the concatenation from the right side
        else:
            concatenation = result+path_to_check[arg_number + 1]
            result = hashlib.sha256(concatenation.encode()).hexdigest()
        # go to the next left or right instruction
        arg_number +=2
    # return if we final result equals to the root
    return root_hash == result

'''
Starting from zero until infinity, get the first number that if we
concatenate it to the hash root we get an hash number with a least 
number of level in the beginning of the new hash string
'''
def difficulty_level(root_hash, level_number):
    found_number = False
    count = 0
    while not found_number:
        concatenation = str(count) + root_hash
        result = hashlib.sha256(concatenation.encode()).hexdigest()
        prefix_result = result[:level_number]
        all_zero = True
        for i in prefix_result:
            if i !='0':
                all_zero = False
        if all_zero:
            return count, result
        count+=1

'''
The function that it is activated if the user selects option 1
'''
def option1(splitted_input):
    global tree
    tree = create_merkle_tree(splitted_input)
    print(tree[len(tree)-1].name)

'''
The function that it is activated if the user selects option 2
'''
def option2(splitted_input):
    global tree
    index = int(splitted_input[1])
    root = tree[len(tree) - 1]
    # checking validation of input
    if index<root.min_index or index>root.max_index:
        quit()
    way_to_proof_of_inclusion = get_inclusion_way(root, index)
    print(way_to_proof_of_inclusion)

'''
The function that it is activated if the user selects option 3
'''
def option3(splitted_input):
    leaf = splitted_input[1]
    root_hash = splitted_input[2]
    path_to_check = splitted_input[3:]
    correct_path = check_path(leaf, root_hash, path_to_check)
    print(correct_path)

'''
The function that it is activated if the user selects option 4
'''
def option4(splitted_input):
    global tree
    level = int(splitted_input[1])
    root_hash = tree[len(tree) - 1].name
    first_number, hash_result = difficulty_level(root_hash, level)
    print(str(first_number) + ' ' + hash_result)

'''
The function that it is activated if the user selects option 5
'''
def option5():
    quit()

def main():
    global tree
    has_tree = False
    while True:
        my_input = input()
        splitted_input = my_input.split(' ')

        if int(splitted_input[0]) == 1:
            option1(splitted_input)
            has_tree = True

        elif int(splitted_input[0]) == 2:
            if has_tree:
                option2(splitted_input)
            else:
                quit()

        elif (int(splitted_input[0])) == 3:
                option3(splitted_input)

        elif (int(splitted_input[0])) == 4:
            if has_tree:
                option4(splitted_input)
            else:
                quit()

        else:
            option5()

if __name__ == "__main__":
    main()