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