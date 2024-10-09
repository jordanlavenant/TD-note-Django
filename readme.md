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

```
pip install -r requirements.txt
```

## Migration

```
cd GestionProduit
python3 manage.py migrate
```

## Features


http://127.0.0.1/app/products
http://127.0.0.1/app/providers

Fournisseur défini une marge (taux)
la production (de produits) initialise un prix de base
Le prix affiché est le prix de base * la marge

