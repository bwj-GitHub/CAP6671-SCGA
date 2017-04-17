"""
Created on Apr 13, 2017

@author: brandon
"""


class SteadyStateGA(object):
    """Brief descript. of class."""

    def __init__(self, chromo_cls, problem, selector, parameters):
        """Brief descript of what is being init.
        
        :param chromo_cls: <class>; descript.

        :param problem: instance of FitnessFunction; descript.

        :param selector: instance of Selector; descript.
        
        :param paramters: instance of Parameters; descript.
        """

        self.chromo_cls = chromo_cls
        self.problem = problem
        self.selector = selector
        self.parameters = parameters

        self.N = self.parameters.N  # population size
        self.max_problem = self.parameters.MAX_PROBLEM  # max if True, else min
        self.verbosity = self.parameters.VERBOSITY

    def select_best(self, chromos, N):
        """Return the N best Chromos in chromos."""

        chromos.sort(key=lambda x: x.raw_fitness, reverse=self.max_problem)
        return chromos[0:N]

    def run(self, population=None, iterations=100):
        """Brief descript. of what this method does."""

        if population is None:
            # Generate a new population of size N:
            population = []
            for _ in range(self.N):
                population.append(self.chromo_cls.get_new_chromo(self.parameters))

        # Evaluate the fitness of the initial population; if an individual
        #  has already been evaluated, they will not be evaluated again.
        for i in range(len(population)):
            if population[i].raw_fitness is None:
                self.problem.do_raw_fitness(population[i])

        for i in range(iterations):
            # Select 2 parents and replace them with the 2 best individuals
            # from the set of those parents and their 2 children.
            parents = self.selector.select(population , 2)  # returns indices
            children = self.chromo_cls.crossover(*parents, self.parameters)
            for child in children:
                self.chromo_cls.mutate(child, self.parameters)
                self.problem.do_raw_fitness(child)
            replacements = self.select_best(parents + children, N=2)
            for pi in parents:
                population[pi] = replacements.pop()
            if self.verbosity > 0: print("Finished iteration {}!".format(i))

        return population

