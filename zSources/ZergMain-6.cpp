#include "ZergMain-6.h"
#include "../../Managers/BuildplanEntry.h"
#include "../../Managers/AgentManager.h"
#include "../RushSquad.h"
#include "../ExplorationSquad.h"
#include "../../Managers/ExplorationManager.h"
ZergMain-6::ZergMain-6() 
{
	// NOTE: Enusre that you add up to 10 squads to the .h file.
	//  each squad should be named squadX, where X is a number 1-11
	// Buildingplan subsection:
	buildplan.push_back(BuildplanEntry(UnitTypes::Zerg_Spawning_Pool, 5));
	buildplan.push_back(BuildplanEntry(UnitTypes::Zerg_Extractor, 5));
	buildplan.push_back(BuildplanEntry(UnitTypes::Zerg_Hatchery, 10));
	buildplan.push_back(BuildplanEntry(UpgradeTypes::Metabolic_Boost, 12));
	buildplan.push_back(BuildplanEntry(UnitTypes::Zerg_Lair, 16));
	buildplan.push_back(BuildplanEntry(UpgradeTypes::Antennae, 18));
	buildplan.push_back(BuildplanEntry(TechTypes::Burrowing, 18));
	buildplan.push_back(BuildplanEntry(UpgradeTypes::Ventral_Sacs, 18));
	buildplan.push_back(BuildplanEntry(UnitTypes::Zerg_Hydralisk_Den, 18));
	buildplan.push_back(BuildplanEntry(UpgradeTypes::Grooved_Spines, 24));
	buildplan.push_back(BuildplanEntry(TechTypes::Lurker_Aspect, 24));
	buildplan.push_back(BuildplanEntry(UnitTypes::Zerg_Evolution_Chamber, 28));
	buildplan.push_back(BuildplanEntry(UnitTypes::Zerg_Spire, 28));
	buildplan.push_back(BuildplanEntry(UpgradeTypes::Zerg_Carapace, 30));
	buildplan.push_back(BuildplanEntry(UpgradeTypes::Zerg_Flyer_Attacks, 30));
	buildplan.push_back(BuildplanEntry(UpgradeTypes::Zerg_Melee_Attacks, 30));
	buildplan.push_back(BuildplanEntry(UpgradeTypes::Zerg_Missile_Attacks, 30));
	buildplan.push_back(BuildplanEntry(UpgradeTypes::Muscular_Augments, 32));
	buildplan.push_back(BuildplanEntry(UpgradeTypes::Pneumatized_Carapace, 32));

	// SquadInit subsection:
	mainSquad = new Squad(0, Squad::OFFENSIVE, "mainSquad", 10);
	mainSquad->addSetup(UnitTypes::Zerg_Hydralisk, 20);
	mainSquad->addSetup(UnitTypes::Zerg_Scourge, 8);
	mainSquad->addSetup(UnitTypes::Zerg_Lurker, 8);
	mainSquad->setBuildup(true);
	mainSquad->setRequired(true);
	mainSquad->setMorphsTo(UnitTypes::Zerg_Lurker);
	squads.push_back(mainSquad);
	

	squad1 = new Squad(1, Squad::RUSH, "squad1", 19);
	squad1->addSetup(UnitTypes::Zerg_Zergling, 18);
	squad1->addSetup(UnitTypes::Zerg_Scourge, 4);
	squad1->addSetup(UnitTypes::Zerg_Mutalisk, 6);
	squad1->setBuildup(false);
	squad1->setRequired(true);
	squads.push_back(squad1);
	

	noWorkers = 11;
	noWorkersPerRefinery = 3;
}
ZergMain-6::~ZergMain-6()
{
	for (Squad* s : squads)
	{
		delete s;
	}
	instance = NULL;
}
void ZergMain-6::computeActions()
{
	computeActionsBase();
	noWorkers = AgentManager::getInstance()->countNoBases() * 6 + AgentManager::getInstance()->countNoUnits(UnitTypes::Zerg_Extractor) * 3;
	int cSupply = Broodwar->self()->supplyUsed() / 2;
	int min = Broodwar->self()->minerals();
	int gas = Broodwar->self()->gas();

	//Rules Subsections:
	if (AgentManager::getInstance()->countNoBases() > 0 && min >= 100 && gas >= 0)
	{
		buildplan.push_back(BuildplanEntry(UnitTypes::Zerg_Creep_Colony, cSupply));
		buildplan.push_back(BuildplanEntry(UnitTypes::Zerg_Extractor, cSupply));
	}
	if (AgentManager::getInstance()->countNoBases() > 0 && min >= 50 && gas >= 0 && AgentManager::getInstance()->countNoFinishedUnits(UnitTypes::Zerg_Spire) > 0)
	{
		squad1->removeSetup(UnitTypes::Zerg_Mutalisk, 5);
	}
	if (AgentManager::getInstance()->countNoBases() > 0 && min >= 450 && gas >= 0)
	{
		mainSquad->setPriority(34);
	}
	if (AgentManager::getInstance()->countNoBases() > 2 && min >= 150 && gas >= 0)
	{
		mainSquad->setActivePriority(1000);
		squad1->setPriority(9);
		mainSquad->setPriority(82);
	}
	if (stage == 0 && AgentManager::getInstance()->countNoBases() > -1 && min >= 50 && gas >= 60 && AgentManager::getInstance()->countNoFinishedUnits(UnitTypes::Zerg_Lurker) > 10)
	{
		squad1->setBuildup(false);
		buildplan.push_back(BuildplanEntry(UnitTypes::Zerg_Hatchery, cSupply));
		squad1->addSetup(UnitTypes::Zerg_Zergling, 8);
		squad1->addSetup(UnitTypes::Zerg_Scourge, 20);
		mainSquad->setActivePriority(1000);
		stage++;
	}
	if (AgentManager::getInstance()->countNoBases() > 1 && min >= 600 && gas >= 30)
	{
		mainSquad->addSetup(UnitTypes::Zerg_Zergling, 8);
		squad1->setPriority(110);
		buildplan.push_back(BuildplanEntry(UnitTypes::Zerg_Extractor, cSupply));
		mainSquad->setBuildup(true);
		buildplan.push_back(BuildplanEntry(UnitTypes::Zerg_Sunken_Colony, cSupply));
	}
}
