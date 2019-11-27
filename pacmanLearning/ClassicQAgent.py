# ClassicQAgent.py
#ref: using code from http://ai.berkeley.edu
#ref: structure inspired by https://github.com/Patrick-wlz

from game import *
from learningAgents import ReinforcementAgent
from featureExtractors import *

import random,util,math

class ClassicQAgent(ReinforcementAgent):
    def __init__(self, epsilon=0.05,gamma=0.8,alpha=0.2, numTraining=0, **args):
        args['epsilon'] = epsilon
        args['gamma'] = gamma
        args['alpha'] = alpha
        args['numTraining'] = numTraining
        self.index = 0  # This is always Pacman
        
        "inherit from ReinforcementAgent"
        ReinforcementAgent.__init__(self, **args)
        
        "holds the Q values"
        self.Q_values = util.Counter()

    def getQValue(self, state, action):
        Q = self.Q_values[(state, action)]
        return Q

    def computeValueFromQValues(self, state):
        possible_actions = self.getLegalActions(state)
        if not possible_actions:
            return 0
            
        possible_Qs = [self.getQValue(state, action) for action in possible_actions]
        return max(possible_Qs) if max(possible_Qs) > float("-inf") else float("-inf")

    def computeActionFromQValues(self, state):
        possible_actions = self.getLegalActions(state)
        if not possible_actions:
            return None

        "get the action that leads to max Q value"
        possible_Qs = [self.getQValue(state, action) for action in possible_actions]
        Q_max = max(possible_Qs)
        if not Q_max > float("-inf"):
            return None
        else:
            return possible_actions[possible_Qs.index(Q_max)]

    def getAction(self, state):
        next_action = None
        possible_actions = self.getLegalActions(state)
        if not possible_actions:
            return next_action

        "explor/exploit"
        if util.flipCoin(self.epsilon):
            next_action = random.choice(possible_actions)
        else:
            next_action = self.computeActionFromQValues(state)
            
        self.doAction(state, next_action)
        return next_action

    def update(self, state, action, nextState, reward):
        #different weight is assigned to previous Q and next Q, with reward
        newQ = (1.0 - self.alpha) * self.getQValue(state, action) + self.alpha * (reward + self.discount * self.computeValueFromQValues(nextState))
        self.Q_values[(state, action)] = newQ

    def getPolicy(self, state):
        return self.computeActionFromQValues(state)

    def getValue(self, state):
        return self.computeValueFromQValues(state)



