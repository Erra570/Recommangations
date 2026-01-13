# RecoMangaTions
Projet DevOps / Algorithme de recommandation d'animes et de mangas
##Requetes GraphQL
```
query ($id: Int) {
  MediaListCollection(userId: $id, type: MANGA, status_in: [COMPLETED], sort: SCORE_DESC) {
    lists {
      entries {
        score
        progress
        media {
          id
          chapters
          episodes
          averageScore
          meanScore
          title {
            english
          }
          genres
          tags {
            name
            rank
            isMediaSpoiler
          }
        }
      }
    }
  }
}
```
```
query ($name: String) {
	User (name: $name) {
		id
		statistics {
			manga {
				tags (sort: COUNT_DESC){
					chaptersRead
					count
					tag{
						name
						description
					}
				}
			}
		}
	}
}
```
