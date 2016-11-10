############
# rsyncFTP #
############

# TODO : se connecter au serveur, synchroniser le serveur
# Config

# Import
from ftplib import FTP
import os
import os.path

# Fonctions
def connectionAuServeurFTP(host, user, password):
    """
    Fonction qui initialise la connection au serveur FTP distant
    :param host: host name
    :type host: str
    :param user:
    :param password:
    """
    ftp = FTP(host, user, password)  # on se connecte
    return ftp

def deconnexionAuServeur(connect):
    connect.quit()  # où "connect" est le nom de la variable dans laquelle vous avez déclaré la connexion !

def affichageFTP(ftp):
    print(FTP.dir(ftp))

def envoyerUnFichier(fichier_chemin,fichier_nom, ftp):
    file = open(fichier_chemin, 'rb') # ici, j'ouvre le fichier ftp.py
    ftp.storbinary('STOR '+ fichier_nom, file) #j'indique le fichier à envoyer
    file.close() # on ferme le fichier

def etatConnexion(ftp):
    etat = ftp.getwelcome()  # grâce à la fonction getwelcome(), on récupère le "message de bienvenue"
    print("Etat : ", etat)

def effacerFichier(ftp, fichier):
    ftp.delete(fichier)

def creerDossier(ftp, dossier):
    ftp.mkd(dossier)

def supprimerDossier(ftp, dossier):
    ftp.rmd(dossier)

def lister(ftp):
    rep = ftp.dir()  # on récupère le listing
    print(rep)  # on l'affiche dans la console

def copierContenuDossier(ftp, chemin, nom_dossier):
    creerDossier(ftp, nom_dossier)
    ftp.cwd(nom_dossier)
    l = os.listdir(chemin)
    print(l)
    for i in l:
        fichier = os.path.join(chemin, i)
        print(fichier)
        #dossierFTP  = os.path.join(ftp,nom_dossier)
        envoyerUnFichier(fichier, i, ftp)
    ftp.cwd('..')
    envoyerUnFichier(fichier,i,ftp)


def pushAuServeurFTP():
    """
    Fonction qui push les donnees vers le serveur FTP distant
    """
    return 1


# ____________________________________________________________________________________________________
# ____________________________________________________________________________________________________
#Test unitaire

def monMain():
    ### Variables

    host = "localhost"  # adresse du serveur FTP
    user = "root"  # votre identifiant
    password = "tomtom"  # votre mot de passe

    directory = os.getcwd() # "C:\Users\ISEN\Desktop\COURS\M1\Python\PycharmProjects\Projects\rsyncFTP"
    filename1 = "texte.txt"
    fichier1 = os.path.join(directory, filename1)
    print(fichier1)

    dossier = "test"
    chemin = os.path.join(directory, dossier)
    print(chemin)
    print(dossier)

    ### Tests des Fonctions

    ftp = connectionAuServeurFTP(host, user, password)
    #affichageFTP(ftp)
    #envoyerUnFichier(fichier1, filename1, ftp)
    #etatConnexion(ftp)
    #effacerFichier(ftp, filename2)
    #creerDossier(ftp, dossier)
    #supprimerDossier(ftp, dossier)
    #lister(ftp)
    #copierContenuDossier(ftp, chemin, dossier)
    deconnexionAuServeur(ftp)

if __name__ == "__main__":
    monMain()