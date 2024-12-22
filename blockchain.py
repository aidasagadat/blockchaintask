































































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
