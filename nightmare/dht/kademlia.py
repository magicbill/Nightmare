"""
Classes and methods for the Kademlia DHT protocol.
"""
from datetime import datetime as dt
from uuid import uuid4
from hashlib import sha1

class ContactInfo(object):
    """
    Class that holds the contact information for a node in the Kademlia
    network. Instances of this class are stored in the k-buckets.
    """

    def __init__(self, ip, port, node_id, last_seen):
        """
        init for a node in a k-bucket.
        """
        self.ip = ip
        self.port = port
        self.node_id = node_id
        self.last_seen = last_seen
        
    def __eq__(self, other):
        return self.node_id == other.node_id
    
    def __ne__(self, other):
        return self.node_id != other.node_id
    
    def __lt__(self, other):
        return self.last_seen < other.last_seen
    
    def __gt__(self, other):
        return self.last_seen > other.last_seen
    
    def __ge__(self, other):
        return self.last_seen >= other.last_seen

    def __le__(self, other):
        return self.last_seen <= other.last_seen
        
    def __str__(self):
        message = 'node<%s>@%s:%d last_seen: %s' 
        return message % (self.node_id, self.ip, self.port, self.last_seen)
    
    def __repr__(self):
        return str(self.__dict__)


class KBucket(object):
    """
    Class to handle k-buckets.
    """
    
    def __init__(self, k=20):
        """
        k --- The number of nodes to store in each KBucket defaults to 20
        """
        self.k = k
        self.buckets = [list() for i in xrange(160)]
        
    def store_node(self, node, distance):
        """
        @param node: The ContactInfo of the node to store in a k-bucket  
        @param distance: The integer XOR of the node's id with the node this KBucket belongs to
        """
        i = self._find_bucket_index(distance)
        to_update = [x for x in self.buckets[i] if x == node]
        if to_update:
            assert(len(to_update) == 1)
            to_update[0].last_seen = dt.now()
        else:                    
            if len(self.buckets[i]) < self.k:                    
                self.buckets[i].append(node) 
            else:
                #need to ping oldest node and if it doesn't respond replace it and if it does drop new contact
                pass                   
        self.buckets[i].sort() 
            
    def _find_bucket_index(self, distance):
        """
        Finds the index of the bucket a node at distance belongs in
        distance --- The integer XOR of the node's id with the node this KBucket belongs to
        """
        for i in xrange(160):
            lower_bound = 2**i
            upper_bound = 2**(i+1)
            if distance >= lower_bound and distance < upper_bound:
                return i
        raise Exception("Did not find kbucket for distance %d" % distance)  
        
class Kademlia(object):
    
    def __init__(self):
        random_uuid = uuid4()
        sha = sha1()
        sha.update(random_uuid.hex)
        self.node_id = sha.hexdigest()
    
    def find_node(self, requestor_info, node_id):
        print 'someone called find node with %s' % node_id
        
    def find_value(self, requestor_info, key):
        print 'find_value key:%s' % key
    
    def ping(self, requestor_info):
        print 'ping'
        
    def store(self, requestor_info, key, value):
        print 'store key:%s value:%s' % (key, value)
                
