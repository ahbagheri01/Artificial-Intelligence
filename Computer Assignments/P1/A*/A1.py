from collections import defaultdict
import heapq
graph = defaultdict(list)
bad_moves,fringe={},[]
n, m, k = [int(i) for i in input().split()]
for _ in range(m):
    u, v = [int(i) for i in input().split()]
    graph[u].append(v)
    graph[v].append(u)
distance = [-1] * (n + 1)
for i in range(k):
    tri_road = tuple(int(i) for i in input().split())
    if tri_road[:2] in bad_moves:
        bad_moves[tri_road[:2]].add(tri_road[2])
    else:
        bad_moves[tri_road[:2]] = set([tri_road[2]])
def put_in_fringe(node,next_node,i,closed,d):
    if node in bad_moves and i in bad_moves[node]:
        return
    if next_node in bad_moves:
        if next_node in closed and closed[next_node] - 1 <= d:
            return
    else:
        if (-1, i) in closed and closed[(-1, i)] - 1 <= d:
            return
        next_node = (-1,i)
    heapq.heappush(fringe, (d + 1, next_node))
    closed[next_node] = d + 1
def start(start_p,distance,fringe,graph):
    closed = {(-1, start_p): 0}
    heapq.heappush(fringe, (0, (-1, 1)))
    while len(fringe) > 0:
        v = heapq.heappop(fringe)
        d,node = v[0],v[1]
        if d != closed[node]:
            continue
        parent,current_node = node[0],node[1]
        if distance[current_node] == -1:
           distance[current_node] = d
        if current_node == n:
            return
        for i in graph[current_node]:
            put_in_fringe(node,(current_node,i),i,closed,d)
start(1,distance,fringe,graph)
print(distance[n])

