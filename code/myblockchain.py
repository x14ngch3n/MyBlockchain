from hashlib import sha256
import time

difficulty = 3
q = 10000
round_times = 5
node_num = 5
evil_num = 2


class Block:
    """
    模拟区块
    """
    def __init__(self, index, timestamp, transactions, prev_hash='0'):
        self.timestamp = timestamp
        self.index = index
        self.transactions = transactions
        self.nonce = 0
        self.prev_hash = prev_hash
        self.hash = self.calc_hash()

    def calc_hash(self):
        """
        计算当前区块的哈希值
        """
        message = str(self.index) + str(self.timestamp) + str(
            self.transactions) + str(self.nonce)
        return sha256(message.encode()).hexdigest()

    def mine(self):
        """
        按照设定的难度挖矿，若成功则返回True
        """
        global difficulty, q
        while not self.hash.startswith('0' * difficulty):
            self.nonce = self.nonce + 1
            if self.nonce <= q:
                self.hash = self.calc_hash()
            else:
                return False
        return True

    def __str__(self):
        """
        打印信息
        """
        return str(self.__dict__)


class Blockchain:
    """
    模拟区块链
    """
    def __init__(self):
        self.blocks = []
        self.create_genesisblock()

    def get_index(self):
        """
        获取当前区块链的长度
        """
        return len(self.blocks)

    def create_genesisblock(self):
        """
        创建创世区块
        """
        self.blocks.append(
            Block(self.get_index(), time.time(), 'genesis block'))

    def get_lastblock(self):
        """
        获取当前区块链最后一个块
        """
        return self.blocks[self.get_index() - 1]

    def add_newblock(self, transactions):
        """
        增加新的区块，成功返回True
        """
        newblock = Block(self.get_index(), time.time(), transactions)
        if newblock.mine():
            newblock.prev_hash = self.get_lastblock().hash
            newblock.calc_hash()
            self.blocks.append(newblock)
            return True
        return False

    def validate(self):
        """
        验证是否为合法区块链，成功返回True
        """
        global difficulty, q
        for i in range(1, len(self.blocks)):
            # 获取当前块和前一块的信息
            curr_block = self.blocks[i]
            prev_block = self.blocks[i - 1]
            # 满足哈希条件，验证哈希值和生成难度
            if curr_block.prev_hash != prev_block.hash or curr_block.hash != curr_block.calc_hash(
            ) or curr_block.nonce > q or not curr_block.hash.startswith(
                    '0' * difficulty):
                return False
            return True

    def __str__(self):
        """
        打印信息
        """
        for i in range(len(self.blocks)):
            print(self.blocks[i])
        return str(self.__dict__)


class Node:
    """
    模拟节点
    """
    global Nodes

    def __init__(self, address, is_evil=False):
        self.address = address
        self.Blockchain = Blockchain()
        self.is_evil = is_evil

    def concensus(self):
        """
        进行区块链共识协议，从所有节点中选取最长的链同步过来
        """
        max_length = self.Blockchain.get_index()
        max_blockchain = Blockchain()
        for blockchain in Blockchains:
            if blockchain.validate() and blockchain.get_index() > max_length:
                max_length = blockchain.get_index()
                max_blockchain = blockchain

        # 同步区块
        if max_blockchain.get_index() == 1:
            pass
        else:
            self.Blockchain.blocks = []
            for block in max_blockchain.blocks:
                self.Blockchain.blocks.append(block)
            # print(self.Blockchain.get_index())

    def attack(self):
        """
        恶意节点新增一条不进行共识的区块链用于攻击
        """
        self.evil_Blockchain = Blockchain()

    def __str__(self):
        """
        打印信息
        """
        print(self.local_blockchain)
        return str(self.__dict__)


Nodes = []
evil_Nodes = []
Blockchains = []
evil_Blockchain = Blockchain()


def run_init():
    """
    初始化全局变量
    """
    # 初始化全局的正常节点列表和恶意节点列表
    for i in range(node_num):
        if i < evil_num:
            evil_Nodes.append(Node(i))
        else:
            Nodes.append(Node(i))
    # 初始化全局的区块链列表
    for i in range(node_num):
        Blockchains.append(Nodes[i].Blockchain)
