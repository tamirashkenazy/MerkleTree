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
    def get_left_child(self):
        return self.left

    def get_right_child(self):
        return self.right

    def __str__(self):
        return self.value
    def __repr__(self):
        return self.value

class MerkleTree(object):
    def __init__(self, root, leaves):
        self.root = root
        self.leaves = leaves

    def create_proof_of_inclusion(self, str_index_in_list):
        try:
            index = int(str_index_in_list[0])
            if not index < len(self.leaves):
                exit(0)
            list_of_proofs = []
            interval = list(range(len(self.leaves)))
            temp_root = self.root
            while len(interval) != 1:
                if index in interval[:len(interval)//2]: #left side
                    right_child = temp_root.get_right_child()
                    temp_root = temp_root.get_left_child()
                    if not right_child:
                        break
                    list_of_proofs.append(right_child.get_value())
                    list_of_proofs.append("r")
                    interval = interval[:len(interval)//2]
                else:
                    left_child = temp_root.get_left_child()
                    temp_root = temp_root.get_right_child()
                    if not left_child:
                        break
                    list_of_proofs.append(left_child.get_value())
                    list_of_proofs.append("l")
                    interval = interval[len(interval) // 2:]
            list_of_proofs.reverse()
            str_proof = (" ").join(list_of_proofs)
            return str_proof
        except:
            exit(0)

    def hash_nonce(self, difficult_level_in_list):
        difficult_level = int(difficult_level_in_list[0])
        str_of_zeros = "0"*difficult_level
        num_to_hash_with_root = 0
        root_val = self.root.get_value()
        while True:
            s = str(num_to_hash_with_root)+root_val
            hashed_value = sha256(s.encode(UTF_8_ENCODE)).hexdigest()
            if hashed_value.startswith(str_of_zeros):
                return num_to_hash_with_root
            num_to_hash_with_root += 1



def build_merkle_tree(str_list):
    if not str_list:
        return None

    nodes = [Node(leaf) for leaf in str_list]
    while len(nodes) != 1:
        left, right = nodes.pop(0), nodes.pop(0)
        temp_string_value = left.get_value() + right.get_value()
        hashed_value = sha256(temp_string_value.encode(UTF_8_ENCODE)).hexdigest()
        father = Node(hashed_value, right, left)
        nodes.append(father)
    return MerkleTree(nodes[0], str_list)


# def create_proof_of_inclusion(index_of_leaf):
#     pass

def check_proof_of_inclusion(args):
    try:
        # 2 means there are no leaf and root
        if len(args) < 2:
            exit(0)
        leaf_to_check = args[0]
        merkle_tree_root = args[1]
        # case of only one leaf
        if len(args) < 3:
            return leaf_to_check == merkle_tree_root
        proof_of_inclusion_list = args[2:]
        if len(proof_of_inclusion_list) % 2 == 1:
            exit(0)
        while len(proof_of_inclusion_list) != 0:
            direction = proof_of_inclusion_list.pop(0)
            other = proof_of_inclusion_list.pop(0)
            if direction == "l":
                leaf_to_check = other + leaf_to_check
            elif direction == "r":
                leaf_to_check = leaf_to_check + other
            else:
                exit(0)
            leaf_to_check = sha256(leaf_to_check.encode(UTF_8_ENCODE)).hexdigest()
        return leaf_to_check == merkle_tree_root
    except:
        exit(0)


def go_out():
    return

HANDLE_FUNCS_MAP = {
    "1" : build_merkle_tree,
    # "2" : create_proof_of_inclusion,
    "3" : check_proof_of_inclusion,
    "4" : None
}

class ArgumentsHandler(object):
    def __init__(self, args, is_merkle_tree=False):
        self.args = args
        self.operation = self.set_operation()
        self.is_merkle_tree = is_merkle_tree
        self.merkle_tree = None

    def set_args(self, args):
        self.args = args
        self.operation = self.set_operation()

    def set_operation(self):
        if len(self.args) >= 1:
            return self.args[0]
        else:
            return None

    def get_operation(self):
        return self.operation

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
    def set_merkle_tree(self, merkle_tree):
        self.merkle_tree = merkle_tree

    def get_merkle_tree(self):
        return self.merkle_tree

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
                    args_handler.set_merkle_tree(merkle_tree)

            elif operation == "2":
                merkle_tree = args_handler.get_merkle_tree()
                proof = merkle_tree.create_proof_of_inclusion(args_handler.get_args_for_function())
                cprint(proof, "green")

            elif operation == "4":
                merkle_tree = args_handler.get_merkle_tree()
                nonce_value = merkle_tree.hash_nonce(args_handler.get_args_for_function())

            else:
                handler_function = args_handler.get_handler() #None or function from dict
                if handler_function:
                    return_value = handler_function(args_handler.get_args_for_function())
                    print(return_value)
                    # TODO - something with the return value

            args = input()
            args = args.split()
            args_handler.set_args(args)
            operation = args_handler.get_operation()

    except:
        exit(0)