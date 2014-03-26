#!/usr/bin/env python
# -*- coding: utf-8 -*
import subprocess
import yaml
import pycurl
import sys

def curlRequest(url):
    class ContentCallback:
         def __init__(self):
            self.contents = ''
         def content_callback(self, buf):
            self.contents = self.contents + buf

    t = ContentCallback()
    try:
        info = pycurl.Curl()
        info.setopt(info.URL, url)
        info.setopt(info.WRITEFUNCTION, t.content_callback)
        info.perform()
        info.close()
    except ValueError:
        print "Error: %s - not found" %url
    return yaml.load(t.contents)


def chooseCluster():
    clusters = curlRequest('http://127.0.0.1:8000/api/v1/clusters/')
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

def getClusterInfo(id = 4):

    clusters = curlRequest('http://127.0.0.1:8000/api/v1/clusters/')
    attributes = curlRequest('http://127.0.0.1:8000/api/v1/clusters/%d/attributes/' % id)
    #print yaml.safe_dump(attributes)
    try:
        cluster_attributes = attributes['editable']
    except:
        print "Incorect cluster date"
        sys.exit(1)

    return (id, cluster_attributes)

def main():
    id = chooseCluster()
    id, cluster = getClusterInfo(id)
    try:
        passwd = raw_input("Enter admin password ")
    except:
        print "Error"
        sys.exit(1)
    cluster['access']['password']['value'] = passwd
    set_cluster_data = ''' sudo -u postgres -H -- psql -d nailgun -c \"update attributes set editable = %s where id = %d;\" ''' % ('"' + str(cluster) + '"', id)

    print set_cluster_data
#    cluster_data = subprocess.Popen(set_cluster_data, shell=True, stdout=subprocess.PIPE)
#    print yaml.safe_dump(cluster)


if __name__ == "__main__":
    main()
