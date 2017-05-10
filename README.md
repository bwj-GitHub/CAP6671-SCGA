# CAP6671-SCGA
Project for CAP6671; a Steady-State Genetic Algorithm for evolving a StarCraft: BroodWar Strategy for OpprimoBot.


# Tournament Manager Setup

Tournament Manager official video tutorial: <https://www.youtube.com/watch?v=tl-nansNbsA?>

The following instructions can be used to setup a server, local client and 1 VM client to execute the
evolution of OpprimoBot.

1. Setup a VirtualBox Windows virtual machine (Untested but, should work with Windows free trial versions)
2. Download TournamentManager folder to server/client and VM
3. Download StarCraft 1.16.1 to server/client and VM
4. Install Java JDK on server/client and virtual machine
6. Compile TournamentManager if necessary
  1. src/clean.bat
  2. src/make.bat
5. For server/client and VM, download BWTA from <https://bitbucket.org/auriarte/bwta2> 
  * Move the files in the windows folder to C:\Windows
6. For the server edit the following files to match your settings
  * server/run\_server\_from\_script\_easy.bat
  * server/run\_server\_from\_script\_hard.bat
  * client/run\_local\_client\_from\_script.bat
  * client/run\_vm\_client\_from\_script.bat
7. For the client VM edit the following files to match your settings
  * client/run\_client\_from\_host.bat
  * client/client\_settings.ini
8. For the local client edit the following files to match your settings
  * client/client\_settings.ini
