############
# rsyncFTP #
############

# TODO : se connecter au serveur, synchroniser le serveur
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
    """
    ftp = FTP(host, user, password)  # on se connecte
    return ftp


def deconnexionAuServeur(connect):
    """
    Fonction qui se deconnecte du serveur
    :param connect: nom de la variable dans laquelle la connexion a ete declaree
    :type connect: ???
    """
    connect.quit()


def affichageFTP(ftp):
    """
    Fonction qui affiche ???
    :param ftp: ???
    :type ftp: ???
    """
    print(FTP.dir(ftp))


def envoyerUnFichier(fichier_chemin, fichier_nom, ftp):
    """
    Fonction qui envoie un fichier
    :param ftp: ???
    :type ftp: ???
    """
    # ouverture du fichier
    file = open(fichier_chemin, 'rb')
    # fichier a envoyer
    ftp.storbinary('STOR ' + fichier_nom, file)
    # fermeture du fichier
    file.close()


def etatConnexion(ftp):
    """
    Fonction qui ???
    :param ftp: ???
    :type ftp: ???
    """
    etat = ftp.getwelcome()  # grâce à la fonction getwelcome(), on récupère le "message de bienvenue"
    print("Etat : ", etat)


def effacerFichier(ftp, fichier):
    """
    Fonction qui ???
    :param ftp: ???
    :type ftp: ???
    :param fichier: ???
    :type fichier: ???
    """
    ftp.delete(fichier)


def creerDossier(ftp, nom_dossier, chemin_dossier):
    """
    Fonction qui cree un dossier spécifié par chemin dans le ftp
    :param ftp: ???
    :type ftp: ???
    :param dossier: ???
    :type dossier: ???
    """
    ftp.cwd(chemin_dossier)
    ftp.mkd(nom_dossier)
    ftp.cwd('..')

def supprimerDossier(ftp, dossier):
    """
    Fonction qui supprime un dossier
    :param ftp: ???
    :type ftp: ???
    :param dossier: ???
    :type dossier: ???
    """
    ftp.rmd(dossier)


def lister(ftp):
    """
    Fonction qui ???
    :param ftp: ???
    :type ftp: ???
    """
    rep = ftp.dir()  # on récupère le listing
    print(rep)  # on l'affiche dans la console

def listerFichiers(ftp):
    ret = []
    ftp.dir("", ret.append)
    ret = [x.split()[-1] for x in ret if x.startswith("d") or x.startswith("-")]
    return ret

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
    if profondeure_copie_autorisee<=0:
        return 1
    liste = listerFichiers(ftp)
    print(liste)
    chemin_ftp += "/"
    print("chemin ftp = {}".format(chemin_ftp))
    # On cree le dossier s'il n'existe pas deja
    dossierExiste = False
    for i in liste:
        if (nom_dossier == i):
            dossierExiste = True
    print(dossierExiste)
    if not dossierExiste:
        print(nom_dossier)
        for i in chemin_ftp.split("/"):
            if i != '':
                ftp.cwd(i)
        creerDossier(ftp, nom_dossier, chemin_ftp)

    print(ftp.pwd())
    ftp.cwd(nom_dossier)
    chemin_ftp += nom_dossier
    print("chemin ftp = {}".format(chemin_ftp))
    print(ftp.pwd())

    l = os.listdir(chemin_local)
    print(l)
    for i in l:
        element = os.path.join(chemin_local, i)
        print(element)
        if os.path.isdir(element):
            print("copie d'un dossier")
            print(ftp.pwd())
            copierContenuDossier(ftp, chemin_ftp, element, i, profondeure_copie_autorisee-1)
        elif os.path.isfile(element):
            print("copie d'un fichier")
            print(ftp.pwd())
            envoyerUnFichier(element, i, ftp)
    l = listerFichiers(ftp)
    print(l)
    ftp.cwd('..')
    l = listerFichiers(ftp)
    print(l)


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

    ### Tests des Fonctions

    ftp = connectionAuServeurFTP(host, user, password)
    chemin1 = "test"
    nom_dossier1 = "test2.1"
    envoyerUnFichier(fichier1, filename1, ftp)
    # etatConnexion(ftp)
    #effacerFichier(ftp, filename2)
    #creerDossier(ftp, nom_dossier1, chemin1)
    #supprimerDossier(ftp, dossier)
    #lister(ftp)
    copierContenuDossier(ftp, "",chemin_local, nom_dossier,5)
    deconnexionAuServeur(ftp)


if __name__ == "__main__":
    monMain()
