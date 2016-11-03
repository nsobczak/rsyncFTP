# git

## Programme qui synchronise un dossier local de notre machine vers un site miroir ftp distant
Python course - TP03

rendu le 18 au soir au plus tard
pdf + zip

## parametres

|Paramètre|Type|Variable|
|---|---|---|
|site ftp distant|obligatoire||
|dossier local|obligatoire||
|liste de fichiers à inclure (les extensions)|obligatoire||
|liste de fichiers à exclure (les extensions)|obligatoire||
|fréquence de rafraichissement|obligatoire||

commande linux = rsync

paramètre en lignes de commande ou dans un fichier ini


- module logging
- main

### site ftp
toujours un quadruplet
- host
- user
- mdp


## Note explicative

Un pdf qui permet d'expliquer notre projet, pourquoi on a choisi de faire le truc comme ça. On va vendre le projet.

- auteurs
- Si librairie supplémentaire => installable par pip
- choix techniques
- choix d'organiser

En lignes de commande



## Architecture

### TODO
 
analyser un dossier sur une certaine profondeur => on utilise DirectorySupervisor

Se connecteur au serveur

push juste les trucs qui sont modifiés

### liste de fonctions



### Main

- initVariables()

- loop()

- main
	initVariables()
	loop()
