# RecoMangaTions
Projet DevOps / Algorithme de recommandation d'animes et de mangas
## Lauch project : 
```
docker compose up --build -d
docker compose exec api alembic -c alembic.ini upgrade head
```
Download database 
```
docker compose exec db pg_dump -U api -d db_anilist> db_anilist.sql
```
Upload database 
```
???
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
