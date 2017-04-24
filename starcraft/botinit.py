"""
Created on Apr 23, 2017

@author: brandon

A Strategy class in Opprimo bot consists of a bot init section and
a compute actions section; this module contains classes necessary to
construct the bot init section.
"""


import random

from ga.chromo import uniform_crossover, single_point_crossover
from starcraft.units import ZergUnits
from ga.parameters import Parameters


class BuildPlan(object):
# The first two rules are always:
#     buildplan.push_back(BuildplanEntry(UnitTypes::Zerg_Spawning_Pool, 5));
#     buildplan.push_back(BuildplanEntry(UnitTypes::Zerg_Extractor, 5));

    # Only these buildings/Upgrades/Techs will be in the building plan,
    # OpprimoBot will  build more Lairs/Hives; Extractors will be
    # added in compute actions.
    TYPES = ["Zerg_Hatchery", "Zerg_Hydralisk_Den", "Zerg_Evolution_Chamber", 
             "Zerg_Lair", "Zerg_Spire", "Zerg_Queens_Nest", "Zerg_Hive",
             "Zerg_Greater_Spire", "Zerg_Defiler_Mound", 
             "Zerg_Ultralisk_Cavern",

             ] # 0-9
    TYPES += list(ZergUnits.UPGRADE_REQS.keys())  # 10 - 25
    TYPES += list(ZergUnits.TECH_REQS.keys())  # 26 +

    def __init__(self, priorities, cutoff=24, debug=False):
        # buildings with priority > than 56 will not be included in Buildplan
        self.priorities = priorities
        self.cutoff = cutoff
        self._correct_priorities()
        
        if debug:  # Print Buildorder:
            for i in range(len(self.priorities)):
                print("{} {}".format(BuildPlan.TYPES[i], self.priorities[i]))

    def _correct_priorities(self):
        """Modify priorities such that requirements are always built before
            their dependents.
        """

        for i in range(len(self.priorities)):
            u_type = BuildPlan.TYPES[i]

            # Determine REQS:
            if i < 10:  # Check for reqs in BUILDINGS:
                reqs = ZergUnits.BUILDING_REQS[u_type]
            elif i < 26:  # Check for reqs in UPGRADES:
                reqs = ZergUnits.UPGRADE_REQS[u_type]
            else:
                reqs = ZergUnits.TECH_REQS[u_type]
            
            # Correct REQS (if necessary):
            if reqs is None:
                continue
            for req in reqs:
                priority = self.priorities[i]
                req_i = None
                if req == "Zerg_Hatchery":  # Always has at beginning
                    req_priority = 1
                elif req == "Zerg_Spawning_Pool":
                    req_priority = 5  # Always built at 5
                elif req is None:
                    continue
                else:
                    req_i = BuildPlan.TYPES.index(req)
                    req_priority = self.priorities[req_i]

                # NOTE: this only works if deps are evaluate first!
                if req_priority >= priority:
                    self.priorities[i] = req_priority + 2


    def get_buildingplan_line(self, unit, cSupply):
        """Return a str representation to add unit_type to the Buildplan."""

        # Determine the type of entry (Unit, Tech, Upgrade):
        if unit in ZergUnits.UPGRADE_REQS.keys():
            unit_type = "UpgradeTypes::" + unit
        elif unit in ZergUnits.TECH_REQS.keys():
            unit_type = "TechTypes::" + unit
        else:
            unit_type = "UnitTypes::" + unit

        # Form str:
        s = "buildplan.push_back(BuildplanEntry({}, {}));".format(unit_type, cSupply)
        return s

    def get_buildplan(self):
        """Return a list of buildings and upgrades in this buildplan."""

        buildings = ["Zerg_Hatchery", "Zerg_Spawning_Pool"]
        buildings += [self.TYPES[i] for i in range(len(self.priorities))
                      if self.priorities[i] <= self.cutoff]
        return buildings

    def get_lines(self):
        """Return a list of strs representing this subsection.
        
        All buildplans begin with both a Zerg_Spawning_Pool and a 
        Zerg_Extractor at 5 Supply.
        """

        lines = [self.get_buildingplan_line("Zerg_Spawning_Pool", 5),
                 self.get_buildingplan_line("Zerg_Extractor", 5)]  # Build second extractor?
        buildorder = [(self.priorities[i], self.TYPES[i])
                      for i in range(len(self.priorities))]
        buildorder.sort()
        for i in range(len(buildorder)):
            if buildorder[i][0] <= self.cutoff:
                lines.append(self.get_buildingplan_line(buildorder[i][1],
                                                        buildorder[i][0]))
        return lines

    def clone(self):
        """Return a deep copy of this BuildPlan."""

        clone = BuildPlan(self.priorities, cutoff=self.cutoff)
        return clone

    @staticmethod
    def crossover(X1, X2, parameters):
        """Perform uniform crossover on BuildPlans X1 and X2 to
            produce two children.
        """

        p1 = X1.priorities.copy()
        p2 = X2.priorities.copy()
        p1, p2 = uniform_crossover(p1, p2, parameters.RAND)

        return BuildPlan(p1, X1.cutoff), BuildPlan(p2, X2.cutoff)

    @staticmethod
    def get_new_buildplan(parameters):
        """Return a new, randomly generated BuildPlan."""

        priorities = [(2 * random.randint(3, 10)
                       * random.randint(1, 2)  # increase variability
                       * ( 1 if i < 5 or i > 10 else random.randint(1, 3)))
                      for i in range(len(BuildPlan.TYPES))
                      ]
        return BuildPlan(priorities, cutoff=parameters.BUILDPLAN_CUTOFF)


