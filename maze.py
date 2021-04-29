from random import shuffle, randrange
import collections
import pygame
import sys

colours = {"BLACK": (0, 0, 0), "WHITE": (255, 255, 255), "RED": (255, 0, 0), "GREEN": (0, 255, 0),
           "YELLOW": (255, 215, 0), "blue": (89, 224, 214), "pastel_blue": (154, 224, 219),
           "pastel_green": (164, 249, 189), "Tardis_Blue": (0, 59, 111),
           "GREY": (220, 220, 220), "WALL_GREY": (46, 48, 48), "TRANS": (1, 1, 1), "BloodOrange": (255, 169, 104)}

margin = 0.0

sys.setrecursionlimit(2000)


# Class which stores information and functions realted to maze creation and solving the maze.
class Maze:
    def __init__(self, screen, size):
        self.screen = screen
        self.maze_size = size
        self.solved = False
        self.maze_structure = []
        self.square_width = (300 // self.maze_size)
        self.square_height = (300 // self.maze_size)
        self.actual_width = ((self.maze_size * 2) + 1)
        self.actual_height = ((self.maze_size * 2) + 1)
        self.wall = 1
        self.speed = int(size * 0.55)
        self.algorithm = "BFS"

    # Function used by the two searching algorithms to update the progress of searching through the maze.
    def update_maze(self, queue, colour):
        for x, y in queue:
            pygame.draw.rect(self.screen, colour,
                             [(margin + self.square_width) * y + margin,
                              (margin + self.square_height) * x + margin,
                              self.square_width, self.square_width])
        pygame.display.flip()

    def bfs(self, maze, start):
        queue = collections.deque([[start]])
        seen = {start}
        while queue:
            path = queue.popleft()
            x, y = path[-1]
            if maze[x][y] == 3:
                return path
            for x2, y2 in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
                if 0 <= x2 < self.actual_width and 0 <= y2 < self.actual_height and maze[x2][y2] != self.wall and (
                        x2, y2) not in seen:
                    queue.append(path + [(x2, y2)])
                    seen.add((x2, y2))
            self.update_maze(seen, colours["RED"])
            pygame.time.wait(self.speed)

    # Function which performs a Depth first search on the maze.
    def dfs(self, maze, start):
        visited = set()  # Set which keeps track of all nodes in the maze that have been visited by the algorithm
        stack = [start]  # Stack which keeps track of what nodes which need to be visited

        while stack:
            current_node = stack.pop()
            x, y = current_node
            if maze[x][y] == 3:
                return visited
            # The algorithm checks the surrounding nodes to find viable paths to check once the current path reaches
            # a dead end or discovers the exit.
            # Up
            if ((x, y - 1) not in visited) and (maze[x][y - 1] != 1):
                stack.append((x, y - 1))  # if a node is not a wall and has not been visited it is added to the stack.
            # Right
            if ((x + 1, y) not in visited) and (maze[x + 1][y] != 1):
                stack.append((x + 1, y))
            # down
            if ((x, y + 1) not in visited) and (maze[x][y + 1] != 1):
                stack.append((x, y + 1))
            # left
            if ((x - 1, y) not in visited) and (maze[x - 1][y] != 1):
                stack.append((x - 1, y))
            visited.add(current_node)
            self.update_maze(visited, colours["RED"])
            pygame.time.wait(self.speed)

    def route(self):
        if not self.solved:
            if self.algorithm == "BFS":
                exit_route = self.bfs(self.maze_structure, (1, 1))
                for x, y in exit_route:
                    pygame.draw.rect(self.screen, colours["Tardis_Blue"],
                                     [(margin + self.square_width) * y + margin,
                                      (margin + self.square_height) * x + margin,
                                      self.square_width, self.square_width])
                    pygame.display.flip()
                    pygame.time.wait(self.speed)
            elif self.algorithm == "DFS":
                exit_route = self.dfs(self.maze_structure, (1, 1))

            self.solved = True
        else:
            self.draw_maze()
            self.solved = False
            self.route()

    def generate(self):
        pygame.draw.rect(self.screen, colours["BLACK"], ((0, 0), (671, 750)))
        self.solved = False
        height = self.maze_size
        width = self.maze_size

        def make_maze(w, h):
            vis = [[0] * w + [1] for k in range(h)] + [[1] * (w + 1)]
            ver = [["10"] * w + ['1'] for i in range(h)] + [[]]
            hor = [["11"] * w + ['1'] for i in range(h + 1)]

            # this function is the one that carves the path, the two co ordinates are passed
            # to it. It calls the path show function, as that call is inside the function
            # it shows a step by step process of the actual generation of the maze
            def create_path(x, y):
                vis[y][x] = 1

                d = [(x - 1, y), (x, y + 1), (x + 1, y), (x, y - 1)]
                shuffle(d)
                for (xx, yy) in d:
                    if vis[yy][xx]:
                        continue
                    if xx == x:
                        hor[max(y, yy)][x] = "10"
                    if yy == y:
                        ver[y][max(x, xx)] = "00"

                    create_path(xx, yy)

            create_path(randrange(w), randrange(h))
            s = ""
            for (a, b) in zip(hor, ver):
                s += ''.join(a + b)
            return s

        string = make_maze(width, height)

        count = 0

        temp = [x for x in string]

        for i in range(self.actual_height):
            self.maze_structure.append([])

        for i in range(self.actual_height):
            for j in range(self.actual_width):
                self.maze_structure[i].append(j)
                self.maze_structure[i][j] = int(temp[count])
                count += 1

        self.maze_structure[1][1] = 2
        self.maze_structure[self.actual_height - 2][self.actual_width - 2] = 3
        self.draw_maze()

    # Function which draws the maze.
    # Is used to refresh the maze when the maze is searched using different algorithms.
    def draw_maze(self):
        for row in range(self.actual_height):
            for column in range(self.actual_width):
                colour = colours["WHITE"]
                if self.maze_structure[row][column] == 1:
                    colour = colours["WALL_GREY"]

                pygame.draw.rect(self.screen, colour,
                                 [(margin + self.square_width) * column + margin,
                                  (margin + self.square_height) * row + margin,
                                  self.square_width, self.square_height])

    # Increases the size of the maze 5.
    def size_up(self):
        if self.maze_size < 65:
            self.maze_size += 5
            self.update()

    # Decreases the size of the maze by 5.
    def size_down(self):
        if self.maze_size > 10:
            self.maze_size -= 5
            self.update()

    # Function which updates the size of each individual square which makes up the maze when the size of the maze is
    # increased or decreased.
    def update(self):
        self.square_width = (300 // self.maze_size)
        self.square_height = (300 // self.maze_size)
        self.actual_width = ((self.maze_size * 2) + 1)
        self.actual_height = ((self.maze_size * 2) + 1)

    # Function which is used to set which algorithm is used to solve the maze
    def algorithm_update_bfs(self):
        self.algorithm = "BFS"

    # Function which is used to set which algorithm is used to solve the maze
    def algorithm_update_dfs(self):
        self.algorithm = "DFS"
