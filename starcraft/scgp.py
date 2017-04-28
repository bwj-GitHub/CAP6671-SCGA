"""
Created on Apr 27, 2017

@author: brandon

Defines a StarCraft Genetic Programming experiment. A Steady-State
Genetic Algorithm (GA) is used.

IMPORTANT: Requires OpeningTest, OpprimoBot is not sufficient!
"""


import pickle
import time

from ga.fitness import Selector  # temporary, for testing.
from ga.parameters import Parameters
from ga.ssga import SteadyStateGA
from starcraft.chromo import SCStrategyChromo
from starcraft.fitness import ReportBasedFitness, LineCountFitness


DEBUG = True
SAVE_POPULATIONS = True
EXP_NUM = 2  # 1 - control, 2 - increase time limit halfway

# EXP Parameters:
BUILDPLAN_CUTOFF = 32  # Don't include items in buildplan with Supply > than this
DLL_DIR = "./"  # TODO: Change this!

# Each of these experiments requires ~384 minutes to evaluate sequentially;
#  each evaluation is assumed to be only a single game.
if EXP_NUM == 1:  # EXP 1:
    N_EVALS = 24
    INIT_TIME_LIMIT = 960  # constant 16 minute cap
    TIME_DELTA_AFTER = None  # do not increase time limit
    TIME_DELTA = None
elif EXP_NUM == 2:  # EXP 2:
    N_EVALS = 36
    INIT_TIME_LIMIT = 480  # Begin with 8 minute cap
    TIME_DELTA_AFTER = 24  # After 24 evals, increase cap by...
    TIME_DELTA = 480       # ... 8 minutes (16 minutes total)

# Initial Population?
INIT_POPULATION = None  # specify filename


def save_population(population, dir_):
    """Pickle the given population to a file in dir_.

    A unique name for the file is created, based on the current
    time.
    """

    timestamp = "{:.0f}".format(time.time())
    filename = dir_ + "population_{}.p".format(timestamp)
    with open(filename, "wb") as fp:
        pickle.dump(population, fp)


def load_population(filename, parameters):
    """Load population file and update parameters.
    
    Sets the next id in parameters to 1 above the highest id
    seen in the population pickle.
    """

    max_int_seen = 0
    with open(filename, "rb") as fp:
        init_pop = pickle.load(fp)
    for X in init_pop:
        X_id = int(X.id)
        if X_id > max_int_seen:
            max_int_seen = X_id
    parameters.next_id = max_int_seen + 1
    return init_pop

# Prepare GA:
params = Parameters(verbosity=2,
                    population_size=8,
                    n_evals = N_EVALS,
                    init_time_limit = INIT_TIME_LIMIT,
                    time_delta_after = TIME_DELTA_AFTER,
                    time_delta = TIME_DELTA
                    )
if DEBUG:
    problem = LineCountFitness(params)  # dummy fitness function for testing
else:
    problem = ReportBasedFitness(params)
selector = Selector(params)
SSGA = SteadyStateGA(chromo_cls=SCStrategyChromo, problem=problem,
                     selector=selector, parameters=params)

# Load Intial Population (?):
if INIT_POPULATION is not None:
    print("Loading initial population...")
    init_pop = load_population(INIT_POPULATION, params)
else:
    init_pop = None

# Run the experiment:
pops, run_stats = SSGA.experiment(population=init_pop, iterations=20, runs=5)
print(run_stats)

# Save population(s):
if SAVE_POPULATIONS:
    print("Saving population...")
    for i in range(len(pops)):
        save_population(pops[i], dir_="../zPopulations/")
    
