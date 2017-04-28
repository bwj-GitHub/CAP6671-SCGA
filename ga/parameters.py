"""
Created on Apr 16, 2017

@author: brandon
"""


from random import Random


class Parameters(object):
    """Holds parameters for various components of a GA."""

    def __init__(self, population_size=10, max_problem=True,
                 selection_type="tournament",
                 rand_gen=Random(), verbosity=0, **kwargs):
        self.N = population_size
        self.MAX_PROBLEM = max_problem
        self.SELECTION_TYPE = selection_type
        self.RAND = rand_gen
        self.VERBOSITY = verbosity
        self.MUT_RATE = .75
        self.LOG_DIR = kwargs.get("log_out", "./LOGS/")
        self.N_EVALS = kwargs.get("n_evals", None)  # if None, go for specified its
        self.next_id = 0

        # Tournament Selection parameters:
        self.TOURNAMENT_SIZE = kwargs.get("tournament_size", 2)
        self.TOURNAMENT_P = kwargs.get("tournament_p", .95)

        # StarCraft. Parameters (TODO: move these to subclass?):
        self.BUILDPLAN_CUTOFF = 32  # Don't include items in buildplan with Supply > than this
        self.DLL_DIR = "./"

        self.INIT_TIME_LIMIT = kwargs.get("init_time_limit", 480)  # default: 8m
        self.TIME_DELTA_AFTER = kwargs.get("time_delta_after", 24)  # default 24 evals
        self.TIME_DELTA = kwargs.get("time_delta", 480)  # default +8m


    def get_new_id(self):
        """Return a unique ID for a Chromo.

        The ID will be unique in terms of IDs produced by this Parameters
        object, IDs produced by other Parameters might overlap with IDs
        produced by this one.
        """

        id_str = "{:0>5}".format(str(self.next_id))
        self.next_id += 1
        return id_str
