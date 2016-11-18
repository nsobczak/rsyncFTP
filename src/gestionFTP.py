"""
############
# rsyncFTP #
##############
# gestionFTP #
##############

@author: Julien Vermeil and Vincent Reynaert and Nicolas Sobczak
"""

# TODO : /
# %%__________________________________________________________________________________________________
# Config

# Import
import ftplib
from ftplib import FTP
import os
import os.path


# %%__________________________________________________________________________________________________
# ____________________________________________________________________________________________________
# Fonctions
def connectionAuServeurFTP(host, user, password):
    """
    Fonction qui initialise la connection au serveur FTP distant
    :param host: host name
    :type host: str
    :param user: user id
    :type user: str
    :param password: password
    :type password: str
    :return: ftp
    :rtype: class 'ftplib.FTP'
    """
    ftp = FTP(host, user, password)  # on se connecte
    return ftp


def deconnexionAuServeur(ftp):
    """
    Fonction qui se deconnecte du serveur
    :param ftp: nom de la variable dans laquelle la connexion a ete declaree
    :type ftp: class 'ftplib.FTP'
    """
    ftp.quit()


def affichageFTP(ftp):
    """
    Fonction qui affiche les infos (fichiers et dossiers) contenues dans le ftp
    :param ftp: serveur ftp
    :type ftp: class 'ftplib.FTP'
    """
    print(FTP.dir(ftp))


def etatConnexion(ftp):
    """
    Fonction qui affiche l'etat de la connexion au serveur ftp
    :param ftp: serveur ftp
    :type ftp: class 'ftplib.FTP'
    """
    etat = ftp.getwelcome()  # grâce à la fonction getwelcome(), on récupère le "message de bienvenue"
    print("Etat : ", etat)


def listerFichiers(ftp):
    """
    Fonction qui liste les fichiers presents dans le repertoire observe sur le ftp
    :param ftp: serveur ftp
    :type ftp: class 'ftplib.FTP'
    """
    ret = []
    ftp.dir("", ret.append)
    ret = [x.split()[-1] for x in ret if x.startswith("-")]
    return ret


def listerDossiers(ftp):
    """
    Fonction qui liste les dossiers presents dans le repertoire observe sur le ftp
    :param ftp: serveur ftp
    :type ftp: class 'ftplib.FTP'
    """
    ret = []
    ftp.dir("", ret.append)
    ret = [x.split()[-1] for x in ret if x.startswith("d")]
    return ret


def listerElements(ftp):
    """
    Fonction qui liste les fichiers et les dossiers presents dans le repertoire observe sur le ftp
    :param ftp: serveur ftp
    :type ftp: class 'ftplib.FTP'
    """
    return listerFichiers(ftp) + listerDossiers(ftp)


def differenceEntreChemins(chemin1,chemin2):
    """
    Fonction qui renvoie la difference chemin1-chemin2 (si chemin1 est plus haut que 2
    alors on retourne une liste contenant des '..')
    :param chemin1: chemin relatif (dont la racine correspond a celle du ftp)
    :type chemin1: str
    :param chemin2: chemin relatif (dont la racine correspond a celle du ftp)
    :type chemin2: str
    :return : liste contenant les dossiers a suivre pour se positionner
                au meme endroit que chemin1 a partir de chemin2
    :rtype : list
    """
    longueur_chemin1 = len(chemin1)
    longueur_chemin2 = len(chemin2)
    res = []
    if longueur_chemin1 == longueur_chemin2 :
        if chemin1 == chemin2:
            return None
        else :
            return ['*']
    elif longueur_chemin1 < longueur_chemin2 :
        dif = str(chemin2[longueur_chemin1:])
        for i in dif.split('/'):
            if i:
                res.append('..')
    else :
        dif = str(chemin1[longueur_chemin2:])
        for i in dif.split('/'):
            if i:
                res.append(i)
    return res


