"""
COMP3506/7505 S2 2023
The University of Queensland

NOTE: This file will not be used for marking and is here to provide you with
a simple way of testing your data structures. You may edit this file by adding
your own test functionality.
"""

# Import helper libraries
import argparse
import sys
import random

# Import our new structures
from structures.entry import Entry
from structures.dynamic_array import DynamicArray
from structures.graph import Graph, LatticeGraph
from structures.map import Map
from structures.pqueue import PriorityQueue
from structures.bloom_filter import BloomFilter
from structures.util import Hashable

def test_pqueue() -> None:
    """
    A simple set of tests for the priority queue.
    This is not marked and is just here for you to test your code.
    """
    print("==== Executing Priority Queue Tests ====")
    my_pq = PriorityQueue()
    my_pq.insert(0, "highest priority item")
    my_pq.insert(10, "priority value 10 item")
    assert my_pq.get_size() == 2
    assert my_pq.remove_min() == "highest priority item"
    assert my_pq.remove_min() == "priority value 10 item"
    my_pq.insert(0, 0)
    my_pq.insert(3, 3)
    my_pq.insert(0, 0)
    my_pq.insert(2, 2)
    assert my_pq.remove_min() == 0
    assert my_pq.remove_min() == 0
    assert my_pq.remove_min() == 2
    assert my_pq.remove_min() == 3  
    my_pq.insert_fifo(3) 
    my_pq.insert_fifo(2) 
    my_pq.insert_fifo(0) 
    my_pq.insert_fifo(10) 
    my_pq.insert_fifo(11) 
    my_pq.insert_fifo(0) 
    assert my_pq.remove_min() == 3
    assert my_pq.remove_min() == 2
    assert my_pq.remove_min() == 0
    assert my_pq.remove_min() == 10 
    assert my_pq.remove_min() == 11  
    assert my_pq.remove_min() == 0
    array = []
    array.append(Entry(0,10)) 
    array.append(Entry(6,3)) 
    array.append(Entry(2,1)) 
    array.append(Entry(8,4)) 
    array.append(Entry(11,6)) 
    array.append(Entry(10,5)) 
    array.append(Entry(4,2)) 
    my_pq.ip_build(array)
    assert my_pq.remove_min() == 10
    assert my_pq.remove_min() == 1
    assert my_pq.remove_min() == 2
    assert my_pq.remove_min() == 3 
    assert my_pq.remove_min() == 4  
    assert my_pq.remove_min() == 5
    assert my_pq.remove_min() == 6
    
    array = []
    array.append(Entry(0,10)) 
    array.append(Entry(6,3)) 
    array.append(Entry(2,1)) 
    array.append(Entry(8,4)) 
    array.append(Entry(11,6)) 
    array.append(Entry(10,5)) 
    array.append(Entry(4,2)) 
    my_pq.ip_build(array)
    sorted_array = my_pq.sort()
    
    for i in range(sorted_array.get_size()):
        print(sorted_array[i].get_key())
    
    

    """
    This one is up to you - we provided most of the code already :-)
    """


def test_map() -> None:
    """
    A simple set of tests for the associative map.
    This is not marked and is just here for you to test your code.
    """
    # Seed PRNG
    # random.seed(1337)
    # print("==== Executing Map Tests ====")
    
    # e = Entry("hhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhha", 3)
    # print(e.get_hash())
    # e = Entry("hhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhb", 1)
    # print(e.get_hash())
    
    
    
    my_map = Map()

    # Make some entries
    # e1 = Entry(1, "value_for_key_1")
    # e2 = Entry(10, "value_for_key_10")
    # my_map.insert(e1)
    # my_map.insert(e2)
    # my_map.insert_kv(2, "Barry rules")
    # my_map[3] = "value_for_key_3" 
    # assert my_map.get_size() == 4
    # assert my_map[3] == "value_for_key_3"
    # assert my_map[1] == "value_for_key_1"
    # assert my_map[10] == "value_for_key_10"
    # assert my_map[2] == "Barry rules"
    # my_map.remove(3)
    # assert my_map[3] == None
    # my_map.remove(3)
    # assert my_map.get_size() == 3
    # e1 = Entry(1, "value_for_key_1")
    # e2 = Entry(10, "value_for_key_10")
    # my_map.insert(e1)
    # my_map.insert(e2)
    # my_map.insert_kv(2, "Barry rules") 
    # my_map[3] = "value_for_key_3" 
    # assert my_map.get_size() == 4
    # assert my_map[3] == "value_for_key_3"
    # assert my_map[1] == "value_for_key_1"
    # assert my_map[10] == "value_for_key_10"
    # assert my_map[2] == "Barry rules"
    
    my_map = Map() 
    for i in range(0, 1000, 1):
        my_map[i] = i
        
    for i in range(0, 1000, 1):
        assert my_map[i] == i
     
    for i in range(0, 1000, 1):
        my_map.remove(i)
    
    for i in range(0, 1000, 1):
        assert my_map[i] == None
        
    
    """
    OK, simple boring hand written tests don't really find bugs... Just
    use them to detect specific corner cases and/or unit test each individual
    function. Let's do some better testing now. Fuzz against a python dict
    to make sure your data structure works. Make sure you capture all functions
    including any resizing that is done.
    """
    


