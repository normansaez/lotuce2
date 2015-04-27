#!/usr/bin/env python

import cPickle as pickle
import pymongo
client = pymongo.MongoClient()
db = client.lotuce2
#db.profiles.count()
one = db.profiles.find_one(sort=[("timestamp", 1 )])
#mongo = pymongo.MongoClient()
#collection = mongo['lotuce2']['profiles']
#collection.ensure_index('timestamp')
#last = db.profiles.find_one(sort=[("timestamp", -1 )])
y = pickle.loads( one['profile'] )
print y.max()
print y.min()
