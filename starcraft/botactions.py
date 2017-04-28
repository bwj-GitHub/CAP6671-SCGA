"""
Created on Apr 23, 2017

@author: brandon
"""


from ga.chromo import single_point_crossover
from ga.parameters import Parameters
from starcraft.units import TerranUnits
from starcraft.botinit import BuildPlan, SquadInit, BotInitSection


class ComputeActionsSection(object):
    """Defines the set of rules to be evaluated and executed during
        in the computeActions method.
    """

    def __init__(self, rules):
        self.rules = rules

    def _correct_stage(self):
        """Ensure that there is a valid progression of stages in rules."""

        # Sort rules by stage (no stage goes last):
        self.rules.sort(key=lambda x: x.stage if x.stage is not None else 11)

        # Adjust stages so that they count up from 0:
        s = 0
        for i in range(len(self.rules)):
            stage = self.rules[i].stage
            if  stage is not None and stage != s:
                self.rules[i].stage = s
                s += 1
            elif stage == s:
                s += 1

    def _correct_rules(self, buildplan, squads, parameters):
        """Change rules to reflect changes in buildplan and/or squads."""

        for rule in self.rules:
            rule.correct_rule(buildplan, squads, parameters)


    def clone(self):
        """Return a deep copy of this ComputeActionsSections."""

        rules = []
        for rule in self.rules:
            rules.append(rule.clone())
        return ComputeActionsSection(rules)

    def mutate(self, buildplan, squads, parameters):
        """Mutate one or more rules in this ComputeActionsSection, and/or
            insert/remove a new rule.
        """

        # Determine some number of rules to mutate:
        n_muts = parameters.RAND.randint(1, 3)
        for _ in range(n_muts):
            R = len(self.rules)
            r = parameters.RAND.random()
            # Determine type of mutation and mutate:
            if r < .1 and R < 10:   # Add new Rule:
                self.rules.append(Rule.get_new_rule(R, buildplan,
                                                    squads, parameters))
            elif r < .2 and R > 2:  # Remove Rule:
                ri = parameters.RAND.randint(0, R-1)
                del self.rules[ri]
            else:                   # Mutate a Rule:
                # Select a rule to mutate:
                ri = parameters.RAND.randint(0, R-1)
                self.rules[ri].mutate(buildplan, squads, parameters)
        
        # Correct stage variables (if necessary):
        self._correct_stage()

    def get_compute_actions_section_lines(self, class_name="TerranMain"):
        """Return a list of lines representing the computeActions method
             of a Strategy class in OpprimoBot.
        """

        # Add constant init lines:

    
        lines = [
                 "void {}::computeActions()".format(class_name),
                 "{",
                 "\tcomputeActionsBase();",
                 "\tnoWorkers = 12 * AgentManager::getInstance()->countNoFinishedUnits(UnitTypes::Terran_Command_Center) + 2 * AgentManager::getInstance()->countNoFinishedUnits(UnitTypes::Terran_Refinery);",
                 "\tif (noWorkers > 30) noWorkers = 30;",
                 "\tint cSupply = Broodwar->self()->supplyUsed() / 2;",
                 "\tint min = Broodwar->self()->minerals();",
                 "\tint gas = Broodwar->self()->gas();",

#                  "\t// Additional code to observe the enemy, based on code from",
#                  "\t//  OpeningTest fork of OpprimoBot by andertavares:",
#                  "\tSpottedObjectSet& enemyUnits = ExplorationManager::getInstance()" \
#                     "->getSpottedUnits();",
                "\n\t//Rules Subsections:"
                 ]

        # Add lines for each Rule:
        for rule in self.rules:
            lines.extend(["\t"+line for line in rule.get_lines()])

        # Complete Section and return lines:
        lines.append("}")
        return lines

    @staticmethod
    def crossover(X1, X2, parameters):
        """Perform single-point crossover on ComputeActionsSection
            X1 and X2 to produce 2 children.
        """

        C1 = X1.clone()
        C2 = X2.clone()
        C1.rules, C2.rules = single_point_crossover(C1.rules, C2.rules,
                                                      parameters.RAND)
        C1._correct_stage()
        C2._correct_stage()
        return C1, C2

    @staticmethod
    def get_new_compute_actions_section(buildplan, squads, parameters):
        """Return a new ComputeActionsSection with 2-10 Rules."""

        rules = []
        n_rules = 2 + parameters.RAND.randint(0, 10) % 9  # favor less
        stage = 0
        for _ in range(n_rules):
            rules.append(Rule.get_new_rule(stage, buildplan, squads, parameters))
            stage = rules[-1].stage + 1 if rules[-1].stage is not None else stage

        return ComputeActionsSection(rules)


