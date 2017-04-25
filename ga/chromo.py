"""
Created on Apr 16, 2017

@author: brandon
"""


class Chromo(object):
    """."""

    def __init__(self, chromo_id):
        self.id = chromo_id

    def clone(self, parameters):
        """Return a Chromo nearly identical self, with a new id."""

        return Chromo(parameters.get_new_id())

    @staticmethod
    def get_new_chromo(parameters):
        return Chromo(parameters.get_new_id())

    @staticmethod
    def mutate(X, parameters):
        return

    @staticmethod
    def crossover(X1, X2, parameters):
        return


def single_point_crossover(L1, L2, rand_gen):
    """Perform single-point crossover on two lists."""

    L_bp = min(len(L1), len(L2))  # Choose point within length of shortest list.
    cross_point = rand_gen.randint(0, L_bp-1)
    print("--------")
    print(L1)
    print(L2)
    print("x-over at {}".format(cross_point))
    temp = L1[cross_point:]
    L1 = L1[0:cross_point] + L2[cross_point:]
    L2 = L2[0:cross_point] + temp
    print(L1)
    print(L2)
    return L1, L2  # In case the operations are not performed in place


def uniform_crossover(L1, L2, rand_gen):
    """Perform uniform crossover on two lists."""

    n = len(L1)
    mask = [rand_gen.randint(0, 1) for _ in range(n)]
    temp1 = L1.copy()
    temp2 = L2.copy()
    L1 = [temp1[i] if mask[i] == 0 else temp2[i]
          for i in range(n)]
    L2 = [temp2[i] if mask[i] == 0 else temp1[i]
          for i in range(n)]
    return L1, L2
