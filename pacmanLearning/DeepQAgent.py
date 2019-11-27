# DeepQAgent.py
import keras
from keras.models import Sequential
from keras.layers import Dense, Flatten
from keras.layers import Conv2D

from game import *
from game import Directions, Agent, Actions
from learningAgents import ReinforcementAgent
import random,util,math
import numpy as np
import copy
from collections import deque

cons = {'grid_width' : 7,
        'grid_height' : 7}

ACTIONS = [Directions.NORTH, Directions.SOUTH, Directions.EAST, Directions.WEST, Directions.STOP]
    
class DeepQAgent(ReinforcementAgent):
    
    def __init__(self, **args):
        ReinforcementAgent.__init__(self, **args)
        self.count = 0
        self.init = 0
        self.epsilon = 0.4
        self.gamma = 0.9
        self.batch_size = 20
        self.grid_width = cons['grid_width']
        self.grid_height = cons['grid_height']
        
        self.state_discription = None
        self.new_episode = True
        self.training = True
        self.best_score = float("-inf")

        self.memory = deque(maxlen=50000)
        self.first_model = self.getModel(self.grid_width, self.grid_height, len(ACTIONS))
        self.second_model = copy.deepcopy(self.first_model)

        

    def update(self, state, action, nextState, reward):
        if not self.getLegalActions(nextState):
            done = True
        else:
            done = False

        if not done:
            self.next_state_disc = self.getStateDiscription(nextState)
        else:
            self.next_state_disc = None

        if not self.new_episode:
            self.remember(self.state_discription, action, reward, self.next_state_disc, done)

        self.count += 1
        if len(self.memory) > 5*self.batch_size and self.training:
            self.replay(self.batch_size)
    
    def getAction(self, state):
        legalActions = self.getLegalActions(state)
        action = None

        "end game"
        if not self.getLegalActions(state):
            return action

        if self.new_episode:
            "Analyze state"
            self.state_discription = self.getStateDiscription(state)
            self.new_episode = False
        
        "Explore or Exploit"
        if util.flipCoin(self.epsilon):
            action = random.choice(legalActions)
        else:
            "predict based on current state"
            
            values = self.first_model.predict(np.array([self.state_discription]))

            for value in values[0]:
                action = ACTIONS[(np.argmax(values[0]))]
                if action not in legalActions:
                    values[0][np.argmax(values[0])] = float("-inf")
                else:
                    break

            if action not in legalActions:
                action = ACTIONS[4]
                
            
        self.doAction(state, action)
        return action

    def final(self, state):
        ReinforcementAgent.final(self, state)

        self.new_episode = True
        if self.training and state.getScore() > self.best_score:
            self.best_score = state.getScore()
            print ("updated best first_models for best score: ", self.best_score)
        if self.episodesSoFar == self.numTraining:
            self.training = False
            pass

    def remember(self, state_discription, action, reward, next_state_discription, done):
        if state_discription is not None:
            self.memory.append((copy.deepcopy(state_discription), action, reward, copy.deepcopy(next_state_discription), done))

    def replay(self, batch_size):
        x_batch, y_batch = [], []
        minibatch = random.sample(self.memory, batch_size)
        for (state_discription, action, reward, next_state_discription, done) in minibatch:
            action_index = ACTIONS.index(action)
            y = self.first_model.predict(np.array([state_discription]))
            y[0][action_index] = reward if done else reward + self.gamma * np.max(self.first_model.predict(np.array([next_state_discription]))[0])
            x_batch.append(state_discription)
            y_batch.append(y[0])

        self.second_model.fit(np.array(x_batch), np.array(y_batch), batch_size=len(x_batch), verbose=0)

        if self.count % 100 == 0:
            self.first_model = copy.deepcopy(self.second_model)

    def getModel(self, n_col, n_row, num_actions):
        shape = (n_row, n_col, 1)
        model = Sequential()
        model.add(Conv2D(32, kernel_size=(4, 4), activation='relu', input_shape=shape))
        model.add(Conv2D(64, (2, 2), activation='relu'))
        model.add(Conv2D(128, (1, 1), activation='relu'))
        model.add(Flatten())
        model.add(Dense(256, activation='relu'))
        model.add(Dense(num_actions))

        model.compile(loss=keras.losses.categorical_crossentropy,
              optimizer=keras.optimizers.Adadelta(),
              metrics=['accuracy'])
        
        return model

    def getStateDiscription(self, state):
        if state is None:
            return None
        
        self.WALL = 1
        self.FOOD = 2
        self.CAPSULE = 3

        self.PACMAN_NORTH = 4
        self.PACMAN_SOUTH = 5
        self.PACMAN_EAST = 6
        self.PACMAN_WEST = 7
        self.PACMAN_STOP = 8

        self.GHOST_NORTH = 9
        self.GHOST_SOUTH = 10
        self.GHOST_EAST = 11
        self.GHOST_WEST = 12
        self.GHOST_STOP = 13

        self.SCARED_GHOST_NORTH = 14
        self.SCARED_GHOST_SOUTH = 15
        self.SCARED_GHOST_EAST = 16
        self.SCARED_GHOST_WEST = 17
        self.SCARED_GHOST_STOP = 18

        layout = state.data.layout
        n_row = layout.height
        n_col = layout.width

        "use a matrix to discribe the current state"
        m = np.zeros((n_row, n_col))

        "layout statioary objects info"
        walls = layout.walls
        food = state.data.food
        capsules = layout.capsules

        for i in range(n_row):
            for j in range(n_col):
                if walls[j][i]:
                    m[-1-i][j] = self.WALL
                    
                if food[j][i]:
                    m[-1-i][j] = self.FOOD

        for i in capsules:
            m[-1-i[1], i[0]] = self.CAPSULE

        "agents"
        for agent in state.data.agentStates:
            position = agent.configuration.getPosition()
            direction = agent.configuration.getDirection()
            val = 0
            if agent.isPacman:
                "pacman"
                if direction == Directions.NORTH:
                    val = self.PACMAN_NORTH
                if direction == Directions.SOUTH:
                    val = self.PACMAN_SOUTH
                if direction == Directions.EAST:
                    val = self.PACMAN_EAST
                if direction == Directions.WEST:
                    val = self.PACMAN_WEST
                if direction == Directions.STOP:
                    val = self.PACMAN_STOP
            else:
                "ghost"
                if not agent.scaredTimer > 0:
                    "normal ghost"
                    if direction == Directions.NORTH:
                        val = self.GHOST_NORTH
                    if direction == Directions.SOUTH:
                        val = self.GHOST_SOUTH
                    if direction == Directions.EAST:
                        val = self.GHOST_EAST
                    if direction == Directions.WEST:
                        val = self.GHOST_WEST
                    if direction == Directions.STOP:
                        val = self.GHOST_STOP
                else:
                    "scared ghost"
                    if direction == Directions.NORTH:
                        val = self.SCARED_GHOST_NORTH
                    if direction == Directions.SOUTH:
                        val = self.SCARED_GHOST_SOUTH
                    if direction == Directions.EAST:
                        val = self.SCARED_GHOST_EAST
                    if direction == Directions.WEST:
                        val = self.SCARED_GHOST_WEST
                    if direction == Directions.STOP:
                        val = self.SCARED_GHOST_STOP
                        
            "fill in agent"
            m[-1-int(position[1])][int(position[0])] = val

        m = np.reshape(m, (n_row, n_col, 1))
        return m

class AutoQueue():
    def __init__(self, size):
        self.maxSize =  size
        self.q = []
        self.size = 0

    def append(self, obj):
        self.q.append(obj)
        self.size += 1
        if len(self.q) > self.maxSize:
            self.pop(0)
            self.size -= 1

