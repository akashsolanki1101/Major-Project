from flask import Flask, request
import json
from Utils.blockchain import Blockchain
from Utils.block import Block
import requests

app = Flask(__name__)

# blockchain 
blockchain = Blockchain()

# endpoint to mine the block
@app.route('/mine', methods=['GET'])
def mine_block():
    ID =  request.get_json()['id']
    block = blockchain.mine_block()

    data = {
        "block":block.toJson(),
        "id":ID
    }

    jsonify_data = json.dumps(data)

    url = "http://127.0.0.1:8000/add_block"
    res = requests.post(url, json=jsonify_data)
    
    if res.status_code == 200:
        print("Block is mined and added to the chain")
        return "success", 200
    else:
        print("Invalid miner")
        return "invalid", 401

# endpoint to validate a transaction
@app.route('/add_block', methods=['POST'])
def validate_and_add():
    data = request.get_json()
    data = json.loads(data)
    block_data = json.loads(data["block"])

    block = Block(block_data["index"], block_data["data"], block_data["timestamp"], block_data["previous_hash"])
    ID = data["id"]
    is_valid_node = blockchain.validate_node(ID)

    if is_valid_node == True:
        block_added = blockchain.add_block(block)

        if block_added == True:
            return "success", 200
    else:
        return "invalid", 401

# endpoint to print the chain
@app.route('/chain', methods=['GET'])
def print_chain():

    for block in blockchain.chain:
        block.print_data()

    return "success", 200

app.run(debug = True, port=8000)