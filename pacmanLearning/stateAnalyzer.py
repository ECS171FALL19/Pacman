import game
import numpy as np

class stateAnalyzer():
    
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
    
    def getStateDiscription(self, state):
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
            m[-1-int(pos[1])][int(pos[0])] = val
            
        return m
