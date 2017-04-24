"""
Created on Apr 22, 2017

@author: brandon
"""


class ZergUnits:
    BUILD_TREE = {
            "Zerg_Hatchery": {
                    "Zerg_Spawning_Pool": {
                            "Zerg_Lair": {
                                    "Zerg_Queens_Nest": {
                                            "Zerg_Hive": {
                                                    "Zerg_Nydus_Canal": None,
                                                    "Zerg_Defiler_Mound": None,
                                                    "Zerg_Greater_Spire": None,
                                                    "Zerg_Ultralisk_Cavern": None
                                                }
                                            },
                                    "Zerg_Spire": None
                                    },
                            "Zerg_Hydralisk_Den": None,
                            "Zerg_Sunken_Colony": None
                            },
                               
                    "Zerg_Evolution_Chamber": {"Zerg_Spore_Colony": None}
                    },
            "Zerg_Extractor": None,
            "Zerg_Creep_Colony": None
            }

    BUILDING_REQS = {
            "Zerg_Hatchery": None,
            "Zerg_Extractor": None,
            "Zerg_Creep_Colony": None,
            "Zerg_Spawning_Pool": ["Zerg_Hatchery"],
            "Zerg_Evolution_Chamber": ["Zerg_Hatchery"],
            "Zerg_Lair": ["Zerg_Spawning_Pool"],
            "Zerg_Hydralisk_Den": ["Zerg_Spawning_Pool"],
            "Zerg_Sunken_Colony": ["Zerg_Spawning_Pool"],
            "Zerg_Queens_Nest": ["Zerg_Lair"],
            "Zerg_Spire": ["Zerg_Lair"],
            "Zerg_Hive": ["Zerg_Queens_Nest"],
            "Zerg_Nydus_Canal": ["Zerg_Hive"],
            "Zerg_Defiler_Mound": ["Zerg_Hive"],
            "Zerg_Greater_Spire": ["Zerg_Hive"],
            "Zerg_Ultralisk_Cavern": ["Zerg_Hive"]
            }

    UPGRADE_REQS = {
            "Zerg_Carapace": ["Zerg_Evolution_Chamber"],
            "Zerg_Melee_Attacks": ["Zerg_Evolution_Chamber"],
            # NOTE: Zerg_Missle_Attacks does not TECHNICALLY require the
            #  Hydralisk Den, there is just little point in building it
            #  otherwise (except for Lurkers)
            "Zerg_Missile_Attacks": ["Zerg_Evolution_Chamber", "Zerg_Hydralisk_Den"],
            "Zerg_Flyer_Carapace": ["Zerg_Spire"],
            "Zerg_Flyer_Attacks": ["Zerg_Spire"],
            "Adrenal_Glands": ["Zerg_Spawning_Pool", "Zerg_Hive"],
            "Metabolic_Boost": ["Zerg_Spawning_Pool"],
            "Ventral_Sacs": ["Zerg_Lair"],
            "Antennae": ["Zerg_Lair"],
            "Pneumatized_Carapace": ["Zerg_Lair"],
            "Muscular_Augments": ["Zerg_Hydralisk_Den"],
            "Grooved_Spines": ["Zerg_Hydralisk_Den"],
            "Gamete_Meiosis": ["Zerg_Queens_Nest"],
            "Anabolic_Synthesis": ["Zerg_Ultralisk_Cavern"],
            "Chitinous_Plating": ["Zerg_Ultralisk_Cavern"],
            "Metasynaptic_Node": ["Zerg_Defiler_Mound"]
            }


    TECH_REQS = {
            "Burrowing": ["Zerg_Hatchery"],
            "Lurker_Aspect": ["Zerg_Lair", "Zerg_Hydralisk_Den"],
            "Ensnare": ["Zerg_Queens_Nest"],
            "Spawn_Broodlings": ["Zerg_Queens_Nest"],
            "Consume": ["Zerg_Defiler_Mound"],
            "Plague": ["Zerg_Defiler_Mound"]
            }

    # NOTE: Some units might require an Upgrade instead of a building
    UNIT_REQS = {
            "Zerg_Zergling": ["Zerg_Spawning_Pool"],
            "Zerg_Hydralisk": ["Zerg_Hydralisk_Den"],
            "Zerg_Mutalisk": ["Zerg_Spire"],
            "Zerg_Scourge": ["Zerg_Spire"],
            "Zerg_Lurker": ["Lurker_Aspect"],  # Requires Upgrade!
#             "Zerg_Overlord": ["Zerg_Hatchery"],  # Opprimo bot takes care of these automatically
            "Zerg_Guardian": ["Zerg_Greater_Spire"],
            "Zerg_Queen": ["Zerg_Queens_Nest"],
            "Zerg_Defiler": ["Zerg_Defiler_Mound"],
            "Zerg_Ultralisk": ["Zerg_Ultralisk_Cavern"]
            }

    @staticmethod
    def get_available_units(buildplan):
        """Return a list of units that can potentially be trained given
            buildplan.
        """

        units = []
        for u in ZergUnits.UNIT_REQS.keys():
            unit_reqs = ZergUnits.UNIT_REQS[u]
            to_add = True
            for req in unit_reqs:
                if req not in buildplan:
                    to_add = False
            if to_add is True:
                units.append(u)
        return units
            

