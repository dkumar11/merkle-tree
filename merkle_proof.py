from utils import *
import math
from node import Node


def merkle_proof(tx, merkle_tree):
    """Given a tx and a Merkle tree object, retrieve its list of tx's and
    parse through it to arrive at the minimum amount of information required
    to arrive at the correct block header. This does not include the tx
    itself.
    Return this data as a list; remember that order matters!
    """
    return merkle_proof_helper(merkle_tree.leaves, tx, [])

def merkle_proof_helper(txs, tx, nodes):
    if len(txs) > 1:
        lst = []
        index = 0
        for idx in range(0, len(txs), 2):
            lst.append(hash_data( txs[idx + 1]  + txs[idx]))
            if (txs[idx + 1] == tx):
                nodes.insert(0, Node('l', txs[idx]))
                index = hash_data(txs[idx] + tx)
            elif (txs[idx] == tx):
                nodes.insert(0, Node('r', txs[idx + 1]))
                index = hash_data(tx + txs[idx + 1])
        return merkle_proof_helper(lst, index, nodes)
    else:
        return nodes



def verify_proof(tx, merkle_proof):
    """Given a Merkle proof - constructed via `merkle_proof(...)` - verify
    that the correct block header can be retrieved by properly hashing the tx
    along with every other piece of data in the proof in the correct order
    """

    return_value = tx
    for data_value in merkle_proof[::-1]:
        if data_value.direction == 'r':
            return_value = hash_data(return_value + data_value.tx)
        elif data_value.direction == 'l':
            return_value = hash_data(data_value.tx + return_value)
        else:
            continue
    return return_value
