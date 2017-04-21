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
    """A ConstructorSection corresponds to the Constructor for an
        OpprimoBot strategy class.
    """

    def __init__(self, buildplan, squads):
        """Add a Buildplan subsection and several SquadInit subsections.

        The ConstructorSection of a SCStrategyChromo has exactly 1
        BuildingplanSubsection, and between 2 and 10 SquadInitSubsections.

        :param buildplan: BuildingplanSubsection; indicates the initial
            build order for the strategy.

        :param squads: list of SquadInitSubsections; indicates the
            initial squad setups for the Strategy.
        """

        self.buildplan = buildplan
        self.squads = squads

    @staticmethod
    def crossover(X1, X2, parameters):
        """Perform single-point cross-over on X1 and X2's buildplans
            and squads (in-place).

        :param X1: SCStrategyChromo; the first parent for cross-over.

        :param X2: SCStrategyChromo; the second parent for cross-over.

        :param parameters: Parameters; wraps the instance of Random
            to be used for randomly generating cross-over points.
        """

        single_point_crossover(X1.buildplan, X2.buildplan, parameters.RAND)
        single_point_crossover(X1.squads, X2.squads, parameters.RAND)

    @staticmethod
    def get_new_section(parameters):
        """Return a new, randomly generated, ConstructorSection.

        Randomly generates a BuildingplanSubsection and between 2
        and 10 SquadInitSubsections and then creates a new
        ConstructorSection with them.

        :param parameters: Parameters; wraps the instance of Random
            to be used for all random number generation.

        :return: ConstructorSection.
        """

        # Create a single BuildingplanSubsection:
        buildplan = BuildingplanSubsection.get_new_subsection(parameters)

        # Randomly generate some number of SquadInitSubsections:
        squads = []
        n_squads = parameters.RAND.randint(2, 10)
        for n in range(n_squads):
            squads.append(SquadInitSubsection.get_new_subsection(n, parameters))

        return ConstructorSection(buildplan, squads)


class ComputeActionsSection(object):
    """A ComputeActionsSection corresponds to the ComputeActions method
        for an OpprimoBot strategy class.
    """

    def __init__(self, rules):
        """A ComputeActionsSection consists of between 2 and 10
            RuleSubsections.

        :param rules: list of RuleSubsections.
        """
        self.rules = rules

    @staticmethod
    def crossover(X1, X2, parameters):
        """Perform single-point cross-over on X1 and X2's rules.
        
        The cross-over is performed in place.

        :param X1: SCStrategyChromo; the first parent for cross-over.

        :param X2: SCStrategyChromo; the second parent for cross-over.

        :param parameters: Parameters; wraps the instance of Random
            to be used for randomly generating cross-over points.
        """

        single_point_crossover(X1.rules, X2.rules, parameters.RAND)

    @staticmethod
    def get_new_section(parameters):
        """Return a new, randomly generated, ComputeActionsSection.

        Randomly generates between 2 and 10 RuleSubsections and then
        creates a new ComputeActionsSection with them.

        :param parameters: Parameters; wraps the instance of Random
            to be used for all random number generation.

        :return: ComputeActionsSection.
        """

        rules = []
        n_rules = parameters.RAND.randint(2, 10)
        for n in range(n_rules):
            rules.append(RuleSubsection.get_new_subsection(n, parameters))

        return ComputeActionsSection(rules)


# SubSection classes: #########################################################

class Subsection(object):
    """Base class for all Subsections.

    All Subsections will contain a list of Macros.
    """

    def __init__(self, macros):
        """A Subsection corresponds to a group of related Macros.

        :param macros: list of Macros.
        """

        self.macros = macros

    def get_subsection_lines(self):
        """Return a list of str, each str representing a single line
        of code in this Subsection.

        :return: list of str; each str corresponds to a line of code
            in the Subsection. The str will contain no additional
            white-space (tabs or newlines).
        """

        return [self.macros[i].get_macro_str() for i in range(len(self.macros))]


class BuildingplanSubsection(Subsection):
    """A Subsection representing the initial build-order of a strategy."""

    def __init__(self, macros):
        """A building plan is an ordered list of BuildMacros.

        A building plan will contain between 5 and 50 BuildMacros.
        """

        super(BuildingplanSubsection, self).__init__(macros)

    @staticmethod
    def get_new_subsection(parameters):
        """Return a new, procedurally generated, BuildingplanSubsection.

        Procedurally generates between 5 and 50 BuildMacros and then
        creates a new BuildingplanSubsection with them.

        Note that the BuildMacro.get_new_macro method is provided
        with the index of each building built, this allows it make
        more intelligent choices when choosing buildings.

        :param parameters: Parameters; wraps the instance of Random
            to be used for all random number generation.

        :return: BuildingplanSubsection.
        """

        buildings = []
        n_buildings = parameters.RAND.randint(5, 50)
        for n in range(n_buildings):
            buildings.append(BuildMacro.get_new_macro(n, parameters))

        return BuildingplanSubsection(buildings)


