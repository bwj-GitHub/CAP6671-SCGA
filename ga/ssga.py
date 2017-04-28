"""
Created on Apr 13, 2017

@author: brandon
"""


import statistics


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

    def run(self, population=None, iterations=100, log_dir=None):
        """Brief descript. of what this method does."""

        n_evals = 0

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
                n_evals += 1
            elif self.verbosity > 1:
                print("Chromo {} init_fitness: {}".format(population[i].id,
                                                          population[i].raw_fitness))

        prev_avg_fitness = statistics.mean([X.raw_fitness for X in population])
        prev_std_fitness = statistics.pstdev([X.raw_fitness for X in population])

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
                n_evals += 1

            replacements = self.select_best(parents + children, N=2)
            for pi in parent_inds:
                population[pi] = replacements.pop()

            # Calculate the average fitness of an iteration:
            avg_fitness = statistics.mean([X.raw_fitness for X in population])
            std_fitness = statistics.pstdev([X.raw_fitness for X in population])

            # Display iteration summary:
            if self.verbosity > 0:
                print("Finished iteration {}!".format(i))
                if self.verbosity > 1:
                    print("New Population:")
                    for chromo in population:
                        print("\tChromo {}, F={}".format(chromo.id, chromo.raw_fitness))
                print("Average Fitness = {} (delta={})".format(
                        avg_fitness, avg_fitness - prev_avg_fitness))
                print("Stdev of Fitness = {} (delta={})".format(
                        std_fitness, std_fitness - prev_std_fitness))
                print()
            prev_avg_fitness = avg_fitness
            prev_std_fitness = std_fitness

            if self.parameters.N_EVALS is not None  \
                    and n_evals >= self.parameters.N_EVALS:
                if self.verbosity > 0:
                    print("EVALUATION LIMIT EXCEEDED! ({}/{} evals)".format(
                            n_evals, self.parameters.N_EVALS))
                break

        return population, avg_fitness, std_fitness

    def experiment(self, population=None, iterations=5, runs=3):
        """Execute several runs of an experiment."""

        run_populations = []
        run_stats = {"avg_fitness": [], "std_fitness": []}
        avg_avg_fitness = 0
        avg_std_fitness = 0
        for i in range(runs):
            if self.verbosity > 0:
                print("*** RUN {} ***".format(i))
            use_pop = None if population is None else population.copy()
            pop_i, avg_fitness, std_fitness = self.run(population=use_pop,
                                                       iterations=iterations)
            run_populations.append(pop_i)
            run_stats["avg_fitness"].append(avg_fitness)
            run_stats["std_fitness"].append(std_fitness)
            avg_avg_fitness += avg_fitness
            avg_std_fitness += std_fitness
        avg_avg_fitness /= runs
        avg_std_fitness /= runs
        if self.verbosity > 0:
            print("Average Average Fitness: {}".format(avg_avg_fitness))
            print("Average Stdev of Fitness: {}".format(avg_std_fitness))

        return run_populations, run_stats

