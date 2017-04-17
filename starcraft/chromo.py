"""
Created on Apr 16, 2017

@author: brandon

SCStrategyChromo requirements:
1) A chromo consists of 2 unique sections: constructor and computeActions
# constructor
2) The constructor section has 2 types of subsections: buildingplan and squad_init
3) There is only a single buildingplan section.
4) There is at least 2 squad_init subsections and at most 10
# computeActions
5) The computeActions setup has 1 type of subsection: rule
6) There is between 2 and 10 rule subsections

"""


from ga.chromo import Chromo


# Section classes: ############################################################

class ConstructorSection(object):

    def __init__(self, buildplan, squads):
        self.buildplan = buildplan
        self.squads = squads

    @staticmethod
    def get_new_section(parameters):
        # Init buildingplan:
        buildplan = BuildingplanSubsection.get_new_subsection(parameters)

        # Randomly generate some number of squads
        squads = []
        n_squads = parameters.RAND.randint(2, 10)
        for n in range(n_squads):
            squads.append(SquadInitSubsection.get_new_subsection(n, parameters))

        return ConstructorSection(buildplan, squads)


class ComputeActionsSection(object):

    def __init__(self, rules):
        self.rules = rules

    @staticmethod
    def get_new_section(parameters):
        rules = []
        n_rules = parameters.RAND.randint(2, 10)
        for n in range(n_rules):
            rules.append(RuleSubsection.get_new_subsection(n, parameters))

        return ComputeActionsSection(rules)


# SubSection classes: #########################################################

class Subsection(object):
    def __init__(self, macros):
        self.macros = macros

    def get_subsection_str(self):
        """Return a list of str representations of this subsection."""

        return [self.macros[i].get_macro_str() for i in range(len(self.macros))]


class BuildingplanSubsection(Subsection):

    def __init__(self, macros):
        super(BuildingplanSubsection, self).__init__(macros)

    @ staticmethod
    def _buildplan_pushback_macro(unit_type, cSupply):
        # RuleSubsection might also need this
        # ... or tech type
        # ex: buildplan.push_back(BuildplanEntry(UnitTypes::Terran_Supply_Depot, 28));
        return "buildplan.push_back(BuildplanEntry({}, {}));".format(unit_type, cSupply)

    @staticmethod
    def get_new_subsection(parameters):
        pass


class SquadInitSubsection(Subsection):

    def __init__(self, macros):
        super(BuildingplanSubsection, self).__init__(macros)

    @staticmethod
    def _squad_addSetup(squad_name, unit_type, num_unit):
        # RuleSubsection might also need this
        # ex: mainSquad->addSetup(UnitTypes::Protoss_Dragoon, 8);
        return "{}->addSetup({}, {});".format(squad_name, unit_type, num_unit)

    @staticmethod
    def get_new_subsection(n, parameters):
        # n indicates how many squads have been produced thus-far
        pass


class RuleSubsection(Subsection):

    def __init__(self, conditions, macros):
        self.conditions = conditions
        self.macros = macros

    def get_conditions_str(self):
        pass  # TODO: Write me!

    @staticmethod
    def get_new_subsection(n, parameters):
        # n indicates how many rules have been produced thus-far
        pass


# Chromo class: ###############################################################

class SCStrategyChromo(Chromo):
    """."""

    def __init__(self, chromo_id, constructor_section, compute_actions_section):
        """.
        """

        super(SCStrategyChromo, self).__init__(chromo_id)
        self.sections = (constructor_section, compute_actions_section)

    @staticmethod
    def get_new_chromo(parameters):
        """Return a new, randomly generated, SCStrategyChromo."""

        return SCStrategyChromo(parameters.get_new_id(),
                                ConstructorSection.get_new_section(parameters),
                                ComputeActionsSection.get_new_section(parameters))

