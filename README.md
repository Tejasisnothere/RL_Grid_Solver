Reinforcement Learning Grid World Visualizer
This project is an interactive web application that demonstrates the Q-learning algorithm solving a grid world environment. Users can set reinforcement learning hyperparameters, train an agent, and visualize the resulting state-values on a dynamic grid.

Features
Interactive Hyperparameter Tuning: Set the Grid Size, Alpha (α), Gamma (γ), Epsilon (ε), and number of training episodes.

Dynamic Environment: The grid, including the start, end, and random obstacles, is generated on the backend for each training session.

State-Value Visualization: The learned value for each state is represented by a color gradient, making it easy to see the optimal path the agent has discovered.

Dark/Light Mode: A theme-toggle is included for user comfort.

Detailed Tooltips: Hover over any cell to see its coordinates, type (Start, Goal, Obstacle), and learned value.

Client-Server Architecture: A clean separation between the Python/Flask backend (handling the RL logic) and the HTML/CSS/JS frontend (handling the UI).

Tech Stack
Backend: Python, Flask

Frontend: HTML5, CSS3, JavaScript

API Communication: Axios (for POST requests)

Core Algorithm: Q-Learning with Epsilon-Greedy exploration and Epsilon Decay.

How It Works
User Input: The user sets the desired RL parameters in the browser and clicks the "Train & Render Grid" button.

API Request: The JavaScript frontend sends a POST request with the parameters to the Flask backend at the /train endpoint.

Agent Training: The backend initializes a Grid environment and runs the Q-learning agent. The agent explores the grid, receives rewards/penalties, and updates its Q-values to learn the best action for each state.

API Response: Once training is complete, the server sends back a JSON object containing the final grid layout and the calculated state-values for each cell.

Rendering: The frontend JavaScript dynamically builds the grid in the DOM, coloring each cell based on its type (start, end, obstacle) or its learned value, creating the final visualization.

How to Run the Project
Prerequisites
Python 3.x installed.

pip for installing Python packages.

1. Backend Setup
   Clone the repository and navigate into the project directory.

# Install required Python libraries

pip install Flask flask-cors

# Start the Flask server

python app.py

The server will now be running on http://127.0.0.1:3000.

2. Frontend Setup
   Simply open the rl_visualizer.html file in any modern web browser. The page will load, and you can start interacting with the application.

Key Reinforcement Learning Concepts Demonstrated
Q-Learning: The core algorithm used for learning the action-value function (Q-values).

State-Value Function: The grid visualizes V(s), which is derived from the maximum Q-value for each state.

Epsilon-Greedy Policy: The agent uses this policy to balance exploration (trying random actions) and exploitation (choosing the best-known action).

Epsilon Decay: The value of epsilon decreases over time, causing the agent to explore less and exploit more as it becomes more confident.
