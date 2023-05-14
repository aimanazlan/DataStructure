from __future__ import annotations
import json
from typing import List
import math

def hash(username:str,j:int,m:int) -> int:
    
    # Convert each character to ASCII and add them together
    char_sum = sum(ord(c) for c in username)
    
    # Concatenate the number with itself until the result is m or greater
    num_str = str(char_sum)
    while int(num_str) < m:
        num_str += num_str
    
    # Raise it to the jth power
    num = int(num_str) ** j
    
    # Extract the same number of leftmost digits as m has
    num_str = str(num)[:len(str(m))]

    # Take the result mod m
    result = int(num_str) % m
    
    return result

# Bloom Filter Class
# DO NOT MODIFY

class Bloom():
    def __init__(self,
                 m         = int,
                 k         = int,
                 fpmax     = float,
                 threshold = int,
                 bitarray  = List[int],
                 usernamedict   = dict,
                 n         = int):
        self.m         = m
        self.k         = k
        self.fpmax     = fpmax
        self.threshold = threshold
        self.bitarray  = [0] * m
        self.usernamedict   = {}
        self.n         = 0

    def dump(self) -> str:
        def _to_dict(b) -> str:
            dict_repr = ''.join([str(i) for i in self.bitarray])
            return(dict_repr)
        return(_to_dict(self.bitarray))

    # If a username has been hacked, record it.
    # If it's hacked threshold times, insert it into the bloom filter.
    def hack(self, username: str):
        # If the username is not already in the dictionary, add it with a count of 1
        if username not in self.usernamedict:
            self.usernamedict[username] = 1
        # If the username is already in the dictionary, increment its count
        else:
            self.usernamedict[username] = self.usernamedict.get(username, 0) + 1
        
        # If the count of hacking attempts has reached the threshold, insert the username into the Bloom filter
        if self.usernamedict[username] >= self.threshold:
            if self.usernamedict[username] == self.threshold:
                self.n = self.n+1
            self.insert(username)


    def rebuild(self):
        i = self.m + 1

        # Calculate the new m value that will give us the desired false positive rate
        new_m = (1 - (1 - 1/self.m)**(self.k*self.n))**self.k

        while (new_m >= self.fpmax/2):
            new_m = (1 - (1 - 1/(i))**(self.k*self.n))**self.k
            i = i+1

        self.m = i-1
        
        # Recreate the bitarray with the new m value
        self.bitarray = [0] * self.m
        
        # Add all the usernames to the new bitarray
        for username in self.usernamedict.keys():
            # Generate k hash values for the username using the new m value
            if (self.usernamedict[username] >= self.threshold):
                self.insert(username)
        


    # Insert a username into the bloom filter.
    def insert(self, username: str):
        # print("here insert")
        # print(username)
        hashes = [hash(username, j+1, self.m) for j in range(self.k)]
        
        # Set the corresponding bits in the bitarray to 1
        for i in hashes:
            hashs = str(i)
            i = 0
            while i < len(hashs):
                idx = int(hashs[i])
                j = i+1
                while(j < len(hashs) and idx*10+int(hashs[j]) < self.m):
                    idx = idx*10+int(hashs[j])
                j += 1
                self.bitarray[idx] = 1

                if j == i+1:
                    i += 1
                else:
                    i = j+1

        # Calculate the current false positive probability
        p = (1 - (1 - 1/self.m)**(self.k*self.n))**self.k
        
        # Rebuild the Bloom filter if the false positive probability exceeds the acceptable probability
        if p > self.fpmax:
            # print("here rebuild")
            self.rebuild()


    # Check if a username is in the bloom filter.
    def check(self, username: str) -> str:
        for j in range(self.k):
            hash_value = hash(username, j+1, self.m)
            if not self.bitarray[hash_value]:
                return json.dumps({'username': username, 'status': 'SAFE'})
        return json.dumps({'username': username, 'status': 'UNSAFE'})