class SquadInit(object):
    """Contains the list of initial squads to create in Constructor."""

    S_TYPES = ["Squad::OFFENSIVE", "Squad::DEFENSIVE", "Squad::EXPLORATION",
               "Squad::SUPPORT", "Squad::RUSH", "Squad::KITE"]

    def __init__(self, squads, buildplan):
        self.squads = squads
        self.buildplan = buildplan  # A list of Buildings/Upgrades/Tech
#         self._correct_squads()

    def _correct_squads(self, parameters):
        """Modify squads so that they only contain units that can be trained
            from buildings in the buildplan.
        """

        new_squads = []
        for i in range(len(self.squads)):
            squad = self.squads[i]
            squad._correct_squad(self.buildplan)
            if len(squad.units) > 0:
                new_squads.append(squad)
            elif squad.name == "mainSquad":  # MUST have mainSquad
                new_squads.append(Squad.get_new_squad("mainSquad", 0,
                                                      self.buildplan, parameters))
        self.squads = new_squads
            

    def clone(self):
        """Return a deepcopy of this SquadInit."""

        squads = []
        for squad in self.squads:
            squads.append(squad.clone())
        return SquadInit(squads, self.buildplan.copy())

    def get_lines(self):
        """Return a list of strs representing the Initial Squad setup."""

        lines = []
        for i in range(len(self.squads)):
            lines.extend(self.squads[i].get_lines())
            lines.append("\n")
        return lines

    @staticmethod
    def crossover(X1, X2, parameters):
        """Perform uniform crossover on SquadInits X1 and X2 to
            produce two children.
            
        All Squads in each SquadInit.squads will remain intact; however,
        if a squad is added to a chromosome that does not have the 
        requisite buildplan, it will be deleted/replaced.
        """

        C1 = X1.clone()
        C2 = X2.clone()
        C1.squads, C2.squads = single_point_crossover(C1.squads, C2.squads,
                                                      parameters.RAND)
        C1._correct_squads(parameters)
        C2._correct_squads(parameters)
        return C1, C2

    @staticmethod
    def get_new_squad_init(buildplan, parameters):
        """Return a new SquadInitSubsection.

        Each SquadInit will have at least 1 mainSquad.
        """

        squads = []
        # Create MainSquad
        squads.append(Squad.get_new_squad("mainSquad", 0,
                                          buildplan, parameters))

        # Create additional squads:
        num_squads = 1 + parameters.RAND.randint(0, 14) % 9  # favor smaller num squads
        for i in range(num_squads):
            squad_name = "squad{}".format(i+1)
            squads.append(Squad.get_new_squad(name=squad_name, s_id=i+1,
                                              buildplan=buildplan,
                                              parameters=parameters))
        return SquadInit(squads, buildplan)


