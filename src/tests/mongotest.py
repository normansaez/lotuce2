#!/usr/bin/env python

import cPickle as pickle
import pymongo
import datetime
from bson.objectid import ObjectId
import time

if __name__ == '__main__':
    client = pymongo.MongoClient()
    db = client.lotuce2
    #db.profiles.count()
    one = db.profiles.find_one(sort=[("timestamp", 1 )])
    #mongo = pymongo.MongoClient()
    #collection = mongo['lotuce2']['profiles']
    #collection.ensure_index('timestamp')
    last = db.profiles.find_one(sort=[("timestamp", -1 )])
    #y = pickle.loads( one['profile'] )
    #print y.max()
    #print y.min()
    
    ts0 = datetime.datetime.fromtimestamp(one['timestamp'])
    ts1 = datetime.datetime.fromtimestamp(last['timestamp'])
    print ts0
    print ts1

    sec = 15
#    gen_time = datetime.datetime.today() - datetime.timedelta(sec=sec) 
    gen_time = ts1 - datetime.timedelta(seconds=sec) 
#    dummy_id = ObjectId.from_datetime(gen_time)
    print gen_time
    ttt = time.mktime(gen_time.timetuple())
    result = list(db.profiles.find({"timestamp": {"$gte": ttt}}))
    print result[0]['timestamp']
