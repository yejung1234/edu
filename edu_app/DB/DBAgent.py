'''
    DBAgent.py
'''
import sqlite3
import json

class DBA:
    agent = None
    list_splitter = '<SPLIT>'
    
    @classmethod
    def initialize(cls, path):
        print(path)
        if DBA.agent is not None:
            return DBA.agent
        return DBA(path)
        
    def __init__(self, path):
        self.connection = sqlite3.connect(path)
        self.cursor = self.connection.cursor()
        self.cursor.execute('pragma foreign_keys=on')
        self.cursor.execute('select * from sqlite_master')
        if len(self.cursor.fetchall()) == 0:
            self.cursor.execute('''
            create table category (
            idx int unique,
            name text unique,
            primary key(idx)
            )
            ''')
            self.cursor.execute('''
            create table problem (
            idx int unique,
            name text unique,
            category_idx int,
            title text,
            choice text,
            picture text,
            answer int,
            primary key(idx),
            foreign key(category_idx) references category(idx) on delete restrict
            )
            ''')
        
    def get_prob(self, prob_num=None, prob_source=None):
        if prob_num is None and prob_source is None:
            raise Exception('Problem index or name not described')
        elif prob_num is not None:
            query = 'idx = {}'.format(str(prob_num))
        else:
            query = 'name = {}'.format(prob_source)
        self.cursor.execute('''
        select idx, name, title, choice, picture, answer, category_idx, category_name
        from problem, (
        select idx as category_idx, name as category_name
        from category
        )
        where {}
        '''.format(query))
        result = self.cursor.fetchone()
        prob_choice = {
            'num':result[0],
            'source':result[1],
            'category':result[6],
            'title':result[2],
            'choices':[part for part in result[3].split(DBA.list_splitter)],
            'picture':[part for part in result[4].split(DBA.list_splitter)],
            'answer':result[5]
        }
        category = {
            'num':result[6],
            'category':result[7]
        }
        json_prob_choice = json.dumps(prob_choice)
        json_category = json.dumps(category)
        
        return json_category, json_prob_choice
    
    #해야함
    def add_prob(self, json_prob):
        pass
    