class SquadInitSubsection(Subsection):
    """A Subsection representing the initial squad setup of a strategy."""

    def __init__(self, macros, squad_id, squad_name, squad_type, squad_priority,
                 set_buildup=True, set_required=True):
        """A squad setup is a list of SquadSetupMacros and additional 
            squad parameters.

        A SquadInitSubsection will initialize a squad and add between
        1 and 10 units to that squad.

        :param macros: list of SquadSetupMacros; a SquadMacro specifies
            a type and number of units of that type to add to the squad.

        :param squad_id: int; unique identifier.

        :param squad_name: str; name of the squad.

        :param squad_type: str; specifies the type of squad, either
            'Squad::OFFENSIVE', 'Squad::DEFENSIVE', 'Squad::Exploration',
            or 'Squad::SUPPORT'.

        :param squad_priority: int; the lower the int, the higher priority
            the squad is, 1 is the highest priority. Squads with priority
            1000 will not be built-up further.

        :param set_buildup: str; indicates that the squad should not activate
            until it is fully built-up; will be either 'true' or 'false'.

        :param set_required: str; indicates that the squad is required
            before an attack; will be either 'true' or 'false'.

        EX:
        mainSquad = new Squad(1, Squad::OFFENSIVE, "MainSquad", 10);
        mainSquad->addSetup(UnitTypes::Protoss_Dragoon, 10);
        mainSquad->setBuildup(true);
        mainSquad->setRequired(true);
        squads.push_back(mainSquad);
        """

        super(BuildingplanSubsection, self).__init__(macros)

        self.id = squad_id
        self.name = squad_name
        self.type = squad_type
        self.priority = squad_priority
        self.set_buildup = set_buildup
        self.set_required = set_required

    def get_subsection_lines(self):
        """Return a list of strs, each str representing a single line
        of code in this Subsection.

        :return: list of str; each str corresponds to a line of code
            in the Subsection. The str will contain no additional
            white-space (tabs or newlines).
        """

        init_line = ["{} = new Squad({}, {}, {}, {});".format(
                self.name, self.id, self.type, self.name, self.priority)]
        squad_setup_lines =  [self.macros[i].get_macro_str()
                              for i in range(len(self.macros))]
        setup_lines = [
                "{}->setBuildup({});".format(self.name, self.set_buildup),
                "{}->setRequired({});".format(self.name, self.set_required)]
        return init_line + squad_setup_lines + setup_lines

    @staticmethod
    def get_new_subsection(n, parameters):
        """Return a new, procedurally generated, SquadInitSubsection.

        Procedurally generates between 1 and 10 SquadSetupMacros and then
        creates a new SquadInitSubsection with them.

        :param parameters: Parameters; wraps the instance of Random
            to be used for all random number generation.

        :return: SquadInitSubsection.
        """

        S_TYPES = ["Squad::OFFENSIVE", "Squad::DEFENSIVE",
                   "Squad::EXPLORATION", "Squad::SUPPORT"]
        # Generate squad setups:
        squad_setups = []
        n_setups = parameters.RAND.randint(1, 10)
        for i in range(n_setups):
            squad_setups.append(SquadSetupMacro.get_new_macro(i, parameters))

        # Generate additional squad parameters
        sid = n
        if n == 0:
            # The first squad will always be the mainSquad
            sname = "mainSquad"
            stype = S_TYPES[0]
            sprio = 10
            sbuildup = "true"
            srequired = "true"
        else:
            sname = "squad" + str(sid)
            stype = S_TYPES[parameters.RAND.randint(0, 3)]
            sprio = 10 + parameters.RAND.randint(-2, 10)
            sbuildup = ["true", "false"][parameters.RAND.randint(0, 1)]
            srequired = ["true", "false"][parameters.RAND.randint(0, 1)]

        return SquadInitSubsection(squad_setups, sid, sname, stype, sprio,
                                   sbuildup, srequired)


class RuleSubsection(Subsection):
    # TODO: Finish me!
    """A Subsection representing a rule for modifying the buildplan or
        any squds during gameplay.
    """

    MAX_STAGE = 0  # Keeps track of which stages have been used thusfar
    UNITS_USED = []  # Keeps track of which units are used in buildplan

    def __init__(self, macros, stage=None, cSupply_min=0, min_min=0, gas_min=0,
                 no_units_completed_type=None, no_units_completed_min=0):
        """.

        conditions include:
        cSupply
        stage
        minerals
        gas
        noUnitsCompleted
        """

        self.macros = macros
        self.stage = stage
        self.cSupply_min = cSupply_min
        self.min_min = min_min
        self.gas_min = gas_min
        self.no_units_completed_type = no_units_completed_type
        self.no_units_completed_min = no_units_completed_min

    def get_subsection_lines(self):
        """Return a list of strs, each str representing a single line
        of code in this Subsection.

        :return: list of str; each str corresponds to a line of code
            in the Subsection. The str will contain no additional
            white-space (tabs or newlines).
        """

        stage_str = ""
        units_type_str = ""
        if self.stage is not None:
            stage_str = "stage == {} &&".format(self.stage)
        if self.no_units_completed_type is not None:
            # TODO: Finish unit_types_str!
            units_type_str = "".format()
        condition_line = [
                "if ({}min >= {} && gas >= {} &&cSupply >= {} {}) {".format(
                        stage_str, units_type_str)
                        ]
        macro_lines =  [self.macros[i].get_macro_str() 
                        for i in range(len(self.macros))]
        return condition_line + macro_lines + ["}"]

    @staticmethod
    def get_new_subsection(n, parameters):
        # n indicates how many rules have been produced thus-far
        pass  # TODO: Write me!


