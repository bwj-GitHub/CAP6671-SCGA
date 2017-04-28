"""
Created on Apr 13, 2017

@author: brandon
"""


from random import Random


class FitnessFunction(object):

    def __init__(self, parameters):
        self.parameters = parameters

    def do_raw_fitness(self, X):
        if self.parameters.VERBOSITY > 1:
            print("Evaluating individual {} for fitness...".format(X.id))
        X.raw_fitness = Random().random()
        return


class Selector(object):
    """Class for selecting some number of individauls from a population."""

    def __init__(self, parameters):
        """."""

        self.parameters = parameters
        self.k = parameters.TOURNAMENT_SIZE
        self.p = parameters.TOURNAMENT_P
        self.max_problem = parameters.MAX_PROBLEM
        self.rand = parameters.RAND
        self.t_kwargs = {"k": self.k, "p": self.p, "_max": self.max_problem,
                         "rand": self.rand}

    def select(self, population, N=2):
        """Select N unique individuals from population."""

        if N != 2:
            raise NotImplementedError("Use N=2 or override this Selector.select.")
        p1 = tournament_selection(population, **self.t_kwargs)
        p1_index = population.index(p1)
        p2 = tournament_selection(population[0:p1_index]
                                  + population[p1_index+1:],
                                  **self.t_kwargs)
        return p1_index, population.index(p2)


def tournament_selection(population, k=2, p=1.0, _max=True, rand=Random()):
    """Select k individuals from population and return the best.
    
    :param k: The tournament size.
    :param p: The probability to select the winner of the tournament;
        losers are selected with probability p * (1-p)^(n-1), where n
        is the losers order (ordered from best to worst).
    :param _max: Indicates that this is a maximization problem.
    """

    # Choose candidates
    inds = [i for i in range(len(population))]
    rand.shuffle(inds)
    pool = [population[inds[i]] for i in range(k)]

    # Sort candidates by fitness
    pool.sort(key=lambda X: X.raw_fitness, reverse=_max)

    # Select best?
    best = 0
    while best < k-1:
        r = rand.random()
        if r <= p:
            return pool[best]
        else:
            best += 1
    return pool[-1]

