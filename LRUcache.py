# Least Recently Used Cache
#
# This program implements a least recently used cache. It uses two
# connected data structures to allow constant time operations.
#
# It uses a dictionary/hash map (lru_dict) to store the (key, value) pairs
# of the LRU cache. It uses a linked list (lru_queue) to store the LRU
# queue. The head of lru_queue contains the least recently used element of
# the cache and the tail contains the most recently used element. When an
# element is inserted or queried, it is put at the tail of the queue. If
# an insertion will exceed the maximum size, then the least recently used
# element (the head of lru_queue) is first removed from the cache.
#
# The two data structures are connected as follows. The data member of
# an element of lru_queue is a key into lru_dict. The dictionary lru_dict
# maps key -> (value,node), where node is an element of lru_queue.
#
# This implementation is mostly functions with two object classes. The
# functions delete_e, insert_e, query_e and print_cache are meant to be
# the public interface. The other functions are meant to be private.
#

class Node:
    def __init__(self, dataval=None):
        self.data = dataval
        self.next_e = None
        self.prev_e = None

class LinkedList:
    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0

lru_queue = LinkedList()
lru_dict = {}
max_elem = 10

# Prints the elements of the LRU Cache, starting with the least recently used
# element.
def print_cache():
    if lru_queue.size == 0:
        print("Error: The LRU cache is empty")
        return

    print("LRU cache contains:")
    node = lru_queue.head
    while node != None:
        key = node.data
        (value,node1) = lru_dict[key]
        print("(", key, ",", value, ")")
        node = node.next_e

# Remove the least recently used element from the LRU Cache. This element is
# at the head of the lru_queue.
def remove_lru():
    if lru_queue.size == 0:
        print("Error: The LRU cache is empty")
        return

    # Remove the head item of lru_queue
    key = lru_queue.head.data
    if lru_queue.size == 1: # Only one item in queue, so clear queue
        lru_queue.head = None
        lru_queue.tail = None
    else:
        new_head = lru_queue.head.next_e
        lru_queue.head = new_head
        lru_queue.head.prev_e = None
    lru_queue.size -= 1
    
    # Remove the head item of lru_queue from lru_dict
    lru_dict.pop(key)

# Add an element to the LRU Cache - both lru_dict and lru_queue. Since it's
# the most recently used item, it gets added to the tail of lru_queue.
def add_to_cache(key,value):
    # If we've reached the maximum size, remove the least recently used item
    if lru_queue.size == max_elem:
        remove_lru()

    # Add key to tail of lru_queue
    node = Node(key)
    if lru_queue.size == 0: # There will be only one item in queue
        lru_queue.head = node
        lru_queue.tail = node
    else:
        node.prev_e = lru_queue.tail
        lru_queue.tail.next_e = node
        lru_queue.tail = node
    lru_queue.size += 1
    
    # Add key -> (value,node) to lru_dict
    lru_dict[key] = (value,node)
    
# Remove a key and its value from the LRU Cache - both lru_dict and lru_queue.
def remove_from_cache(key):
    if lru_queue.size == 0:
        print("Error: The LRU cache is empty")
        return

    # Remove element for key from lru_dict and get associated lru_queue node.
    # Assumes membership in lru_dict was checked before calling function.
    (value,node) = lru_dict.pop(key)
    
    # Remove elem from lru_queue - 4 cases
    if lru_queue.size == 1: # node is only item in queue, so clear queue
        lru_queue.head = None
        lru_queue.tail = None
    elif node == lru_queue.head: # Note: head != tail because size > 1
        new_head = lru_queue.head.next_e
        lru_queue.head = new_head
        lru_queue.head.prev_e = None
    elif node == lru_queue.tail:
        new_tail = lru_queue.tail.prev_e
        lru_queue.tail = new_tail
        lru_queue.tail.next_e = None
    else: # node is neither head nor tail, so remove from middle
        next_node = node.next_e
        prev_node = node.prev_e
        node.prev_e.next_e = next_node
        node.next_e.prev_e = prev_node
    lru_queue.size -= 1

# Insert a (key,value) pair into the cache. Print a message if pair
# is already in cache. Put pair at end of queue because it's the most 
# recently used element.
def insert_e(key,value):
    if key in lru_dict:
        (val,node) = lru_dict[key]
        if val == value:
            print("(", key, ",", value, ")", " already in cache")
        remove_from_cache(key)

    add_to_cache(key,value)

# Delete a key and its value from the cache. Print a message if key
# isn't in cache.
def delete_e(key):
    if key not in lru_dict:
        print(key, "- not in cache")
    else:
        remove_from_cache(key)
        print("removed", key, "from cache")

# Query a key to see if it's in the cache, and return its value.
# If it's in cache, then move to tail of lru_queue since it was just
# used.
def query_e(key):
    if key not in lru_dict:
        print(key, "- not in cache")
        return None
    else:
        (value,node) = lru_dict[key]
        remove_from_cache(key)
        add_to_cache(key,value)
        return value


insert_e("This", 1)
insert_e("is", 2)
insert_e("a", 3)
insert_e("test", 4)
insert_e("of", 5)
insert_e("LRU", 6)
insert_e("cache", 7)
insert_e(1, "one")
insert_e(2, "two")
insert_e(2, "too")
insert_e(3, "three")
print_cache()
insert_e("is", 2)
insert_e("is", 8)
insert_e("another", 9)
print("This", query_e("This"))
print_cache()
print("test", query_e("test"))
print("junk", query_e("junk"))
print(2, query_e(2))
print(4, query_e(4))
delete_e("spam")
delete_e("LRU")
delete_e("is")
delete_e(1)
insert_e("a", 30)
print("is", query_e("is"))
print_cache()
