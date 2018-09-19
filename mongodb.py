from pymongo import MongoClient
import pymongo
import urllib.parse
from datetime import datetime 
import pandas as pd
import os

# db setting
host = os.environ['DB_host']
port = os.environ['DB_port']
username = urllib.parse.quote_plus(os.environ['DB_username'])
password = urllib.parse.quote_plus(os.environ['DB_password'])
# Authentication Database
Authdb='hgbox'

def init_db():
    client = MongoClient('mongodb://%s:%s@%s:%s/%s?authMechanism=SCRAM-SHA-1'
                      % (username, password, host, port, Authdb))
    dbname='hgbox'
    db = client[dbname]
    return db


def insert_one(dic,collection):
    #collection_name = 'users'
    db = init_db()
    coll = db[collection]
    coll.insert_one(dic)

def upsert_one(dic,collection):
    #collection_name = 'users'
    db = init_db()
    coll = db[collection]
    coll.update(dic,{upsert:1})
    

def get_all(collection):
    db = init_db()
    coll = db[collection]
    return list(coll.find())

def find_user(userid,collection):
    db = init_db()
    coll = db[collection]
    return len(list(coll.find({"userid":userid})))

def get_all_userid(collection):
    db = init_db()
    coll = db[collection]
    unsers = list(coll.find())
    
    id_list = []
    for user in unsers:
        id_list.append(user['userid'])
    
    return id_list


def get_ready(userid,collection):
    db = init_db()
    coll = db[collection]
    unserinfo = list(coll.find({"userid":userid}))
    return unserinfo[0]['ready']

def update_byid(userid,setdict,collection):
    db = init_db()
    coll = db[collection]
    coll.update({"userid":userid},{"$set":setdict}) 

def get_user_product(userid,collection):
    db = init_db()
    coll = db[collection]
    user_info = list(coll.find({"userid":userid,"status":0}))

    product_list = []
    for item in user_info:
        product_list.append([item['product'],item['count']])
    return product_list

#def update_user_product(userid,collection):
#    db = init_db()
#    coll = db[collection]

