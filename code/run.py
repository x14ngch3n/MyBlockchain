from myblockchain import run_init, Nodes, node_num, round_times, evil_Blockchain
from threading import Thread, Semaphore
import time

curr_round = 1


def run_node(node, cons_sem, add_sem, mutex, attack_mode):
    """
    每一轮次开始前，先共识，再尝试生成新块，再更新到统一的区块链列表中。
    通过标志位判断为分叉攻击（1）或是自私挖矿攻击（2），从而执行不同的轮次操作
    """
    global curr_round
    # 分叉攻击
    if attack_mode == 1:
        # 诚实节点的操作
        if not node.is_evil:
            while True:
                # 等待主线程释放轮次开始的信号量
                cons_sem.acquire()
                # 进行节点共识，mutex用于实现对全局变量访问的互斥操作
                mutex.acquire()
                node.concensus()
                mutex.release()
                # 尝试生成新的区块
                transactions = 'round:' + str(curr_round) + ' node:' + str(
                    node.address)
                add_sem.acquire()
                mutex.acquire()
                # 通过增加q的倍数来提高恶意节点的算力
                for i in range(2):
                    if node.Blockchain.add_newblock(transactions):
                        break
                mutex.release()
                # 节点和全局区块链列表指向同一个blockchain class，所以不需要额外的扩散操作
        # 恶意节点的操作
        else:
            node.evil_Blockchain = evil_Blockchain
            while True:
                # 等待主线程释放轮次开始的信号量
                cons_sem.acquire()
                # 尝试在恶意区块链上生成新的区块
                add_sem.acquire()
                transactions = '[!!!evil!!!]round:' + str(
                    curr_round) + ' node:' + str(node.address)
                mutex.acquire()
                node.evil_Blockchain.add_newblock(transactions)
                mutex.release()
    # 自私挖矿攻击
    elif attack_mode == 2:
        while True:
            # 等待主线程释放轮次开始的信号量
            cons_sem.acquire()
            # 进行节点共识，mutex用于实现对全局变量访问的互斥操作
            mutex.acquire()
            node.concensus()
            mutex.release()
            # 尝试生成新的区块
            transactions = 'round:' + str(curr_round) + ' node:' + str(
                node.address)
            my_transactions = '[!!!selfish!!!]round:' + str(
                curr_round) + ' node:' + str(node.address)
            add_sem.acquire()
            mutex.acquire()
            node.Blockchain.add_newblock(transactions)
            node.evil_Blockchain.add_newblock(my_transactions)
            mutex.release()
            # 节点和全局区块链列表指向同一个blockchain class，所以不需要额外的扩散操作


def main():
    """
    主函数，进行初始化和控制轮次
    """
    # 初始化线程和信号量
    Threads = []
    cons_sems = []
    add_sems = []
    mutex = Semaphore(1)
    for i in range(node_num):
        cons_sems.append(Semaphore(0))
        add_sems.append(Semaphore(0))
    # 初始化全局节点和区块链列表
    run_init()
    # 启动线程
    for i in range(node_num):
        t = Thread(target=run_node,
                   args=(
                       Nodes[i],
                       cons_sems[i],
                       add_sems[i],
                       mutex,
                       1,
                   ))
        t.setDaemon(True)
        t.start()
        Threads.append(t)

    # 释放信号量来控制轮次
    global curr_round
    for curr_round in range(1, round_times + 1):
        print('-' * 20 + str(curr_round) + '-' * 20)
        # 所有节点进行共识
        for i in range(node_num):
            cons_sems[i].release()
        time.sleep(0.5)
        # 所有节点进行挖矿
        for i in range(node_num):
            add_sems[i].release()
        time.sleep(0.5)
        # 打印每一轮节点信息
        for i in range(node_num):
            print(Nodes[i].Blockchain.get_index())


if __name__ == "__main__":
    main()
