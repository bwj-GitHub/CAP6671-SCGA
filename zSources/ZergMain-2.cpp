#include "ZergMain-2.h"
#include "../../Managers/BuildplanEntry.h"
#include "../../Managers/AgentManager.h"
#include "../RushSquad.h"
#include "../ExplorationSquad.h"
#include "../../Managers/ExplorationManager.h"
ZergMain-2::ZergMain-2() 
{
	// NOTE: Enusre that you add up to 10 squads to the .h file.
	//  each squad should be named squadX, where X is a number 1-11
	// Buildingplan subsection:
	buildplan.push_back(BuildplanEntry(UnitTypes::Zerg_Spawning_Pool, 5));
	buildplan.push_back(BuildplanEntry(UnitTypes::Zerg_Extractor, 5));
	buildplan.push_back(BuildplanEntry(UnitTypes::Zerg_Lair, 6));
	buildplan.push_back(BuildplanEntry(UnitTypes::Zerg_Hatchery, 8));
	buildplan.push_back(BuildplanEntry(UnitTypes::Zerg_Spire, 8));
	buildplan.push_back(BuildplanEntry(UpgradeTypes::Metabolic_Boost, 14));
	buildplan.push_back(BuildplanEntry(TechTypes::Burrowing, 15));
	buildplan.push_back(BuildplanEntry(UpgradeTypes::Pneumatized_Carapace, 16));
	buildplan.push_back(BuildplanEntry(UnitTypes::Zerg_Evolution_Chamber, 16));
	buildplan.push_back(BuildplanEntry(UnitTypes::Zerg_Hydralisk_Den, 16));
	buildplan.push_back(BuildplanEntry(UpgradeTypes::Antennae, 18));
	buildplan.push_back(BuildplanEntry(TechTypes::Lurker_Aspect, 18));
	buildplan.push_back(BuildplanEntry(UpgradeTypes::Muscular_Augments, 18));
	buildplan.push_back(BuildplanEntry(UpgradeTypes::Zerg_Carapace, 18));
	buildplan.push_back(BuildplanEntry(UpgradeTypes::Zerg_Melee_Attacks, 20));
	buildplan.push_back(BuildplanEntry(UpgradeTypes::Zerg_Missile_Attacks, 24));
	buildplan.push_back(BuildplanEntry(UpgradeTypes::Zerg_Flyer_Carapace, 25));
	buildplan.push_back(BuildplanEntry(UpgradeTypes::Grooved_Spines, 28));
	buildplan.push_back(BuildplanEntry(UpgradeTypes::Ventral_Sacs, 28));

	// SquadInit subsection:
	mainSquad = new Squad(0, Squad::OFFENSIVE, "mainSquad", 10);
	mainSquad->addSetup(UnitTypes::Zerg_Zergling, 16);
	mainSquad->addSetup(UnitTypes::Zerg_Hydralisk, 14);
	mainSquad->addSetup(UnitTypes::Zerg_Scourge, 20);
	mainSquad->addSetup(UnitTypes::Zerg_Mutalisk, 8);
	mainSquad->addSetup(UnitTypes::Zerg_Lurker, 2);
	mainSquad->setBuildup(true);
	mainSquad->setRequired(true);
	mainSquad->setMorphsTo(UnitTypes::Zerg_Lurker);
	squads.push_back(mainSquad);
	

	squad1 = new Squad(1, Squad::KITE, "squad1", 16);
	squad1->addSetup(UnitTypes::Zerg_Scourge, 18);
	squad1->addSetup(UnitTypes::Zerg_Zergling, 4);
	squad1->addSetup(UnitTypes::Zerg_Hydralisk, 10);
	squad1->setBuildup(false);
	squad1->setRequired(false);
	squads.push_back(squad1);
	

	squad2 = new Squad(2, Squad::EXPLORER, "squad2", 15);
	squad2->addSetup(UnitTypes::Zerg_Lurker, 1);
	squad2->addSetup(UnitTypes::Zerg_Scourge, 6);
	squad2->setBuildup(true);
	squad2->setRequired(true);
	squad2->setMorphsTo(UnitTypes::Zerg_Lurker);
	squads.push_back(squad2);
	

	squad3 = new Squad(3, Squad::DEFENSIVE, "squad3", 20);
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
	squad5->setBuildup(false);
	squad5->setRequired(true);
	squad5->setMorphsTo(UnitTypes::Zerg_Lurker);
	squads.push_back(squad5);
	

	squad6 = new Squad(6, Squad::SUPPORT, "squad6", 17);
	squad6->addSetup(UnitTypes::Zerg_Zergling, 24);
	squad6->addSetup(UnitTypes::Zerg_Scourge, 8);
	squad6->addSetup(UnitTypes::Zerg_Mutalisk, 14);
	squad6->setBuildup(true);
	squad6->setRequired(false);
	squads.push_back(squad6);
	

	squad7 = new Squad(7, Squad::RUSH, "squad7", 10);
	squad7->addSetup(UnitTypes::Zerg_Scourge, 16);
	squad7->addSetup(UnitTypes::Zerg_Lurker, 5);
	squad7->setBuildup(true);
	squad7->setRequired(true);
	squad7->setMorphsTo(UnitTypes::Zerg_Lurker);
	squads.push_back(squad7);
	

	squad8 = new Squad(8, Squad::KITE, "squad8", 10);
	squad8->addSetup(UnitTypes::Zerg_Hydralisk, 6);
	squad8->addSetup(UnitTypes::Zerg_Lurker, 1);
	squad8->addSetup(UnitTypes::Zerg_Zergling, 18);
	squad8->setBuildup(false);
	squad8->setRequired(false);
	squad8->setMorphsTo(UnitTypes::Zerg_Lurker);
	squads.push_back(squad8);
	

	squad9 = new Squad(9, Squad::SUPPORT, "squad9", 11);
	squad9->addSetup(UnitTypes::Zerg_Scourge, 22);
	squad9->addSetup(UnitTypes::Zerg_Lurker, 2);
	squad9->addSetup(UnitTypes::Zerg_Mutalisk, 2);
	squad9->setBuildup(false);
	squad9->setRequired(false);
	squad9->setMorphsTo(UnitTypes::Zerg_Lurker);
	squads.push_back(squad9);
	

	noWorkers = 11;
	noWorkersPerRefinery = 3;
}
ZergMain-2::~ZergMain-2()
{
	for (Squad* s : squads)
	{
		delete s;
	}
	instance = NULL;
}
void ZergMain-2::computeActions()
{
	computeActionsBase();
	noWorkers = AgentManager::getInstance()->countNoBases() * 6 + AgentManager::getInstance()->countNoUnits(UnitTypes::Zerg_Extractor) * 3;
	int cSupply = Broodwar->self()->supplyUsed() / 2;
	int min = Broodwar->self()->minerals();
	int gas = Broodwar->self()->gas();

	//Rules Subsections:
	if (stage == 0 && AgentManager::getInstance()->countNoBases() > -1 && min >= 450 && gas >= 0)
	{
		buildplan.push_back(BuildplanEntry(UnitTypes::Zerg_Sunken_Colony, cSupply));
		buildplan.push_back(BuildplanEntry(UpgradeTypes::Adrenal_Glands, cSupply));
		buildplan.push_back(BuildplanEntry(UpgradeTypes::Adrenal_Glands, cSupply));
		squad2->addSetup(UnitTypes::Zerg_Defiler, 6);
		stage++;
	}
	if (AgentManager::getInstance()->countNoBases() > -1 && min >= 100 && gas >= 150 && AgentManager::getInstance()->countNoFinishedUnits(UnitTypes::Zerg_Zergling) > 26 && AgentManager::getInstance()->countNoFinishedUnits(UnitTypes::Zerg_Mutalisk) > 18 && AgentManager::getInstance()->countNoFinishedUnits(UnitTypes::Zerg_Hydralisk_Den) > 0)
	{
		mainSquad->setPriority(41);
	}
	if (AgentManager::getInstance()->countNoBases() > -1 && min >= 450 && gas >= 300 && AgentManager::getInstance()->countNoFinishedUnits(UnitTypes::Zerg_Lurker) > 5 && AgentManager::getInstance()->countNoFinishedUnits(UnitTypes::Zerg_Hatchery) > 1 && AgentManager::getInstance()->countNoFinishedUnits(UnitTypes::Zerg_Mutalisk) > 10)
	{
		mainSquad->setActivePriority(8);
		squad1->setBuildup(false);
		squad4->setPriority(44);
	}
}
