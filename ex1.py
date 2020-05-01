# tamir ashkenazy, 204508949, lidor alis, 201025160
from hashlib import sha256
UTF_8_ENCODE = "utf-8"
from termcolor import colored, cprint


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
    if not str_list:
        return None

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
    "1" : build_merkle_tree,
    "2" : create_proof_of_inclusion,
    "3" : check_proof_of_inclusion,
    "4" : None
}

class ArgumentsHandler(object):
    def __init__(self, args, is_merkle_tree=False):
        self.args = args
        self.operation = self.set_operation()
        self.is_merkle_tree = is_merkle_tree


    def set_operation(self):
        if len(args) >= 1:
            return args[0]
        else:
            return None

    def get_handler(self):
        if self.operation in HANDLE_FUNCS_MAP:
            #
            if self.operation == 2 and not self.is_merkle_tree:
                return None

            return HANDLE_FUNCS_MAP[self.operation]
        else:
            return None

    def get_args_for_function(self):
        if len(self.args) >= 1:
           return self.args[1:]
        else:
            return []

    def __repr__(self):
        return self.args

EXIT_OPERATION = "5"

if __name__ == "__main__":
    try:
        args = input()
        args = args.split()
        args_handler = ArgumentsHandler(args)
        operation = args_handler.operation

        while operation != EXIT_OPERATION: # !=5
            if operation == "1":
                merkle_tree = build_merkle_tree(args_handler.get_args_for_function())
                cprint(merkle_tree.root, "blue")
                if merkle_tree:
                    args_handler.is_merkle_tree = True

            else:
                handler_function = args_handler.get_handler() #None or function from dict
                if handler_function:
                    return_value = handler_function()
                    # TODO - something with the return value

            args = input()
            args = args.split()
            args_handler = ArgumentsHandler(args)
            operation = args_handler.set_operation()

    except Exception as e:
        print(e)