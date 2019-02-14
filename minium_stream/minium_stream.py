# coding: utf-8
import numpy as np
from pprint import pprint

"""
https://www.bilibili.com/video/av40682708/?spm_id_from=333.788.videocard.1
最短路
v1：起点；v6：终点
距离
v1->v2: 4
v1->v3: 3
v2->v4: 3
v2->v5: 2
v3->v5: 3
v4->v6: 2
v5->v6: 1

净流量=流出该节点量-流入该节点量
起点只有流出，平衡值为1；终点只有流入，平衡值为-1；其他节点为0.
实际距离
v1: 4*x12+3*x13
v2: 3*x24+2*x25-4*x12
v3: 3*x35-3*x13
v4: 2*x46-3*x24
v5: 1*x56-2*x25-3*x35
v6: -2*x46-1*x56

xab为1或0，表示是否经过此路

最大流
https://blog.csdn.net/tengweitw/article/details/17766133
容量允许的条件下，从源点（起点）到汇点（终点）能通过的最大流量
1. Ford-Fulkerson 
    1. 迭代
    2. 对图中所有顶点对的流（边）大小清零，此时网络流大小也为0。
    3. 每次迭代中，寻找一条“增广路径”来增加流的值
        1. 增广路径：从源点s到汇点t的一条路径。沿着这条路径可以增加更多的流
    4. 不断迭代，直到无法再找到增广路径为止，此时从源点s到汇点t的所有路径中必然至少有一条边的满边
        1. 满边：边的流的大小=边的容量大小
    5. 思想
        1. f(u,v)>0, 残留网络中包含一条容量为f(u,v)的边(v,u)
        2. f(u,v)<c(u,v)，残留网络中包含一条容量为c(u,v)-f(u,v)的边(u,v)
        3. 残留网络中，用广义图搜索算法来寻找增广路径
"""


def search(dist1, vertex):
    # 队列，边的个数，N个顶点的图，任意两点有连接，边数最多为N*(N-1)
    queue = [-1] * N * (N - 1)
    # 判断当前点是否访问过
    flag = [0] * N
    front = rear = temp = 0
    # 源点入队
    queue[rear] = 0
    flag[0] = 1
    rear += 1

    # 队列不为空
    while queue[front] != -1:
        # 队首
        temp = queue[front]
        for i in range(N):
            # 广度搜索法。找到与该点（队首点）所有连通的点
            if dist1[temp][i] != 0 and flag[i] == 0:
                # 队尾进行赋值，并且指针后移
                queue[rear] = i
                rear += 1
                # 标记该点已访问
                flag[i] = 1
                # 顶点序号为队首值
                vertex[i] = temp
        # 队首后移
        front += 1
        # 遍历到最后一个节点
        if front == N:
            break
    # 没有找到路径
    if queue[rear - 1] != 5:
        return 0
    # 有路径
    return 1


def modify(d, dist1, vertex, s, t, flow):
    """
    vertex: 记录顶点
    s: 源点
    t: 汇点
    i表示当前顶点序号，j与其相连的顶点序号，dist1表示ij两点之间的流量（距离/权重）
    """
    min_ = 10000  # 记录找到路径的所能通过的最大流

    # 以汇点作为起始点。
    i = vertex[t]
    j = t
    # 路径所含边的最大流量值中的最小值
    # 从汇点遍历回源点
    while j != s:
        """
        3->5
        1->3
        0->1
        """
        min_ = min(dist1[i][j], min_)  # 记录路径中的最小值
        j = i  # 相连的顶点变为当前顶点
        i = vertex[i]  # 相连顶点的相连顶点变为下一次的相连顶点

    # 回到汇点
    i = vertex[t]
    j = t
    # 记录此路径的最大流量。2+1+1
    flow += min_
    # 重复上诉操作，减去当前路径找到的最小流量
    while j != s:
        # 如果两点间存在流量（有通路），将转置位置（矩阵转置后的位置）也赋上相同的值
        if dist1[i][j] > 0:
            dist1[j][i] = dist1[i][j]
        # 两点间的流量减去当前路径的最大流量
        dist1[i][j] -= min_
        # 原始流网络中，两点流量赋值为当前路径的最大流量-对应转置位置
        d[i][j] += min_ - d[j][i]
        # 原始流网络中，如果两点流量为负，则对应转置位置变为正，且将原位置设为0
        if d[i][j] < 0:
            d[j][i] = -d[i][j]
            d[i][j] = 0

        j = i
        i = vertex[i]

    print("原始流网络矩阵:\n")
    pprint(d)

    print("残留网络矩阵:\n")
    pprint(dist1)

    return flow


def FF(d, dist1):
    # 初始化顶点
    vertex = [0] * N

    flow = 0
    # 判断是否有增广路径
    while search(dist1, vertex):
        flow = modify(d, dist1, vertex, 0, 5, flow)
        print("\n")
    print("最大流为{}".format(flow))


# 6个顶点
N = 6
# 原始网络=初始残留网络
dist1 = [
    [0, 2, 3, 0, 0, 0],  # 第1个顶点与第2个顶点的距离为2，第3个顶点的距离为3
    [0, 0, 0, 3, 1, 0],  # 第2个顶点与第4个顶点的距离为3，第1个顶点的距离为1
    [0, 0, 0, 1, 1, 0],  # 第3个顶点与第4个顶点的距离为1，第5个顶点的距离为1
    [0, 0, 0, 0, 0, 2],  # 第4个顶点与第6个顶点的距离为2
    [0, 0, 0, 0, 0, 3],  # 第5个顶点与第6个顶点的距离为3
    [0, 0, 0, 0, 0, 0],
]
d = [[0] * N for _ in range(N)]
FF(d, dist1)
