# TP-Noté Django

_COURSIMAULT Irvyn - LAVENANT Jordan_

## Virtual Environment

### Activate
```
python -m venv venv
source ~/venv/bin/activate
```

### Deactivate
```
deactivate
```


## Installation 

### Serveur
Installation des dépendances
```
pip install -r requirements.txt
```

Installation de bootstrap
```
cd GestionProduit/app/static/
npm install
```

## Migration
Depuis la racine du projet, effectuez :
```
cd GestionProduit
python3 manage.py makemigrations
python3 manage.py migrate
```

## Seed

Pour ajouter un jeu de données dans la base de données, effectuez ces commandes depuis la racine du projet : 
```
cd GestionProduit
python3 manage.py loaddata seed.json
```
Le jeu de données est disponible dans le fichier `seed.json`, il contient 26 objets, issus des différentes tables du modèle.

## Start server

Pour lancer le serveur (projet principal), effectuez depuis la racine du projet : 
```
cd GestionProduit
python3 manage.py runserver
```
Et rendez-vous sur [http://127.0.0.1:8000/app/](http://127.0.0.1:8000/app/)

## Start client

Pour lancer un client, relié à l'api, effectyez depuis la racine du projet :

```
cd client
flask run
```
Et rendez-vous sur [http://127.0.0.1:5000/](http://127.0.0.1:5000/)

## Admin

Le superuser est `admin` et son mot de passe est `admin`. Il est crée automatique lors du `loaddata`.

Pour accéder à l'interface d'administration, rendez-vous sur [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)

## Features

### Interface

Cette interface est une application de gestion de produits, de fournisseurs, de stocks et de commandes. Il peut être destiné à une enseigne de grande distribution, ou à une entreprise de e-commerce.

#### Produits

- Visualisation des produits
- Visualisation d'un produit et ses fournisseurs associés
- Ajout de produits
- Modification de produits
- Suppression de produits
- Recherche de produits par nom
- Consultation des produits sur un **client web** par l'api

#### Fournisseurs

- Visualisation des fournisseurs
- Visualisation d'un fournisseur et ses produits associés
- Ajout de fournisseurs
- Modification de fournisseurs
- Suppression de fournisseurs
- Recherche de fournisseurs par nom

#### Stocks

- Visualisation des stocks
- Visualisation d'un stock, sa quantité et sa marge
- Ajout de stocks
- Modification de stocks
- Suppression de stocks
- Recherche de stocks par nom de produit et/ou fournisseur

#### Commandes

- Visualisation des commandes (passées et en cours)
- Visualisation d'une commande, son produit associé, sa quantité, sa date et son statut
- Ajout de commandes
- Modification de commandes
- Suppression de commandes
- Recherche de commandes par nom de produit et/ou fournisseur

#### Permissions

- Chaques actions CUD (Create, Update, Delete), nécessitent d'être login à l'application. Chaques boutons relatifs à ces actions vous redirigeront vers la page de login (Les identifiants étant `admin` et `admin`).

## Work in progress

Parmi les features en cours, en voici quelques-unes : 


- Ajout d'une `order` dans l'interface client qui représenterait une entité de panier (Produit, fournisseur associé, quantité).
- Gestion d'un panier qui contiendrait des `orders`.
- Gestion du panier, qui décrémenterait la quantité du stock concerné par les `orders`, et vérifications de la validation du panier.
- Ces features auraient nécessités une connexion d'utilisateur sur l'interface client, pour associer un panier à un utilisateur.

## API

Les routes du modèle sont disponibles dans l'API, et sont accessibles en lecture seule (pour des raisons de sécurité).

### Routes 

- `GET /api/products/` : Récupère tous les produits
- `GET /api/products/<int:id>` : Récupère un produit par son id
- `GET /api/products/?name=<string:product_name>` : Récupère un produit par son id
- `GET /api/providers/` : Récupère toutes les catégories
- `GET /api/providers/<int:id>` : Récupère une catégorie par son id
- `GET /api/stock/` : Récupère tous les stocks
- `GET /api/stock/<int:id>` : Récupère un stock par son id
- `GET /api/stock/?product=<int:product_id}` : Récupère tous les stocks d'un produit spécifique
- `GET /api/stock/?provider=<int:provider_id>` : Récupère tous les stocks d'un fournisseur spécifique
- `GET /api/commands/` : Récupère toutes les commandes
- `GET /api/commands/<int:id>` : Récupère une commande par son id
- `GET /api/orders/` : Récupère toutes les entités d'un panier d'un client
- `GET /api/carts/` : Récupère tous les paniers
- `GET /api/carts/?user=<int:user_id>` : Récupère tous les paniers

Exemple d'utilisation : 

```bash
curl -X GET http://localhost:8000/api/products/
```
```json
[{"id":1,"name":"iPhone 16","price_ht":"1700.00","status":0,"date_creation":"2024-10-15T00:08:16+02:00"},{"id":2,"name":"iPhone 11","price_ht":"400.00","status":0,"date_creation":"2024-10-15T00:10:32+02:00"},{"id":3,"name":"Dell XPS 17","price_ht":"1700.00","status":0,"date_creation":"2024-10-15T00:10:32+02:00"}]
```

Ou encore : 

```bash
curl -X GET http://localhost:8000/api/products/1
```
```json
{"id":1,"name":"iPhone 16","price_ht":"1700.00","status":0,"date_creation":"2024-10-15T00:08:16+02:00"}
```

Enfin, l'api supporte la recherche par nom, par exemple : 

```bash
curl -X GET http://localhost:8000/api/products/?name=xps
```
```json
[{"id":3,"name":"Dell XPS 17","price_ht":"1700.00","status":0,"date_creation":"2024-10-15T00:10:32+02:00"}]
```

Pour accéder à l'interface de l'API, rendez-vous sur [http://127.0.0.1:8000/api/](http://127.0.0.1:8000/api/)

## Tests unitaires

On se rend dans le projet :
```
cd GestionProduit
```

### Model
Pour lancer les tests unitaires du `Model`, effectuez :
```
python3 manage.py test app.tests.Model
```

### Url
Pour lancer les tests unitaires des `Url`, effectuez :
```
python3 manage.py test app.tests.Url
```

### Views
Pour lancer les tests unitaires des `Views`, effectuez :
```
python3 manage.py test app.tests.View
```

### Forms
Pour lancer les tests unitaires des `Form`, effectuez :
```
python3 manage.py test app.tests.Form
```

## Coverage

On se rend dans le projet :
```
cd GestionProduit
```

Pour lancer le coverage, effectuez :
```
coverage run --source=app manage.py test app/tests
coverage report
```
