#
# solution for the second puzzle of Advent of Code: http://adventofcode.com/2016/day/2
#

import re


def parse_room_id(room_id):
    """
    Split a room id into it's parts.

    :param room_id: A room id (e.g. 'aaaaa-bbb-z-y-x-123[abxyz]')
    :return: A tuple of string (name, sector, checksum)
    """
    result = re.match('^([a-z-]+)-([0-9]+)\[([a-z]+)\]$', room_id)
    if result is None:
        return None, None, None

    return result.group(1,2,3)


def compute_checksum(name, skip='-'):
    """
    Compute the room checksum from a room name

    :param name: the room name to produce the checksum for
    :param skip: string/list of characters to ignore from the room name
    :return: checksum string
    """
    # build a frequency table
    frequency_table = {}
    for c in name:
        if c in skip:
            continue
        count = frequency_table.get(c,0)
        frequency_table[c] = count+1

    # get a list (of (c,count) tuples) in frequency order
    # sort in ascending order of the reversed tuple (-freq, char) so that order equal-frequency characters alphabetically
    # we sort by -freq since we want to sort 'ascending' but get the highest frequency first
    itemsbyfrequency = sorted( frequency_table.items(), key=lambda x: (-x[1], x[0]) )

    # the checksum is the top five characters (or fewer if there are not 5 distinct characters)
    checksum = "".join([x[0] for x in itemsbyfrequency[0:5]])
    return checksum

def day4a_solver(room_ids):
    """
    Find the total of the sector id's of the valid room_ids

    :param room_ids: list of room id strings
    :return: total of the sector id's
    """

    # parse all the room id's into their parts
    room_tuples = [parse_room_id(room_id) for room_id in room_ids]

    # filter by those whose expected checksums match the computed ones
    valid_tuples = [(n, s, ec) for n, s, ec in room_tuples if ec == compute_checksum(n)]

    # sum the sector_ids
    sum_sector_ids = sum([int(s) for n, s, ec in valid_tuples ])

    return sum_sector_ids


def decrypt_room_name(name, sector_num):
    """
    Decrypts a room name.

    :param name: room name to decrypt as a string
    :param sector_num: the sector number the room is in, as an integer
    :return: string containing the decrypted room name
    """
    alphabet = list('abcdefghijklmnopqrstuvwxyz')
    blank = '-'

    decrypted=[]
    for c in name:
        # if this is a character to blank, do so
        if c in blank:
            decrypted.append(' ')
            continue

        # otherwise, this MUST be an alphabet character, so rotate it
        index = alphabet.index(c)
        decrypted_c = alphabet[(index+sector_num) % len(alphabet)]

        decrypted.append(decrypted_c)

    return "".join(decrypted)

def day4b_solver(room_ids):
    """
    Find north pole rooms.

    :param room_ids: list of room ids
    :return: a list of tuples (name, sector) for rooms which are valid and mention 'north' in their name
    """
    # parse all the room id's into their parts
    room_tuples = [parse_room_id(room_id) for room_id in room_ids]

    # filter by those whose expected checksums match the computed ones
    valid_tuples = [(n, s, ec) for n, s, ec in room_tuples if ec == compute_checksum(n)]

    # get all the decrypted names and sector ids
    decrypted = [ (decrypt_room_name(n,int(s)),s) for n,s,ec in valid_tuples ]

    # check for names that mention 'north'
    north_pole_names = [(n,s) for n,s in decrypted if 'north' in n]

    return north_pole_names

if __name__ == '__main__':
    with(open('input_4a.txt', 'r')) as infile:
        room_id_list = infile.read().splitlines()

    print(day4a_solver(room_id_list))
    print(day4b_solver(room_id_list))
