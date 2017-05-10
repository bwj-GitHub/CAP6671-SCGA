"""
Created on Apr 14, 2017

@author: brandon
"""

import os
import sys
import subprocess
import time
import csv
from shutil import copyfile
from collections import defaultdict
from ga.fitness import FitnessFunction
from starcraft.chromo import SCStrategyChromo


class LineCountFitness(FitnessFunction):
    """A fitness function for testing; goal: maximize number of lines."""

    def __init__(self, parameters):
        """Set parameters."""

        super(LineCountFitness, self).__init__(parameters)

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
        self.dll_out_dir = parameters.DLL_OUT_DIR
        self.bot_src_dir = parameters.BOT_SRC_DIR
        self.ms_build = parameters.MS_BUILD
        self.bot_sln = parameters.BOT_SLN
        self.tm_dir = parameters.TM_DIR

		
    def do_raw_fitness(self, X):
        """Calculate and set the raw fitness score of Chromo X."""

        FitnessFunction.do_raw_fitness(self, X)

        # Compile the bot
        path_to_dll = compile_bot(X,
                                  self.dll_out_dir,
                                  self.bot_src_dir,
                                  self.ms_build,
                                  self.bot_sln)

        # If compilation failed, try one more time
        if (not path_to_dll):
            path_to_dll = compile_bot(X,
                                      self.dll_out_dir,
                                      self.bot_src_dir,
                                      self.ms_build,
                                      self.bot_sln)

            # If compilation still failed, fitness is 0
            if (not path_to_dll):
                X.raw_fitness = 0
                return

        fitness = 0
            
        # Play a tournament against easy opponents
        results_easy = defaultdict(lambda: 0)
        results_file_easy = execute_tournament(path_to_dll, self.tm_dir, 'easy')
        results_easy = parse_results_file(results_file_easy)

        time.sleep(15)

        # If we won a match against easy opponents, play against a harder opponent
        results_hard = defaultdict(lambda: 0)
        if (results_easy['wins'] > 0):
            # Fitness bonus for winning
            fitness += 10000
            results_file_hard = execute_tournament(path_to_dll, self.tm_dir, 'hard')
            results_hard = parse_results_file(results_file_hard)

        # Calculate fitness from results:               
        fitness += results_easy['relative_score'] + results_hard['relative_score']
        X.raw_fitness = fitness


def compile_bot(X, dll_out_dir, bot_src_dir, ms_build, bot_sln):
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
    # Add .cpp to project
    X.write_lines(bot_src_dir + r"\Commander\Terran" + "\\", "TerranMain")

    # Build settings
    msbuild = ms_build   
    project = bot_sln
    rebuild = '/t:Rebuild'
    release = '/p:Configuration=Release'
    win32 = '/p:Platform=Win32'
    output = '/p:OutDir=' + dll_out_dir
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
         return dll_out_dir + "Bot{}.dll".format(X.id)
    # Build failed
    else:
        return None


def execute_tournament(path_to_dll, tm_dir, difficulty):
    """Play several games of starcraft with bot at path_to_dll.
    
    :param path_to_dll: str; path to .dll for StarCraft bot to
        be executed.

    :return: str; path to tournament statistics directory
    """
    path_to_local_client = tm_dir + r"\client\run_local_client_from_script.bat"
    path_to_vm_client = tm_dir + r"\client\run_vm_client_from_script.bat"
    bot_name = path_to_dll.split("\\")[-1][:-4]
    
    if difficulty == 'easy':
        path_to_server = tm_dir + r"\server\run_server_from_script_easy.bat"
        path_to_settings = tm_dir + r"\server\server_settings_easy.ini"
        results_file = bot_name + "Easy.txt"
    elif difficulty == 'hard':
        path_to_server = tm_dir + r"\server\run_server_from_script_hard.bat"
        path_to_settings = tm_dir + r"\server\server_settings_hard.ini"
        results_file = bot_name + "Hard.txt"

    # Create directories of new bot
    path_to_bot = tm_dir + r"\server\bots" + "\\" + bot_name
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
    try:
        path_to_new_dll = path_to_bot_ai + "\\" + path_to_dll.split("\\")[-1]
        copyfile(path_to_dll, path_to_new_dll)
    except:
        pass

    # Edit settings as follows:
    #   Rewrite bot name
    #   Rewrite games list name
    #   Rewrite results name
    with open(path_to_settings, 'r') as file:
        data = file.readlines()
        data[19] = "Bot  " + bot_name + "        Terran  dll  BWAPI_412\n"
        data[82] = "GamesListFile games" + results_file + "\n"
        data[89] = "ResultsFile results" + results_file + "\n"

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

    return tm_dir + r"\server\results" + results_file


def parse_results_file(results_file):
    """."""
    print("Parsing results: " + results_file)
    results = defaultdict(lambda: 0)
    
    with open(results_file, 'r') as file:
        prev_line = []
        for i, line in enumerate(file):
            if ((i+1) % 2 == 0):
                stats = line.split()
                home = stats[2]
                away = stats[3]
                game_map = stats[4]
                hostwon = stats[5]
                hostcrash = stats[6]
                opponentcrash = stats[7]
                draw = stats[8]
                hostscore = int(stats[9])
                opponentscore = int(stats[10])

                results['relative_score'] += hostscore - opponentscore

                if (hostwon == 'true' and prev_line.split()[5] == 'true'):
                    results['wins'] += 1
                elif (draw == 'true' or opponentcrash == 'true'):
                    results['draws'] += 1
                elif (hostwon == 'false' and draw == 'false' or hostcrash == 'true'):
                    results['loses'] += 1
            else:
                prev_line = line
        
    return results
        
