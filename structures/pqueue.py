"""
Skeleton for COMP3506/7505 A2, S2, 2024
The University of Queensland
Joel Mackenzie and Vladimir Morozov
"""

from typing import Any
from structures.entry import Entry
from structures.dynamic_array import DynamicArray

class PriorityQueue:
    """
    An implementation of the PriorityQueue ADT. We have used the implicit
    tree method: an array stores the data, and we use the heap shape property
    to directly index children/parents.

    The provided methods consume keys and values. Keys are called "priorities"
    and should be comparable numeric values; smaller numbers have higher
    priorities.
    Values are called "data" and store the payload data of interest.
    We use the Entry types to store (k, v) pairs.
    """
    
    def __init__(self):
        """
        Empty construction
        """
        self._arr = DynamicArray()
        self._max_priority = 0

    def _parent(self, ix: int) -> int:
        """
        Given index ix, return the index of the parent
        """
        return (ix) // 2

    def insert(self, priority: int, data: Any) -> None:
        """
        Insert some data to the queue with a given priority.
        """
        new = Entry(priority, data)
        # Put it at the back of the heap
        self._arr.append(new)
        ix = self._arr.get_size() - 1
        # Now swap it upwards with its parent until heap order is restored
        while ix > 0 and self._arr[ix].get_key() < self._arr[self._parent(ix)].get_key():
            parent_ix = self._parent(ix)
            self._arr[ix], self._arr[parent_ix] = self._arr[parent_ix], self._arr[ix]
            ix = parent_ix

    def insert_fifo(self, data: Any) -> None:
        """
        Insert some data to the queue in FIFO mode. Note that a user
        should never mix `insert` and `insert_fifo` calls, and we assume
        that nobody is silly enough to do this (we do not test this).
        """
        self.insert(self._max_priority, data)
        self._max_priority += 1

    def get_min_priority(self) -> Any:
        """
        Return the priority of the min element
        """
        if self.is_empty():
            return None
        return self._arr[0].get_key()

    def get_min_value(self) -> Any:
        """
        Return the highest priority value from the queue, but do not remove it
        """
        if self.is_empty():
            return None
        return self._arr[0].get_value()

    def remove_min(self) -> Any:
        """
        Extract (remove) the highest priority value from the queue.
        You must then maintain the queue to ensure priority order.
        """
        if self.is_empty():
            return None
        result = self._arr[0]
        self._arr[0] = self._arr[self.get_size() - 1]
        self._arr.remove_at(self.get_size() - 1)

        cur = 0
        while cur < self.get_size():
            left = (cur + 1) * 2 - 1
            right = (cur + 1) * 2

            smallest = cur
            if left < self.get_size() and self._arr[smallest].get_key() > self._arr[left].get_key():
                smallest = left
            if right < self.get_size() and self._arr[smallest].get_key() > self._arr[right].get_key():
                smallest = right
            if smallest != cur:
                self._arr[cur], self._arr[smallest] = self._arr[smallest],  self._arr[cur]
                cur = smallest
            else:
                break
        return result.get_value()

    def get_size(self) -> int:
        """
        Does what it says on the tin
        """
        return self._arr.get_size()

    def is_empty(self) -> bool:
        """
        Ditto above
        """
        return self._arr.is_empty()

    def ip_build(self, input_list: DynamicArray) -> None:
        """
        Take ownership of the list of Entry types, and build a heap
        in-place. That is, turn input_list into a heap, and store it
        inside the self._arr as a DynamicArray. You might like to
        use the DynamicArray build_from_list function. You must use
        only O(1) extra space.
        """
        
        self._arr.build_from_list(input_list)
        
        sorted_to_index = 0 
        ix = 0
        parent_ix = 0
        
        while sorted_to_index < self.get_size():
            ix = sorted_to_index 
            sorted_to_index += 1
            # Now swap it upwards with its parent until heap order is restored
            while ix > 0 and self._arr[ix].get_key() < self._arr[self._parent(ix)].get_key():
                parent_ix = self._parent(ix)
                self._arr[ix], self._arr[parent_ix] = self._arr[parent_ix], self._arr[ix]
                ix = parent_ix
                
        
        

    def sort(self) -> DynamicArray:
        """
        Use HEAPSORT to sort the heap being maintained in self._arr, using
        self._arr to store the output (in-place). You must use only O(1)
        extra space. Once sorted, return self._arr (the DynamicArray of
        Entry types).

        Once this sort function is called, the heap can be considered as
        destroyed and will not be used again (hence returning the underlying
        array back to the caller).
        """
        
        # populate sorted list from back
        
        len = self.get_size()
        
        while len > 0:
            
            popped = self._arr[0]
            self._arr[0] = self._arr[len - 1] 

            cur = 0
            while cur < len:
                left = (cur + 1) * 2 - 1
                right = (cur + 1) * 2

                smallest = cur
                if left < len and self._arr[smallest].get_key() > self._arr[left].get_key():
                    smallest = left
                if right < len and self._arr[smallest].get_key() > self._arr[right].get_key():
                    smallest = right
                if smallest != cur:
                    self._arr[cur], self._arr[smallest] = self._arr[smallest],  self._arr[cur]
                    cur = smallest
                else:
                    break 
                
            self._arr[len - 1] = popped
            len -= 1
        
        
        # flip sorted list
        last_index = self.get_size()-1
        for i in range(self.get_size()//2):
            self._arr[i], self._arr[last_index-i] = self._arr[last_index-i], self._arr[i]
        
        return self._arr
