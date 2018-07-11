import hashlib
import json
from time import time
from urllib.parse import urlparse
from uuid import uuid4

import requests
from flask import Flask, jsonify, request


class Blockchain:
    def __init__(self):
        self.current_actions = []
        self.chain = []
        self.transactions = {}
        self.nodes = set()
        self.proof = 0

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
            if not self.valid_proof(last_block['proof'], block['proof'], last_block_hash):
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
            block = {
                'index': index,
                'timestamp': time(),
                'transactions': self.transactions,
            }
            if index == 1:
                current_hash = blockchain.proof_of_work(block)
                previous_hash = '0'
            else:
                current_hash = blockchain.proof_of_work(block)
                previous_hash = self.last_block['previous_hash']

            block['proof'] = self.proof
            block['current_hash'] = current_hash
            block['previous_hash'] = previous_hash
            # Reset the current list of transactions
            self.transactions = {}

            self.chain.append(block)
            return block

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
            self.transactions = {
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

    def proof_of_work(self, last_block):
        """
        Simple Proof of Work Algorithm:
         - Find a number p' such that hash(pp') contains leading 4 zeroes
         - Where p is the previous proof, and p' is the new proof

        :param last_block: <dict> last Block
        :return: <int>
        """

        last_proof = last_block['proof']
        block_string = json.dumps(last_block, sort_keys=True).encode()
        last_hash = self.hash(block_string)
        self.proof = 0

        while True:
            flag, current_hash = self.valid_proof(last_proof, self.proof, last_hash)
            self.proof += 1
            if flag is True:
                break
        return current_hash

    @staticmethod
    def valid_proof(last_proof, proof, last_hash):
        """
        Validates the Proof
        :param last_proof: <int> Previous Proof
        :param proof: <int> Current Proof
        :param last_hash: <str> The hash of the Previous Block
        :return: <bool> True if correct, False if not.
        """

        guess = '{0}{1}{2}'.format(last_proof, proof, last_hash).encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000", guess_hash

    @staticmethod
    def add_block(values):
        block = blockchain.new_block(values)

        if block is not None:
            return True
        else:
            return False

    @staticmethod
    def full_chain():
        response = {
            'chain': blockchain.chain,
            'length': len(blockchain.chain),
        }
        return jsonify(response), 200


# Instantiate the Node
app = Flask(__name__)

# Generate a globally unique address for this node
node_identifier = str(uuid4()).replace('-', '')

# Instantiate the Blockchain
blockchain = Blockchain()


@app.route('/nodes/register', methods=['POST'])
def register_nodes():
    values = request.get_json()

    nodes = values.get('nodes')
    if nodes is None:
        return "Error: Please supply a valid list of nodes", 400

    for node in nodes:
        blockchain.register_node(node)

    response = {
        'message': 'New nodes have been added',
        'total_nodes': list(blockchain.nodes),
    }
    return jsonify(response), 201


@app.route('/nodes/resolve', methods=['GET'])
def consensus():
    replaced = blockchain.resolve_conflicts()

    if replaced:
        response = {
            'message': 'Our chain was replaced',
            'new_chain': blockchain.chain
        }
    else:
        response = {
            'message': 'Our chain is authoritative',
            'chain': blockchain.chain
        }

    return jsonify(response), 200
