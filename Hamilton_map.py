# coding: utf-8
import numpy as np


"""
https://zhuanlan.zhihu.com/p/47584758
哈密顿通图

P类问题：23*37易得。复杂问题在多项式时间内解决
NP类问题：分解一个大质数为两个质数相乘难得，比如分解740914799。复杂问题不能确定在多项式时间内解决。
NP-hard是比NP问题更难的问题，比如围棋

算法流程：
1. 分为两个栈：访问栈与路径栈
2. 选定起始点，在当前顶点压入两个栈中
3. 列出与当前顶点连通的顶点，随即选一个相通的点。有两种情况。
    1. 如果选的点不在访问栈中，则选择此点作为当前顶点。重复3。
    2. 如果选的点已经在访问栈中，则不选此点作为当前顶点，选择其他点。两种情况。
        1. 有连通点不在访问栈中，则选择此点作为当前顶点。重复3。
        2. 如果所有连通的点都在访问栈中，那么需要判断是否所有点都在路径栈中
            1. 如果全都在，那么就结束。当前路径栈为当前图的哈密顿通图。
            2. 如果不是全都在，则需要返回上一顶点（父顶点），并从访问栈和路径栈中删除顶点。重复上一步。
"""


def get_index(i, j, G):
    num = 0
    # 前i行有多少个0
    for a in range(i):
        num += G[a].count("0")
    # 当前行多少个0
    for b in range(j):
        if G[i][b] == "0":
            num += 1
    # i*列数+j表示当前顶点位置。但是由于位置可能为0，所以需要统计0，并减去num
    return i * len(G) + j - num


def get_graph(G):
    """
    转换为关系图
    G: 形象的1、0图，表示当前位置有无顶点
    EG: 顶点间的关系。比如[[1,6],[2,0]]，表示第0个顶点与第1个顶点和第6个顶点是连通的，第1个顶点与第2个顶点和第0个顶点是连通的。从0开始计数
    """
    EG = []
    # 遍历每个位置
    for i in range(len(G)):
        for j in range(len(G[i])):
            # 如果当前位置不存在顶点，就跳过
            if G[i][j] == "0":
                continue

            # 统计当前位置四周的连通的顶点（不在边界时）
            side_lst = []

            # 不在右边界且邻边位置有顶点，当前点的右边
            if j + 1 <= len(G[i]) - 1 and G[i][j + 1] == "1":
                index = get_index(i, j + 1, G)
                side_lst.append(index)
            # 不在左边界且邻边位置有顶点，当前点的左边
            if j - 1 >= 0 and G[i][j - 1] == "1":
                # 得到连通的顶点序号
                index = get_index(i, j - 1, G)
                side_lst.append(index)
            # 不在下边界且邻边位置有顶点，当前点的下边
            if i + 1 <= len(G) - 1 and G[i + 1][j] == "1":
                index = get_index(i + 1, j, G)
                side_lst.append(index)
            # 不在上边界且邻边位置有顶点，当前点的上边
            if i - 1 >= 0 and G[i - 1][j] == "1":
                index = get_index(i - 1, j, G)
                side_lst.append(index)
            # 得到当前点的所有连通点
            EG.append(side_lst)
    # len(EG)应该等于顶点个数
    return EG


def dfs(graph, path, used, step):
    # 如果遍历完了所有点，则输入
    if step == len(graph):
        print(path)
        return True
    else:
        # 按顺序遍历所有顶点
        for i in range(len(graph)):
            # 满足两个条件：1. 不在访问栈中 2. 当前遍历的点与当前顶点是连通的
            # path[step-1]表示当前顶点，graph[step-1][i]表示连通的点
            if not used[i] and graph[path[step - 1]][i] == 1:
                # 将遍历的点放入访问栈和路径栈中
                used[i] = True
                path[step] = i
                # 继续深度遍历
                if dfs(graph, path, used, step + 1):
                    return True
                # 如果遍历失败，则此顶点从访问栈和路径栈取出
                else:
                    used[i] = False
                    path[step] = -1
    # 此方法无解
    return False


def main(graph, v):
    # 访问栈与路径栈
    used = []
    path = []
    # 顶点长度的列表
    for _ in range(len(graph)):
        used.append(False)
        path.append(-1)
    # 将起始点作为当前顶点
    used[v] = True
    path[0] = v
    # 开始dfs
    dfs(graph, path, used, 1)


def get_mat(graph):
    # 把结果转化为2维列表，邻接矩阵。矩阵形状为顶点个数x顶点个数
    # 每一行表示每个顶点与其连通的顶点。
    # 比如[[0,1,0,1], [1,0,0,1], [1,0,0,0], [0,1,0,0]]表示第0个顶点与第1个和第4个顶点有连接，第1个顶点与第0个和第4个顶点有连接，第2个顶点与第1个顶点有连接，第3个顶点与第1个顶点有连接。
    # P.S 从0开始计数，这个例子并不严谨，谨作理解
    result = [[0] * len(graph) for _ in range(len(graph))]
    for i in range(len(graph)):
        for j in graph[i]:
            result[i][j] = 1
    return result


"""
原图
0   1   2   3   4   5
6       7   8       9
10  11  12  13  14  15
16      17  18      19
20  21  22  23  24  25
"""
# 1 表示顶点，即可以走的路；0 表示无路可走
map_lst = ["111111", "101101", "111111", "101101", "111111", "000000"]
# 转换为关系图
G = get_graph(map_lst)
# 转换为邻接矩阵
map_mat = get_mat(G)
# 起始点
SP = 14
# dfs
main(map_mat, SP)
# [14, 13, 8, 3, 4, 5, 9, 15, 19, 25, 24, 23, 18, 17, 22, 21, 20, 16, 10, 6, 0, 1, 2, 7, 12, 11]
