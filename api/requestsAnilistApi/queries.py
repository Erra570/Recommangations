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

QUERY_USER_LIST_ANIME = """
query ($page: Int, $perPage: Int, $sort: [MediaSort]) {
  Page(page: $page, perPage: $perPage) {
    pageInfo {
      currentPage
      hasNextPage
    }
    media(type: ANIME, sort: $sort) {
      id

      averageScore
      favourites
      episodes
      format
      countryOfOrigin
      status

      startDate {
        day
        month
        year
      }

      genres

      tags {
        id
        rank
      }

      studios(isMain: true) {
        nodes {
          id
        }
      }

      staff(sort: RELEVANCE, perPage: 5) {
        nodes {
          id
        }
        edges {
          role
        }
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

      title {
        romaji
        english
      }
    }
  }
}
"""

QUERY_USER_LIST_MANGA = """
query ($page: Int, $perPage: Int, $sort: [MediaSort]) {
  Page(page: $page, perPage: $perPage) {
    pageInfo {
      currentPage
      hasNextPage
    }
    media(type: MANGA, sort: $sort) {
      id

      averageScore
      chapters
      volumes
      countryOfOrigin
      format
      status
      favourites

      startDate {
        day
        month
        year
      }

      genres

      tags {
        id
        rank
      }

      staff(sort: RELEVANCE, perPage: 5) {
        nodes {
          id
        }
        edges {
          role
        }
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

      title {
        romaji
        english
      }
    }
  }
}
"""