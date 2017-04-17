"""
Created on Apr 14, 2017

@author: brandon
"""


from ga.fitness import FitnessFunction


class ReportBasedFitness(FitnessFunction):
    """Describes the problem to be solved in terms of Report Statistics."""

    def __init__(self, parameters):
        """Set parameters."""

        super(ReportBasedFitness, self).__init__(parameters)
        self.output_dir = parameters.DLL_DIR

    def do_raw_fitness(self, X):
        """Calculate and set the raw fitness score of Chromo X."""

        FitnessFunction.do_raw_fitness(self, X)

        # Compile, play tournament, parse results files, and chew bubble-gum:
        path_to_dll = compile_bot(X, self.output_dir)
        results_file = execute_tournament(path_to_dll)
        results = parse_results_file(results_file)
        ## can't find bubble-gum :'(

        # Calculate fitness from results:
        W = [1, 1 ,1 ,1 ,1]  # TODO: weights for results
        fitness = W[0] * results["military_victories"]
        fitness += W[1] * results["economic_victories"]
        fitness += W[2] * results["relative_destruction"]
        fitness += W[3] * results["time_to_loss"]
        fitness += W[4] * results["relative_economy"]
        X.raw_fitness = fitness


def compile_bot(X, output_dir):
    """Compile OpprimoBot with strategy represented by X, output .dll
        to output_dir.

    The output file will be named: "Bot{}.dll".format(X.id).

    :param X: SCStrategyChromo; a chromosome representing a (zerg?)
        strategy class for OpprimoBot.

    :param output_dir: str; path to directory to output .dll to.

    :return: str; the path to .dll, if build was successful, else None.
    """

    raise NotImplementedError()


def execute_tournament(path_to_dll):
    """Play several games of starcraft with bot at path_to_dll.
    
    :param path_to_dll: str; path to .dll for StarCraft bot to
        be executed.

    :return: str; path to tournament results file.
    """

    raise NotImplementedError()


def parse_results_file(filename):
    """."""

    raise NotImplementedError()
        
