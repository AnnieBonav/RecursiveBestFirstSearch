import random, os, sys
parent_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(parent_path)

from OptimizationFunctions import FunctionToOptimize
from AlgData import AlgData

# Define the GeneticAlgorithm class
class GeneticAlgorithm:
    # Initialize the genetic algorithm with the population size, number of dimensions, mutation rate, and crossover rate
    def __init__(self, functionToOptimize:FunctionToOptimize):
        self.algData = AlgData() # Default values, can be changed when calling testing
        self.functionToOptimize = functionToOptimize
        self.population = []

    # Initialize the population with random individuals
    def initializePopulation(self):
        # We use a range of -5.12 to 5.12 for each dimension as it is a conventional range for the sphere function
        # TODO: Change to be by class implementation
        self.population = [[random.uniform(-5.12, 5.12) for _ in range(self.algData.numDimensions)] for _ in range(self.algData.populationSize)]

    # Evaluate the fitness of each individual in the population using the sphere function
    def evaluatePopulation(self):
        fitnessScores = []
        for individual in self.population:
            fitnessScores.append(self.functionToOptimize(individual))
        return fitnessScores

    # Select parents from the population using fitness proportionate selection
    def selectParents(self, fitnessScores):
        parents = []
        match self.algData.selectionMethod:
            case "RouletteSelection":
                totalFitness = sum(fitnessScores)
                for _ in range(2):
                    cumulativeFitness = 0
                    randomValue = random.uniform(0, totalFitness)
                    for i, fitness in enumerate(fitnessScores):
                        cumulativeFitness += fitness
                        if cumulativeFitness >= randomValue:
                            parents.append(self.population[i])
                            break
            case "TournamentSelection":
                for _ in range(2):  # Select two parents
                    tournament = random.sample(self.population, self.algData.tournamentSize)
                    best = min(tournament, key=lambda individual: self.functionToOptimize(individual))
                    parents.append(best)
        return parents

    # Perform crossover on the parents to produce a child. In uniform crossover, each gene is chosen from either parent with equal probability. The crossoverRate parameter can be used to adjust this probability. If crossoverRate is high, genes from the first parent are more likely to be chosen, and if it's low, genes from the second parent are more likely to be chosen.
    def crossover(self, parents):
        child = []
        if self.algData.verboseChanges: print(f"\nStarts crossover with Parent 0: {parents[0]}, Parent 1: {parents[1]}")
        for i in range(self.algData.numDimensions):
            if random.random() < self.algData.crossoverRate:
                toAppend = parents[0][i]
                if self.algData.verboseChanges: print("Appended from parent 0:", parents[0][i])
            else:
                toAppend = parents[1][i]
                if self.algData.verboseChanges: print("Appended from parent 1:", parents[0][i])
            child.append(toAppend)
        if self.algData.verboseChanges: print("Child:", child)
        return child

    # Perform mutation on the child
    def mutate(self, child):
        if self.algData.verboseChanges: print(f"\nStarts mutation with Child: {child}")
        for i in range(self.algData.numDimensions):
            if random.random() < self.algData.mutationRate:
                # TODO: Change limits so each function has its own implementatio (and limits)
                child[i] = random.uniform(-5.12, 5.12)
                if self.algData.verboseChanges: print(f"Mutated at index {i} to {child[i]}")
        if self.algData.verboseChanges: print("Mutated Child:", child)
        return child

    # Evolve the population for a certain number of generations
    def evolve(self, numGenerations):
        self.initializePopulation()
        bestFitnesses = []
        worstFItnesses = []
        avgFitnesses = []
        match self.algData.evolveMethod:
            case "BasicReplacement":
                for i in range(numGenerations):
                    if self.algData.verboseChanges: print(f"\n************************************************************\nIteration #{i}")
                    fitnessScores = self.evaluatePopulation()
                    parents = self.selectParents(fitnessScores)
                    child = self.crossover(parents)
                    child = self.mutate(child)
                    self.population.append(child)
                    self.population.pop(0)
                    bestFitnesses.append(min(fitnessScores))
                    worstFItnesses.append(max(fitnessScores))
                    avgFitnesses.append(sum(fitnessScores) / len(fitnessScores))
                bestIndividual = min(self.population, key = lambda x: self.functionToOptimize(x))
            case "ElitismAndGenerational":
                for _ in range(numGenerations):
                    fitnessScores = self.evaluatePopulation()
                    newPopulation = sorted(self.population, key=lambda individual: self.functionToOptimize(individual))[:self.algData.elitismCount]
                    
                    while len(newPopulation) < self.algData.populationSize:
                        parents = self.selectParents(fitnessScores)  # Ensure your selection method is compatible
                        child = self.crossover(parents)
                        child = self.mutate(child)
                        newPopulation.append(child)

                    self.population = newPopulation
                    
                    bestFitnesses.append(self.functionToOptimize(newPopulation[0]))  # Assuming the first individual is the best due to sorting
                    worstFItnesses.append(self.functionToOptimize(newPopulation[-1]))  # Assuming the last individual is the worst due to sorting
                    avgFitnesses.append(sum(fitnessScores) / len(fitnessScores))
                bestIndividual = self.population[0]  # The best individual
        return bestIndividual, bestFitnesses, worstFItnesses, avgFitnesses

    # Can sent a new algData (to not use the default values)
    def test(self, algData = None | AlgData):
        if algData is not None:
            self.algData = algData
        
        pass