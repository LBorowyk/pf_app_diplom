import sqlite3
import os

class DBConnection:
    def __init__(self, dbfilename):
        self.dbfilename = dbfilename

    def dict_factory(self, cursor, row):
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return d

    def dboperation(function_to_decorate):
        def the_wrapper_around_the_original_function(self, *args, **kwargs):
            self.dbconn = sqlite3.connect(self.dbfilename)
            self.dbconn.row_factory = self.dict_factory
            self.dbcursor = self.dbconn.cursor()
            result = function_to_decorate(self, *args, **kwargs)
            self.dbconn.close()
            return result
        return the_wrapper_around_the_original_function

    @dboperation
    def select(self, tables, columns, where, order):
        sql = f''' 
        select 
            {', '.join(columns)} 
        from 
            {', '.join(tables)}
        { f' where {where}' if where else '' } 
        { f' order by {", ".join(order)}' if order else ''} 
        '''
        print(sql)
        self.dbcursor.execute(sql)
        return self.dbcursor.fetchall()

    @dboperation
    def onlyinsert(self, table, values):
        sql = f''' 
            insert 
            into {table} 
                ({', '.join(values.keys())}) 
            values 
                ({', '.join(list(map(lambda v: f'"{v}"' , values.values())))})
        '''
        print('sql', sql)
        self.dbcursor.execute(sql)
        self.dbconn.commit()
        
    def insert(self, table, values):
        self.onlyinsert(table, values)
        return self.select([table], ['*'], '', '')

    @dboperation
    def execute(self, sql):
        self.dbcursor.execute(sql)