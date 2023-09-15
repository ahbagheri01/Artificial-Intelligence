import queue

# 1:up
# 2:left
# 3:right
# 4 : down

lst = list(map(int, input().split()))
x_packman, y_packman = lst[0], lst[1]
lst = list(map(int, input().split()))
x_food, y_food = lst[0], lst[1]
lst = list(map(int, input().split()))
row, col = lst[0], lst[1]
matrix = [[] for _ in range(row)]
matrix_path = [[-1 for x in range(col)] for y in range(row)]
def print_table():
    for i in range(row):
        for j in range(col):
            print(matrix_path[i][j],end=" ")
        print("")
    print("")
def h(x, y):
    return abs(x - x_food) + abs(y - y_food)

def put_in_fringe(cost, x, y,direction):
    if x >= row or y >= col or x < 0 or y < 0 or matrix[x][y] == '%' or matrix_path[x][y] != -1:
        return
    fringe.put((cost+h(x,y) ,cost,x,y,direction))
def expand():
    v = fringe.get()
    cost, direction, x, y = v[1], v[4], v[2], v[3]
    matrix_path[x][y] = direction
    if x == x_food and y == y_food:
        return True
    put_in_fringe(cost + 1, x - 1, y,1)
    put_in_fringe(cost + 1, x, y - 1,2)
    put_in_fringe(cost + 1, x, y + 1,3)
    put_in_fringe(cost + 1, x + 1, y,4)
    return False
def print_path(x,y):
    direction = matrix_path[x][y]
    if direction == 0:
        print(x,y)
        return
    if direction == 1:
        print_path(x+1,y)
    elif direction == 2:
        print_path(x,y+1)
    elif direction == 3:
        print_path(x,y-1)
    else:
        print_path(x-1,y)
    print(x,y)
for f in range(row):
    matrix[f] = input()
fringe = queue.PriorityQueue()
heurestic = h(x_packman, x_food)
fringe.put((heurestic, 0, x_packman, y_packman,0))
while not fringe.empty():
    if expand() == True:
        print_path(x_food,y_food)
        break
