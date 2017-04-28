"""
Created on Apr 27, 2017

@author: brandon

Defines a StarCraft Genetic Programming experiment. A Steady-State
Genetic Algorithm (GA) is used.
"""


import pickle
import time

from ga.fitness import FitnessFunction, Selector  # temporary, for testing.
from ga.parameters import Parameters
from ga.ssga import SteadyStateGA
from starcraft.chromo import SCStrategyChromo
from starcraft.fitness import ReportBasedFitness, LineCountFitness


DEBUG = True


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


# To save time, we'll create a single initial population for use in
#  all experiments!
# ~6hr eval (384 mins): 192 minutes at 8min games, 192 minutes at 16 minute games
N_EVALS = 36  # 24 with 8min cap, 12 with 16 minute cap


# TODO: Load parameters from config file.
params = Parameters(verbosity=2,
                    population_size=8,
                    n_evals = N_EVALS)  # Default parameters are fine
if DEBUG:
    problem = LineCountFitness(params)  # Just use dummy fitness function for testing
else:
    problem = ReportBasedFitness(params)
selector = Selector(params)

SSGA = SteadyStateGA(chromo_cls=SCStrategyChromo, problem=problem,
                     selector=selector, parameters=params)

init_pop = load_population("../zPopulations/population_1493340294.p", params)
print(init_pop[0].raw_fitness)
pops, run_stats = SSGA.experiment(population=init_pop, iterations=5, runs=5)


# save_population(pops[0], dir_="../zPopulations/")
print(run_stats)
