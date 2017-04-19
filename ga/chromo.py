"""
Created on Apr 16, 2017

@author: brandon
"""


class Chromo(object):
    """."""

    def __init__(self, chromo_id):
        self.id = chromo_id

    def clone(self, X, parameters):
        """Return a Chromo nearly identical X, with a new id."""

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
