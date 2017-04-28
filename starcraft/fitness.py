"""
Created on Apr 14, 2017

@author: brandon
"""

import os
import sys
import subprocess
import csv
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
        print("EVAL #{}".format(self.n_evals))
        self.n_evals += 1


class ReportBasedFitness(FitnessFunction):
    """Describes the problem to be solved in terms of Report Statistics."""

    def __init__(self, parameters):
        """Set parameters."""

        super(ReportBasedFitness, self).__init__(parameters)
        self.output_dir = r"C:\TM\TournamentManager\server\"
        self.game_time_limit = parameters.INIT_TIME_LIMIT

    def do_raw_fitness(self, X):
        """Calculate and set the raw fitness score of Chromo X."""

        FitnessFunction.do_raw_fitness(self, X)

        # Check if game time limit should increase:
        if self.n_evals > 0 and self.n_evals % self.parameters.TIME_DELTA_AFTER == 0:
            self.game_time_limit += self.parameters.TIME_DELTA

        # Compile, play tournament, parse results files, and chew bubble-gum:
        path_to_dll = compile_bot(X, self.output_dir)
        results_file = execute_tournament(path_to_dll, self.game_time_limit)
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
        self.n_evals += 1


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
    #command.append(rebuild)
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


def execute_tournament(path_to_dll, game_time_limit=None):
    """Play several games of starcraft with bot at path_to_dll.
    
    :param path_to_dll: str; path to .dll for StarCraft bot to
        be executed.

	:param game_time_limit: int or None; specifies the maximum
        time that a game will be played (in seconds) before it
        is forced to end; if None, there is no limit.

    :return: str; path to tournament statistics directory
    """
    path_to_settings= r"C:\TM\TournamentManager\server\server_settings.ini"
    path_to_server = r"C:\TM\TournamentManager\server\run_server_from_script.bat"
    path_to_local_client = r"C:\TM\TournamentManager\client\run_local_client_from_script.bat"
    path_to_vm_client = r"C:\TM\TournamentManager\client\run_vm_client_from_script.bat"
    bot_name = path_to_dll.split("\\")[-1][:-4]

    # Create directories of new bot
    path_to_bot = r"C:\TM\TournamentManager\server\bots" + "\\" + bot_name
    if not os.path.exists(path_to_bot):
        os.makedirs(path_to_bot)

    path_to_bot_ai = path_to_bot + r"\AI"
    if not os.path.exists(path_to_bot_ai):
        os.makedirs(path_to_bot_ai)

    path_to_bot_read = path_to_bot + r"\read"
    if not os.path.exists(path_to_bot_read):
        os.makedirs(path_to_bot_read)

    path_to_bot_write = path_to_bot + r"\write"
    if not os.path.exists(path_to_bot_write):
        os.makedirs(path_to_bot_write)

    # Move .dll to appropriate location
    path_to_new_dll = path_to_bot_ai + "\\" + path_to_dll.split("\\")[-1]
    os.rename(path_to_dll, path_to_new_dll)

    # Edit settings as follows:
    #   Rewrite bot name
    #   Rewrite games list name
    #   Rewrite results name
    with open(path_to_settings, 'r') as file:
        data = file.readlines()
        data[19] = "Bot  " + bot_name + "        Zerg  dll  BWAPI_412\n"
        data[82] = "GamesListFile games" + bot_name + ".txt\n"
        data[89] = "ResultsFile results" + bot_name + ".txt\n"

    with open(path_to_settings, 'w') as file:
        file.writelines(data)

    # Launch Local client
    process = subprocess.Popen([path_to_local_client], shell=True)
    
    # Launch VM Client1
    process = subprocess.Popen([path_to_vm_client], shell=True)

    # Launch Server
    process = subprocess.Popen([path_to_server], shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    while True:
        nextline = process.stdout.readline()
        if nextline == b'' and process.poll() != None:
            break
        sys.stdout.write(nextline.decode('cp949'))      # adjust the codepage for your console
        sys.stdout.flush()        
    output = process.communicate()[0]

    return path_to_bot_write


def parse_results_file(path_to_results):
    """."""
    results = {}
    results['unit_score'] = 0
    results['building_score'] = 0
    results['kill_score'] = 0
    games_counter = 0
    for filename in os.listdir(path_to_results):
        if (filename.endswith('.csv')):
            games_counter += 1
            with open(path_to_results + "\\" + filename, 'r') as file:
                reader = csv.reader(file, delimiter=";", quotechar='"', quoting=csv.QUOTE_ALL)
                for row in reader:
                    self_race = row[0]
                    enemy_race = row[1]
                    game_map = row[2]
                    result = row[3]
                    unit_score = int(row[4])
                    building_score = int(row[5])
                    kill_score = int(row[6])

                    results['enemy_race'] = enemy_race
                    results['result'] = result
                    results['unit_score'] += unit_score
                    results['building_score'] += building_score
                    results['kill_score'] += kill_score

    results['unit_score'] /= games_counter
    results['building_score'] /= games_counter
    results['kill_score'] /= games_counter                             
        
    return results
        
