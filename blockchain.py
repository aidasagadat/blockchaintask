































































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