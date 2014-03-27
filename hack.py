#!/usr/bin/env python
# -*- coding: utf-8 -*
import subprocess
import sys
import httplib
import urllib2

#from nailgun.db.sqlalchemy.models import cluster
from nailgun.api.models import cluster
from nailgun.db import db
#from nailgun import utils as hlp
import json

def chooseCluster():
    json_clusters = urllib2.urlopen('http://127.0.0.1:8000/api/v1/clusters/').read()
    clusters = json.loads(json_clusters)
    print "You have get %d clusters:" % len(clusters)
    print "ID\t| name \t| mode \t| network type \t"
    for i in clusters:
        print i['id'], "\t",  i['name'], "\t", i['mode'], "\t", i['net_provider']

    try:
        env_id = int(raw_input("Enter environment ID: "))
        return env_id
    except ValueError:
        print "ID is not number"
        sys.exit(1)

def getClusterInfo(id):

    json_attributes = json.loads(urllib2.urlopen('http://127.0.0.1:8000/api/v1/clusters/%d/attributes/' % id).read())
    #try:
    #    cluster_attributes = json_attributes['editable']
    #except:
    #    print "Incorect cluster date"
    #    sys.exit(1)

    return (id, json_attributes)
    
def load_data(id, data):
    try:
        db().query(cluster.Attributes).filter_by(cluster_id=int(id)).update(data)
        db().commit()
    except:
        db().rollback()

        raise

def main():
    id = chooseCluster()
    id, cluster = getClusterInfo(id)
    try:
        passwd = raw_input("Enter admin password ")
    except:
        print "Error"
        sys.exit(1)
    cluster['editable']['access']['password']['value'] = passwd
    load_data(id, cluster)

if __name__ == "__main__":
    main()
