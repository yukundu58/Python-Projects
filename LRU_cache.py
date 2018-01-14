from collections import namedtuple
from functools import wraps
import urllib.request
import urllib.error

class Node:
    def __init__(self, k, v):
        self.key = k
        self.val = v
        self.prev = None
        self.next = None

class LRUCache:
    def __init__(self, capacity):
        self.capacity = capacity
        self.dic = dict()
        self.head = Node(0, 0)
        self.tail = Node(0, 0)
        self.head.next = self.tail
        self.tail.prev = self.head

    def get(self, key):
        if key in self.dic:
            n = self.dic[key]
            self._remove(n)
            self._add(n)
            return n.val
        return -1

    def set(self, key, value):
        if key in self.dic:
            self._remove(self.dic[key])
        n = Node(key, value)
        self._add(n)
        self.dic[key] = n
        if len(self.dic) > self.capacity:
            n = self.head.next
            self._remove(n)
            del self.dic[n.key]

    def _remove(self, node):
        p = node.prev
        n = node.next
        p.next = n
        n.prev = p

    def _add(self, node):
        p = self.tail.prev
        p.next = node
        self.tail.prev = node
        node.prev = p
        node.next = self.tail

def lru_cache(maxsize = 128):
    def decorator(func):
        hits = 0
        misses = 0
        currsize = 0
        cache = LRUCache(maxsize)

        @wraps(func)
        def inner(*args, **kwargs):
            key = (args, tuple([(x.key, x.value) for x in kwargs]))
            nonlocal hits
            nonlocal misses
            nonlocal currsize
            result = cache.get(key)
            if result == -1:
                misses += 1
                result = func(*args, **kwargs)
                cache.set(key, result)
            else:
                hits += 1
            currsize = len(cache.dic)
            return result

        def infotuple():
            Point = namedtuple('CacheInfo', ['hits', 'misses', 'maxsize', 'currsize'])
            return Point(hits, misses, maxsize, currsize)
        inner.cache_info = infotuple

        return inner
    return decorator