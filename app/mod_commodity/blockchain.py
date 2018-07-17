import hashlib
import json
from time import time
from uuid import uuid4

from flask import Flask, jsonify

MAX_COUNT = 50000


class Blockchain:
    __slots__ = ('chain', '__transactions', 'nodes', 'proof', '__modify_count')

    def __init__(self):
        self.chain = []
        self.__transactions = {}
        self.nodes = set()
        self.proof = 0
        self.__modify_count = 0

    def valid_chain(self):
        """
        Determine if a given blockchain is valid
        :return: True if valid, False if not
        """
        if len(self.chain) > 1:
            last_block = self.chain[0]
            current_index = 1
            global last_block_hash
            while current_index < len(self.chain):
                block = self.chain[current_index]
                # Check that the hash of the block is correct
                last_block_hash = last_block['current_hash']
                if block['previous_hash'] != last_block_hash:
                    return False

                # Check that the Proof of Work is correct
                valid_block = {
                    'previous_hash': last_block['previous_hash'],
                    'index': last_block['index'],
                    'timestamp': last_block['timestamp'],
                    'transactions': last_block['transactions'],
                    'proof': 0
                }

                valid_block_string = json.dumps(valid_block).encode()
                valid_block_hash = self.hash(valid_block_string)
                if self.valid_proof(last_block['proof'], valid_block_hash)[0] is False:
                    return False
                last_block = block
                current_index += 1
        print("valid chain")
        return True

    def new_block(self, values):
        """
        Create a new Block in the Blockchain
        :param values: product values
        :type values: dict
        :return: New Block
        """

        if not Blockchain.new_transaction(self, values):
            return None
        else:
            index = len(self.chain) + 1
            if index == 1:
                previous_hash = '0'
            else:
                previous_hash = self.last_block['current_hash']
            block = {
                'previous_hash': previous_hash,
                'index': index,
                'timestamp': time(),
                'transactions': self.__transactions,
                'proof': 0
            }
            current_hash = self.proof_of_work(block)

            block['proof'] = self.proof
            block['current_hash'] = current_hash
            # Reset the current list of transactions

            return block

    def __new_block_for_modify(self, block: dict):
        """
        :param block： new block:
        """

        current_hash = self.proof_of_work(block, modify=True)
        if current_hash is None:
            return None, None
        block['time'] = time()
        block['proof'] = self.proof
        block['current_hash'] = current_hash

        return block, current_hash

    def new_transaction(self, values):
        """
        :param values: Product values
        :type values: dict
        :return True is successful, False is failed
        """

        required = ['product_id', 'name', 'address', 'date', 'description', 'status']
        if not all(value in values for value in required):
            return False
        else:
            self.__transactions = {
                'product_id': values['product_id'],
                'name': values['name'],
                'address': values['address'],
                'date': values['date'],
                'description': values['description'],
                'status': values['status'],
            }
            return True

    @property
    def last_block(self):
        return self.chain[-1]

    @staticmethod
    def hash(block_string):
        """
        Creates a SHA-256 hash of a Block
        :param block_string: Block to json
        """

        # We must make sure that the Dictionary is Ordered, or we'll have inconsistent hashes
        return hashlib.sha256(block_string).hexdigest()

    def proof_of_work(self, block, modify=False):
        """
        Simple Proof of Work Algorithm:
         - Find a number p' such that hash(pp') contains leading 4 zeroes
         - Where p is the previous proof, and p' is the new proof

        :param modify: the type of operation
        :param block: <dict> new Block
        :return: <int>
        """
        block_string = json.dumps(block).encode()
        _hash = self.hash(block_string)
        self.proof = 0
        if modify is False:
            while True:
                new_block_flag, current_hash = self.valid_proof(self.proof, _hash)
                print(self.proof)
                if new_block_flag:
                    break
                self.proof += 1
        else:
            while True:
                modify_block_flag, current_hash = self.valid_proof(self.proof, _hash)
                if self.proof % 10000 == 0:
                    self.__modify_count += self.proof
                    if self.__modify_count > MAX_COUNT:
                        return None
                print(self.proof)
                if modify_block_flag is True:
                    break
                self.proof += 1

        return current_hash

    @staticmethod
    def valid_proof(proof, _hash):
        """
        Validates the Proof
        :param proof: <int> Current Proof
        :param _hash: <str> The hash of the New Block
        :return: <bool> True if correct, False if not.
        """

        guess = '{0}{1}'.format(proof, _hash).encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000", guess_hash

    def add_block(self, block):
        """
        :param block: new block
        :type block: dict
        """
        if block is None:
            return False

        self.chain.append(block)
        self.__transactions = {}

    def full_chain(self):
        response = {
            'chain': self.chain,
            'length': len(self.chain),
        }
        return jsonify(response), 200

    def modify_block(self, transactions):
        """
        :param transactions: modified transaction information
        :type transactions: dict
        """
        chain_index = transactions['index']
        block_list = []
        block = self.chain[chain_index - 1]
        del transactions['index']
        block['transactions'] = transactions
        block, current_hash = self.__new_block_for_modify(block)
        if block is None:
            return None
        block_list.append(block)
        self.__modify_count = self.proof
        for index in range(chain_index, len(self.chain)):
            block = self.chain[index]
            block['previous_hash'] = current_hash
            block, current_hash = self.__new_block_for_modify(block)
            if block is None:
                return None
            block_list.append(block)
        modify_dict = {'index': chain_index,
                       'blocks': block_list}
        return modify_dict

    def get_role(self, product_id):
        global target_index
        for index in range(0, len(self.chain)):
            if product_id == self.chain[index].get('product_id'):
                target_index = index
                continue
            else:
                continue
        return self.chain[target_index].get('status')


# Instantiate the Node
app = Flask(__name__)

# Generate a globally unique address for this node
node_identifier = str(uuid4()).replace('-', '')
