from flask import Flask, request, jsonify, render_template
import random
from flask_cors import CORS

app = Flask(__name__)
CORS(app)




import random
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from collections import defaultdict

class Grid:
    def __init__(self, size, start, end, alpha, epsilon, gamma, restricted):
        self.start = start
        self.size = size
        self.restricted = restricted
        self.end = end
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.grid = []
        self.grid_init()
        self.Q_values = {
            (i, j): {'U': 0.0, 'D': 0.0, 'L': 0.0, 'R': 0.0}
            for i in range(self.size)
            for j in range(self.size)
            if (i, j) not in self.restricted
        }
        self.moves = {'U': [-1, 0], 'D': [1, 0], 'L': [0, -1], 'R': [0, 1]}

        self.move_number = 0
        self.episode_size = self.size * 3
        self.total_reward = 0
        self.episode_number = 0

        self.returns = defaultdict(list)
        self.V = defaultdict(float)

    def grid_init(self):
        self.grid = [['a' if (i, j) not in self.restricted else 'b'
                      for j in range(self.size)] for i in range(self.size)]
        
    def serialize_grid(self):
        grid_data = []
        for i in range(self.size):
            row = []
            for j in range(self.size):
                if (i, j) in self.restricted:
                    row.append(1)  
                elif (i, j) == self.start:
                    row.append(2) 
                elif (i, j) == self.end:
                    row.append(3)  
                else:
                    row.append(0)   
            grid_data.append(row)
        return grid_data


    def reward_giver(self, curr, next, action):
        reward = -1
        if next == self.end:
            reward += 100
        elif next in self.restricted:
            reward -= 50
        return reward

    def updateVals(self, curr, next, action, reward):
        if curr not in self.Q_values:
            return
        if next not in self.Q_values:
            target = reward
        else:
            target = reward + self.gamma * max(self.Q_values[next].values())
        self.Q_values[curr][action] = self.Q_values[curr][action] + self.alpha * (
            target - self.Q_values[curr][action]
        )

    def choose_move_type(self):
        return "r" if random.random() < self.epsilon else "g"

    def move_random(self, state):
        choices_instance = list(self.moves.keys())
        while choices_instance:
            choice = random.choice(choices_instance)
            valid, new_state = self.move(state, choice)
            if valid:
                return choice, tuple(new_state)
            choices_instance.remove(choice)
        return None, state

    def move_greedy(self, state):
        q_actions = self.Q_values[state]
        sorted_actions = sorted(q_actions, key=q_actions.get, reverse=True)
        for action in sorted_actions:
            new_state = (state[0] + self.moves[action][0],
                         state[1] + self.moves[action][1])
            if 0 <= new_state[0] < self.size and 0 <= new_state[1] < self.size:
                return action
        return None

    def move(self, state, action):
        if self.move_number > self.episode_size:
            return False, False
        self.move_number += 1
        new_state = (state[0] + self.moves[action][0],
                     state[1] + self.moves[action][1])
        if 0 <= new_state[0] < self.size and 0 <= new_state[1] < self.size:
            return True, new_state
        else:
            return False, False

    def run_episode(self):
        self.move_number = 0
        self.total_reward = 0
        state = self.start
        trajectory = []  

        while self.move_number < self.episode_size:
            if state not in self.Q_values:
                break
            move_type = self.choose_move_type()
            if move_type == "r":
                action, next_state = self.move_random(state)
            else:
                action = self.move_greedy(state)
                valid, next_state = self.move(state, action)
                if not valid:
                    break
            if not action or not next_state:
                break
            reward = self.reward_giver(state, next_state, action)
            self.updateVals(state, next_state, action, reward)
            self.total_reward += reward
            trajectory.append((state, reward))
            state = next_state
            if state == self.end:
                break

        G = 0
        for (s, r) in reversed(trajectory):
            G = self.gamma * G + r
            self.returns[s].append(G)
            self.V[s] = sum(self.returns[s]) / len(self.returns[s])

        self.episode_number += 1

    def state_value(self):
        values = [[0 for _ in range(self.size)] for _ in range(self.size)]
        for (i, j) in self.Q_values:
            values[i][j] = round(self.V[(i, j)], 2)
        return values
    
    def to_dict(self):
        return {
            "size": self.size,
            "alpha": self.alpha,
            "epsilon": self.epsilon,
            "gamma": self.gamma,
            "state_values": self.state_value(),   
            "restricted": list(self.restricted), 
            "start": self.start,
            "end": self.end
        }


    def print_values(self):
        values = self.state_value()
        for row in values:
            print(row)

    def train(self, episodes=20):
        for _ in range(episodes):
            self.run_episode()
        print("\nFinal State Values:")
       



import random

@app.route("/")
def get_home():
    return render_template("test.html")

@app.route("/train", methods=["POST"])
def train():
    data = request.json
    size = int(data.get("size", 10))
    alpha = float(data.get("alpha", 0.1))
    epsilon = float(data.get("epsilon", 0.1))
    gamma = float(data.get("gamma", 0.9))
    episodes = int(data.get("episodes", 300))
    num_res = int(data.get("restricted", random.randint(0,int(size*size/5))))
    start = (0, 0)
    end = (size - 1, size - 1)

    restricted = set()
    
    no_res = num_res
    while len(restricted) < no_res:
        ri, rj = random.randint(0, size - 1), random.randint(0, size - 1)
        if (ri, rj) != start and (ri, rj) != end:
            restricted.add((ri, rj))

    g = Grid(size, start, end, alpha, epsilon, gamma, restricted)
    g.train(episodes=episodes)
    g.print_values()

    return jsonify({

        "state_values": g.state_value(),
    "grid": g.serialize_grid(),
    "size": g.size
    })


if __name__ == "__main__":
    app.run()
