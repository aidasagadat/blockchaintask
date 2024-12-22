import time

def right_rotate(value, shift):
    return (value >> shift) | (value << (32 - shift)) & 0xFFFFFFFF

def sha256(data):
    k = [
        0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5, 0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
        0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3, 0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
        0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc, 0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
        0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7, 0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
        0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13, 0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,
        0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3, 0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
        0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0b5d9, 0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3,
        0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208, 0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2
    ]
    
    def pad_data(data):
        length = len(data) * 8
        data += b'\x80'
        while len(data) % 64 != 56:
            data += b'\x00'
        data += length.to_bytes(8, 'big')
        return data

    def message_schedule(data):
        w = list(data)
        for i in range(16, 64):
            s0 = right_rotate(w[i-15], 7) ^ right_rotate(w[i-15], 18) ^ (w[i-15] >> 3)
            s1 = right_rotate(w[i-2], 17) ^ right_rotate(w[i-2], 19) ^ (w[i-2] >> 10)
            w.append((w[i-16] + s0 + w[i-7] + s1) & 0xFFFFFFFF)
        return w
        
    def compress_block(h, w):
        a, b, c, d, e, f, g, h_ = h
        for i in range(64):
            t1 = (h_ + (right_rotate(e, 6) ^ right_rotate(e, 11) ^ right_rotate(e, 25)) + ((e & f) ^ (~e & g)) + k[i] + w[i]) & 0xFFFFFFFF
            t2 = (right_rotate(a, 2) ^ right_rotate(a, 13) ^ right_rotate(a, 22) + ((a & b) ^ (a & c) ^ (b & c))) & 0xFFFFFFFF
            h_ = g
            g = f
            f = e
            e = (d + t1) & 0xFFFFFFFF
            d = c
            c = b
            b = a
            a = (t1 + t2) & 0xFFFFFFFF
        return [(a + h[0]) & 0xFFFFFFFF, (b + h[1]) & 0xFFFFFFFF, (c + h[2]) & 0xFFFFFFFF,
                (d + h[3]) & 0xFFFFFFFF, (e + h[4]) & 0xFFFFFFFF, (f + h[5]) & 0xFFFFFFFF,
                (g + h[6]) & 0xFFFFFFFF, (h_ + h[7]) & 0xFFFFFFFF]
        
    h = [0x6a09e667, 0xbb67ae85, 0x3c6ef372, 0xa54ff53a, 0x510e527f, 0x9b05688c, 0x1f83d9ab, 0x5be0cd19]
    data = pad_data(data)
    for i in range(0, len(data), 64):
        block = data[i:i+64]
        w = message_schedule([int.from_bytes(block[j:j+4], 'big') for j in range(0, 64, 4)])
        h = compress_block(h, w)
    return ''.join(f'{x:08x}' for x in h)






























































class Transaction:
    def __init__(self, sender, receiver, amount):
        self.sender = sender
        self.receiver = receiver
        self.amount = amount



    def __str__(self):
        return f"{self.sender} -> {self.receiver}: {self.amount}"

def create_merkle_root(transactions):
    if len(transactions) == 0:
        return "0"
    tx_hashes = [sha256(str(tx).encode('utf-8')) for tx in transactions]
    while len(tx_hashes) > 1:
        tx_hashes = [sha256((tx_hashes[i] + tx_hashes[i+1]).encode('utf-8')) for i in range(0, len(tx_hashes), 2)]
    return tx_hashes[0]


class Block:
    def __init__(self, previous_hash, timestamp, transactions):
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.transactions = transactions
        self.merkle_root = create_merkle_root(transactions)
        self.hash = self.hash_block()

    def hash_block(self):
        block_data = f"{self.previous_hash}{self.timestamp}{self.merkle_root}"
        return sha256(block_data.encode('utf-8'))
    


class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]
        self.pending_transactions = []


    def create_genesis_block(self):
        return Block("0", time.time(), [])

    def mine_block(self):
        block = Block(self.chain[-1].hash, time.time(), self.pending_transactions)
        self.chain.append(block)
        self.pending_transactions = []

    def add_transaction(self, sender, receiver, amount):
        transaction = Transaction(sender, receiver, amount)
        self.pending_transactions.append(transaction)

    def validate_blockchain(self):
        for i in range(1, len(self.chain)):
            if self.chain[i].hash != self.chain[i].hash_block():
                return False
            if self.chain[i].previous_hash != self.chain[i-1].hash:
                return False
        return True

    def print_blockchain(self):
        for i, block in enumerate(self.chain):
            print(f"Block {i} Hash: {block.hash}")
            print(f"Previous Hash: {block.previous_hash}")
            print(f"Merkle Root: {block.merkle_root}")
            print(f"Timestamp: {block.timestamp}\n")


blockchain = Blockchain()
blockchain.add_transaction("Alice", "Bob", 100)
blockchain.mine_block()
blockchain.add_transaction("Bob", "Charlie", 50)
blockchain.mine_block()

blockchain.add_transaction("Aidaa", "Adiya", 30)
blockchain.mine_block()

blockchain.add_transaction("Aida", "Amina", 30)
blockchain.mine_block()

blockchain.add_transaction("Amina", "Adiya", 30)
blockchain.mine_block()

blockchain.add_transaction("Lala", "Lalalala", 30)
blockchain.mine_block()

blockchain.add_transaction("Jaja", "Jajajaja", 30)
blockchain.mine_block()

blockchain.add_transaction("Nana", "Nananana", 30)
blockchain.mine_block()

blockchain.add_transaction("Uaua", "Uauauaua", 30)
blockchain.mine_block()

blockchain.add_transaction("Haha", "Hahahaha", 30)
blockchain.mine_block()

blockchain.print_blockchain()

print("Blockchain Valid: ", blockchain.validate_blockchain())
