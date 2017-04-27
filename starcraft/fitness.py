"""
Created on Apr 14, 2017

@author: brandon
"""

import os
import sys
import subprocess
from ga.fitness import FitnessFunction


class LineCountFitness(FitnessFunction):
    """A fitness function for testing; goal: maximize number of lines."""

    def __init__(self, parameters):
        """Set parameters."""

        super(LineCountFitness, self).__init__(parameters)
        self.output_dir = parameters.DLL_DIR

    def do_raw_fitness(self, X):
        """Calculate and set the raw fitness score of Chromo X."""

        FitnessFunction.do_raw_fitness(self, X)
        X.raw_fitness = len(X.get_lines())


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

    :param output_dir: The output directory to store the .dll file.
        Should end in a slash. In order to be compatible with
        TournamentManager, the .dll should be stored in
        TournamentManager\server\bots\<botname>\

    :return: str; the path to .dll, if build was successful, else None.
    """
    # TODO:
    # Generate .cpp file(s) and add to visual studio project

    msbuild = r"C:\Program Files (x86)\MSBuild\12.0\Bin\MSBuild.exe"      
    project = r"C:\TM\SCGABot\SCProjects\SCProjects.sln"
    rebuild = '/t:Rebuild'
    release = '/p:Configuration=Release'
    win32 = '/p:Platform=Win32'
    output = '/p:OutDir=' + output_dir
    name = "/p:TargetName=Bot{}".format(X.id)

    # Specify MSBuild path
    command = [msbuild]
    # Specify project to build
    command.append(project)
    # Specify build type
    command.append(rebuild)
    # Specify target architecture
    command.append(win32)
    # Specify relase type
    command.append(release)
    # Specify the output path
    command.append(output)
    # Specify the name of the bot
    command.append(name)

    # Build the solution
    print ('Build Start ************************')
    
    process = subprocess.Popen(args = command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    while True:
        nextline = process.stdout.readline()
        if nextline == b'' and process.poll() != None:
            break
        sys.stdout.write(nextline.decode('cp949'))      # adjust the codepage for your console
        sys.stdout.flush()

    output = process.communicate()[0]
    exitCode = process.returncode
    
    print ('************************')
    print('build finished %d ' % process.returncode)
    
    # Build successful    
    if (exitCode == 0):
         return output_dir + "Bot{}.dll".format(X.id)
    # Build failed
    else:
        return None


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
        