class Squad(object):
    """A Subsection representing the initial squad setup of a strategy."""

    def __init__(self, units, squad_id, squad_name, squad_type, squad_priority,
                 set_buildup=True, set_required=True):
        """A squad setup is a list of SquadSetupMacros and additional 
            squad parameters.

        A SquadInitSubsection will initialize a squad and add between
        1 and 10 units to that squad.

        :param units: list of tuples; a list of tuples of unit type and count.

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

        self.units = units
        self.id = squad_id
        self.name = squad_name
        self.type = squad_type
        self.priority = squad_priority
        self.set_buildup = set_buildup
        self.set_required = set_required

    def _correct_squad(self, buildplan):
        """Modify squad so that it only contains units which can be trained
            from buildings in buildplan.
        """

        new_units = []
        for i in range(len(self.units)):
            unit_t = self.units[i][0]
            unit_reqs = ZergUnits.UNIT_REQS[unit_t]
            to_add = True
            for req in unit_reqs:
                if req not in buildplan:
                    to_add = False
            if to_add is True:
                new_units.append(self.units[i])
        self.units = new_units

    def clone(self):
        """Return a deep copy of this Squad."""

        return Squad(units=self.units.copy(), squad_id=self.id,
                     squad_name=self.name, squad_type=self.type,
                     squad_priority=self.priority,
                     set_buildup=self.set_buildup,
                     set_required=self.set_required)

    def get_lines(self):
        """Return a list of strs, each str representing a single line
        of code in this Subsection.

        :return: list of str; each str corresponds to a line of code
            in the Subsection. The str will contain no additional
            white-space (tabs or newlines).
        """

        # Create new Squad:
        unit_types, unit_counts = zip(*self.units)
        init_line = ["{} = new Squad({}, {}, \"{}\", {});".format(
                self.name, self.id, self.type, self.name, self.priority)]

        # Append unit setup lines to section strs:
        squad_setup_lines =  [
                Squad.get_unit_line(self.name,
                                    "UnitTypes::" + unit_types[i],
                                    unit_counts[i])
                for i in range(len(self.units))]

        # Finish setting up the squad:
        setup_lines = [
                "{}->setBuildup({});".format(self.name, self.set_buildup),
                "{}->setRequired({});".format(self.name, self.set_required)]
        # Set Morph, if there are any Zerg_Lurkers:
        if "Zerg_Lurker" in unit_types:
            setup_lines.append(
                    "{}->setMorphsTo(UnitTypes::Zerg_Lurker);".format(self.name))
        setup_lines.append("squads.push_back({});".format(self.name))
        # TODO: if has lurkers, set morph!
        return init_line + squad_setup_lines + setup_lines

    @staticmethod
    def get_unit_line(squad_name, unit_type, num_unit):
        # RuleSubsection might also need this
        # ex: mainSquad->addSetup(UnitTypes::Protoss_Dragoon, 8);
        return "{}->addSetup({}, {});".format(squad_name, unit_type, num_unit)

    @staticmethod
    def get_new_squad(name, s_id, buildplan, parameters):

        # Generate squad parameters:
        if name == "mainSquad":
            squad_type = "OFFENSIVE"
            set_buildup = "true"
            set_required = "true"
            priority = 10
        else:
            squad_type = SquadInit.S_TYPES[parameters.RAND.randint(
                    0, len(SquadInit.S_TYPES)-1)]
            set_buildup = ["true", "false"][parameters.RAND.randint(0, 1)]
            set_required = ["true", "false"][parameters.RAND.randint(0, 1)]
            priority = 10 + parameters.RAND.randint(-2, 10)

        # Add setups to this Squad:
        UNITS = ZergUnits.get_available_units(buildplan)
        units = []
        unit_types_seen = []  # Keep track of what has been added to squad
        n_units = 1 + parameters.RAND.randint(0, 15) % 9  # prefer small n_units
        for _ in range(n_units):
            ui = parameters.RAND.randint(0, len(UNITS)-1)
            u_type = UNITS[ui]
            if u_type in unit_types_seen:
                continue  # Don't add the same unit multiple times (although you can)
            unit_types_seen.append(u_type)
            if u_type not in ["Zerg_Zergling", "Zerg_Hydralisk", "Zerg_Mutalisk",
                              "Zerg_Scourge"]:
                u_count = 1 + parameters.RAND.randint(0, 9) % 8
            else:
                u_count = 2 * (parameters.RAND.randint(1, 12))
            units.append((u_type, u_count))

        return Squad(units=units, squad_id=s_id, squad_name=name,
                     squad_type=squad_type, squad_priority=priority,
                     set_buildup=set_buildup, set_required=set_required)


def crossover_bot_init_section(X1, X2, parameters):
    # TODO: Write me!
    # NOTE: after crossing over on buildplans, make sure to update buildplan
    #  in SquadInit Subsections
    pass

def get_bot_init_section_lines(class_name="ZergMain", buildplan=None,
                               squad_init=None):
    """Return a list of lines representing the constructor of a
        Strategy class in OpprimoBot.
    """

    lines = ["{}::{}() {}".format(class_name, class_name, "\n{"), "\t// Buildingplan subsection:"]
    lines.extend(["\t"+line for line in buildplan.get_lines()])
    lines.append("\n\t// SquadInit subsection:")
    lines.extend(["\t"+line for line in squad_init.get_lines()])
    lines.extend(["\tnoWorkers = 11;", "\tnoWorkersPerRefinery = 3;", "}"])
    return lines
    


if __name__ == "__main__":
    parameters = Parameters()
    # Test BuildPlan:
    BP1 = BuildPlan.get_new_buildplan(parameters)
    BP2 = BuildPlan.get_new_buildplan(parameters)
 
    # Print buildplans:
#     lines1 = BP1.get_lines()
#     lines2 = BP2.get_lines()
#     print("BP1:")
#     for line in lines1:
#         print(line)
 
#     # Crossover:
#     children = BuildPlan.crossover(BP1, BP2, parameters)
# 
#     # print children
#     for child in children:
#         print("child:")
#         lines = child.get_subsection_lines()
#         for line in lines:
#             print(line)
#         print(child.get_buildplan())
#         print("can train: {}".format(
#                 ZergUnits.get_available_units(child.get_buildplan())))

#     # Test Squad:
#     print("Squad units:")
#     S1 = Squad.get_new_squad("mainSquad", 0, BP1.get_buildplan(), parameters)
#     print(S1.units)
#     squad_lines = S1.get_subsection_lines()
#     for line in squad_lines:
#         print(line)

    # Test SquadInit:
    SI1 = SquadInit.get_new_squad_init(BP1.get_buildplan(), parameters)
    squad_init_lines = SI1.get_lines()
#     print("\n")
#     for line in squad_init_lines:
#         print(line)
#     print("BP2:")
#     for line in lines2:
#         print(line)
    SI2 = SquadInit.get_new_squad_init(BP2.get_buildplan(), parameters)
    squad_init_lines = SI2.get_lines()
#     print("\n")
#     for line in squad_init_lines:
#         print(line)
#     # Make Love, not StarCraft (that doesn't make any sense!)
#     print("\nMaking CHidlren!\n")
#     C1, C2 = SquadInit.crossover(SI1, SI2, parameters)
#     c1lines = C1.get_lines()
#     for line in c1lines:
#         print(line)
#     print("\nC2:")
#     c2lines = C2.get_lines()
#     for line in c2lines:
#         print(line)
    
    # Test get_bot_init_section_lines:
#     print("\n")
    lines = get_bot_init_section_lines(class_name="ZergMain", buildplan=BP1,
                               squad_init=SI1)
    for line in lines:
        print(line)
