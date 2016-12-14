import re
import hashlib


class Day14KeyGenerator(object):
    # regex for matching 3 characters
    match_3_hexchar_re = re.compile(r'([0-9a-f])\1{2}')

    def __init__(self, salt, stretched = False):
        """
        Generate keys for communicating with santa.

        :param salt: salt for this instance
        :param stretched: if True, uses the 'stretched' hashing form
        """
        self.salt = salt
        self.stretched = stretched

        self.hashes = []
        self.hash_index = 0
        self.search_index = -1  # start at -1 since we will pre-increment this

    def generate_next_hash(self):
        """
        Make the next hash and append it to the end of the hash list.

        :return: None
        """
        tohash = self.salt+str(self.hash_index)

        if self.stretched:
            hash = tohash
            for i in range(2017):
                hash = hashlib.md5(hash.encode('ascii')).hexdigest().lower()
        else:
            hash = hashlib.md5(tohash.encode('ascii')).hexdigest().lower()

        self.hashes.append(hash)
        self.hash_index += 1

    def get_hash(self, index):
        """
        Get a hash, computing it by extendeding the hash list if necessary.
        :param index: index of hash
        :return: string containing the md5 hash of salt+index
        """
        while(index>=len(self.hashes)):
            self.generate_next_hash()

        return self.hashes[index]

    def step(self):
        """
        Single step of the search for keys. Generates the next possible key and checks if it's valid.

        :return: a tuple of (key, didmatch3, didmatch5) such that
                    if the key processed for this step is valid, key is a string holding the valid key, and didmatch3 and didmatch5 will both be True
                    otherwise, key will be None, and didmatch3 and didmatch5 indicate whether this candidate key passed those validation checks.
        """
        self.search_index += 1

        # candidate hashes must contain a 3 character run
        candidate_hash = self.get_hash(self.search_index)
        match = self.match_3_hexchar_re.search(candidate_hash)
        if not match:
            return None, False, False

        # if one of the next 1000 hashes containsa 7-character run of the same character from candidate_hash
        require = match.group(1) * 5
        for test_hash_index in range(self.search_index+1, self.search_index+1001):
            test_hash = self.get_hash(test_hash_index)

            if require in test_hash:
                return candidate_hash, True, True

        return None, True, False


    def find_next_valid_key(self):
        """
        :return: a string containing the next valid key
        """
        key = None
        while not key:
            key, didmatch3, didmatch5 = self.step()

        return key


def day14a_solver():
    solver = Day14KeyGenerator('ahsbgdzn')
    for i in range(64):
        key = solver.find_next_valid_key()

    return solver.search_index


def day14b_solver():
    solver = Day14KeyGenerator('ahsbgdzn', stretched=True)
    for i in range(64):
        key = solver.find_next_valid_key()
        print('key %d at index %d is %s' % (i, solver.search_index, key))

    return solver.search_index

if __name__ == '__main__':
    print(day14a_solver())
    print(day14b_solver())
