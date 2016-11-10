############
# rsyncFTP #
############

# TODO : completer les commentaires | supprimer les variables globales commentees
# ____________________________________________________________________________________________________
# Config

# Import
import logger
import os
import time

# ____________________________________________________________________________________________________
# ____________________________________________________________________________________________________


# Variables globales <= a supprimer par la suite


# dp = None #path to the directory
# depth = None
# frequence = None
# arbrePrecedent = None
# startinglevel = None
# logger = None
# supervisionTime = None


# ___________________________________________________________________________________________________
# Fonctions de creation de l'arbre du dossier et de comparaison

def createSurveyList(tree, startinglevel, depth):
    """
    Function which create a list of tupples form by (fileName, dateOfLastModif) corresponding to the files in the tree
    :param tree: tree
    :type tree: ???
    :param startinglevel:
    :type startinglevel: int
    :param depth:
    :type depth: int
    :return listOfModifFiles: list for he deleted files
    :rtype listOfModifFiles: list
    """
    listOfModifFiles = []
    i = 0
    while (i < len(tree)):
        path, dirs, files = tree[i]
        level = path.count(os.sep) - startinglevel
        if (level <= depth):
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
    Fonction qui compare 2 listes :
    :param oldListe: old list
    :type oldListe: list
    :param newListe:new list
    :type newListe: list
    :return: tuple of list for the modified files, list for the added files, list for the deleted files
    :rtype: tuple
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


def logTheMADLists(logger, M, A, D):
    """
    Function that log information contained in the 3 lists :
    :param M: modified files
    :type M: list
    :param A: added files
    :type A: list
    :param D: deleted files
    :type D: list
    :param logger: logger
    :type logger: log
    """
    if len(M):
        logger.info("M")
        for (mFile, mTime) in M:
            logger.info(
                time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime(mTime)) + " " + str(mFile) + " is modified")
    if len(A):
        logger.info("A")
        for (aFile, aTime) in A:
            logger.info(time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime(aTime)) + " " + str(aFile) + " is added")
    if len(D):
        logger.info("D")
        for (dFile, dTime) in D:
            logger.info(time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime(dTime)) + " last time " + str(
                dFile) + " is viewed before delete")


# ___________________________________________________________________________________________________
# Fonctions principales

def loop(logger, frequence, supervisionTime, arbrePrecedent, dp):
    """
    Fonction: si stop() => arret, sinon compareArbre()
    :param logger: logger
    :type logger: log
    :param frequence: frequence de supervision
    :type frequence: int
    :param supervisionTime: temps de supervision, si -1 alors infini
    :type supervisionTime: int
    :param arbrePrecedent: tree arbre precedent
    :type arbrePrecedent: tree ???
    :param dp: chemin du dossier
    :type dp: str
    :return: 1
    :rtype: int
    """
    # si supervision time est a -1 on fait une boucle infinie
    infinite = False
    if (supervisionTime==-1):
        logger.info("supervisionTime = -1 => supervision en continue")
        infinite = True

    totalTime = 0
    oldTime = time.time()
    newTime = time.time()

    while totalTime < (supervisionTime * frequence) or infinite:
        newTime = time.time()
        if (newTime - oldTime) > (1 / frequence):
            # logger.info(str(totalTime / frequence) + " sec depuis lancement du programme")
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
# Test unitaire
def monMain():
    MAIN_LOGGER = logger.initLog()


if __name__ == "__main__":
    print('')
    print(type(os._isdir('C:\\Users\\vvinc_000\\Documents\\Cours\\ISEN\\M1\\Python')))
    monMain()
