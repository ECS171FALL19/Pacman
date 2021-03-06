#AppxQAgent.py
#ref: using code from http://ai.berkeley.edu
#ref: structure inspired by https://github.com/Patrick-wlz

from game import *
from featureExtractors import *
from ClassicQAgent import *

#approximimate Q learning agent
#inherite from Classic Q agent
class AppxQAgent(ClassicQAgent):
    def __init__(self, extractor='IdentityExtractor', **args):
        #feature extractor can extract info from the current state of gam
        # here we find the user specified extractor
        self.featExtractor = util.lookup(extractor, globals())()
        ClassicQAgent.__init__(self, **args)
        self.weights = util.Counter()

    def getWeights(self):
	    return self.weights

    def getQValue(self, state, action):
        "util.Counter() overides the * operation by vector dot product"
        return self.getWeights() * self.featExtractor.getFeatures(state, action)
    
    def update(self, state, action, nextState, reward):
        "util.Counter() overides the - operation by vector subtraction"
        realQ = reward + self.discount * self.getValue(nextState)
        diffQ = realQ - self.getQValue(state, action)
        features = self.featExtractor.getFeatures(state, action)

        #update weight correspoding to each feature, using gradient descent
        for feature in features:
            features[feature] *= self.alpha * diffQ
        self.weights = self.weights + features
   		
    def final(self, state):
        ClassicQAgent.final(self, state)
        if self.episodesSoFar == self.numTraining:
            pass

