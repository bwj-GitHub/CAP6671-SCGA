"""
Created on Apr 16, 2017

@author: brandon
"""


from random import Random

class Parameters(object):
    """Holds parameters for various components of a GA."""

    def __init__(self, population_size, max_problem=True,
                 selection_type="tournament",
                 rand_gen=Random(), verbosity=0, **kwargs):
        self.N = population_size
        self.MAX_PROBLEM = max_problem
        self.SELECTION_TYPE = selection_type
        self.RAND = rand_gen
        self.VERBOSITY = verbosity
        self.next_id = 0

        # Tournament Selection parameters:
        self.TOURNAMENT_SIZE = kwargs.get("tournament_size")
        self.TOURNAMENT_P = kwargs.get("tournament_p")

    def get_new_id(self):
        """Return a unique ID for a Chromo.

        The ID will be unique in terms of IDs produced by this Parameters
        object, IDs produced by other Parameters might overlap with IDs
        produced by this one.
        """

        id_str = "{:0>5}".format(str(self.next_id))
        self.next_id += 1
        return id_str
