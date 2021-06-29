import mysql.connector as mysql
import config.config as cnf
config = cnf.Config()

def connect():
  db_connector = mysql.connect(host=config.mysql_host, user=config.mysql_user, password=config.mysql_pw, database=config.mysql_db)
  return db_connector

def connect_local():
  db_connector = mysql.connect(host=config.mysql_host_local, user=config.mysql_user, password=config.mysql_pw, database=config.mysql_db)
  return db_connector

def select_query(db_connector, query):
  db_cursor = db_connector.cursor()
  db_cursor.execute(query)
  myresult = db_cursor.fetchall()
  return myresult

def insert_query(db_connector, query):
  db_cursor = db_connector.cursor()
  db_cursor.execute(query)
  db_connector.commit()
  return db_cursor.lastrowid, 200

def insert_query_data(db_connector, query, data):
  db_cursor = db_connector.cursor()
  db_cursor.execute(query, data)
  db_connector.commit()
  return db_cursor.lastrowid, 200

def update_query_data(db_connector, query, data):
  db_cursor = db_connector.cursor()
  db_cursor.execute(query, data)
  db_connector.commit()
  return db_cursor.lastrowid, 200

def update_query(db_connector, query):
  db_cursor = db_connector.cursor()
  db_cursor.execute(query)
  db_connector.commit()
  return db_cursor.rowcount, 200

def delete_query(db_connector, query):
  db_cursor = db_connector.cursor()
  db_cursor.execute(query)
  db_connector.commit()
  return db_cursor.rowcount, 200
