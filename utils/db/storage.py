# import the PostgreSQL adapter for Python

import psycopg2

      
class DatabaseManager(object):
    def __init__(self, DB_URI):
        #self.conn = lite.connect(path)
        self.conn = psycopg2.connect(DB_URI, sslmode='require')
        self.cur = self.conn.cursor()
    # Connect to the PostgreSQL database server

    def create_tables(self):
        self.query('CREATE TABLE IF NOT EXISTS products (idx SERIAL, title varchar(256), body varchar(256), photo BYTEA, price INTEGER NOT NULL, tag varchar(256));')
        self.query('CREATE TABLE IF NOT EXISTS orders (id SERIAL, cid INTEGER, usr_name varchar(256), usr_address varchar(256), usr_street varchar(256), usr_phone varchar(256), is_active INTEGER);')
        self.query('CREATE TABLE IF NOT EXISTS cart (idx INTEGER, cid INTEGER, quantity INTEGER);')
        self.query('CREATE TABLE IF NOT EXISTS categories (idx SERIAL, title varchar(256));')
        self.query('CREATE TABLE IF NOT EXISTS orders_and_products (id SERIAL, order_id INTEGER, product_id INTEGER, product_count INTEGER)')
    def query(self, arg, values=None):
        if values == None:
            self.cur.execute(arg)
        else:
            self.cur.execute(arg, values)
        self.conn.commit()

    def fetchone(self, arg, values=None):
        if values == None:
            self.cur.execute(arg)
        else:
            self.cur.execute(arg, values)
        return self.cur.fetchone()

    def fetchall(self, arg, values=None):
        if values == None:
            self.cur.execute(arg)
        else:
            self.cur.execute(arg, values)
        return self.cur.fetchall()

    def __del__(self):
        self.conn.close()
