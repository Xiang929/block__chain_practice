import hashlib
import json
from time import time
from urllib.parse import urlparse
from uuid import uuid4

import requests
from flask import Flask, jsonify, request

MAX_COUNT = 5000000


class Blockchain:
    __slots__ = ('chain', '__transactions', 'nodes', 'proof', '__modify_count')

    def __init__(self):
        self.chain = []
        self.__transactions = {}
        self.nodes = set()
        self.proof = 0
        self.__modify_count = 0

    def register_node(self, address):
        """
        Add a new node to the list of nodes
        :param address: Address of node. Eg. 'http://192.168.0.5:5000'
        """

        parsed_url = urlparse(address)
        if parsed_url.netloc:
            self.nodes.add(parsed_url.netloc)
        elif parsed_url.path:
            # Accepts an URL without scheme like '192.168.0.5:5000'.
            self.nodes.add(parsed_url.path)
        else:
            raise ValueError('Invalid URL')

    def valid_chain(self, chain):
        """
        Determine if a given blockchain is valid
        :param chain: A blockchain
        :return: True if valid, False if not
        """

        last_block = chain[0]
        current_index = 1

        while current_index < len(chain):
            block = chain[current_index]
            print(last_block)
            print(block)
            print("\n-----------\n")
            # Check that the hash of the block is correct
            last_block_hash = self.hash(last_block)
            if block['previous_hash'] != last_block_hash:
                return False

            # Check that the Proof of Work is correct
            if not self.valid_proof(block['proof'], last_block_hash):
                return False

            last_block = block
            current_index += 1

        return True

    def resolve_conflicts(self):
        """
        This is our consensus algorithm, it resolves conflicts
        by replacing our chain with the longest one in the network.
        :return: True if our chain was replaced, False if not
        """

        neighbours = self.nodes
        new_chain = None

        # We're only looking for chains longer than ours
        max_length = len(self.chain)

        # Grab and verify the chains from all the nodes in our network
        for node in neighbours:

            response = requests.get('http://{node}/chain'.format(node=node))
            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']

                # Check if the length is longer and the chain is valid
                if length > max_length and self.valid_chain(chain):
                    max_length = length
                    new_chain = chain

        # Replace our chain if we discovered a new, valid chain longer than ours
        if new_chain:
            self.chain = new_chain
            return True

        return False

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
                'proof': self.proof
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

        required = ['number', 'name', 'address', 'date', 'description', 'status']
        if not all(value in values for value in required):
            return False
        else:
            self.__transactions = {
                'number': values['number'],
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
        block_string = json.dumps(block, sort_keys=True).encode()
        self.proof = 0
        if modify is False:
            while True:
                _hash = self.hash(block_string)
                flag, current_hash = self.valid_proof(self.proof, _hash)
                self.proof += 1
                if flag is True:
                    break
        else:
            while True:
                _hash = self.hash(block_string)
                flag, current_hash = self.valid_proof(self.proof, _hash)
                if self.proof % 1000000 == 0:
                    self.__modify_count += self.proof
                    if self.__modify_count > MAX_COUNT:
                        return None
                self.proof += 1
                if flag is True:
                    break
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
        return guess_hash[:6] == "000000", guess_hash

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


# Instantiate the Node
app = Flask(__name__)

# Generate a globally unique address for this node
node_identifier = str(uuid4()).replace('-', '')


@app.route('/nodes/register', methods=['POST'])
def register_nodes():
    values = request.get_json()

    nodes = values.get('nodes')
    if nodes is None:
        return "Error: Please supply a valid list of nodes", 400

    for node in nodes:
        Blockchain.register_node(node)

    response = {
        'message': 'New nodes have been added',
        'total_nodes': list(Blockchain.nodes),
    }
    return jsonify(response), 201


@app.route('/nodes/resolve', methods=['GET'])
def consensus():
    replaced = Blockchain.resolve_conflicts()

    if replaced:
        response = {
            'message': 'Our chain was replaced',
            'new_chain': Blockchain.chain
        }
    else:
        response = {
            'message': 'Our chain is authoritative',
            'chain': Blockchain.chain
        }

    return jsonify(response), 200
