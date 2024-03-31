import psycopg2


def connect():
    return psycopg2.connect(host='localhost',
                            port=5432,
                            database='project',
                            user='postgres',
                            password='system')
