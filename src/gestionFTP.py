############
# rsyncFTP #
##############
# gestionFTP #
##############

# TODO : se connecter au serveur, synchroniser le serveur, completer les commentaires
# ____________________________________________________________________________________________________
# Config

# Import
from ftplib import FTP
import os
import os.path


# ____________________________________________________________________________________________________
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


def envoyerUnFichier(fichier_chemin, fichier_nom, ftp):
    """
    Fonction qui envoie un fichier existant vers le serveur ftp
    :param fichier_chemin: chemin vers le fichier local
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


def etatConnexion(ftp):
    """
    Fonction qui affiche l'etat de la connexion au serveur ftp
    :param ftp: serveur ftp
    :type ftp: class 'ftplib.FTP'
    """
    etat = ftp.getwelcome()  # grâce à la fonction getwelcome(), on récupère le "message de bienvenue"
    print("Etat : ", etat)


def supprimerFichier(ftp, fichier_chemin, fichier_nom):
    """
    Fonction qui supprime un fichier dans le ftp
    :param ftp: serveur ftp
    :type ftp: class 'ftplib.FTP'
    :param fichier_chemin: chemin vers le fichier local
    :type fichier_chemin: str
    :param fichier_nom: nom du fichier
    :type fichier_nom: str
    """
    ftp.cwd(fichier_chemin)
    ftp.delete(fichier_nom)
    for i in fichier_chemin.split('/') :
        if i!='' :
            ftp.cwd('..')



def creerDossier(ftp, dossier_chemin, dossier_nom):
    """
    Fonction qui cree un dossier dans le ftp
    :param ftp: serveur ftp
    :type ftp: class 'ftplib.FTP'
    :param dossier_chemin: chemin vers le dossier local
    :type dossier_chemin: str
    :param dossier_nom: nom du fichier
    :type dossier_nom: str
    """
    ftp.cwd(dossier_chemin)
    ftp.mkd(dossier_nom)
    ftp.cwd('..')

def listerFichiers(ftp):
    ret = []
    ftp.dir("", ret.append)
    ret = [x.split()[-1] for x in ret if x.startswith("-")]
    return ret

def listerDossiers(ftp):
    ret = []
    ftp.dir("", ret.append)
    ret = [x.split()[-1] for x in ret if x.startswith("d")]
    return ret

def listerElements(ftp):
    return listerFichiers(ftp)+listerDossiers(ftp)

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
    print(ftp.pwd())
    ftp.cwd(dossier_chemin)
    print(ftp.pwd())
    ftp.cwd(dossier_nom)
    print(ftp.pwd())
    liste_sous_dossiers = listerDossiers(ftp)
    liste_fichiers = listerFichiers(ftp)
    print(liste_fichiers+liste_sous_dossiers)
    if (not liste_sous_dossiers and not liste_fichiers):
        ftp.cwd('..')
        print('Supprimons le dossier vide '+dossier_nom)
        ftp.rmd(dossier_nom)
    else :
        for i in liste_fichiers:
            print('supprimons le fichier '+i)
            supprimerFichier(ftp, '', i)
        for i in liste_sous_dossiers:
            print('supprimons le dossier '+i)
            print(ftp.pwd())
            supprimerDossier(ftp, '', i)
    ftp.cwd('..')
    ftp.rmd(dossier_nom)


def copierContenuDossier(ftp, chemin_ftp, chemin_local, nom_dossier, profondeure_copie_autorisee):
    """
    Fonction qui copie les fichiers d'un dossier spécifié
    :param ftp: serveur ftp
    :type ftp:
    :param chemin_ftp: chemin dans le dossier lointain
    :type chemin_ftp: str
    :param chemin_local: chemin complet du dossier
    :type chemin_local: str
    :param nom_dossier: nom du dossier
    :type nom_dossier: str
    :param profondeure_copie_autorisee:
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
            copierContenuDossier(ftp, chemin_ftp, element, i, profondeure_copie_autorisee-1)
        elif os.path.isfile(element):
            if profondeure_copie_autorisee > 0:
                envoyerUnFichier(element, i, ftp)
    l = listerFichiers(ftp)
    ftp.cwd('..')
    l = listerFichiers(ftp)


def pushAuServeurFTP():
    """
    Fonction qui push les donnees vers le serveur FTP distant
    """
    return 1


# ____________________________________________________________________________________________________
# ____________________________________________________________________________________________________
# Test unitaire

def monMain():
    ### Variables

    host = "localhost"  # adresse du serveur FTP
    user = "root"  # votre identifiant
    password = "0000"  # votre mot de passe

    directory = "C:\\Users\\vvinc_000\\Documents\\Cours\\ISEN\\M1\\Python\\1"
    filename1 = "1.1.1.txt"
    fichier1 = os.path.join(directory, filename1)

    nom_dossier = "Nouveau_dossier"
    chemin_local = os.path.join(directory, nom_dossier)
    nom_dossier1 = "1.1"
    chemin_local1 = os.path.join(directory, nom_dossier1)

    ### Tests des Fonctions

    ftp = connectionAuServeurFTP(host, user, password)
    print(type(ftp))
    chemin1 = "test"
    #envoyerUnFichier(fichier1, ftp)
    # etatConnexion(ftp)
    #supprimerFichier(ftp, filename2)
    #creerDossier(ftp, chemin1, nom_dossier1)
    #supprimerDossier(ftp, dossier)
    #lister(ftp)
    copierContenuDossier(ftp, "",chemin_local, nom_dossier, 5)
    supprimerDossier(ftp,'',nom_dossier)

    deconnexionAuServeur(ftp)


if __name__ == "__main__":
    monMain()
