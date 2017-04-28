#include "ZergMain-5.h"
#include "../../Managers/BuildplanEntry.h"
#include "../../Managers/AgentManager.h"
#include "../RushSquad.h"
#include "../ExplorationSquad.h"
#include "../../Managers/ExplorationManager.h"
ZergMain-5::ZergMain-5() 
{
	// NOTE: Enusre that you add up to 10 squads to the .h file.
	//  each squad should be named squadX, where X is a number 1-11
	// Buildingplan subsection:
	buildplan.push_back(BuildplanEntry(UnitTypes::Zerg_Spawning_Pool, 5));
	buildplan.push_back(BuildplanEntry(UnitTypes::Zerg_Extractor, 5));
	buildplan.push_back(BuildplanEntry(UnitTypes::Zerg_Lair, 6));
	buildplan.push_back(BuildplanEntry(TechTypes::Burrowing, 8));
	buildplan.push_back(BuildplanEntry(UnitTypes::Zerg_Hydralisk_Den, 8));
	buildplan.push_back(BuildplanEntry(UpgradeTypes::Ventral_Sacs, 10));
	buildplan.push_back(BuildplanEntry(UnitTypes::Zerg_Hatchery, 10));
	buildplan.push_back(BuildplanEntry(UnitTypes::Zerg_Evolution_Chamber, 12));
	buildplan.push_back(BuildplanEntry(UpgradeTypes::Pneumatized_Carapace, 14));
	buildplan.push_back(BuildplanEntry(UpgradeTypes::Zerg_Carapace, 14));
	buildplan.push_back(BuildplanEntry(UpgradeTypes::Muscular_Augments, 18));
	buildplan.push_back(BuildplanEntry(UpgradeTypes::Grooved_Spines, 20));
	buildplan.push_back(BuildplanEntry(UpgradeTypes::Antennae, 32));

	// SquadInit subsection:
	mainSquad = new Squad(0, Squad::OFFENSIVE, "mainSquad", 10);
	mainSquad->addSetup(UnitTypes::Zerg_Zergling, 12);
	mainSquad->addSetup(UnitTypes::Zerg_Hydralisk, 14);
	mainSquad->setBuildup(true);
	mainSquad->setRequired(true);
	squads.push_back(mainSquad);
	

	squad1 = new Squad(1, Squad::OFFENSIVE, "squad1", 18);
	squad1->addSetup(UnitTypes::Zerg_Zergling, 22);
	squad1->addSetup(UnitTypes::Zerg_Hydralisk, 24);
	squad1->setBuildup(true);
	squad1->setRequired(true);
	squads.push_back(squad1);
	

	squad2 = new Squad(2, Squad::KITE, "squad2", 12);
	squad2->addSetup(UnitTypes::Zerg_Zergling, 8);
	squad2->addSetup(UnitTypes::Zerg_Hydralisk, 6);
	squad2->setBuildup(false);
	squad2->setRequired(true);
	squads.push_back(squad2);
	

	squad3 = new Squad(3, Squad::OFFENSIVE, "squad3", 16);
	squad3->addSetup(UnitTypes::Zerg_Hydralisk, 10);
	squad3->addSetup(UnitTypes::Zerg_Zergling, 20);
	squad3->setBuildup(true);
	squad3->setRequired(false);
	squads.push_back(squad3);
	

	squad4 = new Squad(4, Squad::KITE, "squad4", 15);
	squad4->addSetup(UnitTypes::Zerg_Hydralisk, 2);
	squad4->addSetup(UnitTypes::Zerg_Zergling, 20);
	squad4->setBuildup(false);
	squad4->setRequired(true);
	squads.push_back(squad4);
	

	squad5 = new Squad(5, Squad::EXPLORER, "squad5", 8);
	squad5->addSetup(UnitTypes::Zerg_Zergling, 20);
	squad5->addSetup(UnitTypes::Zerg_Hydralisk, 2);
	squad5->setBuildup(true);
	squad5->setRequired(false);
	squads.push_back(squad5);
	

	squad6 = new Squad(6, Squad::EXPLORER, "squad6", 9);
	squad6->addSetup(UnitTypes::Zerg_Hydralisk, 20);
	squad6->addSetup(UnitTypes::Zerg_Zergling, 12);
	squad6->setBuildup(false);
	squad6->setRequired(false);
	squads.push_back(squad6);
	

	squad7 = new Squad(7, Squad::OFFENSIVE, "squad7", 20);
	squad7->addSetup(UnitTypes::Zerg_Zergling, 22);
	squad7->setBuildup(false);
	squad7->setRequired(true);
	squads.push_back(squad7);
	

	squad8 = new Squad(8, Squad::RUSH, "squad8", 19);
	squad8->addSetup(UnitTypes::Zerg_Hydralisk, 6);
	squad8->addSetup(UnitTypes::Zerg_Zergling, 14);
	squad8->setBuildup(true);
	squad8->setRequired(true);
	squads.push_back(squad8);
	

	noWorkers = 11;
	noWorkersPerRefinery = 3;
}
ZergMain-5::~ZergMain-5()
{
	for (Squad* s : squads)
	{
		delete s;
	}
	instance = NULL;
}
void ZergMain-5::computeActions()
{
	computeActionsBase();
	noWorkers = AgentManager::getInstance()->countNoBases() * 6 + AgentManager::getInstance()->countNoUnits(UnitTypes::Zerg_Extractor) * 3;
	int cSupply = Broodwar->self()->supplyUsed() / 2;
	int min = Broodwar->self()->minerals();
	int gas = Broodwar->self()->gas();

	//Rules Subsections:
	if (AgentManager::getInstance()->countNoBases() > -1 && min >= 50 && gas >= 300 && AgentManager::getInstance()->countNoFinishedUnits(UnitTypes::Zerg_Zergling) > 20)
	{
		squad3->removeSetup(UnitTypes::Zerg_Zergling, 2);
		buildplan.push_back(BuildplanEntry(UnitTypes::Zerg_Creep_Colony, cSupply));
		squad5->addSetup(UnitTypes::Zerg_Hydralisk, 6);
		buildplan.push_back(BuildplanEntry(TechTypes::Lurker_Aspect, cSupply));
		squad6->addSetup(UnitTypes::Zerg_Zergling, 18);
	}
	if (stage == 0 && AgentManager::getInstance()->countNoBases() > 1 && min >= 350 && gas >= 240)
	{
		buildplan.push_back(BuildplanEntry(UpgradeTypes::Zerg_Missile_Attacks, cSupply));
		squad3->setActivePriority(1);
		squad7->removeSetup(UnitTypes::Zerg_Zergling, 8);
		stage++;
	}
}
