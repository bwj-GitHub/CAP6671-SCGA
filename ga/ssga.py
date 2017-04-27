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

        if self.verbosity > 0:
            print("Selected {} from {}".format(
                    [("{} (F={})".format(c.id, c.raw_fitness)) for c in chromos[0:N]],
                    [("{} (F={})".format(c.id, c.raw_fitness)) for c in chromos]))
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
            if self.verbosity > 0:
                print("Iteration {}:".format(i))
            # Select 2 parents and replace them with the 2 best individuals
            # from the set of those parents and their 2 children.
            parent_inds = self.selector.select(population , 2)  # returns indices
            if self.verbosity > 0:
                print("\nSelected for crossover: {}".format(
                        [population[pi].id for pi in parent_inds]))
            parents = [population[i] for i in parent_inds]

            children = self.chromo_cls.crossover(*parents, parameters=self.parameters)
            if self.verbosity > 0:
                print("Added children: {}".format([child.id for child in children]))
            for child in children:
                self.chromo_cls.mutate(child, self.parameters)
                self.problem.do_raw_fitness(child)

            replacements = self.select_best(parents + children, N=2)
            for pi in parent_inds:
                population[pi] = replacements.pop()
            if self.verbosity > 0:
                print("Finished iteration {}!".format(i))
                print("New Population:")
                for chromo in population:
                    print("\tChromo {}, F={}".format(chromo.id, chromo.raw_fitness))
                print()

        return population

