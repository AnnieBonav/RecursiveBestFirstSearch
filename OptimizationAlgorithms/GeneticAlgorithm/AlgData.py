# This is used on the algorithms to handle the non-changing data passed to them
# Could be a struct or a dictionary, but I prefer a class for better readability

class AlgData:
    def __init__(self,
                 numDimensions = 3,
                 populationSize = 100,
                 numGenerations = 100,
                 mutationRate = 0.01,
                 crossoverRate = 0.95,
                 selectionMethod = "RouletteSelection",
                 tournamentSize = 5,
                 evolveMethod = "BasicReplacement", 
                 elitismCount = 2,
                 verboseChanges = False,
                 showComplexPlot = False,
                 showPlots = True,
                 ):
        self.numDimensions = numDimensions
        self.populationSize = populationSize
        self.numGenerations = numGenerations
        self.mutationRate = mutationRate
        self.crossoverRate = crossoverRate

        self.selectionMethod = selectionMethod
        self.tournamentSize = tournamentSize
        self.evolveMethod = evolveMethod
        self.elitismCount = elitismCount

        self.verboseChanges = verboseChanges
        self.showComplexPlot = showComplexPlot
        self.showPlots = showPlots

    def getParameters(self, parameters:list) -> list:
        return [getattr(self, parameter) for parameter in parameters]
    
    def getParameter(self, parameter) -> any:
        return getattr(self, parameter)
    
    def increaseParameters(self, parameters, increasementsBy) -> None:
        for parameter, increaseBy in zip(parameters, increasementsBy):
            setattr(self, parameter, getattr(self, parameter) + increaseBy)
            
    def increaseParameter(self, parameter, increaseBy) -> None:
        setattr(self, parameter, getattr(self, parameter) + increaseBy)

    def setParameters(self, parameters, values) -> None:
        for parameter, value in zip(parameters, values):
            setattr(self, parameter, value)