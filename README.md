# LRUcache

This program implements a least recently used cache. It uses two connected data structures to allow constant time operations.

It uses a dictionary/hash map (lru_dict) to store the (key, value) pairs of the LRU cache. It uses a linked list (lru_queue) to store the LRU queue. The head of lru_queue contains the least recently used element of the cache and the tail contains the most recently used element. When an element is inserted or queried, it is put at the tail of the queue. If an insertion will exceed the maximum size, then the least recently used element (the head of lru_queue) is first removed from the cache.

The two data structures are connected as follows. The data member of an element of lru_queue is a key into lru_dict. The dictionary lru_dict maps key -> (value,node), where node is an element of lru_queue.

This implementation is mostly functions with two object classes. The functions delete_e, insert_e, query_e and print_cache are meant to be the public interface. The other functions are meant to be private.
