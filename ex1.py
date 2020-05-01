# tamir ashkenazy, 204508949, lidor alis, 201025160
import sys
from hashlib import sha256
UTF_8_ENCODE = "utf-8"



class Node(object):
    def __init__(self, value, right=None, left=None):
        self.value = value
        self.right = right
        self.left = left
    def get_value(self):
        return self.value

    def __str__(self):
        return self.value
    def __repr__(self):
        return self.value

class MerkleTree(object):
    def __init__(self, root):
        self.root = root




def build_merkle_tree(str_list):
    nodes = [Node(leaf) for leaf in str_list]
    while len(nodes) != 1:
        left, right = nodes.pop(0), nodes.pop(0)
        temp_string_value = left.get_value() + right.get_value()
        hashed_value = sha256(temp_string_value.encode(UTF_8_ENCODE)).hexdigest()
        father = Node(hashed_value, left, right)
        nodes.append(father)
    return MerkleTree(nodes[0])


def create_proof_of_inclusion(index_of_leaves):
    pass

def check_proof_of_inclusion(leaf_to_check, merkle_tree_root, proof_of_inclusion_list):
    pass

def go_out():
    return

HANDLE_FUNCS_MAP = {
    1 : build_merkle_tree,
    2 : create_proof_of_inclusion,
    3 : check_proof_of_inclusion,
    4 : None
}

class ArgumentsHandler(object):
    def __init__(self, args):
        self.args = args
        self.operation = args[0]
        self.merkle_tree = None


    def set_operation(self, index):
        self.operation = index

    def get_handler(self):
        if self.operation in HANDLE_FUNCS_MAP:
            return HANDLE_FUNCS_MAP[self.operation]
        else:
            return None

    def set_merkle_tree(self, merkle_tree):
        self.merkle_tree = merkle_tree

    def get_merkle_tree(self):
        return self.merkle_tree


OPERATION_INDEX = 0
EXIT_OPERATION = 5

if __name__ == "__main__":
    try:
        args = input()
        args = args.split()
        # args_handler = ArgumentsHandler(args)
        operation = 0
        if len(args) >= 1:
            operation = args[OPERATION_INDEX]

        while operation != EXIT_OPERATION:
            if operation in HANDLE_FUNCS_MAP:
                HANDLE_FUNCS_MAP[operation](args[1:])

            args = input()
            args = args.split()
            if len(args) > 1:
                operation = args[OPERATION_INDEX]

    except Exception as e:
        print(e)