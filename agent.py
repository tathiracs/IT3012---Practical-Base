from collections import deque
import heapq

class SearchAgent:

    def __init__(self):
        self.plan = []
        self.active_algo = "BFS"

    def get_neighbors(self, state, walls, width, height):

        x, y = state

        neighbors = []

        # Up
        if y + 1 < height and (x, y + 1) not in walls:
            neighbors.append(((x, y + 1), "Up"))

        # Down
        if y - 1 >= 0 and (x, y - 1) not in walls:
            neighbors.append(((x, y - 1), "Down"))

        # Left
        if x - 1 >= 0 and (x - 1, y) not in walls:
            neighbors.append(((x - 1, y), "Left"))

        # Right
        if x + 1 < width and (x + 1, y) not in walls:
            neighbors.append(((x + 1, y), "Right"))

        return neighbors

        
    def bfs_search(self, start, goal, walls, width, height):

        frontier = deque()

        frontier.append((start, []))

        reached = {start}

        while frontier:

            state, path = frontier.popleft()

            if state == goal:
                return path

            for next_state, action in self.get_neighbors(
                state, walls, width, height
            ):

                if next_state not in reached:

                    reached.add(next_state)

                    new_path = path + [action]

                    frontier.append((next_state, new_path))

        return []


    def dfs_search(self, start, goal, walls, width, height):

        frontier = []

        frontier.append((start, []))

        reached = {start}

        while frontier:

            state, path = frontier.pop()

            if state == goal:
                return path

            for next_state, action in self.get_neighbors(
                state, walls, width, height
            ):

                if next_state not in reached:

                    reached.add(next_state)

                    new_path = path + [action]

                    frontier.append((next_state, new_path))

        return []


    def ucs_search(self, start, goal, walls, width, height):

        frontier = []

        counter = 0

        heapq.heappush(
            frontier,
            (0, counter, start, [])
        )

        reached = {start: 0}

        while frontier:

            cost, _, state, path = heapq.heappop(frontier)

            if state == goal:
                return path

            for next_state, action in self.get_neighbors(
                state, walls, width, height
            ):

                new_cost = cost + 1

                if (
                    next_state not in reached
                    or new_cost < reached[next_state]
                ):

                    reached[next_state] = new_cost

                    counter += 1

                    heapq.heappush(
                        frontier,
                        (
                            new_cost,
                            counter,
                            next_state,
                            path + [action]
                        )
                    )

        return []

    def sense_and_act(self, percept):

        if percept["food_here"]:
            return "Eat"

        if not self.plan:

            grid_size = percept["grid_size"]
            walls = set(percept["walls"])
            all_food = percept["all_food"]

            width, height = grid_size

            start = tuple(percept["agent_pos"])

            if not all_food:
                return "Forward"

            # Find the closest food
            closest_food = min(
                all_food,
                key=lambda food:
                    abs(food[0] - start[0]) +
                    abs(food[1] - start[1])
            )

            # Choose search algorithm
            if self.active_algo == "BFS":

                self.plan = self.bfs_search(
                    start,
                    closest_food,
                    walls,
                    width,
                    height
                )

            elif self.active_algo == "DFS":

                self.plan = self.dfs_search(
                    start,
                    closest_food,
                    walls,
                    width,
                    height
                )

            elif self.active_algo == "UCS":

                self.plan = self.ucs_search(
                    start,
                    closest_food,
                    walls,
                    width,
                    height
                )

        if self.plan:
            return self.plan.pop(0)

        return "Forward"

