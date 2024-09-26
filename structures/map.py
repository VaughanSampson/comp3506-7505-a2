"""
Skeleton for COMP3506/7505 A2, S2, 2024
The University of Queensland
Joel Mackenzie and Vladimir Morozov

Please read the following carefully. This file is used to implement a Map
class which supports efficient insertions, accesses, and deletions of
elements.

There is an Entry type defined in entry.py which *must* be used in your
map interface. The Entry is a very simple class that stores keys and values.
The special reason we make you use Entry types is because Entry extends the
Hashable class in util.py - by extending Hashable, you must implement
and use the `get_hash()` method inside Entry if you wish to use hashing to
implement your map. We *will* be assuming Entry types are used in your Map
implementation.
Note that if you opt to not use hashing, then you can simply override the
get_hash function to return -1 for example.
"""

from typing import Any
from structures.entry import Entry
from random import randint
from structures.util import hash

class Map:
    """
    An implementation of the Map ADT.
    The provided methods consume keys and values via the Entry type.
    """

    def __init__(self) -> None:
        """
        Construct the map.
        You are free to make any changes you find suitable in this function
        to initialise your map.
        """
        self._prime_index = 0
        self._primes = [5,11,17,31,59,157,269,541,1087,2131,4289,8627,17327,36109,73079,154823,309259,603791,1097897,2089273,4084931,8090651,15485863] 
        self._capacity = self._primes[self._prime_index]
        self._buckets = [None] * self._capacity
        self._count = 0
        #self._a = 2 >> randint(0,10)
        #self._b = randint(0,875)

    def get_bucket_index(self, key) -> int:
       # return (self._a * entry.get_hash() + self._b) % self._capacity
       return hash(key) % self._capacity
   
    def get_bucket_index_with_capacity(self, key, capacity) -> int:
       # return (self._a * entry.get_hash() + self._b) % self._capacity
       return hash(key) % capacity
    
    def resize(self):
        load_factor = self._count / self._capacity
        if load_factor > 0.7:
            self.grow()
        elif load_factor < 0.2 and self._prime_index > 0:
            self.shrink()
            
    def grow(self):
        
        # Find next capacity
        new_capacity = self._capacity
        self._prime_index += 1
        if self._prime_index < len(self._primes):
            new_capacity = self._primes[self._prime_index]
        else:
            new_capacity = self._capacity * 3
        
        print("Do resize to ", new_capacity)
        
        # Rehash 
        new_buckets  = [None] * new_capacity
        
        for i in self._buckets:
            if i == None:
                continue
            node = i
            while node != None: 
                next_node = node._next
                
                # rehash and insert value
                bucket_index = self.get_bucket_index_with_capacity(node._entry._key, new_capacity) 
                if new_buckets[bucket_index] == None:
                    node._next = None
                    new_buckets[bucket_index] = node  
                else:
                    node._next = new_buckets[bucket_index]
                    new_buckets[bucket_index] = node
                    
                node = next_node
        
        self._capacity = new_capacity
        self._buckets = new_buckets
        
    
    def shrink(self):
        # Find new capacity
        new_capacity = self._capacity
        self._prime_index -= 1
        if self._prime_index < len(self._primes):
            new_capacity = self._primes[self._prime_index]
        else:
            new_capacity = self._capacity // 3
        
        print("Do resize to ", new_capacity)
        
        # Rehash 
        new_buckets  = [None] * new_capacity
        
        for i in self._buckets:
            if i == None:
                continue
            node = i
            while node != None: 
                next_node = node._next
                
                # rehash and insert value
                bucket_index = self.get_bucket_index_with_capacity(node._entry._key, new_capacity) 
                if new_buckets[bucket_index] == None:
                    node._next = None
                    new_buckets[bucket_index] = node  
                else:
                    node._next = new_buckets[bucket_index]
                    new_buckets[bucket_index] = node
                    
                node = next_node
        
        self._capacity = new_capacity
        self._buckets = new_buckets 
    
    def insert(self, entry: Entry) -> Any | None:
        """
        Associate value v with key k for efficient lookups. If k already exists
        in your map, you must return the old value associated with k. Return
        None otherwise. (We will not use None as a key or a value in our tests).
        Time complexity for full marks: O(1*)
        """
         
        self.resize()
        
        bucket_index = self.get_bucket_index(entry._key)
        
        node = self._buckets[bucket_index]
        if node == None:
            self._buckets[bucket_index] = BucketNode(entry)
            self._count += 1
            return None
        
        last_node = None 
        while node != None:
            if node._entry._key == entry._key: # node already exists
                old_value = node._entry._value
                node._entry._value = entry._value
                return old_value
            last_node = node
            node = node._next 
        last_node._next = BucketNode(entry) # node doesn't exist
        self._count += 1
        return None
          
        

    def insert_kv(self, key: Any, value: Any) -> Any | None:
        """
        A version of insert which takes a key and value explicitly.
        Handy if you wish to provide keys and values directly to the insert
        function. It will return the value returned by insert, so keep this
        in mind. You can modify this if you want, as long as it behaves.
        Time complexity for full marks: O(1*)
        """
        entry = Entry(key, value) 
        return self.insert(entry)

    def __setitem__(self, key: Any, value: Any) -> None:
        """
        For convenience, you may wish to use this as an alternative
        for insert as well. However, this version does _not_ return
        anything. Can be used like: my_map[some_key] = some_value
        Time complexity for full marks: O(1*)
        """
        self.insert_kv(key, value)

    def remove(self, key: Any) -> None:
        """
        Remove the key/value pair corresponding to key k from the
        data structure. Don't return anything.
        Time complexity for full marks: O(1*)
        """
        self.resize()
        
        bucket_index = self.get_bucket_index(key)
        
        node = self._buckets[bucket_index]
        if node != None:  
            if node._entry._key == key:
                self._buckets[bucket_index] = None
                self._count -= 1
                return
            else:
                last_node = node
                node = node._next 
                while node != None:
                    if node._entry._key == key:
                        last_node._next = node._next
                        self._count -= 1
                        return
                    last_node = node
                    node = node._next 

    def find(self, key: Any) -> Any | None:
        """
        Find and return the value v corresponding to key k if it
        exists; return None otherwise.
        Time complexity for full marks: O(1*)
        """
        bucket_index = self.get_bucket_index(key)
        node = self._buckets[bucket_index]
        while node != None:
            if node._entry._key == key:
                return node._entry._value
            node = node._next
        return None

    def __getitem__(self, key: Any) -> Any | None:
        """
        For convenience, you may wish to use this as an alternative
        for find()
        Time complexity for full marks: O(1*)
        """
        return self.find(key)
            

    def get_size(self) -> int:
        """
        Time complexity for full marks: O(1)
        """
        return self._count

    def is_empty(self) -> bool:
        """
        Time complexity for full marks: O(1)
        """
        return self._count == 0

class BucketNode:
    """
    A node used for a hash set bucket.
    """
    
    def __init__(self, entry: Entry) -> None:
        self._next = None
        self._entry = entry
    