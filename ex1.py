# tamir ashkenazy, 204508949, lidor alis, 201025160
from hashlib import sha256
UTF_8_ENCODE = "utf-8"

class Node(object):
    """
    Node of value, left and right child (node of binary tree)
    """
    def __init__(self, value, right=None, left=None):
        self.value = value
        self.right = right
        self.left = left

    def get_value(self):
        """
        :return: value of the node
        """
        return self.value
    def get_left_child(self):
        """
        :return: the left child
        """
        return self.left

    def get_right_child(self):
        """
        :return: the right child of the node
        """
        return self.right

    def __str__(self):
        """
        :return: the value as a string
        """
        return self.value
    def __repr__(self):
        """
        :return: the representation of the node (as the value)
        """
        return self.value

class MerkleTree(object):
    """
    Merkle Tree - Binary
    """
    def __init__(self, root, leaves):
        """
        :param root: the root of the Merkle tree
        :param leaves: the leaves given from the user
        """
        self.root = root
        self.leaves = leaves

    def create_proof_of_inclusion(self, str_index_in_list):
        """
        create a proof of inclusion to the tree
        :param str_index_in_list: the leaves given from the user
        :return: proof of inclusion to the index of the leaf (the user insert)
        """
        try:
            # the index that the user insert
            index = int(str_index_in_list[0])
            # check that the index is not bigger then the length
            if not index < len(self.leaves):
                exit(0)
            list_of_proofs = []

            interval = list(range(len(self.leaves)))
            temp_root = self.root
            while len(interval) != 1:
                if index in interval[:len(interval) // 2]: #check if the root in left side
                    right_child = temp_root.get_right_child()
                    temp_root = temp_root.get_left_child()
                    if not right_child:
                        break
                    list_of_proofs.append(right_child.get_value()) # append the value of the right child
                    list_of_proofs.append("r")  # append "r"
                    interval = interval[:len(interval) // 2] # update the interval to the left side
                else: #the child is in the right side
                    left_child = temp_root.get_left_child()
                    temp_root = temp_root.get_right_child()
                    if not left_child:
                        break
                    list_of_proofs.append(left_child.get_value()) # append the value of the left child
                    list_of_proofs.append("l")  #append "l"
                    interval = interval[len(interval) // 2:] #update the interval to the right side
            list_of_proofs.reverse()
            str_proof = (" ").join(list_of_proofs) #build the string to return
            return str_proof #return the proof as a string
        except:
            exit(0)

    def hash_nonce(self, difficult_level_in_list):
        """
        :param difficult_level_in_list: difficult level from the user
        :return: the nonce and the hash with the nonce
        """
        try:
            difficult_level = int(difficult_level_in_list[0])
            # add the number of zeros the difficult level
            str_of_zeros = "0"*difficult_level
            #initialize the num of the hash with the root
            num_to_hash_with_root = 0
            # set the root value
            root_val = self.root.get_value()
            # while we will not find
            while True:
                # set the string and make hash of the num with the root and the root value
                s = str(num_to_hash_with_root) + root_val
                hashed_value = sha256(s.encode(UTF_8_ENCODE)).hexdigest()
                #if the hashed value start with the zeros as the difficult level return, else, try again
                if hashed_value.startswith(str_of_zeros):
                    return num_to_hash_with_root, hashed_value
                #add 1 to the num to hash with the root
                num_to_hash_with_root += 1
        except:
            exit(0)

    def __repr__(self):
        """
        :return: the root value as the representation of the Merkle tree
        """
        return self.root.get_value()
    def __str__(self):
        """
        :return:the root value a string
        """
        return self.root.get_value()
def build_merkle_tree(str_list):
    """
    building the Merkle tree from list
    :param str_list: list of leaves
    :return: the root of the Merkle Tree and the string list (of the leaves)
    """
    try:
        # if there is no list  - return the root as "None"
        if not str_list:
            return None
        # convert every leaf to node (with no childs)
        nodes = [Node(leaf) for leaf in str_list]
        #while there are nodes
        while len(nodes) != 1:
            #pop two nodes (from the beggining of the nodes list - add them and make hash
            left, right = nodes.pop(0), nodes.pop(0)
            temp_string_value = left.get_value() + right.get_value()
            hashed_value = sha256(temp_string_value.encode(UTF_8_ENCODE)).hexdigest()
            #make a father node with value of the hash and right and left child
            father = Node(hashed_value, right, left)
            # adding the father the nodes list
            nodes.append(father)
        return MerkleTree(nodes[0], str_list)
    except:
        exit(0)

def check_proof_of_inclusion(args):
    """
    checks if the proof of inclusion is currect
    :param args: [node, root, args of r/l and nodes by value]
    :return: True/False
    """
    try:
        # 2 means there are no leaf and root
        if len(args) < 2:
            exit(0)
        # the first argument is the leaf to check
        leaf_to_check = args[0]
        #the second argument is the root to check
        merkle_tree_root = args[1]
        # case of only one leaf
        if len(args) < 3:
            return leaf_to_check == merkle_tree_root
        #the other arguments - l/r and the node value
        proof_of_inclusion_list = args[2:]
        #if the length of the inclusion is odd - so its not legal - and exit
        if len(proof_of_inclusion_list) % 2 == 1:
            exit(0)
        while len(proof_of_inclusion_list) != 0:
            # pop the directio - right/left
            direction = proof_of_inclusion_list.pop(0)
            # pop node value from the arguments
            other = proof_of_inclusion_list.pop(0)
            # if the direction is left add the node from the left
            if direction == "l":
                leaf_to_check = other + leaf_to_check
            # if the direction is right add the node from the right
            elif direction == "r":
                leaf_to_check = leaf_to_check + other
            else:
                exit(0)
            # hash the two leaves that added
            leaf_to_check = sha256(leaf_to_check.encode(UTF_8_ENCODE)).hexdigest()
        # return True/ False if all the path equal to the merkle root
        return leaf_to_check == merkle_tree_root
    except:
        exit(0)


def go_out():
    """
    :return: nothing - just go out
    """
    return

HANDLE_FUNCS_MAP = {
    "1" : build_merkle_tree,
    "3" : check_proof_of_inclusion,
}

class ArgumentsHandler(object):
    # handler to separate the missions
    def __init__(self, args, is_merkle_tree=False):
        """
        init all the handler
        :param args: all the arguments
        :param is_merkle_tree: check if there is a merkle tree (otherwise - we can't run mission 2)
        """
        self.args = args
        self.operation = self.set_operation()
        self.is_merkle_tree = is_merkle_tree
        self.merkle_tree = None

    def set_args(self, args):
        """
        :param args: the arguments from the user
        """
        self.args = args
        self.operation = self.set_operation()

    def set_operation(self):
        """
        set the operation and run the function
        """
        if len(self.args) >= 1:
            return self.args[0]
        else:
            return None

    def get_operation(self):
        """
        :return: the operation
        """
        return self.operation

    def get_handler(self):
        """
        :return:  the function to use
        """
        if self.operation in HANDLE_FUNCS_MAP:
            # if the user asks for mission 2 but there is no merkle tree
            if self.operation == 2 and not self.is_merkle_tree:
                return None
            return HANDLE_FUNCS_MAP[self.operation]
        else:
            return None

    def get_args_for_function(self):
        """
        get the arguments to the function
        :return: args to the function
        """
        if len(self.args) >= 1:
           return self.args[1:]
        else:
            return []
    def set_merkle_tree(self, merkle_tree):
        """
        setting the merkle tree
        :param merkle_tree: a merkle tree
        """
        self.merkle_tree = merkle_tree

    def get_merkle_tree(self):
        """
        :return: Merkle tree
        """
        return self.merkle_tree

    def __repr__(self):
        """
        :return: representation of the Argument Handler as the args
        """
        return self.args


EXIT_OPERATION = "5"


if __name__ == "__main__":
    try:
        args = input()
        args = args.split()
        args_handler = ArgumentsHandler(args)
        operation = args_handler.operation
        # while the user didnt choose "5"
        while operation != EXIT_OPERATION:
            if operation == "1":
                # operation 1 - build merkle tree
                merkle_tree = build_merkle_tree(args_handler.get_args_for_function())
                print(merkle_tree.root.get_value())
                # if there is a merkle tree - set the Argument handler to True (merkle tree)
                if merkle_tree:
                    args_handler.is_merkle_tree = True
                    args_handler.set_merkle_tree(merkle_tree)
            # proof of inclusion to the merkle tree
            elif operation == "2":
                merkle_tree = args_handler.get_merkle_tree()
                proof = merkle_tree.create_proof_of_inclusion(args_handler.get_args_for_function())
                print(proof)
            # operation 4 to print the nonce and the hashed value
            elif operation == "4":
                merkle_tree = args_handler.get_merkle_tree()
                nonce_value, hashed_value = merkle_tree.hash_nonce(args_handler.get_args_for_function())
                print("{} {}".format(nonce_value, hashed_value))

            else:
                handler_function = args_handler.get_handler() #None or function from dict
                if handler_function:
                    return_value = handler_function(args_handler.get_args_for_function())
                    print(return_value)

            args = input()
            args = args.split()
            args_handler.set_args(args)
            operation = args_handler.get_operation()

    except:
        exit(0)