QUERY_USER_ID = """
query ($username: String) {
  User(name: $username) {
    id
    name
  }
}
"""

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