def redirigeVers(ftp, chemin_relatif):
    """
    Fonction qui positionne dans le ftp en suivant le chemin relatif 'chemin' entre en parametre
    :param ftp: serveur ftp
    :type ftp: class 'ftplib.FTP'
    :param chemin: chemin relatif (dont la racine correspond a celle du ftp)
    :type chemin: str
    """
    # retour a la racine du ftp
    while ftp.pwd() != '/':
        ftp.cwd('..')
    # on redirige vers chemin
    for i in chemin_relatif.split('/'):
        if i:
            try :
                ftp.cwd(i)
            except ftplib.error_perm:
                break


def positionnementDansLeFTP(ftp, chemin):
    """
    Fonction qui positionne dans le ftp en suivant le chemin relatif 'chemin' entre en parametre
    :param ftp: serveur ftp
    :type ftp: class 'ftplib.FTP'
    :param chemin: chemin relatif (dont la racine correspond a celle du ftp)
    :type chemin: str
    """
    l = differenceEntreChemins(chemin,ftp.pwd())
    if l :
        if l[0]=='*':
            redirigeVers(ftp, chemin)
        else :
            for i in l:
                try :
                    ftp.cwd(i)
                except ftplib.error_perm:
                    redirigeVers(ftp, chemin)


def rePositionnementDansLeFTP(ftp, chemin):
    """
    Fonction qui fait le chemin inverse de la fonction positionnementDansLeFTP
    :param ftp: serveur ftp
    :type ftp: class 'ftplib.FTP'
    :param chemin: chemin relatif (dont la racine correspond a celle du ftp)
    :type chemin: str
    """
    l = differenceEntreChemins(ftp.pwd(), chemin)
    if l:
        for i in l:
            try :
                ftp.cwd(i)
            except ftplib.error_perm:
                break


# %%__________________________________________________________________________________________________
def envoyerUnFichier(fichier_chemin, fichier_nom, ftp):
    """
    Fonction qui envoie un fichier existant vers le serveur ftp
    :param fichier_chemin: chemin absolu (avec le nom du fichier) vers le fichier local
    :type fichier_chemin: str
    :param fichier_nom: nom du fichier
    :type fichier_nom: str
    :param ftp: serveur ftp
    :type ftp: class 'ftplib.FTP'
    """
    # ouverture du fichier
    file = open(fichier_chemin, 'rb')
    # fichier a envoyer
    ftp.storbinary('STOR ' + fichier_nom, file)
    # fermeture du fichier
    file.close()


def supprimerFichier(ftp, fichier_chemin, fichier_nom):
    """
    Fonction qui supprime un fichier dans le ftp
    :param ftp: serveur ftp
    :type ftp: class 'ftplib.FTP'
    :param fichier_chemin: chemin relatif (sans le nom du fichier) vers le fichier local
    :type fichier_chemin: str
    :param fichier_nom: nom du fichier
    :type fichier_nom: str
    """
    ftp.cwd(fichier_chemin)
    ftp.delete(fichier_nom)
    for i in fichier_chemin.split('/'):
        if i != '':
            ftp.cwd('..')


def creerDossier(ftp, dossier_chemin, dossier_nom):
    """
    Fonction qui cree un dossier dans le ftp
    :param ftp: serveur ftp
    :type ftp: class 'ftplib.FTP'
    :param dossier_chemin: chemin relatif (sans le nom du dossier) vers le dossier local
    :type dossier_chemin: str
    :param dossier_nom: nom du fichier
    :type dossier_nom: str
    """
    ftp.cwd(dossier_chemin)
    try:
        ftp.mkd(dossier_nom)
    except ftplib.error_perm:
        None
    ftp.cwd('..')


