#include "ZergMain-3.h"
#include "../../Managers/BuildplanEntry.h"
#include "../../Managers/AgentManager.h"
#include "../RushSquad.h"
#include "../ExplorationSquad.h"
#include "../../Managers/ExplorationManager.h"
ZergMain-3::ZergMain-3() 
{
	// NOTE: Enusre that you add up to 10 squads to the .h file.
	//  each squad should be named squadX, where X is a number 1-11
	// Buildingplan subsection:
	buildplan.push_back(BuildplanEntry(UnitTypes::Zerg_Spawning_Pool, 5));
	buildplan.push_back(BuildplanEntry(UnitTypes::Zerg_Extractor, 5));
	buildplan.push_back(BuildplanEntry(UnitTypes::Zerg_Lair, 6));
	buildplan.push_back(BuildplanEntry(UpgradeTypes::Antennae, 8));
	buildplan.push_back(BuildplanEntry(TechTypes::Burrowing, 8));
	buildplan.push_back(BuildplanEntry(UnitTypes::Zerg_Queens_Nest, 8));
	buildplan.push_back(BuildplanEntry(UnitTypes::Zerg_Spire, 8));
	buildplan.push_back(BuildplanEntry(UpgradeTypes::Pneumatized_Carapace, 10));
	buildplan.push_back(BuildplanEntry(TechTypes::Spawn_Broodlings, 10));
	buildplan.push_back(BuildplanEntry(TechTypes::Ensnare, 12));
	buildplan.push_back(BuildplanEntry(UpgradeTypes::Gamete_Meiosis, 12));
	buildplan.push_back(BuildplanEntry(UnitTypes::Zerg_Hive, 14));
	buildplan.push_back(BuildplanEntry(UnitTypes::Zerg_Hydralisk_Den, 14));
	buildplan.push_back(BuildplanEntry(TechTypes::Lurker_Aspect, 16));
	buildplan.push_back(BuildplanEntry(UpgradeTypes::Zerg_Flyer_Attacks, 16));
	buildplan.push_back(BuildplanEntry(UpgradeTypes::Metabolic_Boost, 18));
	buildplan.push_back(BuildplanEntry(UpgradeTypes::Adrenal_Glands, 20));
	buildplan.push_back(BuildplanEntry(UpgradeTypes::Grooved_Spines, 20));
	buildplan.push_back(BuildplanEntry(UnitTypes::Zerg_Greater_Spire, 20));
	buildplan.push_back(BuildplanEntry(UpgradeTypes::Muscular_Augments, 28));
	buildplan.push_back(BuildplanEntry(UnitTypes::Zerg_Evolution_Chamber, 28));
	buildplan.push_back(BuildplanEntry(UpgradeTypes::Zerg_Carapace, 30));
	buildplan.push_back(BuildplanEntry(UpgradeTypes::Zerg_Missile_Attacks, 30));
	buildplan.push_back(BuildplanEntry(UpgradeTypes::Ventral_Sacs, 32));
	buildplan.push_back(BuildplanEntry(UnitTypes::Zerg_Hatchery, 32));

	// SquadInit subsection:
	mainSquad = new Squad(0, Squad::OFFENSIVE, "mainSquad", 10);
	mainSquad->addSetup(UnitTypes::Zerg_Queen, 2);
	mainSquad->addSetup(UnitTypes::Zerg_Guardian, 3);
	mainSquad->setBuildup(true);
	mainSquad->setRequired(true);
	squads.push_back(mainSquad);
	

	squad1 = new Squad(1, Squad::RUSH, "squad1", 8);
	squad1->addSetup(UnitTypes::Zerg_Guardian, 3);
	squad1->addSetup(UnitTypes::Zerg_Hydralisk, 6);
	squad1->addSetup(UnitTypes::Zerg_Scourge, 18);
	squad1->addSetup(UnitTypes::Zerg_Lurker, 5);
	squad1->addSetup(UnitTypes::Zerg_Queen, 1);
	squad1->setBuildup(true);
	squad1->setRequired(true);
	squad1->setMorphsTo(UnitTypes::Zerg_Lurker);
	squads.push_back(squad1);
	

	squad2 = new Squad(2, Squad::DEFENSIVE, "squad2", 18);
	squad2->addSetup(UnitTypes::Zerg_Guardian, 6);
	squad2->addSetup(UnitTypes::Zerg_Scourge, 8);
	squad2->addSetup(UnitTypes::Zerg_Lurker, 1);
	squad2->addSetup(UnitTypes::Zerg_Zergling, 24);
	squad2->addSetup(UnitTypes::Zerg_Hydralisk, 4);
	squad2->setBuildup(true);
	squad2->setRequired(true);
	squad2->setMorphsTo(UnitTypes::Zerg_Lurker);
	squads.push_back(squad2);
	

	squad3 = new Squad(3, Squad::SUPPORT, "squad3", 12);
	squad3->addSetup(UnitTypes::Zerg_Mutalisk, 22);
	squad3->addSetup(UnitTypes::Zerg_Guardian, 1);
	squad3->addSetup(UnitTypes::Zerg_Queen, 3);
	squad3->addSetup(UnitTypes::Zerg_Lurker, 7);
	squad3->setBuildup(true);
	squad3->setRequired(true);
	squad3->setMorphsTo(UnitTypes::Zerg_Lurker);
	squads.push_back(squad3);
	

	squad4 = new Squad(4, Squad::SUPPORT, "squad4", 10);
	squad4->addSetup(UnitTypes::Zerg_Mutalisk, 10);
	squad4->addSetup(UnitTypes::Zerg_Queen, 2);
	squad4->addSetup(UnitTypes::Zerg_Zergling, 8);
	squad4->addSetup(UnitTypes::Zerg_Scourge, 12);
	squad4->addSetup(UnitTypes::Zerg_Hydralisk, 20);
	squad4->setBuildup(false);
	squad4->setRequired(true);
	squads.push_back(squad4);
	

	squad5 = new Squad(5, Squad::DEFENSIVE, "squad5", 9);
	squad5->addSetup(UnitTypes::Zerg_Queen, 8);
	squad5->addSetup(UnitTypes::Zerg_Lurker, 2);
	squad5->addSetup(UnitTypes::Zerg_Mutalisk, 12);
	squad5->addSetup(UnitTypes::Zerg_Scourge, 18);
	squad5->setBuildup(false);
	squad5->setRequired(false);
	squad5->setMorphsTo(UnitTypes::Zerg_Lurker);
	squads.push_back(squad5);
	

	squad6 = new Squad(6, Squad::DEFENSIVE, "squad6", 19);
	squad6->addSetup(UnitTypes::Zerg_Lurker, 5);
	squad6->addSetup(UnitTypes::Zerg_Mutalisk, 10);
	squad6->addSetup(UnitTypes::Zerg_Hydralisk, 8);
	squad6->setBuildup(true);
	squad6->setRequired(true);
	squad6->setMorphsTo(UnitTypes::Zerg_Lurker);
	squads.push_back(squad6);
	

	squad7 = new Squad(7, Squad::DEFENSIVE, "squad7", 20);
	squad7->addSetup(UnitTypes::Zerg_Zergling, 18);
	squad7->addSetup(UnitTypes::Zerg_Lurker, 5);
	squad7->setBuildup(false);
	squad7->setRequired(false);
	squad7->setMorphsTo(UnitTypes::Zerg_Lurker);
	squads.push_back(squad7);
	

	squad8 = new Squad(8, Squad::KITE, "squad8", 9);
	squad8->addSetup(UnitTypes::Zerg_Queen, 8);
	squad8->addSetup(UnitTypes::Zerg_Zergling, 2);
	squad8->setBuildup(false);
	squad8->setRequired(false);
	squads.push_back(squad8);
	

	noWorkers = 11;
	noWorkersPerRefinery = 3;
}
ZergMain-3::~ZergMain-3()
{
	for (Squad* s : squads)
	{
		delete s;
	}
	instance = NULL;
}
void ZergMain-3::computeActions()
{
	computeActionsBase();
	noWorkers = AgentManager::getInstance()->countNoBases() * 6 + AgentManager::getInstance()->countNoUnits(UnitTypes::Zerg_Extractor) * 3;
	int cSupply = Broodwar->self()->supplyUsed() / 2;
	int min = Broodwar->self()->minerals();
	int gas = Broodwar->self()->gas();

	//Rules Subsections:
	if (AgentManager::getInstance()->countNoBases() > 1 && min >= 200 && gas >= 240)
	{
		buildplan.push_back(BuildplanEntry(UnitTypes::Zerg_Nydus_Canal, cSupply));
	}
	if (stage == 0 && AgentManager::getInstance()->countNoBases() > 1 && min >= 500 && gas >= 150)
	{
		squad5->setBuildup(false);
		squad5->setPriority(84);
		stage++;
	}
	if (stage == 1 && AgentManager::getInstance()->countNoBases() > 2 && min >= 450 && gas >= 300)
	{
		squad2->setActivePriority(46);
		squad3->setBuildup(true);
		mainSquad->setActivePriority(18);
		buildplan.push_back(BuildplanEntry(UpgradeTypes::Zerg_Melee_Attacks, cSupply));
		stage++;
	}
	if (AgentManager::getInstance()->countNoBases() > 0 && min >= 150 && gas >= 180 && AgentManager::getInstance()->countNoFinishedUnits(UnitTypes::Zerg_Mutalisk) > 15 && AgentManager::getInstance()->countNoFinishedUnits(UnitTypes::Zerg_Guardian) > 7 && AgentManager::getInstance()->countNoFinishedUnits(UnitTypes::Zerg_Evolution_Chamber) > 0)
	{
		buildplan.push_back(BuildplanEntry(UpgradeTypes::Zerg_Melee_Attacks, cSupply));
	}
	if (stage == 2 && AgentManager::getInstance()->countNoBases() > 0 && min >= 200 && gas >= 90 && AgentManager::getInstance()->countNoFinishedUnits(UnitTypes::Zerg_Lurker) > 18)
	{
		mainSquad->setPriority(7);
		stage++;
	}
}
