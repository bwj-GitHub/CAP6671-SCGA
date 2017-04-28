"""
Created on Apr 16, 2017

@author: brandon

IMPORTANT: Requires OpeningTest, OpprimoBot is not sufficient!

SCStrategyChromo requirements:
1) A chromo consists of 2 unique sections: constructor and computeActions
# constructor
2) The constructor section has 2 types of subsections: buildingplan and squad_init
3) There is only a single buildingplan section.
4) There is at least 2 squad_init subsections and at most 10
# computeActions
5) The computeActions setup has 1 type of subsection: rule
6) There is between 2 and 10 rule subsections

Special:
Overlords and Lairs/Hives are automatically built
Only the following buildings will need to be added more than once to
the buildplan: Hatchery/Lair/Hive, Extractor(*), Nydus Canal, and
Creep/Sunken/Spore Colonies. (EXCEPTION?, upgrading faster with multiple
spires? We will assume that this will never be done.)

There should be no more than 2 Extractors per Hatchery/Lair/Hive;
"""


from ga.chromo import Chromo
from starcraft.botinit import BotInitSection
from starcraft.botactions import ComputeActionsSection
from ga.parameters import Parameters


class SCStrategyChromo(Chromo):
    """."""

    def __init__(self, chromo_id, bot_init_section, compute_actions_section):
        # TODO: document me!
        """.
        """

        super(SCStrategyChromo, self).__init__(chromo_id)
        self.BIS = bot_init_section
        self.CAS = compute_actions_section

    def clone(self, X, parameters):
        """Return a Chromo nearly identical X, with a new id."""

        BIS = self.BIS.clone()
        CAS = self.CAS.clone()
        return SCStrategyChromo(parameters.get_new_id(), BIS, CAS)

    def get_lines(self, class_name="ZergMain"):
        """Return a list of lines representing the code for an
            OpprimoBot Strategy cpp class.
        """

        # Includes:
        lines = [
                "#include \"{}.h\"".format(class_name),
                "#include \"../../Managers/BuildplanEntry.h\"",
                "#include \"../../Managers/AgentManager.h\"",
                "#include \"../RushSquad.h\"",
                "#include \"../ExplorationSquad.h\"",
                "#include \"../../Managers/ExplorationManager.h\""
                 ]
        # Constructor (BotInitSection):
        lines.extend(self.BIS.get_bot_init_section_lines(class_name))
        # Deconstructor:
        lines.extend([
                "{}::~{}()".format(class_name, class_name),
                "{",
                    "\tfor (Squad* s : squads)",
                    "\t{",
                        "\t\tdelete s;",
                    "\t}",
                    "\tinstance = NULL;",
                "}"
                      ])
        # computeActions (ComputeActionsSection):
        lines.extend(self.CAS.get_compute_actions_section_lines(class_name))
        return lines

    def write_lines(self, output_dir, class_name):
        """Write this Chromo as a cpp class for OpprimoBot."""

        lines = self.get_lines(class_name)
        filename = output_dir + class_name + ".cpp"
        with open(filename, "w") as fp:
            for line in lines:
                fp.write(line + "\n")

    @staticmethod
    def get_new_chromo(parameters):
        """Return a new, randomly generated, SCStrategyChromo."""

        BIS = BotInitSection.get_new_bot_init_section(parameters)
        CAS = ComputeActionsSection.get_new_compute_actions_section(
                BIS.get_buildplan(), BIS.get_squads(), parameters)
 
        return SCStrategyChromo(parameters.get_new_id(), BIS, CAS)

    @staticmethod
    def mutate(X, parameters):
        """Mutate Chromo X with probability indicated by parameters.

        The mutation types in the original GP bot included, check
        the respective sections to see which types were ACTUALLY
        implemented. Also, unlike the original GP bot, multiple
        types of mutation might occur.
        1) InsertSubsection
        2) RemoveSubsection
        3) ReplaceSubsection
        4) InsertMacro
        5) Remove Macro
        6) ReplaceMacro
        7) SingleParameterMutation
        8) AlterParametersMutation
        # TODO: Indicate what the "original GP bot" is referring to.
        """

        r = parameters.RAND.random()
        if r < parameters.MUT_RATE:
            if parameters.VERBOSITY > 1:
                print("Mutating chromo {}".format(X.id))
            # Mutate the BuildPlan and/or Rules
            r = parameters.RAND.random()
            if r < .75:
                X.BIS.mutate(parameters)
            if r > .25:
                X.CAS.mutate(X.BIS.get_buildplan(), X.BIS.get_squads(), parameters)

    @staticmethod
    def crossover(X1, X2, parameters):
        """Perform single-point crossover on Chromos X1 and X2 Sections
            to produce two children..

        Single-point crossover will be performed on both the Construtor
        and ComputeAction sections, separately. The crossover will
        swap the subsections in those sections after some point; all
        subsections are ordered.
        
        :return: list; list of two children SCStrategyChromos.
        """

        C1_BIS, C2_BIS = BotInitSection.crossover(X1.BIS, X2.BIS, parameters)

        C1_CAS, C2_CAS = ComputeActionsSection.crossover(X1.CAS, X2.CAS, parameters)
        C1_CAS._correct_rules(C1_BIS.get_buildplan(), C1_BIS.get_squads(), parameters)
        C2_CAS._correct_rules(C2_BIS.get_buildplan(), C2_BIS.get_squads(), parameters)
        
        C1 = SCStrategyChromo(parameters.get_new_id(), C1_BIS, C2_CAS)
        C2 = SCStrategyChromo(parameters.get_new_id(), C2_BIS, C2_CAS)
        return [C1, C2]


if __name__ == "__main__":
    parameters = Parameters()
    SCC = SCStrategyChromo.get_new_chromo(parameters)
    SCC.get_new_chromo(parameters)
    lines = SCC.get_lines("TerranMain")
    for line in lines:
        print(line)
    SCStrategyChromo.mutate(SCC, parameters)
    lines = SCC.get_lines("TerranMain")
    for line in lines:
        print(line)
