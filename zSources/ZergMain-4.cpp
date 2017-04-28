#include "ZergMain-4.h"
#include "../../Managers/BuildplanEntry.h"
#include "../../Managers/AgentManager.h"
#include "../RushSquad.h"
#include "../ExplorationSquad.h"
#include "../../Managers/ExplorationManager.h"
ZergMain-4::ZergMain-4() 
{
	// NOTE: Enusre that you add up to 10 squads to the .h file.
	//  each squad should be named squadX, where X is a number 1-11
	// Buildingplan subsection:
	buildplan.push_back(BuildplanEntry(UnitTypes::Zerg_Spawning_Pool, 5));
	buildplan.push_back(BuildplanEntry(UnitTypes::Zerg_Extractor, 5));
	buildplan.push_back(BuildplanEntry(UnitTypes::Zerg_Hatchery, 8));
	buildplan.push_back(BuildplanEntry(UpgradeTypes::Metabolic_Boost, 12));
	buildplan.push_back(BuildplanEntry(UnitTypes::Zerg_Hydralisk_Den, 12));
	buildplan.push_back(BuildplanEntry(UnitTypes::Zerg_Lair, 14));
	buildplan.push_back(BuildplanEntry(UpgradeTypes::Antennae, 16));
	buildplan.push_back(BuildplanEntry(UpgradeTypes::Pneumatized_Carapace, 16));
	buildplan.push_back(BuildplanEntry(UpgradeTypes::Ventral_Sacs, 16));
	buildplan.push_back(BuildplanEntry(TechTypes::Burrowing, 20));
	buildplan.push_back(BuildplanEntry(TechTypes::Lurker_Aspect, 20));
	buildplan.push_back(BuildplanEntry(UpgradeTypes::Muscular_Augments, 20));
	buildplan.push_back(BuildplanEntry(UnitTypes::Zerg_Evolution_Chamber, 20));
	buildplan.push_back(BuildplanEntry(UpgradeTypes::Zerg_Melee_Attacks, 22));
	buildplan.push_back(BuildplanEntry(UpgradeTypes::Grooved_Spines, 24));

	// SquadInit subsection:
	mainSquad = new Squad(0, Squad::OFFENSIVE, "mainSquad", 10);
	mainSquad->addSetup(UnitTypes::Zerg_Zergling, 22);
	mainSquad->addSetup(UnitTypes::Zerg_Lurker, 2);
	mainSquad->setBuildup(true);
	mainSquad->setRequired(true);
	mainSquad->setMorphsTo(UnitTypes::Zerg_Lurker);
	squads.push_back(mainSquad);
	

	squad1 = new Squad(1, Squad::OFFENSIVE, "squad1", 13);
	squad1->addSetup(UnitTypes::Zerg_Hydralisk, 8);
	squad1->setBuildup(true);
	squad1->setRequired(true);
	squads.push_back(squad1);
	

	squad2 = new Squad(2, Squad::RUSH, "squad2", 15);
	squad2->addSetup(UnitTypes::Zerg_Zergling, 8);
	squad2->addSetup(UnitTypes::Zerg_Hydralisk, 4);
	squad2->addSetup(UnitTypes::Zerg_Lurker, 6);
	squad2->setBuildup(true);
	squad2->setRequired(false);
	squad2->setMorphsTo(UnitTypes::Zerg_Lurker);
	squads.push_back(squad2);
	

	squad3 = new Squad(3, Squad::RUSH, "squad3", 12);
	squad3->addSetup(UnitTypes::Zerg_Hydralisk, 12);
	squad3->addSetup(UnitTypes::Zerg_Lurker, 5);
	squad3->setBuildup(true);
	squad3->setRequired(false);
	squad3->setMorphsTo(UnitTypes::Zerg_Lurker);
	squads.push_back(squad3);
	

	squad4 = new Squad(4, Squad::SUPPORT, "squad4", 11);
	squad4->addSetup(UnitTypes::Zerg_Zergling, 16);
	squad4->addSetup(UnitTypes::Zerg_Lurker, 4);
	squad4->addSetup(UnitTypes::Zerg_Hydralisk, 20);
	squad4->setBuildup(false);
	squad4->setRequired(false);
	squad4->setMorphsTo(UnitTypes::Zerg_Lurker);
	squads.push_back(squad4);
	

	squad5 = new Squad(5, Squad::SUPPORT, "squad5", 16);
	squad5->addSetup(UnitTypes::Zerg_Lurker, 2);
	squad5->addSetup(UnitTypes::Zerg_Hydralisk, 16);
	squad5->addSetup(UnitTypes::Zerg_Zergling, 2);
	squad5->setBuildup(false);
	squad5->setRequired(true);
	squad5->setMorphsTo(UnitTypes::Zerg_Lurker);
	squads.push_back(squad5);
	

	squad6 = new Squad(6, Squad::EXPLORER, "squad6", 18);
	squad6->addSetup(UnitTypes::Zerg_Zergling, 10);
	squad6->setBuildup(false);
	squad6->setRequired(false);
	squads.push_back(squad6);
	

	noWorkers = 11;
	noWorkersPerRefinery = 3;
}
ZergMain-4::~ZergMain-4()
{
	for (Squad* s : squads)
	{
		delete s;
	}
	instance = NULL;
}
void ZergMain-4::computeActions()
{
	computeActionsBase();
	noWorkers = AgentManager::getInstance()->countNoBases() * 6 + AgentManager::getInstance()->countNoUnits(UnitTypes::Zerg_Extractor) * 3;
	int cSupply = Broodwar->self()->supplyUsed() / 2;
	int min = Broodwar->self()->minerals();
	int gas = Broodwar->self()->gas();

	//Rules Subsections:
	if (stage == 0 && AgentManager::getInstance()->countNoBases() > 0 && min >= 250 && gas >= 360)
	{
		mainSquad->setBuildup(false);
		stage++;
	}
	if (stage == 1 && AgentManager::getInstance()->countNoBases() > 0 && min >= 600 && gas >= 300 && AgentManager::getInstance()->countNoFinishedUnits(UnitTypes::Zerg_Hatchery) > 1 && AgentManager::getInstance()->countNoFinishedUnits(UnitTypes::Zerg_Evolution_Chamber) > 0 && AgentManager::getInstance()->countNoFinishedUnits(UnitTypes::Zerg_Zergling) > 15)
	{
		mainSquad->addSetup(UnitTypes::Zerg_Hydralisk, 4);
		mainSquad->removeSetup(UnitTypes::Zerg_Zergling, 6);
		stage++;
	}
	if (stage == 2 && AgentManager::getInstance()->countNoBases() > 0 && min >= 100 && gas >= 300)
	{
		squad1->setPriority(145);
		stage++;
	}
	if (stage == 3 && AgentManager::getInstance()->countNoBases() > -1 && min >= 300 && gas >= 90 && AgentManager::getInstance()->countNoFinishedUnits(UnitTypes::Zerg_Zergling) > 28)
	{
		buildplan.push_back(BuildplanEntry(UnitTypes::Zerg_Hatchery, cSupply));
		squad6->removeSetup(UnitTypes::Zerg_Zergling, 1);
		buildplan.push_back(BuildplanEntry(UnitTypes::Zerg_Hatchery, cSupply));
		stage++;
	}
}
