# tcejorp MILD (DLIM project)

![Logo de `tcejorp MILD`](src/static/DLIMProjectLogo.png)

Création d'un moteur de recherche d'images.

## Membres de l'équipe

Equipe `kcab si MILD` :
- Temano FROGIER `<temano.frogier>`
- Paul GALAND `<paul.galand>`
- Mélanie TCHEOU `<melanie.tcheou>`

## Arborescence du projet

```sh
.
├── README.md           # Ce README
├── requirements.txt    # Dépendances Python
└── src                 # Code source du projet
    ├── *.py            # Fichier nécessaires pour l'API
    ├── api.py          # Serveur API/WebApp
    ├── setup.py        # Setup complet de l'environnement de l'API
    ├── static          # Resources de l'API
    └── templates       # Pages de la WebApp
```

## Installation et lancement de l'API

(OPTIONEL) Placez vous dans un environnement virtuel :
```sh
python -m venv dlim
. ./dlim/bin/activate
```

Téléchargez les librairies requises (peut prendre un certain temps) :
```sh
pip install --upgrade pip
pip install -r requirements.txt
```

Placez vous dans le dossier source :
```sh
cd src
```

Mettez en place le serveur (téléchargement des données et pré-traitement des images) :
```sh
python setup.py
```

Lancez l'API :
```sh
python api.py
```

## Utilisation de l'API

Une fois que l'API est lancée (quelque chose semblable est affiché dans votre terminal) :
```
Loading the model...
Model loaded!
 * Serving Flask app 'api'
 * Debug mode: off
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on http://127.0.0.1:5000
Press CTRL+C to quit
```

Vous pouvez accéder a la WebApp sur votre navigateur avec l'URL dans le terminal (ici `http://127.0.0.1:5000`).

Vous pouvez aussi faire vos requetes vers l'API directement depuis votre terminal. Avec `curl` :
```sh
curl -X POST {URL_ROOT}/search [-F text={SEARCHED_TEXT}] [-F file=@{FILE_PATH}] [-F maxRes={MAX_RESULT_NUMBER}]
```
- `URL_ROOT`: l'URL dans le terminal.
- `SEARCHED_TEXT` (optionnel): le texte avec lequel vous souhaitez chercher.
- `FILE_PATH` (optionnel): l'image avec laquelle vous souhaitez chercher.
- `MAX_RESULT_NUMBER` (optionnel): le nombre maximal de résultats que vous souhaitez récuperer.

Par exemple :
```sh
curl -X POST http://127.0.0.1:5000/search -F text="Un bateau qui navigue" -F file=@Photo.jpg -F maxRes=150
```

## Contribution

| partie                                | temano.frogier | paul.galand | melanie.tcheou |
| ------------------------------------- |:--------------:|:-----------:|:--------------:|
| CBIR \| Recherche avec image (Modèle) |        X       |             |        X       |
| CBIR \| Recherche avec image (Reduce) |        X       |             |                |
| TBIR \| Recherche avec texte          |        X       |      X      |                |
| API (et WebApp)                       |                |      X      |       X        |