class Rule(object):

    """A Rule specifies a set of Macros to be executed if the rule's 
        conditions are satisfied.
    """
    # These enemy units types can be checked for in a rule's condition:
    E_AIR = ["UnitTypes::Terran_Battlecruiser", "UnitTypes::Terran_Wraith"]
    E_MECH = ["UnitTypes::Terran_Battlecruiser",
              "UnitTypes::Terran_Siege_Tank_Siege_Mode",
              "UnitTypes::Terran_Siege_Tank_Tank_Mode",
              "UnitTypes::Terran_Vulture",
              "UnitTypes::Terran_Science_Vessel",
              "UnitTypes::Terran_Wraith",
              "UnitTypes::Terran_Goliath"
              ]
    E_LAND = ["UnitTypes::Terran_Marine",
              "UnitTypes::Terran_Firebat",
              "UnitTypes::Terran_Ghost",
              "UnitTypes::Terran_Goliath",
              "UnitTypes::Terran_Vulture",
              "UnitTypes::Terran_Siege_Tank_Siege_Mode",
              "UnitTypes::Terran_Siege_Tank_Tank_Mode",
              "UnitTypes::Terran_Bunker"]

    def __init__(self, macros, stage, no_bases, minerals, gas, unit_reqs, enemy_has):
        """Set the macros to execute when the specified conditions are met.

        :param macros: list of Macros; code to execute when conditions are met.

        :param stage: int or None; if int, this rule will only be executed
            if the global stage == self.stage. This rule will ALWAYS
            increment the stage variable.

        :param no_bases; int or None; if int, this rule will only be executed
            if the bot has a number of bases greater than no_bases.

        :param minerals: int.

        :param gas: int.
        
        :param unit_reqs: None or list of tuples (str, int); indicates which
            (if any), and how many, units/buildings/upgrades/techs should be
            present for this rule to execute.

        :param enemy_has: None or list of tuples (str, int); indicates which,
            and how many, enemy units of the given type should have been
            spotted for this rule to execute.
        """

        self.macros = macros
        self.stage = stage
        self.no_bases = no_bases
        self.minerals = minerals
        self.gas = gas
        self.unit_reqs = unit_reqs
        self.enemy_has = enemy_has

    def correct_rule(self, buildplan, squads, parameters):
        """Remove conditions/macros from the Rule that couldn't possibly
            be evaluated/executed based on buildplan.
            
        Macros will be removed if: they reference non-existing squads;
        add a building whose prerequisites don't exist; adds an existing
        building.
        """

        new_macros = []
        for macro in self.macros:
            if macro[0] == "build":
                if macro[1] in buildplan:
                    continue
                # Determine type of build
                if macro[1] in TerranUnits.BUILDING_REQS.keys():
                    reqs = TerranUnits.BUILDING_REQS[macro[1]]
                elif macro[1] in TerranUnits.UPGRADE_REQS.keys():
                    reqs = TerranUnits.UPGRADE_REQS[macro[1]]
                else:
                    reqs = TerranUnits.TECH_REQS[macro[1]]
                # Check for reqs:
                if reqs is not None and reqs[0] not in buildplan:
                    continue
                else:
                    new_macros.append(macro)
            else:  # squad macro
                if macro[1][1]-1 >= len(squads):  # squad doesn't exist
                    continue
                else:
                    new_macros.append(macro)
        self.macros = new_macros

    def _get_macro_lines(self):
        """Return a list of strs representing self.macros."""

        lines = []
        for macro in self.macros:
            # Determine type of macro:
            if macro[0] == "build":
                macro_line = "\t" + BuildPlan.get_buildingplan_line(
                        macro[1], "cSupply")
            else:
                macro_line = "\t" + macro[2][0].format(macro[1][0], *macro[2][1:])
#                 macro_line = "\t{}".format(macro)
            lines.append(macro_line)
        return lines

    def get_lines(self):
        """Return a list of strs representing this rule."""

        stage_str = ""
        units_str = ""
        enemy_str = ""
        # stage == ?
        if self.stage is not None:
            stage_str = "stage == {} && ".format(self.stage)

        # check own units?
        if self.unit_reqs is not None:
            for req in self.unit_reqs:
                units_str += " && AgentManager::getInstance()" \
                        "->countNoFinishedUnits({}) > {}".format(
                        TerranUnits.get_full_name(req[0]), req[1])

        # check enemy units?
        if self.enemy_has is not None:
            for req in self.enemy_has:
                enemy_str += " && enemyUnits.countUnitsOfType({}) > {}".format(
                        req[0], req[1])

        # All other conditions can be 0 if they are not desired
        condition_line = [
                "if ({}AgentManager::getInstance()->countNoBases() > {} " \
                        "&& min >= {} && gas >= {}{}{})".format(
                        stage_str, self.no_bases, self.minerals, self.gas,
                        units_str, enemy_str),
                        "{"]
        macro_lines = self._get_macro_lines()
