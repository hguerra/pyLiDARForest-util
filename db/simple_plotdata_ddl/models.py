import peewee
from playhouse.postgres_ext import PostgresqlExtDatabase

psql_db = PostgresqlExtDatabase('simple_plotdata', user='eba', password='ebaeba18')


class Family(peewee.Model):
    """
    ORM model of the Family table
    """
    name = peewee.CharField()

    class Meta:
        database = psql_db


if __name__ == '__main__':
    for art in Family.select():
        print(art.name)
