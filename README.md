# RecoMangaTions
Projet DevOps / Algorithme de recommandation d'animes et de mangas

## Lauch project : 
```
cp -R mlflow_outputs/ api/
docker compose up --build -d
docker compose exec -T db pg_restore -U api -d db_anilist --clean --if-exists < backups/db_anilist.dump
```

## Model retrain
```
export DATABASE_URL=postgresql+psycopg://api:api@localhost:5432/db_anilist
python3 mlflow/logistic_regression.py --media MANGA
python3 mlflow/logistic_regression.py --media ANIME
```

## Database interaction
Download database 
```
docker compose exec db pg_dump -U api -d db_anilist -Fc > backups/db_anilist.dump
```
Upload database 
```
docker compose exec -T db pg_restore -U api -d db_anilist --clean --if-exists < backups/db_anilist.dump
```
Interact with database 
```
docker compose exec db psql -U api -d db_anilist
```
En cas de changement de la structure de la base de donnée dans le code :
```
docker compose exec api alembic -c alembic.ini revision --autogenerate -m "description_de_votre_migration"
docker compose exec api alembic -c alembic.ini upgrade head
```

## Dashboard Grafana : 
Pour afficher le dashboard Grafana, rendez vous sur http://localhost:3002
Puis dans Dashboard -> New -> Import, déposez le fichier grafana/GrafanaDashboard_RecoMangaTion.json

## To do 
- store already recommended animes/mangas 
- merge the differents season of the same anime together
- do differents sections
- have an https domain for the back-end to be able to link it to the github-pages front