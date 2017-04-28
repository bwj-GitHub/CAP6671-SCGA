#include "ZergMain-7.h"
#include "../../Managers/BuildplanEntry.h"
#include "../../Managers/AgentManager.h"
#include "../RushSquad.h"
#include "../ExplorationSquad.h"
#include "../../Managers/ExplorationManager.h"
ZergMain-7::ZergMain-7() 
{
	// NOTE: Enusre that you add up to 10 squads to the .h file.
	//  each squad should be named squadX, where X is a number 1-11
	// Buildingplan subsection:
	buildplan.push_back(BuildplanEntry(UnitTypes::Zerg_Spawning_Pool, 5));
	buildplan.push_back(BuildplanEntry(UnitTypes::Zerg_Extractor, 5));
	buildplan.push_back(BuildplanEntry(UpgradeTypes::Metabolic_Boost, 6));
	buildplan.push_back(BuildplanEntry(UnitTypes::Zerg_Hatchery, 6));
	buildplan.push_back(BuildplanEntry(UnitTypes::Zerg_Lair, 6));
	buildplan.push_back(BuildplanEntry(UnitTypes::Zerg_Queens_Nest, 14));
	buildplan.push_back(BuildplanEntry(TechTypes::Burrowing, 16));
	buildplan.push_back(BuildplanEntry(UpgradeTypes::Gamete_Meiosis, 16));
	buildplan.push_back(BuildplanEntry(UpgradeTypes::Ventral_Sacs, 16));
	buildplan.push_back(BuildplanEntry(UnitTypes::Zerg_Evolution_Chamber, 16));
	buildplan.push_back(BuildplanEntry(UpgradeTypes::Zerg_Carapace, 18));
	buildplan.push_back(BuildplanEntry(UnitTypes::Zerg_Spire, 18));
	buildplan.push_back(BuildplanEntry(UpgradeTypes::Zerg_Flyer_Attacks, 20));
	buildplan.push_back(BuildplanEntry(UpgradeTypes::Zerg_Flyer_Carapace, 20));
	buildplan.push_back(BuildplanEntry(UnitTypes::Zerg_Hive, 20));
	buildplan.push_back(BuildplanEntry(UpgradeTypes::Zerg_Melee_Attacks, 20));
	buildplan.push_back(BuildplanEntry(UpgradeTypes::Adrenal_Glands, 22));
	buildplan.push_back(BuildplanEntry(TechTypes::Spawn_Broodlings, 24));
	buildplan.push_back(BuildplanEntry(UnitTypes::Zerg_Greater_Spire, 24));
	buildplan.push_back(BuildplanEntry(UnitTypes::Zerg_Hydralisk_Den, 28));
	buildplan.push_back(BuildplanEntry(UpgradeTypes::Grooved_Spines, 30));
	buildplan.push_back(BuildplanEntry(TechTypes::Lurker_Aspect, 30));
	buildplan.push_back(BuildplanEntry(UpgradeTypes::Muscular_Augments, 30));
	buildplan.push_back(BuildplanEntry(UpgradeTypes::Zerg_Missile_Attacks, 30));
	buildplan.push_back(BuildplanEntry(UpgradeTypes::Antennae, 32));
	buildplan.push_back(BuildplanEntry(TechTypes::Ensnare, 32));
	buildplan.push_back(BuildplanEntry(UnitTypes::Zerg_Defiler_Mound, 32));

	// SquadInit subsection:
	mainSquad = new Squad(0, Squad::OFFENSIVE, "mainSquad", 10);
	mainSquad->addSetup(UnitTypes::Zerg_Defiler, 7);
	mainSquad->addSetup(UnitTypes::Zerg_Mutalisk, 12);
	mainSquad->addSetup(UnitTypes::Zerg_Zergling, 10);
	mainSquad->setBuildup(true);
	mainSquad->setRequired(true);
	squads.push_back(mainSquad);
	

	squad1 = new Squad(1, Squad::OFFENSIVE, "squad1", 8);
	squad1->addSetup(UnitTypes::Zerg_Mutalisk, 14);
	squad1->addSetup(UnitTypes::Zerg_Defiler, 7);
	squad1->addSetup(UnitTypes::Zerg_Lurker, 4);
	squad1->addSetup(UnitTypes::Zerg_Guardian, 1);
	squad1->setBuildup(false);
	squad1->setRequired(true);
	squad1->setMorphsTo(UnitTypes::Zerg_Lurker);
	squads.push_back(squad1);
	

	squad2 = new Squad(2, Squad::DEFENSIVE, "squad2", 8);
	squad2->addSetup(UnitTypes::Zerg_Queen, 7);
	squad2->addSetup(UnitTypes::Zerg_Hydralisk, 24);
	squad2->addSetup(UnitTypes::Zerg_Defiler, 8);
	squad2->addSetup(UnitTypes::Zerg_Lurker, 8);
	squad2->setBuildup(false);
	squad2->setRequired(false);
	squad2->setMorphsTo(UnitTypes::Zerg_Lurker);
	squads.push_back(squad2);
	

	squad3 = new Squad(3, Squad::EXPLORER, "squad3", 15);
	squad3->addSetup(UnitTypes::Zerg_Hydralisk, 24);
	squad3->addSetup(UnitTypes::Zerg_Defiler, 8);
	squad3->setBuildup(true);
	squad3->setRequired(true);
	squads.push_back(squad3);
	

	noWorkers = 11;
	noWorkersPerRefinery = 3;
}
ZergMain-7::~ZergMain-7()
{
	for (Squad* s : squads)
	{
		delete s;
	}
	instance = NULL;
}
void ZergMain-7::computeActions()
{
	computeActionsBase();
	noWorkers = AgentManager::getInstance()->countNoBases() * 6 + AgentManager::getInstance()->countNoUnits(UnitTypes::Zerg_Extractor) * 3;
	int cSupply = Broodwar->self()->supplyUsed() / 2;
	int min = Broodwar->self()->minerals();
	int gas = Broodwar->self()->gas();

	//Rules Subsections:
	if (stage == 0 && AgentManager::getInstance()->countNoBases() > 2 && min >= 300 && gas >= 360 && AgentManager::getInstance()->countNoFinishedUnits(UnitTypes::Zerg_Spawning_Pool) > 0 && AgentManager::getInstance()->countNoFinishedUnits(UnitTypes::Zerg_Spire) > 0)
	{
		squad1->setBuildup(false);
		mainSquad->setPriority(138);
		squad3->addSetup(UnitTypes::Zerg_Queen, 3);
		squad2->setActivePriority(27);
		stage++;
	}
	if (stage == 1 && AgentManager::getInstance()->countNoBases() > 0 && min >= 300 && gas >= 240 && AgentManager::getInstance()->countNoFinishedUnits(UnitTypes::Zerg_Defiler) > 2 && AgentManager::getInstance()->countNoFinishedUnits(UnitTypes::Zerg_Mutalisk) > 15)
	{
		squad2->setActivePriority(1);
		squad3->setBuildup(true);
		stage++;
	}
	if (stage == 2 && AgentManager::getInstance()->countNoBases() > 0 && min >= 200 && gas >= 240 && AgentManager::getInstance()->countNoFinishedUnits(UnitTypes::Zerg_Greater_Spire) > 0)
	{
		squad3->setActivePriority(1);
		stage++;
	}
}