#         macro_lines =  [self.macros[i].get_macro_str() 
#                         for i in range(len(self.macros))]
        if self.stage is not None:
            macro_lines.append("\tstage++;")
        return condition_line + macro_lines + ["}"]

    def clone(self):
        u_reqs = self.unit_reqs.copy() if self.unit_reqs is not None else None
        e_has = self.enemy_has.copy() if self.enemy_has is not None else None
        return Rule(self.macros.copy(), self.stage, self.no_bases,
                    self.minerals, self.gas,
                    u_reqs, e_has)

    def _mutate_conditions(self, parameters):
        """Randomly change the conditions of this Rule.
        
        Changes can be to minerals, gas, no_bases, and/or enemy_has
        """

        # TODO: do something more... sensical?
        ri = parameters.RAND.randint(0, 100)
        if ri % 2 == 0:
            self.minerals += 25 * parameters.RAND.randint(-5, 5)
#         else:
#             self.enemy_has = self._get_enemy_has(parameters, 1)
        if ri < 20:
            self.gas += 15 * parameters.RAND.randint(-5, 5)
        if ri % 20 == 0:
            self.no_bases += parameters.RAND.randint(-1, 1)

    def mutate(self, buildplan, squads, parameters):
        """Randomly change the parameters of this rule or its macros.

        Mutation types include:
        1) Insert a new macro
        2) Remove an existing macro
        3) change conditions
        """

        # Chose mutation type:
        r = parameters.RAND.random()
        if r < .165:        # Insert new (buildplan) macro
            self.macros.append(Rule._get_buildplan_macro(buildplan, parameters))
        elif r < .33:       # Insert new (squad) macro
            self.macros.append(Rule._get_squad_macro(buildplan, squads, parameters))
        elif r < .66 and len(self.macros) > 1:  # Remove existing macro
            # chose macro to delete:
            mi = parameters.RAND.randint(0, len(self.macros)-1)
            del self.macros[mi]
        else:               # Change conditions
            self._mutate_conditions(parameters)

    # NOTE: Crossover will not be performed on individual Rules
