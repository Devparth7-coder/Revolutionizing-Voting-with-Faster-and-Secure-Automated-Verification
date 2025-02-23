import hashlib
import time
from models import store_vote

# Simple in-memory blockchain list for MVP
blockchain = []

def compute_hash(index, timestamp, data, previous_hash):
    block_string = f"{index}{timestamp}{data}{previous_hash}"
    return hashlib.sha256(block_string.encode()).hexdigest()

def create_genesis_block():
    index = 0
    timestamp = time.time()
    data = "Genesis Block"
    previous_hash = "0"
    block_hash = compute_hash(index, timestamp, data, previous_hash)
    return {
        'index': index,
        'timestamp': timestamp,
        'data': data,
        'previous_hash': previous_hash,
        'hash': block_hash
    }

def add_vote_block(voter_id, candidate):
    global blockchain
    if len(blockchain) == 0:
        genesis_block = create_genesis_block()
        blockchain.append(genesis_block)
    
    previous_block = blockchain[-1]
    index = previous_block['index'] + 1
    timestamp = time.time()
    data = {"voter_id": voter_id, "candidate": candidate}
    previous_hash = previous_block['hash']
    block_hash = compute_hash(index, timestamp, str(data), previous_hash)
    block = {
        'index': index,
        'timestamp': timestamp,
        'data': data,
        'previous_hash': previous_hash,
        'hash': block_hash
    }
    blockchain.append(block)
    # Optionally store the vote in the database
    store_vote(voter_id, candidate)
    return block

def get_vote_counts():
    counts = {}
    for block in blockchain[1:]:  # Skip genesis block
        candidate = block['data']['candidate']
        counts[candidate] = counts.get(candidate, 0) + 1
    return counts