# Macro classes: ##############################################################

class Macro(object):
    # TODO: Finish me!
    """A Macro represents a single line of code in a OpprimoBot
        strategy class.
    """

    def __init__(self):
        pass

    def get_macro_str(self):
        return ""


class BuildMacro(Macro):
    # TODO: Finish me!
    """."""

    def __init__(self):
        """."""
        pass

    @ staticmethod
    def _buildplan_pushback_macro(unit_type, cSupply):
        # RuleSubsection might also need this
        # ... or tech type
        # ex: buildplan.push_back(BuildplanEntry(UnitTypes::Terran_Supply_Depot, 28));
        return "buildplan.push_back(BuildplanEntry({}, {}));".format(unit_type, cSupply)


class SquadSetupMacro(Macro):
    # TODO: Finish me!
    """."""

    def __init__(self):
        """."""
        pass

    @staticmethod
    def _squad_addSetup(squad_name, unit_type, num_unit):
        # RuleSubsection might also need this
        # ex: mainSquad->addSetup(UnitTypes::Protoss_Dragoon, 8);
        return "{}->addSetup({}, {});".format(squad_name, unit_type, num_unit)


# Chromo class: ###############################################################

class SCStrategyChromo(Chromo):
    """."""

    def __init__(self, chromo_id, constructor_section, compute_actions_section):
        # TODO: document me!
        """.
        """

        super(SCStrategyChromo, self).__init__(chromo_id)
        self.sections = (constructor_section, compute_actions_section)

        # Convenience attributes:
        self.buildplan = self.sections[0].buildplan
        self.squads = self.sections[0].squads
        self.rules = self.sections[1].rules

    def clone(self, X, parameters):
        """Return a Chromo nearly identical X, with a new id."""

        return Chromo(parameters.get_new_id())

    @staticmethod
    def get_new_chromo(parameters):
        """Return a new, randomly generated, SCStrategyChromo."""

        return SCStrategyChromo(parameters.get_new_id(),
                                ConstructorSection.get_new_section(parameters),
                                ComputeActionsSection.get_new_section(parameters))

    @staticmethod
    def mutate(X, parameters):
        # TODO: Finish me!
        """Mutate Chromo X with probability indicated by parameters.

        A mutation will occur with probability parameters.MUT_RATE.
        The mutation will be exactly one of the following types of
        mutations:
        1) InsertSubsection
        2) RemoveSubsection
        3) ReplaceSubsection
        4) InsertMacro
        5) Remove Macro
        6) ReplaceMacro
        7) SingleParameterMutation
        8) AlterParametersMutation
        """
        
        # Mutation types: #####################################################
        def insert_subsection(X, parameters):
            pass
        
        def remove_subsection(X, parameters):
            pass
        
        def replace_subsection(X, parameters):
            pass
        
        def insert_macro(X, parameters):
            pass

        def remove_macro(X, parameters):
            pass
        
        def replace_macro(X, parameters):
            pass

        def single_param(X, parameters):
            pass
        
        def alter_params(X, parameters):
            pass

        # End Mutation types ##################################################

        MUT_TYPES = [insert_subsection, remove_subsection, replace_subsection,
                     insert_macro, remove_macro, replace_macro,
                     single_param, alter_params]
        r = parameters.RAND.random()
        if r > parameters.MUT_RATE:
            # Randomly choose mutation type:
            mt = parameters.RAND.randint(0, len(MUT_TYPES)-1)
            MUT_TYPES[mt](X, parameters)
        else:
            return  # No mutation

    @staticmethod
    def crossover(X1, X2, parameters):
        """Perform single-point crossover on Chromos X1 and X2 Sections
            to produce two children..

        Single-point crossover will be performed on both the Construtor
        and ComputeAction sections, separately. The crossover will
        swap the subsections in those sections after some point; all
        subsections are ordered.
        """

        C1 = X1.clone()
        C2 = X2.clone()
        ConstructorSection.crossover(C1, C2, parameters)
        ComputeActionsSection.crossover(C1, C2, parameters)
        return C1, C2

def single_point_crossover(L1, L2, rand_gen):
    """Perform single-point crossover on two lists."""

    L_bp = min(len(L1), len(L2))  # Choose point within length of shortest list.
    cross_point = rand_gen.randint(0, L_bp-1)
    temp = L1[cross_point:]
    L1 = L1[0:cross_point] + L2[cross_point:]
    L2 = L2[0:cross_point] + temp
