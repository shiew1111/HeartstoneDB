import sqlite3
from sqlite3 import Error

import os.path


class SqlLine:
    def __init__(self, sort_by=None, filter_by=None, columns=None, sort_way='asc', delete=None):
        self.delete = delete
        self.sort_way = sort_way
        self.columns = columns
        self.filter_by = filter_by
        self.sort_by = sort_by

    def sqlSelect(self):
        if not self.filter_by:
            sql_select = """SELECT """ + self.columns + """ FROM Cards ORDER BY """ + self.sort_by + """ """ + self.sort_way + """; """
        else:
            sql_select = """SELECT """ + self.columns + """ FROM Cards where """ + self.sort_by + """ ORDER BY """ + self.sort_by + """ """ + self.sort_way + """;"""
        return str(sql_select)

    def sqlDelete(self):
        sql_delete = """DELETE FROM Cards WHERE cardId=""" + self.delete + """;"""
        return sql_delete


class DataBase:

    def __init__(self, attributes_dict='none', db_file="CardDatabase.sqlite"):
        self.attributes_dict = attributes_dict
        self.creating_new_db = False
        self.db_file = db_file
        if type(self.attributes_dict) == dict:
            self.attributes_tuple = (
                self.attributes_dict["cardId"], self.attributes_dict["name"], self.attributes_dict["cardSet"],
                self.attributes_dict["type"],
                self.attributes_dict["faction"], self.attributes_dict["rarity"], self.attributes_dict["cost"],
                self.attributes_dict["attack"],
                self.attributes_dict["health"], self.attributes_dict["Phrase"], self.attributes_dict["artist"],
                self.attributes_dict["collectible"],
                self.attributes_dict["ISelite"], self.attributes_dict["race"])
        # check if database exists, if not create new, empty with table
        if not os.path.isfile('CardDatabase.sqlite'):
            self.creating_new_db = True
            self.createConnection()

    def update(self, update_cardId):
        sql_update = """UPDATE Cards SET cardId=?,name=?,cardSet=?,type=?,faction=?,rarity=?,cost=?,attack=?,health=?,
        Phrase=?,artist=?,collectible=?,ISelite=?,race=? WHERE cardId= """ + update_cardId + """;"""
        conn = self.createConnection()
        if conn is not None:

            self.execSql(conn, sql_update, self.attributes_tuple)
        else:
            print("Error! cannot create the database connection.")

    def delete(self, delete):
        conn = self.createConnection()
        if conn is not None:
            sql_delete = self.execSql(conn, delete)
            return sql_delete
        else:
            print("Error! cannot create the database connection.")

    def insert(self):

        sql_insert = """insert into Cards (cardId,name,cardSet,type,faction,rarity,cost,attack,health,Phrase,artist,
        collectible,ISelite,race) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?  ); """
        conn = self.createConnection()
        if conn is not None:

            self.execSql(conn, sql_insert, self.attributes_tuple)
        else:
            print("Error! cannot create the database connection.")

    def select(self, sql_select):
        conn = self.createConnection()
        if conn is not None:
            select = self.execSql(conn, sql_select)
            return select
        else:
            print("Error! cannot create the database connection.")

    # method that create Database with table Cards or just create connection
    def createConnection(self):
        conn = None
        try:
            conn = sqlite3.connect(self.db_file)
            print(sqlite3.version)

            if self.creating_new_db:
                sql_create_table = """
                CREATE TABLE IF NOT EXISTS Cards (
                cardId text PRIMARY KEY,
                name text NOT NULL,
                cardSet text,
                type text,
                faction text,
                rarity text,
                cost integer,
                attack integer,
                health integer,
                Phrase text,
                artist text,
                collectible text,
                ISelite text,
                race text);
                """

                if conn is not None:

                    self.execSql(conn, sql_create_table)
                else:
                    print("Error! cannot create the database connection.")
        except Error as e:
            print(e)

        return conn

    # that method "takes" sql code and execute it
    @staticmethod
    def execSql(conn, sqlcode, *args):
        try:
            c = conn.cursor()
            c.execute(sqlcode, *args)
            conn.commit()
            rows = c.fetchall()
            return rows

        except Error as e:
            print(e)