#     @staticmethod
#     def crossover(R1, R2, parameters):
#         """."""
# 
#         pass

    @staticmethod
    def _u_no_(u_type, parameters):
        """Return an appropriate count for u_type."""

        # Expensive/Support units, not likely to have more than 6
        if u_type in ["Terran_Battlecruiser", "Terran_Siege_Tank_Tank_Mode",
                      "Terran_Science_Vessel", "Terran_Dropship"]:
            return parameters.RAND.randint(0, 6) % 6
        # Very cheap unit, likely to have many of these
        if u_type == "Terran_Marine":
            return parameters.RAND.randint(10, 30)
        # Not sure about other units, let GA take care of that!
        return parameters.RAND.randint(0, 21) % 20

    @staticmethod
    def _get_unit_reqs(buildplan, units, parameters):
        """Return a list of buildings/units to check for.

        Don't check for a building if it is NOT in buildingplan;
        note that the buildplan SHOULD include items that were
        added by previous Rules.
        """

        def filter_buildplan(buildplan):
            """Return a list of Buildings in buildplan.

            buildplan containts a mixture of buildings, upgrades,
            and tech.
            """

            buildings = []
            for b in buildplan:
                if b in TerranUnits.BUILDING_REQS.keys():
                    buildings.append(b)
            return buildings

        # Filter buildplan and determine number of units to check for:
        buildings = filter_buildplan(buildplan)  # ignore upgrades/tech
        unit_reqs = []
        n_units = 1 + parameters.RAND.randint(0, 3) % 3  # favor 1
        u_track = []  # track units already added

        # Create n_units unit reqs:
        for _ in range(n_units):
            # Check for some building or unit:
            r = parameters.RAND.random()
            if r < .5:  # check for some building:
                u_type = buildings[parameters.RAND.randint(0, len(buildings)-1)]
                u_count = parameters.RAND.randint(0, 3)

            else:       # check for some unit:
                u_type = units[parameters.RAND.randint(0, len(units)-1)]
                u_count = Rule._u_no_(u_type, parameters)
            # Do not add the same unit_t twice:
            if u_type in u_track:
                continue
            u_track.append(u_type)
            unit_reqs.append((u_type, u_count))
        return unit_reqs

    @staticmethod
    def _e_no(e_type, parameters):
        """Return an appropriate count for e_type.

        Because of varying unit costs, some units are unlikely to
        appear in certain quantities (i.e.: you will never see 20
        Battlecruisers).
        """

        # Battlecruisers are expensive, and ghosts require micro management
        if e_type in ["UnitTypes::Terran_Battlecruiser",
                      "UnitTypes::Terran_Ghost"]:
            return parameters.RAND.randint(0, 6) % 6  # increase p(0)
        # At least a handful of marines will almost always be used
        if e_type == "UnitTypes::Terran_Marine":
            return parameters.RAND.randint(10, 30)
        # Not sure about other units, let GA take care of that!
        return parameters.RAND.randint(0, 21) % 20  # increase p(0|1)

    @staticmethod
    def _get_enemy_has(parameters, n=None):
        """Return a list of enemy units to check for.

        :return: list; a list of tuples containing a str representing
            an enemy unit type and an int, representing the min count
            to trigger the rule.
        """

        # Check for 1-3 enemy units (0 will occur if this not called)
        enemy_units = []
        e_track = []  # don't check for same enemy_t twice!
        n_units = n if n is not None else parameters.RAND.randint(1, 3)
        for _ in range(n_units):
            # Choose an E_* list to draw from:
            E = [Rule.E_AIR, Rule.E_MECH, Rule.E_LAND][parameters.RAND.randint(0, 2)]
            unit_t = E[parameters.RAND.randint(0, len(E)-1)]
            # Do not add the same unit_t twice:
            if unit_t in e_track:
                continue
            e_track.append(unit_t)
            # Choose a min count of unit_t:
            e_count = Rule._e_no(unit_t, parameters)
            enemy_units.append((unit_t, e_count))
        return enemy_units

    @staticmethod
    def _get_buildplan_macro(buildplan, parameters):
        """Return a tuple representing a change to the buildplan.

        :return: tuple; the tuple will be of form:
            (building/tech/upgrade, *Type)
        """

        # Chose type:
        m_type = ["building", "tech", "upgrade"][parameters.RAND.randint(0, 2)]
        m_unit = TerranUnits.next_on_buildplan(buildplan, parameters, type_=m_type)
        # NOTE: m_unit might still be building, even if m_type is not.
        return ("build", m_unit)

    @staticmethod
    def _get_squad_macro(buildplan, squads, parameters):
        """Return a tuple representing a change to squads.
        
        There are 5 types of squad macros:
        1) removeSetup(unit, no): removes some unit from the squad; can
            only be used if that unit is ALREADY a part of that squad.
        2) addSetup(unit, no): adds some unit to the squad; can only be
            used if that unit's reqs are satisfied.
        3) setBuildup(true/false): determines if the squad can be set
            to active; if true, this squad will not activate.
        4) setPriority(prio): sets the relative importance of this
            squad, with 1 being the most important. More important
            squads will be filled first. If 1000, the squad will
            not be built up.
        5) setActivePriority(prio): sets the priority of this squad
            AFTER it has been activated.

        :param buildplan: list; list of buildings that MIGHT be built by
            this strategy.

        :param squads: list of Squads.
        """

        # Determine what squad this macro will affect:
        squad_i = parameters.RAND.randint(0, len(squads)-1)

        # Determine what kind of macro this will be:
        m_type = 1 + parameters.RAND.randint(1, 5) % 5  # favor 1 (addSetup)
        m_parameters = None
        if m_type == 1:  # removeSetup()
            s_units, s_counts = zip(*squads[squad_i].units)
            u = parameters.RAND.randint(0, len(s_units)-1)  # choose unit
            d_count = parameters.RAND.randint(1, s_counts[u])
            m_parameters = ("{}->removeSetup({}, {});",
                            TerranUnits.get_full_name(s_units[u]), d_count)

        elif m_type == 2:  # addSetup()
            # Add some number of some unit that can be built given buildplan:
            u_type = parameters.RAND.choice(TerranUnits.get_available_units(buildplan))
            if u_type not in ["Terran_Marine", "Terran_Firebat", "Terran_Wraith",
                                          "Terran_Medic"]:
                u_count = 1 + parameters.RAND.randint(0, 9) % 8
            else:
                u_count = 2 * parameters.RAND.randint(1, 12)
            m_parameters = ("{}->addSetup({}, {});",
                            TerranUnits.get_full_name(u_type), u_count)

        elif m_type == 3:   # setBuildup()
            m_parameters = ("{}->setBuildup({});",
                            parameters.RAND.choice(["true", "false"]))

        elif m_type == 4:  # setPriority()
            m_parameters = ("{}->setPriority({});", 
                            5 + parameters.RAND.randint(0, 200) % 146)

        else:  # type 5
            # Set to 1 or 1000 with probabilities .25 and .25, respectively;
            # set to integer between 5 and 150 with probability .5
            a_prio = 1000
            r = parameters.RAND.random()
            if r < .25:
                a_prio = 1
            elif r < .75:
                a_prio = 5 + parameters.RAND.randint(0, 200) % 146  # favor low
            m_parameters = ("{}->setActivePriority({});", a_prio)

        return ("squad", (squads[squad_i].name,
                          squads[squad_i].id), m_parameters)

    @staticmethod
    def get_new_rule(n, buildplan, squads, parameters):
        """Return a new Rule Subsection.

        :param n: int; indicates which stage this Rule MIGHT be. stage
            could also be set to None for this Rule.

        :param buildplan: list; list of buildings that MIGHT be built by
            this strategy.

        :param units: list; list of units that MIGHT be built by this
            strategy. A unit MIGHT be built if it is added to AT LEAST
            one squad, either in the bot_init section or in a PREVIOUS
            Rule.

        :param squads: list of Squads.
        """

        # n indicates potential stage (won't necessarily be used)
        # NOTE: buildplan includes items that MIGHT be built during computeActions

        # Generate condition parameters:
        units = SquadInit.get_units(squads)
        stage = None
        r = parameters.RAND.random()
        if r < .5:
            stage = n
        no_bases = -1 + parameters.RAND.randint(0, 5) % 4  # favor 0/1
        minerals = 50 * parameters.RAND.randint(0, 12)  # 0 - 600
        gas = 30 * parameters.RAND.randint(0, 12)  # 0 - 360
        unit_reqs = None
        enemy_has = None
        r = parameters.RAND.random()
        if r < .5:                  # check for finished units
            unit_reqs = Rule._get_unit_reqs(buildplan, units, parameters)
            # TODO: enemy rules don't work with OpprimoBot
