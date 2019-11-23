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

  def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
    self.index = 0 # Pacman is always agent index 0
    self.evaluationFunction = util.lookup(evalFn, globals())
    self.depth = int(depth)

######################################################################################
# Problem 1b: implementing minimax

class MinimaxAgent(MultiAgentSearchAgent):
  """
    Your minimax agent (problem 1)
  """

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
  def breaktie(self, actions, gameState):
    food = gameState.getFood()
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
            
    #print("Actions : {}, with same distance: {}".format(min_action, min_dis) )
    return random.choice(min_action)


  def getAction(self, gameState):
    #get all actions pacman can move
    legalMoves = gameState.getLegalActions(0)
    #print
    #find best action
    max_action = []
    max_val = float('-inf')
    for action in legalMoves:
        eval = self.minimax( gameState.generateSuccessor(0, action), self.depth, 1)
        #print("Current action: {}, score: {}".format(action, eval) )
        
        if(eval == max_val):
            max_action.append(action)
        elif(eval > max_val):
            del max_action[:]
            max_action.append(action)
            max_val = eval
    
    if(len(max_action) == 1):
        return max_action[0]
    else:
        #print("Actions : {}, with same score: {}".format(max_action, max_val) )
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
        
"""
  def getAction(self, gameState):
    #get all actions pacman can move
    legalMoves = gameState.getLegalActions(0)
    
    #find best action
    max_action = None
    max_val = float('-inf')
    for action in legalMoves:
        eval = self.minimax( gameState.generateSuccessor(0, action), self.depth, 1)
       # print("Current action: {}, score: {}".format(action, eval) )
        if(eval > max_val):
            max_action = action
            max_val = eval
            
    return max_action
    
    
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
"""
            
            



######################################################################################
# Problem 2a: implementing alpha-beta

class AlphaBetaAgent(MultiAgentSearchAgent):
  """
    Your minimax agent with alpha-beta pruning (problem 2)
  """

  def getAction(self, gameState):
    """
      Returns the minimax action using self.depth and self.evaluationFunction
    """

    # BEGIN_YOUR_CODE (our solution is 36 lines of code, but don't worry if you deviate from this)
    raise Exception("Not implemented yet")
    # END_YOUR_CODE

######################################################################################
# Problem 3b: implementing expectimax

class ExpectimaxAgent(MultiAgentSearchAgent):
  """
    Your expectimax agent (problem 3)
  """

  def getAction(self, gameState):
    """
      Returns the expectimax action using self.depth and self.evaluationFunction

      All ghosts should be modeled as choosing uniformly at random from their
      legal moves.
    """

    # BEGIN_YOUR_CODE (our solution is 20 lines of code, but don't worry if you deviate from this)
    raise Exception("Not implemented yet")
    # END_YOUR_CODE

######################################################################################
# Problem 4a (extra credit): creating a better evaluation function

def betterEvaluationFunction(currentGameState):
  """
    Your extreme, unstoppable evaluation function (problem 4).

    DESCRIPTION: <write something here so we know what you did>
  """

  # BEGIN_YOUR_CODE (our solution is 13 lines of code, but don't worry if you deviate from this)
  raise Exception("Not implemented yet")
  # END_YOUR_CODE

# Abbreviation
better = betterEvaluationFunction
