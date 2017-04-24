"""
Created on Apr 23, 2017

@author: brandon
"""


from ga.parameters import Parameters


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

    def correct_rule(self, buildplan, parameters):
        """Remove conditions/macros from the Rule that couldn't possibly
            be evaluated/executed based on buildplan.
        """

        pass

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
                        req[0], req[1])
        # check enemy units?
        if self.enemy_has is not None:
            for req in self.enemy_has:
                enemy_str += " && enemyUnits.countUnitsOfType({}) > {}".format(
                        req[0], req[1])

        # All other conditions can be 0 if they are not desired
        condition_line = [
                "if ({}min >= {} && gas >= {}{}{})".format(
                        stage_str, self.minerals, self.gas, units_str, enemy_str),
                        "{"]
        macro_lines = ["\t<do some stuff>"]
#         macro_lines =  [self.macros[i].get_macro_str() 
#                         for i in range(len(self.macros))]
        return condition_line + macro_lines + ["}"]

    def clone(self):
        pass

    @staticmethod
    def crossover(R1, R2, parameters):
        pass

    @staticmethod
    def _get_unit_reqs(buildplan, units, parameters):
        """Return a list of buildings/units to check for.

        Don't check for a building if it is NOT in buildingplan;
        note that the buildplan SHOULD include items that were
        added by previous Rules.
        """

        unit_reqs = []
        n_units = 1+ parameters.RAND.randint(0, 3) % 3  # favor 1
        u_track = []  # track units already added
        # Create n_units unit reqs:
        for _ in range(n_units):
            # Check for some building or unti:
            r = parameters.RAND.random()
            if r < .5:  # Check for some building:
                u_type = buildplan[parameters.RAND.randint(0, len(buildplan)-1)]
                if u_type == "Zerg_Hatchery":
                    u_count = parameters.RAND.randint(0, 2)
                else:
                    u_count = 0  # Not much reason to have multiple of other buildings
            else:
                u_type = units[parameters.RAND.randint(0, len(units)-1)]
                u_count = parameters.RAND.randint(0, 24) % 20  # favor lower counts
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
    def _get_enemy_has(parameters):
        """Return a list of enemy units to check for.

        :return: list; a list of tuples containing a str representing
            an enemy unit type and an int, representing the min count
            to trigger the rule.
        """

        # Check for 1-3 enemy units (0 will occur if this not called)
        enemy_units = []
        e_track = []  # don't check for same enemy_t twice!
        n_units = parameters.RAND.randint(1, 3)
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
    def get_new_rule(n, buildplan, units, parameters):
        """Return a new Rule Subsection.

        :param n: int; indicates which stage this Rule MIGHT be. stage
            could also be set to Noen for this Rule.

        :param buildplan: list; list of buildings that MIGHT be built by
            this strategy.

        :param units: list; list of units that MIGHT be built by this
            strategy. A unit MIGHT be built if it is added to AT LEAST
            one squad, either in the bot_init section or in a PREVIOUS
            Rule.
        """

        # n indicates potential stage (won't necessarily be used)
        # NOTE: buildplan includes items that MIGHT be built during computeActions

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
        if r < .5:
            unit_reqs = Rule._get_unit_reqs(buildplan, units, parameters)
        if r >= .25 and r < .75:
            enemy_has = Rule._get_enemy_has(parameters)

        macros = []  # TODO: generate!

        return Rule(macros, stage, no_bases, minerals, gas,
                    unit_reqs, enemy_has)


def get_compute_actions_section_lines(class_name="ZergMain", rules=[]):
    """Return a list of lines representing the computeActions method
         of a Strategy class in OpprimoBot.
    """

    # Add constant init lines:
    lines = [
             "void {}::computeActions()".format(class_name),
             "{",
             "\tcomputeActionsBase();",
             "\tnoWorkers = AgentManager::getInstance()->countNoBases() * 6 " \
                    "+ AgentManager::getInstance()->countNoUnits(" \
                    "UnitTypes::Zerg_Extractor) * 3;",
             "\tint cSupply = Broodwar->self()->supplyUsed() / 2;",
             "\tint min = Broodwar->self()->minerals();",
             "\tint gas = Broodwar->self()->gas();",
             
             "\t// Additional code to observe the enemy, based on code from",
             "\t//  OpeningTest fork of OpprimoBot by andertavares:",
             "\tSpottedObjectSet& enemyUnits = explorationManager" \
                "->getSpottedUnits();",
            "\n\t//Rules Subsections:"
             ]

    # Add lines for each Rule:
    for rule in rules:
        lines.extend(["\t"+line for line in rule.get_lines()])

    # Complete Section and return lines:
    lines.append("}")
    return lines


if __name__ == "__main__":
    R = Rule.get_new_rule(0, buildplan=["UnitTypes::Zerg_Spawning_Pool",
                                        "UnitTypes::Zerg_Hydralisk_Den",
                                        "UnitTypes::Zerg_Lair",
                                        "UnitTypes::Zerg_Spire"],
                          units=["Zerg_Zergling", "Zerg_Hydralisk",
                                 "Zerg_Mutalisk"],
                          parameters=Parameters())
    r_lines = R.get_lines()
    for line in r_lines:
        print(line)
