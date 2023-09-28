from time import time
STRAIGHT = 10
DIAGONAL = 14
t_addition = lambda t1, t2: (t1[0] + t2[0], t1[1] + t2[1])
t_subtraction = lambda t1, t2: (t1[0] - t2[0], t1[1] - t2[1])


class Node:
    def __init__(self, coords, cfrom=None, f_cost=None, moves=-1):
        self.cfrom = cfrom  # cfrom should be a Node or None
        self.f_cost = f_cost
        self.moves = moves
        self.coords = coords


class PriorityQueue:
    def __init__(self):
        self.arr = []

    def __repr__(self):
        return f"{self.arr}"

    def empty(self):
        return len(self.arr) != 0

    def sort_arr(self):
        self.arr.sort(key=lambda x: x[0])

    def insert(self, priority, value):
        vp = (priority, value)
        self.arr.append(vp)
        self.sort_arr()

    def pop(self):
        return self.arr.pop(0)[1]


class A_Star:
    def __init__(self, arr, start, end, blockers=9):
        self.start = start
        self.end = end
        self.arr = arr
        self.blockers = blockers
        # print(type(self.start), type(self.end))
        self.arr_data = {
            (i, j): Node((i, j))
            for i in range(len(self.arr))
            for j in range(len(arr[i]))
        }
        self.moves = 1
        # print(self.arr_data)
        self.arr_data[self.start] = Node(None, None, 0)
        self.queue = PriorityQueue()

    def find_replace(self, arr, f, r):
        for i in range(len(arr)):
            if arr[i] == f:
                arr[i] = r
        return arr

    def get_moves(self, head: Node):
        output = 0
        output2 = []
        chead = head
        while chead.coords != self.start:
            # print(output, chead)
            output += 1

            output2.append(chead.coords)
            chead = chead.cfrom
            if not chead:
                break
        return (output, self.find_replace(output2, None, self.start))

    def print_arr(self):
        for r in self.arr:
            for c in r:
                print(c, end=" ")
            print()

    def in_bound(self, t):
        print(t, len(self.arr[0]))
        return not (
            (t[0] < 0 or t[0] >= len(self.arr))
            or (t[1] < 0 or t[1] >= len(self.arr[0]))
            or (self.arr[t[0]][t[1]] == self.blockers)
        )
        # if not (
        #     (t[0] < 0 or t[0] > len(self.arr)) or (t[1] < 0 or t[1] > len(self.arr[0]))
        # ):
        #     return False
        # return not (self.arr[t[0]][t[1]] == self.blockers)
    def dist_from(self, t1, t2):
        x1, y1 = t1
        x2, y2 = t2
        x_dist, y_dist = abs(x1 - x2), abs(y1 - y2)
        # print(x_dist, y_dist)
        return DIAGONAL * min(x_dist, y_dist) + abs(x_dist - y_dist) * 10


    def convert(self, t):
        output = [None, None]
        for i in range(2):
            if t[i] == 0:
                output[i] = 0
                continue
            if t[i] < 0:
                output[i] = -1
            if t[i] > 0:
                output[i] = 1
        return tuple(output)

    def f_cost_list(self, l: list[tuple]):
        output = []
        for i in l:
            output.append(self.convert(i))
        sum_ = 0
        for i in output:
            sum_ += self.get_f_cost(i)

        return sum_

    def get_f_cost(self, t):
        if self.in_bound(t):
            return self.dist_from(self.start, t) + self.dist_from(self.end, t)
        else:
            return 0

    def explore(self, t):
        flag = False
        f_costs = {}
        x, y = t
        # print("HOLDUP", t, self.end)
        if t == self.end:
            flag = True
            print("HERE")
            print(x, y)
        steps, path = self.get_moves(self.arr_data[(x, y)])
        print(x, y, path, path)
        for i in range(x - 1, x + 2):
            for j in range(y - 1, y + 2):
                if (i, j) != (x, y):
                    if self.in_bound((i, j)):
                        curnode = self.arr_data[(i, j)]
                        if (
                            curnode.moves == -1
                            or curnode.moves > steps
                            and curnode not in path
                        ):
                            curnode.moves = steps
                            curnode.cfrom = self.arr_data[(x, y)]
                            curnode.f_cost = self.get_f_cost((i, j))
                            print(curnode.f_cost, curnode.coords)
                            curnode.coords = (i, j)
                            f_costs[curnode.f_cost] = curnode

        self.moves += 1
        if flag:
            return self.get_moves(self.arr_data[self.end])
        for k, v in f_costs.items():
            self.queue.insert(k, v)
            # print(self.queue)

        return self.explore(self.queue.pop().coords)


if __name__ == "__main__":
    a_star = A_Star(
        [[1, 0, 0, 0], [0, 9, 0, 0], [0, 9, 0, 0], [9, 9, 0, 0], [2, 0, 0, 0]],
        (0, 0),
        (4, 0),
    )
    score, path = a_star.explore((0, 0))
    print(f"solution is {path[::-1]};")

    print(f"took {a_star.moves} iterations to find solution")
    # print(a_star.get_moves(a_star.arr_data[(0, 1)]))
    a_star.print_arr()
