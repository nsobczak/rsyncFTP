############
# rsyncFTP #
############

# TODO : Remplacer les noms des fonctions arbre par des noms francais + creer fonction loop
# ____________________________________________________________________________________________________
# Config

# Import
import logging
import sys
import argparse
import os
import time

# ____________________________________________________________________________________________________
# ____________________________________________________________________________________________________
# Variables globales


dp = None
lp = None
depth = None
frequence = None
arbrePrecedent = None
startinglevel = None
logger = None
supervisionTime = None


# ____________________________________________________________________________________________________
# Fonctions d'initialisation

def initLog(logPath):
    """
    log format
    logging.basicConfig(datefmt='', format='%asctime', level=logging.INFO)
    """
    logging.basicConfig(
        filename=logPath + "/DirectorySupervisor.log", \
        datefmt="%d/%m/%Y-%H:%M:%S", \
        format="%(asctime)s %(levelname)s %(funcName)s %(message)s", \
        level=logging.INFO)     # 'filename': '/path/to/DirectorySupervisor.debug.log',
    logging.info("Programme lance")


def initVariablesGlobales():
    """
    Fonction qui initialise les variables globales en fonction de ce que l'utilisateur a entre.
    La fonction genere une info recapitulant la liste des parametres entres.
    """
    global dp
    global lp
    global depth
    global frequence
    global supervisionTime
    global startinglevel
    global arbrePrecedent

    parser = argparse.ArgumentParser(description='Supervision de dossier with DirectorySupervisor')
    # obligatoire
    parser.add_argument("dp", type=str, help="path to the directory")
    parser.add_argument("lp", type=str, help="path where to generate log")
    # optionnel
    parser.add_argument("-d", "--depth", default=2, help="depth of the surpervision directory, default = 2")
    parser.add_argument("-f", "--frequence", default=1, help="add supervision frequency in hz, default = 1 hz")
    parser.add_argument("-st", "--supervisionTime", default=60, help="add supervision time (in sec), default = 60 sec")

    # initialisation des parametres globaux
    args = parser.parse_args()
    dp = args.dp
    lp = args.lp
    depth = int(args.depth)
    frequence = int(args.frequence)
    supervisionTime = int(args.supervisionTime)
    startinglevel = dp.count(os.sep)        # indique le niveau de profondeur initiale
    arbrePrecedent = createSurveyList(list(os.walk(dp)))


def afficheArgument():
    """affichage des arguments rentres"""
    logging.info(
        ":\npath to the directory : %s \npath where to generate log : %s \ndepth of the directory : %s \nfrequency : %s hz \nsupervision time : %s sec\n",
        dp, lp, depth, frequence, supervisionTime)


# ___________________________________________________________________________________________________
# Fonctions de creation de l'arbre du dossier et de comparaison

def createSurveyList(tree):
    """
    create a list of tupples form by (fileName, dateOfLastModif) corresponding to the files in the tree
    """
    listOfModifFiles = []
    i = 0
    while (i < len(tree)):
        path, dirs, files = tree[i]
        level = path.count(os.sep) - startinglevel
        if (level <= depth):
            # logging.info('### depth ' + str(level) + ' ### ' + str(path) + ' #####')
            # logging.info("Sous dossiers : %s" % dirs)
            # logging.info("Fichiers : %s" % files)
            for dir in dirs:
                modifTime = os.path.getmtime(os.path.join(path, dir))
                listOfModifFiles += [(path + '/' + dir, modifTime)]
            for file in files:
                modifTime = os.path.getmtime(os.path.join(path, file))
                listOfModifFiles += [(path + '/' + file, modifTime)]
        i += 1
    return (listOfModifFiles)


def comparateSurveyList(oldListe, newListe):
    """
	args 2 lists which will be compared
	return 3 lists :
		- for the modified files
		- for the added files
		- for the deleted files
	"""
    if oldListe == newListe:
        return [], [], []
    else:
        listOfSupprFiles = []
        listOfAddFiles = []
        listOfModifFiles = []
        isCreated = [True] * len(newListe)
        for o in oldListe:
            isDeleted = True
            for n in newListe:
                nIndex = newListe.index(n)
                oName, oTime = o
                nName, nTime = n
                if oName == nName:
                    isDeleted = False
                    isCreated[nIndex] = False
                    if oTime != nTime:
                        listOfModifFiles += [n]
            if isDeleted:
                listOfSupprFiles += [o]
        for n in newListe:
            nIndex = newListe.index(n)
            if isCreated[nIndex]:
                listOfAddFiles += [n]
        return (listOfModifFiles, listOfAddFiles, listOfSupprFiles)


def logTheMADLists(M, A, D):
    """
    	log the informations contained in the 3 lists :
    		-M = modified files
    		-A = added files
    		-D = deleted files
    """
    if len(M):
        logging.info("M")
        for (mFile, mTime) in M:
            logging.info(
                time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime(mTime)) + " " + str(mFile) + " is modified")
    if len(A):
        logging.info("A")
        for (aFile, aTime) in A:
            logging.info(time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime(aTime)) + " " + str(aFile) + " is added")
    if len(D):
        logging.info("D")
        for (dFile, dTime) in D:
            logging.info(time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime(dTime)) + " last time " + str(
                dFile) + " is viewed before delete")


# ___________________________________________________________________________________________________
# Fonctions principales

def loop():
    """
    si stop() => arret
	sinon
		compareArbre()
    """
    global arbrePrecedent
    totalTime = 0
    oldTime = time.time()
    newTime = time.time()
    while totalTime < (supervisionTime*frequence):
        newTime = time.time()
        if (newTime - oldTime) > (1 / frequence):
            # logging.info(str(totalTime / frequence) + " sec depuis lancement du programme")
            oldTime = time.time()
            nouvelArbre = createSurveyList(list(os.walk(dp)))
            M, A, D = comparateSurveyList(arbrePrecedent, nouvelArbre)
            if len(M) or len(A) or len(D):
                arbrePrecedent = nouvelArbre
                logTheMADLists(M, A, D)
            totalTime += 1
    return 1


# ____________________________________________________________________________________________________
# ____________________________________________________________________________________________________
def monMain():
    initVariablesGlobales()
    initLog(lp)
    afficheArgument()
    loop()


if __name__ == "__main__":
    monMain()
