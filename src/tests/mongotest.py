#!/usr/bin/env python

import cPickle as pickle
import pymongo
import datetime
from bson.objectid import ObjectId
import time

if __name__ == '__main__':
    client = pymongo.MongoClient()
    db = client.lotuce2
    #
    # Creating index
    #
    # db.profiles.ensure_index('timestamp')
    # db.centroid.ensure_index('timestamp')
    # db.cov.ensure_index('timestamp')
#mongo modifications

#    one = db.profiles.find_one(sort=[("timestamp", 1 )])
#    last = db.profiles.find_one(sort=[("timestamp", -1 )])
    #y = pickle.loads( one['profile'] )
    #print y.max()
    #print y.min()
#    ts0 = datetime.datetime.fromtimestamp(one['timestamp'])
#    ts1 = datetime.datetime.fromtimestamp(last['timestamp'])
#    print ts0
#    print ts1

#    sec = 15*60
#    gen_time = datetime.datetime.today() - datetime.timedelta(sec=sec) 
#    gen_time =  datetime.datetime.today() - datetime.timedelta(seconds=sec)#ts1 - datetime.timedelta(seconds=sec) 
#    print gen_time
#    ttt = time.mktime(gen_time.timetuple())
#    result = list(db.profiles.find({"timestamp": {"$gte": ttt}}))
#print result[0]
#    centro = db.centroid.find_one(sort=[('timestamp',1)])
#    print centro
#    ftime = time.mktime(datetime.datetime.today().timetuple())
#    data = []
#    data.append(pickle.loads(centro["x0"])) 
#    data.append(pickle.loads(centro["y0"]))
#    data.append(pickle.loads(centro["x1"]))
#    data.append(pickle.loads(centro["y1"]))
#    data.append(pickle.loads(centro["x2"]))
#    data.append(pickle.loads(centro["y2"]))
#    data.append(pickle.loads(centro["x3"]))
#    data.append(pickle.loads(centro["y3"]))
#    db.centroid.insert({"timestamp":ftime,"x0":float(data[0]) 
#                                         ,"y0":float(data[1])  
#                                         ,"x1":float(data[2])
#                                         ,"y1":float(data[3])
#                                         ,"x2":float(data[4])
#                                         ,"y2":float(data[5])
#                                         ,"x3":float(data[6])
#                                         ,"y3":float(data[7])})
    print db.centroid.find_one(sort=[("timestamp", -1 )])
     
