import math
from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """
    def __init__(self):
        self.lastPositions = []
        self.dc = None


    def getAction(self, gameState):
        """
        getAction chooses among the best options according to the evaluation function.

        getAction takes a GameState and returns some Directions.X for some X in the set {North, South, West, East, Stop}
        ------------------------------------------------------------------------------
        Description of GameState and helper functions:

        A GameState specifies the full game state, including the food, capsules,
        agent configurations and score changes. In this function, the |gameState| argument
        is an object of GameState class. Following are a few of the helper methods that you
        can use to query a GameState object to gather information about the present state
        of Pac-Man, the ghosts and the maze.

        gameState.getLegalActions():
            Returns the legal actions for the agent specified. Returns Pac-Man's legal moves by default.

        gameState.generateSuccessor(agentIndex, action):
            Returns the successor state after the specified agent takes the action.
            Pac-Man is always agent 0.
        gameState.getPacmanState():
            Returns an AgentState object for pacman (in game.py)
            state.configuration.pos gives the current position
            state.direction gives the travel vector

        gameState.getGhostStates():
            Returns list of AgentState objects for the ghosts

        gameState.getNumAgents():
            Returns the total number of agents in the game

        gameState.getScore():
            Returns the score corresponding to the current state of the game


        The GameState class is defined in pacman.py and you might want to look into that for
        other helper methods, though you don't need to.
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best


        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (oldFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        oldFood = currentGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        return successorGameState.getScore()


def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """
    def breaktie(self, actions, gameState):
        food = gameState.getFood()
        #print("Length: {}".format(len(gameState.getFood().asList())))
        # print(gameState.getFood().asList())
        aa = None
        bb = None
        for x in range(food.width):
            for y in range(food.height):
                if(food[x][y] == True):
                    if(aa != None):
                        bb = [x,y]
                        break
                    aa = [x, y]

            if(bb != None):
                break

        # print("food position: {}".format(aa))
        if(bb == None):
            bb = aa
        min_dis = float('+inf')
        min_action = []
        for a in actions:
            dis = manhattanDistance(aa,gameState.generateSuccessor(0,a).getPacmanPosition() )+ manhattanDistance(bb, gameState.generateSuccessor(0,a).getPacmanPosition() )
            if(dis < min_dis):
                min_dis = dis
                del min_action[:]
                min_action.append(a)
            elif(dis == min_dis):
                min_action.append(a)

        return random.choice(min_action)

    def __init__(self, evalFn = 'EvaluationFunction_6features', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

######################################################################################
# Problem 1b: implementing minimax

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Returns the minimax action from the current gameState using self.depth
      and self.evaluationFunction. Terminal states can be found by one of the following:
      pacman won, pacman lost or there are no legal moves.
  
      Here are some method calls that might be useful when implementing minimax.
  
      gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1
  
      Directions.STOP:
        The stop direction, which is always legal
  
      gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action
  
      gameState.getNumAgents():
        Returns the total number of agents in the game
  
      gameState.getScore():
        Returns the score corresponding to the current state of the game
  
      gameState.isWin():
        Returns True if it's a winning state
  
      gameState.isLose():
        Returns True if it's a losing state
  
      self.depth:
        The depth to which search should continue
  
    """

    def getAction(self, gameState):
        #get all actions pacman can move
        legalMoves = gameState.getLegalActions(0)

        #find best action
        max_action = []
        max_val = float('-inf')
        for action in legalMoves:
            eval = self.minimax( gameState.generateSuccessor(0, action), self.depth, 1)
            if(eval == max_val):
                max_action.append(action)
            elif(eval > max_val):
                del max_action[:]
                max_action.append(action)
                max_val = eval

        if(len(max_action) == 1):
            return max_action[0]
        else:
            return self.breaktie(max_action, gameState)

    def minimax(self, gameState, depth, agentIndex):
        #if all ghost's makes a move, this depth is finished
        if(agentIndex >= gameState.getNumAgents()):
            # move to next depth, start with pacman: agentIndex==0
            return self.minimax(gameState, depth-1, 0)

        if(depth == 0 or len(gameState.getLegalActions(agentIndex)) == 0):
            #print("Get evalution score {}".format(self.evaluationFunction(gameState)) )
            return self.evaluationFunction(gameState)

        legalMoves = gameState.getLegalActions(agentIndex)

        if(agentIndex == 0): # if pacman's move
            max_val = float('-inf')
            max_action = None
            for action in legalMoves:
                eval = self.minimax( gameState.generateSuccessor(agentIndex, action),
                                     depth,
                                     agentIndex+1)

                if(eval > max_val):
                    max_action = action
                    max_val = eval
            return max_val

        else:#if ghost's move
            min_val = float('+inf')
            min_action = None
            for action in legalMoves:
                eval = self.minimax( gameState.generateSuccessor(agentIndex, action),
                                     depth,
                                     agentIndex+1)
                if(eval < min_val):
                    min_action = action
                    min_val = eval
            return min_val



class AlphaBetaAgent(MultiAgentSearchAgent):

    def getAction(self, gameState):
        #get all actions pacman can move
        legalMoves = gameState.getLegalActions(0)
        #print
        #find best action
        max_action = []
        max_val = float('-inf')
        alpha = float('-inf')
        for action in legalMoves:
            eval = self.minimax( gameState.generateSuccessor(0, action),
                                 self.depth, 1,
                                 alpha,
                                 float('+inf'))
            if(eval == max_val):
                max_action.append(action)
            elif(eval > max_val):
                del max_action[:]
                max_action.append(action)
                max_val = eval
            alpha = max(eval, alpha)

        if(len(max_action) == 1):
            return max_action[0]
        else:
            return self.breaktie(max_action, gameState)


    def minimax(self, gameState, depth, agentIndex, alpha, beta):
        if(agentIndex >= gameState.getNumAgents()):
            return self.minimax(gameState, depth-1, 0, alpha, beta)

        if(depth == 0 or len(gameState.getLegalActions(agentIndex)) == 0):
            return self.evaluationFunction(gameState)

        legalMoves = gameState.getLegalActions(agentIndex)

        if(agentIndex == 0): # if pacman's move
            max_val = float('-inf')
            max_action = None
            for action in legalMoves:
                eval = self.minimax( gameState.generateSuccessor(agentIndex, action),
                                     depth,
                                     agentIndex+1,
                                     alpha,
                                     beta)

                if(eval > max_val):
                    max_action = action
                    max_val = eval
                alpha = max(alpha, eval)
                if(alpha >= beta):
                    break
            return max_val

        else:#if ghost's move
            min_val = float('+inf')
            min_action = None
            for action in legalMoves:
                eval = self.minimax( gameState.generateSuccessor(agentIndex, action),
                                     depth,
                                     agentIndex+1,
                                     alpha,
                                     beta)
                if(eval < min_val):
                    min_action = action
                    min_val = eval
                beta = min(beta, eval)
                if(beta <= alpha):
                    break
            return min_val



class ExpectimaxAgent(MultiAgentSearchAgent):
    def getAction(self, gameState):
        # Get all legal actions for pacman
        legalMoves = gameState.getLegalActions(0)
        max_action = None
        max_val = float('-inf')

        for action in legalMoves:
            eval = self.Expectimax(gameState.generateSuccessor(0, action), 1, self.depth)
            # Finding the max value and return the action
            if(eval >= max_val):
                max_action = action
                max_val = eval

        return max_action

    def Expectimax(self, gameState, agentIndex, depth):
        # If all agent in current depth has moved
        if(agentIndex >= gameState.getNumAgents()):
            # Moving to the next depth starting with pacman
            return self.Expectimax(gameState, 0, depth-1)

        if(depth == 0 or len(gameState.getLegalActions(agentIndex)) == 0):
            #print("Get evalution score {}".format(self.evaluationFunction(gameState)) )
            return self.evaluationFunction(gameState)



        legalMoves = gameState.getLegalActions(agentIndex)

        if(agentIndex == 0): # if pacman's move
            max_val = float('-inf')
            sum_score_max = 0
            for action in legalMoves:
                eval = self.Expectimax( gameState.generateSuccessor(agentIndex, action),
                                        agentIndex+1,
                                        depth)
                if(eval > max_val):
                    max_val = eval
                sum_score_max += max_val
            return max_val

        else:#if ghost's move
            min_val = float('+inf')
            sum_score_min = 0
            for action in legalMoves:
                eval = self.Expectimax( gameState.generateSuccessor(agentIndex, action),
                                        agentIndex+1,
                                        depth)
                if(eval < min_val):
                    min_val = eval
                sum_score_min += min_val
            return sum_score_min/len(gameState.getLegalActions(agentIndex))


######################################################################################
# Problem 4a (extra credit): creating a better evaluation function


def EvaluationFunction_4features(currentGameState):

    pacman_loc = currentGameState.getPacmanPosition()
    ghosts_state = currentGameState.getGhostStates()

    #print
    """1. game score"""
    evaluation_score = currentGameState.getScore() * 11
    #print("Place 1: {}".format(evaluation_score))

    """2. distance to the nearest food, the bigger the worse: negative score added"""
    food = currentGameState.getFood().asList()
    min_dis = float('+inf')
    for f in food:
        dis = manhattanDistance(pacman_loc, f)
        min_dis = min(dis, min_dis)

    if(len(food) == 0):
        evaluation_score += 10000
    else:
        evaluation_score -= min_dis * 6
    #print("Place 2: {}".format(evaluation_score))

    """3. distance to the nearest active ghost, the smaller the worse: positve score added"""
    scared_ghosts = []
    active_ghosts = []
    min_ghost_dis = float('+inf')
    for ghost in ghosts_state:
        if(ghost.scaredTimer > 0):
            scared_ghosts.append(ghost)
        else:
            active_ghosts.append(ghost)
            dis = manhattanDistance(ghost.getPosition(), pacman_loc)
            min_ghost_dis = min(dis, min_ghost_dis)

    #there are active ghosts
    if(len(active_ghosts) != 0):
        # with square we will care about this distance more when the ghost is close.
        evaluation_score += min_ghost_dis * min_ghost_dis * 0.4
    #print("Place 3: {}".format(evaluation_score))



    """4. number of food left + number of capsules left
    """
    num_food = len(food)
    num_capsule = len(currentGameState.getCapsules())
    evaluation_score -= (num_food + num_capsule) * 10
    return evaluation_score


def EvaluationFunction_6features(currentGameState):

    pacman_loc = currentGameState.getPacmanPosition()
    ghosts_state = currentGameState.getGhostStates()


    """1. game score"""
    evaluation_score = currentGameState.getScore() * 11
    #print("Place 1: {}".format(evaluation_score))

    """2. distance to the nearest food, the bigger the worse: negative score added"""
    food = currentGameState.getFood().asList()
    min_dis = float('+inf')
    for f in food:
        dis = manhattanDistance(pacman_loc, f)
        min_dis = min(dis, min_dis)

    if(len(food) == 0):
        evaluation_score += 10000
    else:
        evaluation_score -= min_dis * 6
    #print("Place 2: {}".format(evaluation_score))

    """3. distance to the nearest active ghost, the smaller the worse: positve score added"""
    scared_ghosts = []
    active_ghosts = []
    min_ghost_dis = float('+inf')
    for ghost in ghosts_state:
        if(ghost.scaredTimer > 0):
            scared_ghosts.append(ghost)
        else:
            active_ghosts.append(ghost)
            dis = manhattanDistance(ghost.getPosition(), pacman_loc)
            min_ghost_dis = min(dis, min_ghost_dis)

    #there are active ghosts
    if(len(active_ghosts) != 0):
        # with square we will care about this distance more when the ghost is close.
        evaluation_score += min_ghost_dis * min_ghost_dis * 0.4
    #print("Place 3: {}".format(evaluation_score))


    #there are active ghosts
    if(len(active_ghosts) != 0):
        # with square we will care about this distance more when the ghost is close.
        if (min_ghost_dis <= 3):
            evaluation_score += min_ghost_dis * min_ghost_dis * 0.4
    #print("Place 3: {}".format(evaluation_score))



    """feature 4. distance to neareast scared ghost"""

    min_scared = 0
    for ghost in scared_ghosts:
        dis = manhattanDistance(ghost.getPosition(), pacman_loc)
        min_scared = min(min_scared, dis)
    evaluation_score += 0.8 * min_scared


    """feature 5. number of legal actions"""
    num_actions = len(currentGameState.getLegalActions(0))
    evaluation_score += 0.4 * num_actions


    """feature 6. number of food left + number of capsules left"""
    num_food = len(food)
    num_capsule = len(currentGameState.getCapsules())
    evaluation_score -= (num_food + num_capsule) * 10
    #print("Place 6: {}".format(evaluation_score))
    return evaluation_score
