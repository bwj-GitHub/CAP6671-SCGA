#include "ZergMain-0.h"
#include "../../Managers/BuildplanEntry.h"
#include "../../Managers/AgentManager.h"
#include "../RushSquad.h"
#include "../ExplorationSquad.h"
#include "../../Managers/ExplorationManager.h"
ZergMain-0::ZergMain-0() 
{
	// NOTE: Enusre that you add up to 10 squads to the .h file.
	//  each squad should be named squadX, where X is a number 1-11
	// Buildingplan subsection:
	buildplan.push_back(BuildplanEntry(UnitTypes::Zerg_Spawning_Pool, 5));
	buildplan.push_back(BuildplanEntry(UnitTypes::Zerg_Extractor, 5));
	buildplan.push_back(BuildplanEntry(UnitTypes::Zerg_Hatchery, 6));
	buildplan.push_back(BuildplanEntry(UpgradeTypes::Metabolic_Boost, 16));
	buildplan.push_back(BuildplanEntry(UnitTypes::Zerg_Lair, 18));
	buildplan.push_back(BuildplanEntry(UpgradeTypes::Antennae, 20));
	buildplan.push_back(BuildplanEntry(TechTypes::Burrowing, 20));
	buildplan.push_back(BuildplanEntry(UpgradeTypes::Pneumatized_Carapace, 20));
	buildplan.push_back(BuildplanEntry(UpgradeTypes::Ventral_Sacs, 20));
	buildplan.push_back(BuildplanEntry(UnitTypes::Zerg_Evolution_Chamber, 20));
	buildplan.push_back(BuildplanEntry(UpgradeTypes::Zerg_Melee_Attacks, 22));
	buildplan.push_back(BuildplanEntry(UnitTypes::Zerg_Hydralisk_Den, 24));
	buildplan.push_back(BuildplanEntry(UpgradeTypes::Grooved_Spines, 26));
	buildplan.push_back(BuildplanEntry(TechTypes::Lurker_Aspect, 26));
	buildplan.push_back(BuildplanEntry(UpgradeTypes::Muscular_Augments, 26));
	buildplan.push_back(BuildplanEntry(UpgradeTypes::Zerg_Missile_Attacks, 26));
	buildplan.push_back(BuildplanEntry(UpgradeTypes::Zerg_Carapace, 32));
	buildplan.push_back(BuildplanEntry(UnitTypes::Zerg_Spire, 32));

	// SquadInit subsection:
	mainSquad = new Squad(0, Squad::OFFENSIVE, "mainSquad", 10);
	mainSquad->addSetup(UnitTypes::Zerg_Scourge, 4);
	mainSquad->setBuildup(true);
	mainSquad->setRequired(true);
	squads.push_back(mainSquad);
	

	squad1 = new Squad(1, Squad::DEFENSIVE, "squad1", 18);
	squad1->addSetup(UnitTypes::Zerg_Mutalisk, 14);
	squad1->addSetup(UnitTypes::Zerg_Hydralisk, 16);
	squad1->setBuildup(false);
	squad1->setRequired(false);
	squads.push_back(squad1);
	

	squad2 = new Squad(2, Squad::OFFENSIVE, "squad2", 10);
	squad2->addSetup(UnitTypes::Zerg_Scourge, 12);
	squad2->addSetup(UnitTypes::Zerg_Zergling, 12);
	squad2->setBuildup(true);
	squad2->setRequired(true);
	squads.push_back(squad2);
	

	squad3 = new Squad(3, Squad::SUPPORT, "squad3", 15);
	squad3->addSetup(UnitTypes::Zerg_Scourge, 2);
	squad3->addSetup(UnitTypes::Zerg_Lurker, 5);
	squad3->setBuildup(false);
	squad3->setRequired(false);
	squad3->setMorphsTo(UnitTypes::Zerg_Lurker);
	squads.push_back(squad3);
	

	squad4 = new Squad(4, Squad::RUSH, "squad4", 20);
	squad4->addSetup(UnitTypes::Zerg_Lurker, 7);
	squad4->setBuildup(true);
	squad4->setRequired(false);
	squad4->setMorphsTo(UnitTypes::Zerg_Lurker);
	squads.push_back(squad4);
	

	noWorkers = 11;
	noWorkersPerRefinery = 3;
}
ZergMain-0::~ZergMain-0()
{
	for (Squad* s : squads)
	{
		delete s;
	}
	instance = NULL;
}
void ZergMain-0::computeActions()
{
	computeActionsBase();
	noWorkers = AgentManager::getInstance()->countNoBases() * 6 + AgentManager::getInstance()->countNoUnits(UnitTypes::Zerg_Extractor) * 3;
	int cSupply = Broodwar->self()->supplyUsed() / 2;
	int min = Broodwar->self()->minerals();
	int gas = Broodwar->self()->gas();

	//Rules Subsections:
	if (AgentManager::getInstance()->countNoBases() > 0 && min >= 150 && gas >= 150 && AgentManager::getInstance()->countNoFinishedUnits(UnitTypes::Zerg_Spawning_Pool) > 0 && AgentManager::getInstance()->countNoFinishedUnits(UnitTypes::Zerg_Mutalisk) > 12)
	{
		squad3->removeSetup(UnitTypes::Zerg_Lurker, 5);
	}
	if (stage == 0 && AgentManager::getInstance()->countNoBases() > 0 && min >= 600 && gas >= 0 && AgentManager::getInstance()->countNoFinishedUnits(UnitTypes::Zerg_Hydralisk) > 0 && AgentManager::getInstance()->countNoFinishedUnits(UnitTypes::Zerg_Hydralisk_Den) > 0 && AgentManager::getInstance()->countNoFinishedUnits(UnitTypes::Zerg_Zergling) > 24)
	{
		squad2->addSetup(UnitTypes::Zerg_Mutalisk, 8);
		squad2->setActivePriority(54);
		squad3->setPriority(19);
		squad3->removeSetup(UnitTypes::Zerg_Scourge, 2);
		buildplan.push_back(BuildplanEntry(UpgradeTypes::Zerg_Flyer_Carapace, cSupply));
		stage++;
	}
	if (AgentManager::getInstance()->countNoBases() > 1 && min >= 150 && gas >= 300)
	{
		buildplan.push_back(BuildplanEntry(UnitTypes::Zerg_Queens_Nest, cSupply));
		mainSquad->removeSetup(UnitTypes::Zerg_Scourge, 2);
		buildplan.push_back(BuildplanEntry(UnitTypes::Zerg_Creep_Colony, cSupply));
	}
	if (AgentManager::getInstance()->countNoBases() > 0 && min >= 100 && gas >= 330)
	{
		squad3->addSetup(UnitTypes::Zerg_Mutalisk, 16);
		buildplan.push_back(BuildplanEntry(UnitTypes::Zerg_Creep_Colony, cSupply));
		squad4->addSetup(UnitTypes::Zerg_Hydralisk, 2);
		mainSquad->removeSetup(UnitTypes::Zerg_Scourge, 2);
	}
}
