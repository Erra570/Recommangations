###
# Queries graphql testées dans le sandbox https://studio.apollographql.com/sandbox/explorer
#
###

QUERY_USER_ID = """
query ($username: String) {
  User(name: $username) {
    id
    name
  }
}
"""

# Récupère la liste des medias favoris de l'user (en Ids)
QUERY_USER_GET_FAVORITES = """
query User($userId: Int) {
  User(id: $userId) {
    favourites {
      manga {
        nodes {
          id
        }
      }
      anime {
        nodes {
          id
        }
      }
    }
  }
}
"""

# Récupère les Oeuvres (tout types) enregistrés sur le profile de l'User, avec : 
# id oeuvre 
# note de l'user sur l'oeuvre
# nb chapitres lus
# statut de l'oeuvre (dropped, paused, etc)
# dates ( lastUpdate, finished date, start date )
# nb de repeats
QUERY_USER_GET_ENTRIES = """
query UserMediaList(
  $userId: Int,
  $type: MediaType
) {
  MediaListCollection(userId: $userId, type: $type) {
    lists {
      entries {
        media {
          id
        }
        score
        progress
        status
        repeat
        updatedAt
        completedAt {
          month
          year
          day
        }
        startedAt {
          month
          year
          day
        }
      }
    }
  }
}
"""







# Pas sûr qu'ils soient utilisés : 
# TODO : maybe delete

QUERY_LIST_ANIME = """
query($page: Int) {
  Page(page: $page, perPage: 50) {
    pageInfo {
      total
      currentPage
      lastPage
      hasNextPage
    }
    media(type: ANIME, sort: UPDATED_AT_DESC, status_not: NOT_YET_RELEASED) {
      id
      title {
				romaji
        english
      }
      countryOfOrigin
      format
      startDate {
        day
        month
        year
      }
      stats {
        scoreDistribution {
          score
          amount
        }
        statusDistribution {
          status
          amount
        }
      }
      status
      tags {
        id
        rank
      }
      favourites
      staff(sort: RELEVANCE) {
        nodes {
          id
        }
        edges {
          role
        }
      }
      updatedAt
      genres
      studios(isMain: true) {
        nodes {
          id
        }
      }
      episodes
      coverImage {
        large
      }
      isAdult
    }
  }
}
"""

QUERY_LIST_MANGA = """
query($page: Int) {
  Page(page: $page, perPage: 50) {
    pageInfo {
      total
      currentPage
      lastPage
      hasNextPage
    }
    media(type: MANGA, sort: UPDATED_AT_DESC, status_not: NOT_YET_RELEASED) {
      id
      chapters
      title {
	      romaji
        english
      }
      countryOfOrigin
      format
      startDate {
        day
        month
        year
      }
      stats {
        scoreDistribution {
          score
          amount
        }
        statusDistribution {
          status
          amount
        }
      }
      status
      tags {
        id
        rank
      }
      favourites
      staff(sort: RELEVANCE) {
        nodes {
          id
        }
        edges {
          role
        }
      }
      genres
      updatedAt
      coverImage {
        large
      }
      isAdult
    }
  }
}
"""