#         if r >= .25 and r < .75:    # check enemy's units
#             enemy_has = Rule._get_enemy_has(parameters)

        # Generate macros:
        macros = []
        n_macros = 1 + parameters.RAND.randint(0, 5) % 5  # favor 1
        for _ in range(n_macros):
            # Determine the type of Macro to add (buildplan or squad):
            r = parameters.RAND.random()
            if r < .4:  # buildplan macro
                macros.append(Rule._get_buildplan_macro(buildplan, parameters))
            else:       # squad macro
                macros.append(Rule._get_squad_macro(buildplan, squads, parameters))
            # TODO: update buildplan?
        return Rule(macros, stage, no_bases, minerals, gas,
                    unit_reqs, enemy_has)


if __name__ == "__main__":
    parameters = Parameters()

    # Build BISections:
    BIS = BotInitSection.get_new_bot_init_section(parameters)
    BIS2 = BotInitSection.get_new_bot_init_section(parameters)

    # Build CASections:
    CAS = ComputeActionsSection.get_new_compute_actions_section(
            BIS.get_buildplan(),
            BIS.squad_init.squads, parameters)
    CAS2 = ComputeActionsSection.get_new_compute_actions_section(
            BIS2.get_buildplan(),
            BIS2.squad_init.squads, parameters)

    # Print 1:
    lines = BIS.get_bot_init_section_lines("TerranMain")
    for line in lines:
        print(line)
    print()
    ca_lines = CAS.get_compute_actions_section_lines("TerranMain")
    print()
    for line in ca_lines:
        print(line)
    print()

    # Print 2:
    lines = BIS2.get_bot_init_section_lines("TerranMain2")
    for line in lines:
        print(line)
    print()
    ca_lines = CAS2.get_compute_actions_section_lines("TerranMain2")
    print()
    for line in ca_lines:
        print(line)

    # Crossover (BIS):
    C1, C2 = ComputeActionsSection.crossover(CAS, CAS2, parameters)

    # Print children:
    clines = C1.get_compute_actions_section_lines("Child1")
    print()
    for line in clines:
        print(line)
    print()
    clines = C2.get_compute_actions_section_lines("Child2")
    print()
    for line in clines:
        print(line)