def test_bloom() -> None:
    """
    Bloom Filter tests. Not marked.
    """
    # Seed PRNG
    random.seed(1337)

    # Some parameters we might like to mess around with
    MAX_KEYS = 200_000
    GEN_MAX = 100_000
    MIN_LEN = 5
    MAX_LEN = 15

    print("==== Executing BFF Tests ====")
    bf = BloomFilter(MAX_KEYS)
    assert bf.is_empty()==True, "Error: is_empty() is not True on an empty BF."

    print("Generating", GEN_MAX, "random strings to insert into the BF...")
    alphabet = ["a", "b", "c", "d", "e", "f", "g", "h"]
    random_strings = [''.join(random.choice(alphabet) for _ in range(random.randint(MIN_LEN, MAX_LEN))) for _ in range(GEN_MAX)]
    print("Removing duplicates...")
    random_strings = list(set(random_strings))
    print("Retained", len(random_strings), "elements...")

    # Now add them to the BF
    print ("Adding all strings to the BF now...")
    for string in random_strings:
        bf.insert(string)
    print ("Done!")

    # Now look them all up
    print ("Now looking up every key; the BF must return true for every single one.")
    for string in random_strings:
        assert bf.contains(string) == True, "Bloom Filter did not return True for a key that was inserted."

    # Now generate some new random strings
    print ("Generating new query strings that ARE NOT contained in the BF...")
    query_strings = [''.join(random.choice(alphabet) for _ in range(random.randint(5, 15))) for _ in range(100000)]
    query_strings = list(set(query_strings).difference(random_strings))
    print ("Retained", len(query_strings), "query strings that are NOT in the BF.")

    # Now we'll look for these; we might get false positives, so we can measure
    # this and return the false positive rate
    pos = 0
    for string in query_strings:
        if bf.contains(string):
            pos += 1
    print("Querying for", len(query_strings), "unique strings not in the BF returned a count of", pos, " 'True' - False positive rate = ", pos / len(query_strings))

    """
    You need to now decide if this FP rate is acceptable or not. You could
    also try mixed query sets where some elements are inside, and some not.
    You can always track the fp/tp rate by maintaining a list/map/dict/set of
    elements that you have inserted, and checking against that as you go.
    """


def test_hash() -> None:
    """
    A simple set of tests for the associative map.
    This is not marked and is just here for you to test your code.
    """
    # Seed PRNG
    random.seed(1337)
    print("==== Executing Map Tests ====")
    
    e = Entry(1211111, 3)
    print(e.get_hash())
    e = Entry(1211112, 11111111111111)
    print(e.get_hash())
    
# The actual program we're running here
if __name__ == "__main__":
    # Get and parse the command line arguments
    parser = argparse.ArgumentParser(description="COMP3506/7505 Assignment Two: Data Structure Tests")

    parser.add_argument("--pq", action="store_true", help="Run Priority Queue tests?")
    parser.add_argument("--map", action="store_true", help="Run Map tests?")
    parser.add_argument("--bloom", action="store_true", help="Run Bloom Filter tests?")
    parser.add_argument("--hash", action="store_true", help="Hash tests?")
    parser.set_defaults(pq=False, map=False, bloom=False)

    args = parser.parse_args()

    # No arguments passed
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(-1)

    # Test each
    if args.pq:
        test_pqueue()
    if args.map:
        test_map()
    if args.bloom:
        test_bloom()
    if args.hash:
        test_hash()
