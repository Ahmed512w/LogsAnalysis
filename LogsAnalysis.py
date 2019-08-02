#!/usr/bin/env python3

import psycopg2, sys

DBNAME = "news"

top_3_articles = '''
    SELECT article, count(*) AS views
    FROM   log_article_auther
    GROUP BY article
    ORDER BY views DESC
    LIMIT 3
    ;
    '''

top_authors = '''
    SELECT author, count(*) AS views
    FROM   log_article_auther
    GROUP BY author
    ORDER BY views DESC
    ;
    '''

errors_percent = '''
    SELECT day, percent
    FROM error_percent
    WHERE percent > 1
    ;
    '''

def get(query):
    try:
        db = psycopg2.connect(
            user = "postgres",
            password = "sql",
            host = "127.0.0.1",
            port = "5432",
            database = DBNAME
            )
    except psycopg2.Error as error:
        print( error )
        sys.exit()

    c = db.cursor()
    c.execute(query)
    result = c.fetchall()
    db.close()
    return result


def popular_3_articles():
    popular_3_articles = get(top_3_articles)
    print("\nMost popular three articles of all time\n")
    for title, num in popular_3_articles:
        print('''\t"{}" -- {} views'''.format(title, num))


def popular_authors():
    popular_authors = get(top_authors)
    print("\nMost popular article authors of all time:\n")
    for title, num in popular_authors:
        print('''\t"{}" -- {} views'''.format(title, num))



def high_error_day():
    high_error_day = get(errors_percent)
    print("\nDays with more than 1% of requests lead to errors:\n")
    for day, per in high_error_day:
        print('''\t{0:%B %d, %Y} -- {1:.2f} % errors'''.format(day, per))


if __name__ == '__main__':
    popular_3_articles()
    popular_authors()
    high_error_day()
