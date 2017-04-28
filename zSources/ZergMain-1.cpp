#include "ZergMain-1.h"
#include "../../Managers/BuildplanEntry.h"
#include "../../Managers/AgentManager.h"
#include "../RushSquad.h"
#include "../ExplorationSquad.h"
#include "../../Managers/ExplorationManager.h"
ZergMain-1::ZergMain-1() 
{
	// NOTE: Enusre that you add up to 10 squads to the .h file.
	//  each squad should be named squadX, where X is a number 1-11
	// Buildingplan subsection:
	buildplan.push_back(BuildplanEntry(UnitTypes::Zerg_Spawning_Pool, 5));
	buildplan.push_back(BuildplanEntry(UnitTypes::Zerg_Extractor, 5));
	buildplan.push_back(BuildplanEntry(UnitTypes::Zerg_Lair, 6));
	buildplan.push_back(BuildplanEntry(UnitTypes::Zerg_Spire, 8));
	buildplan.push_back(BuildplanEntry(UpgradeTypes::Zerg_Flyer_Attacks, 10));
	buildplan.push_back(BuildplanEntry(TechTypes::Burrowing, 12));
	buildplan.push_back(BuildplanEntry(UpgradeTypes::Metabolic_Boost, 14));
	buildplan.push_back(BuildplanEntry(UnitTypes::Zerg_Evolution_Chamber, 14));
	buildplan.push_back(BuildplanEntry(UpgradeTypes::Antennae, 16));
	buildplan.push_back(BuildplanEntry(UpgradeTypes::Pneumatized_Carapace, 16));
	buildplan.push_back(BuildplanEntry(UpgradeTypes::Zerg_Carapace, 16));
	buildplan.push_back(BuildplanEntry(UnitTypes::Zerg_Hydralisk_Den, 16));
	buildplan.push_back(BuildplanEntry(UpgradeTypes::Zerg_Melee_Attacks, 16));
	buildplan.push_back(BuildplanEntry(TechTypes::Lurker_Aspect, 18));
	buildplan.push_back(BuildplanEntry(UpgradeTypes::Muscular_Augments, 18));
	buildplan.push_back(BuildplanEntry(UpgradeTypes::Zerg_Missile_Attacks, 20));
	buildplan.push_back(BuildplanEntry(UnitTypes::Zerg_Queens_Nest, 24));
	buildplan.push_back(BuildplanEntry(TechTypes::Ensnare, 26));
	buildplan.push_back(BuildplanEntry(UpgradeTypes::Gamete_Meiosis, 26));
	buildplan.push_back(BuildplanEntry(TechTypes::Spawn_Broodlings, 26));
	buildplan.push_back(BuildplanEntry(UnitTypes::Zerg_Hive, 26));
	buildplan.push_back(BuildplanEntry(UpgradeTypes::Grooved_Spines, 28));
	buildplan.push_back(BuildplanEntry(UnitTypes::Zerg_Defiler_Mound, 28));
	buildplan.push_back(BuildplanEntry(UnitTypes::Zerg_Greater_Spire, 28));
	buildplan.push_back(BuildplanEntry(UnitTypes::Zerg_Ultralisk_Cavern, 28));
	buildplan.push_back(BuildplanEntry(UpgradeTypes::Anabolic_Synthesis, 30));
	buildplan.push_back(BuildplanEntry(UpgradeTypes::Chitinous_Plating, 30));
	buildplan.push_back(BuildplanEntry(TechTypes::Consume, 30));
	buildplan.push_back(BuildplanEntry(UpgradeTypes::Metasynaptic_Node, 30));
	buildplan.push_back(BuildplanEntry(TechTypes::Plague, 32));
	buildplan.push_back(BuildplanEntry(UpgradeTypes::Ventral_Sacs, 32));

	// SquadInit subsection:
	mainSquad = new Squad(0, Squad::OFFENSIVE, "mainSquad", 10);
	mainSquad->addSetup(UnitTypes::Zerg_Defiler, 1);
	mainSquad->addSetup(UnitTypes::Zerg_Guardian, 4);
	mainSquad->addSetup(UnitTypes::Zerg_Ultralisk, 6);
	mainSquad->addSetup(UnitTypes::Zerg_Hydralisk, 6);
	mainSquad->addSetup(UnitTypes::Zerg_Queen, 5);
	mainSquad->setBuildup(true);
	mainSquad->setRequired(true);
	squads.push_back(mainSquad);
	

	squad1 = new Squad(1, Squad::KITE, "squad1", 16);
	squad1->addSetup(UnitTypes::Zerg_Scourge, 18);
	squad1->addSetup(UnitTypes::Zerg_Zergling, 4);
	squad1->addSetup(UnitTypes::Zerg_Ultralisk, 1);
	squad1->addSetup(UnitTypes::Zerg_Hydralisk, 10);
	squad1->setBuildup(false);
	squad1->setRequired(false);
	squads.push_back(squad1);
	

	squad2 = new Squad(2, Squad::EXPLORER, "squad2", 15);
	squad2->addSetup(UnitTypes::Zerg_Guardian, 6);
	squad2->addSetup(UnitTypes::Zerg_Lurker, 1);
	squad2->addSetup(UnitTypes::Zerg_Ultralisk, 2);
	squad2->addSetup(UnitTypes::Zerg_Scourge, 6);
	squad2->setBuildup(true);
	squad2->setRequired(true);
	squad2->setMorphsTo(UnitTypes::Zerg_Lurker);
	squads.push_back(squad2);
	

	squad3 = new Squad(3, Squad::DEFENSIVE, "squad3", 20);
	squad3->addSetup(UnitTypes::Zerg_Queen, 1);
	squad3->addSetup(UnitTypes::Zerg_Ultralisk, 1);
	squad3->addSetup(UnitTypes::Zerg_Hydralisk, 18);
	squad3->setBuildup(true);
	squad3->setRequired(false);
	squads.push_back(squad3);
	

	squad4 = new Squad(4, Squad::EXPLORER, "squad4", 13);
	squad4->addSetup(UnitTypes::Zerg_Zergling, 20);
	squad4->addSetup(UnitTypes::Zerg_Scourge, 14);
	squad4->setBuildup(false);
	squad4->setRequired(false);
	squads.push_back(squad4);
	

	squad5 = new Squad(5, Squad::OFFENSIVE, "squad5", 9);
	squad5->addSetup(UnitTypes::Zerg_Hydralisk, 14);
	squad5->addSetup(UnitTypes::Zerg_Lurker, 7);
	squad5->addSetup(UnitTypes::Zerg_Queen, 7);
	squad5->setBuildup(false);
	squad5->setRequired(true);
	squad5->setMorphsTo(UnitTypes::Zerg_Lurker);
	squads.push_back(squad5);
	

	squad6 = new Squad(6, Squad::SUPPORT, "squad6", 17);
	squad6->addSetup(UnitTypes::Zerg_Queen, 7);
	squad6->addSetup(UnitTypes::Zerg_Zergling, 24);
	squad6->addSetup(UnitTypes::Zerg_Scourge, 8);
	squad6->addSetup(UnitTypes::Zerg_Mutalisk, 14);
	squad6->setBuildup(true);
	squad6->setRequired(false);
	squads.push_back(squad6);
	

	squad7 = new Squad(7, Squad::RUSH, "squad7", 10);
	squad7->addSetup(UnitTypes::Zerg_Scourge, 16);
	squad7->addSetup(UnitTypes::Zerg_Queen, 2);
	squad7->addSetup(UnitTypes::Zerg_Lurker, 5);
	squad7->addSetup(UnitTypes::Zerg_Defiler, 4);
	squad7->addSetup(UnitTypes::Zerg_Ultralisk, 2);
	squad7->setBuildup(true);
	squad7->setRequired(true);
	squad7->setMorphsTo(UnitTypes::Zerg_Lurker);
	squads.push_back(squad7);
	

	squad8 = new Squad(8, Squad::KITE, "squad8", 10);
	squad8->addSetup(UnitTypes::Zerg_Hydralisk, 6);
	squad8->addSetup(UnitTypes::Zerg_Lurker, 1);
	squad8->addSetup(UnitTypes::Zerg_Zergling, 18);
	squad8->addSetup(UnitTypes::Zerg_Defiler, 1);
	squad8->setBuildup(false);
	squad8->setRequired(false);
	squad8->setMorphsTo(UnitTypes::Zerg_Lurker);
	squads.push_back(squad8);
	

	noWorkers = 11;
	noWorkersPerRefinery = 3;
}
ZergMain-1::~ZergMain-1()
{
	for (Squad* s : squads)
	{
		delete s;
	}
	instance = NULL;
}
void ZergMain-1::computeActions()
{
	computeActionsBase();
	noWorkers = AgentManager::getInstance()->countNoBases() * 6 + AgentManager::getInstance()->countNoUnits(UnitTypes::Zerg_Extractor) * 3;
	int cSupply = Broodwar->self()->supplyUsed() / 2;
	int min = Broodwar->self()->minerals();
	int gas = Broodwar->self()->gas();

	//Rules Subsections:
	if (AgentManager::getInstance()->countNoBases() > 0 && min >= 200 && gas >= 240 && AgentManager::getInstance()->countNoFinishedUnits(UnitTypes::Zerg_Spire) > 0)
	{
		buildplan.push_back(BuildplanEntry(UpgradeTypes::Zerg_Flyer_Carapace, cSupply));
	}
	if (stage == 0 && AgentManager::getInstance()->countNoBases() > 0 && min >= 300 && gas >= 90 && AgentManager::getInstance()->countNoFinishedUnits(UnitTypes::Zerg_Hydralisk) > 11 && AgentManager::getInstance()->countNoFinishedUnits(UnitTypes::Zerg_Mutalisk) > 14 && AgentManager::getInstance()->countNoFinishedUnits(UnitTypes::Zerg_Evolution_Chamber) > 0)
	{
		mainSquad->setBuildup(false);
		buildplan.push_back(BuildplanEntry(UnitTypes::Zerg_Nydus_Canal, cSupply));
		stage++;
	}
	if (stage == 1 && AgentManager::getInstance()->countNoBases() > -1 && min >= 450 && gas >= 0)
	{
		buildplan.push_back(BuildplanEntry(UnitTypes::Zerg_Sunken_Colony, cSupply));
		buildplan.push_back(BuildplanEntry(UpgradeTypes::Adrenal_Glands, cSupply));
		buildplan.push_back(BuildplanEntry(UpgradeTypes::Adrenal_Glands, cSupply));
		squad2->addSetup(UnitTypes::Zerg_Defiler, 6);
		stage++;
	}
}