def supprimerDossier(ftp, dossier_chemin, dossier_nom):
    """
    Fonction qui cree un dossier dans le ftp
    :param ftp: serveur ftp
    :type ftp: class 'ftplib.FTP'
    :param dossier_chemin: chemin relatif vers le dossier local contenant le dossier a supprimer
    :type dossier_chemin: str
    :param dossier_nom: nom du dossier
    :type dossier_nom: str
    """
    try:
        ftp.cwd(dossier_chemin)
        ftp.cwd(dossier_nom)

        liste_sous_dossiers = listerDossiers(ftp)
        liste_fichiers = listerFichiers(ftp)
        print(liste_fichiers + liste_sous_dossiers)

        if (not liste_sous_dossiers and not liste_fichiers):
            ftp.cwd('..')
            ftp.rmd(dossier_nom)
        else:
            for i in liste_fichiers:
                supprimerFichier(ftp, '', i)
            for i in liste_sous_dossiers:
                supprimerDossier(ftp, '', i)
            ftp.cwd('..')
            ftp.rmd(dossier_nom)
    except:
        return("Warning: dossier inexistant sur le serveur FTP => il ne peut pas etre supprime")


def copierContenuDossier(ftp, chemin_ftp, chemin_local, nom_dossier, profondeure_copie_autorisee):
    """
    Fonction qui copie les fichiers d'un dossier specifie
    :param ftp: serveur ftp
    :type ftp:
    :param chemin_ftp: chemin dans le dossier distant
    :type chemin_ftp: str
    :param chemin_local: chemin absolu (avec nom du dossier) du dossier
    :type chemin_local: str
    :param nom_dossier: nom du dossier
    :type nom_dossier: str
    :param profondeure_copie_autorisee: profondeur de copie autorisee
    :type profondeure_copie_autorisee: int
    """
    if profondeure_copie_autorisee < 0:
        return 1
    liste = listerElements(ftp)
    chemin_ftp += "/"
    # On cree le dossier s'il n'existe pas deja
    dossierExiste = False
    for i in liste:
        if (nom_dossier == i):
            dossierExiste = True
    if not dossierExiste:
        creerDossier(ftp, chemin_ftp, nom_dossier)
        i = chemin_ftp.split("/")[-2]
        if i != '':
            ftp.cwd(i)
    ftp.cwd(nom_dossier)
    chemin_ftp += nom_dossier
    l = os.listdir(chemin_local)
    for i in l:
        element = os.path.join(chemin_local, i)
        if os.path.isdir(element):
            copierContenuDossier(ftp, chemin_ftp, element, i, profondeure_copie_autorisee - 1)
        elif os.path.isfile(element):
            if profondeure_copie_autorisee > 0:
                envoyerUnFichier(element, i, ftp)
    l = listerFichiers(ftp)
    ftp.cwd('..')
    l = listerFichiers(ftp)


# %%__________________________________________________________________________________________________
# ____________________________________________________________________________________________________
# Tests unitaires

def monMain():
    ### Variables
    host = "localhost"  # adresse du serveur FTP
    user = "root"  # votre identifiant
    password = "0000"  # votre mot de passe

    directory = "C:\\Users\\ISEN\\Desktop\\COURS\\M1\\Python\\PycharmProjects\\Projects\\rsync"
    # "/home/nicolas/Documents/Git/rsyncFTP"
    filename1 = "1.1.1.txt"
    fichier1 = os.path.join(directory, filename1)

    nom_dossier = "test0"
    chemin_local = os.path.join(directory, nom_dossier)
    nom_dossier1 = "1.1"
    chemin_local1 = os.path.join(directory, nom_dossier1)

    ### Tests des Fonctions

    ftp = connectionAuServeurFTP(host, user, password)
    print(type(ftp))
    chemin1 = "test"
    # envoyerUnFichier(fichier1, ftp)
    # etatConnexion(ftp)
    # supprimerFichier(ftp, filename2)
    # creerDossier(ftp, chemin1, nom_dossier1)
    # supprimerDossier(ftp, dossier)
    # lister(ftp)
    # copierContenuDossier(ftp, "",chemin_local, nom_dossier, 5)
    supprimerDossier(ftp, '', nom_dossier)

    deconnexionAuServeur(ftp)


if __name__ == "__main__":
    monMain()
