"""
Created on Apr 27, 2017

@author: brandon

Defines a StarCraft Genetic Programming experiment. A Steady-State
Genetic Algorithm (GA) is used.
"""


from ga.fitness import FitnessFunction, Selector  # temporary, for testing.
from ga.parameters import Parameters
from ga.ssga import SteadyStateGA
from starcraft.chromo import SCStrategyChromo
from starcraft.fitness import ReportBasedFitness, LineCountFitness


DEBUG = True


# TODO: Load parameters from config file.
params = Parameters(verbosity=1)  # Default parameters are fine
if DEBUG:
    problem = LineCountFitness(params)  # Just use dummy fitness function for testing
else:
    problem = ReportBasedFitness(params)
selector = Selector(params)

SSGA = SteadyStateGA(chromo_cls=SCStrategyChromo, problem=problem,
                     selector=selector, parameters=params)

pop = SSGA.run(population=None, iterations=5)
print(pop)
