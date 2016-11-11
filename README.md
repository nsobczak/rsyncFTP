# rsyncFTP

## Programme qui synchronise un dossier local de notre machine vers un site miroir ftp distant
Python course - TP03

rendu le 18 au soir au plus tard
pdf + zip


## parametres

|Paramètre|Type|Variable|
|---|---|---|
|site ftp distant|obligatoire|ftp|
|chemin vers le dossier local (directory path)|obligatoire|dp|
|chemin pour generer le fichier log (log path)|obligatoire|lp|
|2-uple contenant les extensions de la liste de fichiers a inclure et de la liste de fichiers a exclure|obligatoire|ie|
|chemin vers le fichier conf du log (gestion des handler)|optionnel|"-lc", "--logConf"|
|profondeur de la supervision du dossier, default = 2|optionnel|"-p", "--profondeur"|
|taille maximale des fichiers transferes en Mo, default = 500 Mo|optionnel|"-sf","--sizeFile"|
|frequence de supervision en s, default = 1 s|optionnel|"-f", "--frequence"|
|temps de supervision en s, default = 60 sec|optionnel|"-st", "--supervisionTime"|


commande linux = rsync

paramètre en lignes de commande ou dans un fichier ini


## Note explicative

Un pdf qui permet d'expliquer notre projet, pourquoi on a choisi de faire le truc comme ça. Faut vendre le projet.

- auteurs
- Si librairie supplémentaire => installable par pip
- choix techniques
- choix d'organisation

En lignes de commande


