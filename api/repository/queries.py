def USER_QUERY(mediatype: str):
    return """
        SELECT
          COUNT(*) AS nb,
          AVG(m.mean_score) AS mean_mean_score,
          AVG(m.variance_score) AS mean_variance_score,
          AVG(m.favourites) AS mean_favourites,
          avg(extract(epoch from start_date)) AS mean_start
        FROM user_"""+mediatype.lower()+""" um
        JOIN """+mediatype.lower()+""" m ON m.id = um."""+mediatype.lower()+"""_id
        WHERE (um.status = 'COMPLETED' OR um.status = 'CURRENT') AND (um.score = 0 OR um.score >= 7) AND user_id = :user_id
    """

def USER_MEDIA_QUERY(mediatype: str):
    return """
        SELECT """+mediatype.lower()+"""_id AS media_id
        FROM user_"""+mediatype.lower()+"""
        WHERE (status = 'COMPLETED' OR status = 'CURRENT') AND (score = 0 OR score >= 7) AND user_id = :user_id
    """

def USER_COUNTRY_OF_ORIGIN_QUERY(mediatype: str):
    return """
        SELECT
            m.country_of_origin,
            (CASE WHEN AVG(score) > 0 THEN AVG(score)/10 ELSE 0.7 END)*(COUNT(*) + SUM(favourite::int)*2 + SUM(repeat)) as nb
        FROM user_"""+mediatype.lower()+""" um
        JOIN """+mediatype.lower()+""" m ON m.id = um."""+mediatype.lower()+"""_id
        WHERE (um.status = 'COMPLETED' OR um.status = 'CURRENT') AND (um.score = 0 OR um.score >= 7) AND um.user_id = :user_id
        GROUP BY m.country_of_origin
        ORDER BY nb DESC NULLS LAST
    """

def USER_FORMAT_QUERY(mediatype: str):
    return """
        SELECT
            m.format,
            (CASE WHEN AVG(score) > 0 THEN AVG(score)/10 ELSE 0.7 END)*(COUNT(*) + SUM(favourite::int)*2 + SUM(repeat)) as nb
        FROM user_"""+mediatype.lower()+""" um
        JOIN """+mediatype.lower()+""" m ON m.id = um."""+mediatype.lower()+"""_id
        WHERE (um.status = 'COMPLETED' OR um.status = 'CURRENT') AND (um.score = 0 OR um.score >= 7) AND um.user_id = :user_id
        GROUP BY m.format
        ORDER BY nb DESC NULLS LAST
    """

def USER_GENRE_QUERY(mediatype: str):
    return """
        SELECT
            g.genre_name,
            (CASE WHEN AVG(score) > 0 THEN AVG(score)/10 ELSE 0.7 END)*(COUNT(*) + SUM(favourite::int)*2 + SUM(repeat)) as nb
        FROM user_"""+mediatype.lower()+""" um
        JOIN """+mediatype.lower()+""" m ON m.id = um."""+mediatype.lower()+"""_id
        LEFT JOIN """+mediatype.lower()+"""_genre g ON g."""+mediatype.lower()+"""_id = m.id
        WHERE (um.status = 'COMPLETED' OR um.status = 'CURRENT') AND (um.score = 0 OR um.score >= 7) AND um.user_id = :user_id
        GROUP BY g.genre_name
        ORDER BY nb DESC NULLS LAST
        LIMIT 10
    """

def USER_TAG_QUERY(mediatype: str):
    return """
        SELECT
            t.tag_id,
            (AVG(rank)/100)*(CASE WHEN AVG(score) > 0 THEN AVG(score)/10 ELSE 0.7 END)*(COUNT(*) + SUM(favourite::int)*2 + SUM(repeat)) as nb
        FROM user_"""+mediatype.lower()+""" um
        JOIN """+mediatype.lower()+""" m ON m.id = um."""+mediatype.lower()+"""_id
        LEFT JOIN """+mediatype.lower()+"""_tag t ON t."""+mediatype.lower()+"""_id = m.id
        WHERE (um.status = 'COMPLETED' OR um.status = 'CURRENT') AND (um.score = 0 OR um.score >= 7) AND um.user_id = :user_id
        GROUP BY t.tag_id
        ORDER BY nb DESC NULLS LAST
        LIMIT 25
    """

def USER_STAFF_QUERY(mediatype: str):
    return """
        SELECT
            s.staff_id,
            (CASE WHEN AVG(score) > 0 THEN AVG(score)/10 ELSE 0.7 END)*(COUNT(*) + SUM(favourite::int)*2 + SUM(repeat)) as nb
        FROM user_"""+mediatype.lower()+""" um
        JOIN """+mediatype.lower()+""" m ON m.id = um."""+mediatype.lower()+"""_id
        LEFT JOIN """+mediatype.lower()+"""_staff s ON s."""+mediatype.lower()+"""_id = m.id
        WHERE (um.status = 'COMPLETED' OR um.status = 'CURRENT') AND (um.score = 0 OR um.score >= 7) AND um.user_id = :user_id
        GROUP BY s.staff_id
        ORDER BY nb DESC NULLS LAST
        LIMIT 25
    """