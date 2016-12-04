import unittest

from day4 import parse_room_id, compute_checksum, day4a_solver, decrypt_room_name

class Day4Tests(unittest.TestCase):

    def test_parsing1(self):
        # check a simple example parses to the right parts
        name, sector, checksum = parse_room_id('aaaaa-bbb-z-y-x-123[abxyz]')

        self.assertEqual(name,'aaaaa-bbb-z-y-x')
        self.assertEqual(sector,'123')
        self.assertEqual(checksum,'abxyz')


    def test_parsing2(self):
        # check a simple example parses to the right parts
        name, sector, checksum = parse_room_id('a-b-c-d-e-f-g-h-987[abcde]')

        self.assertEqual(name, 'a-b-c-d-e-f-g-h')
        self.assertEqual(sector, '987')
        self.assertEqual(checksum, 'abcde')

    def test_compute_checksum1(self):
        checksum = compute_checksum('aaaaa-bbb-z-y-x')
        self.assertEqual(checksum,'abxyz')

    def test_compute_checksum2(self):
        checksum = compute_checksum('a-b-c-d-e-f-g-h')
        self.assertEqual(checksum, 'abcde')

    def test_day4a_solver(self):
        room_ids = ['aaaaa-bbb-z-y-x-123[abxyz]',
                    'a-b-c-d-e-f-g-h-987[abcde]',
                    'not-a-real-room-404[oarel]',
                    'totally-real-room-200[decoy]']
        # Of the real rooms from the list above, the sum of their sector IDs is 1514

        sum_sector_ids = day4a_solver(room_ids)
        self.assertEqual(sum_sector_ids, 1514)

    def test_decrypt(self):
        # For example, the real name for qzmt-zixmtkozy-ivhz-343 is very encrypted name.
        decrypted = decrypt_room_name('qzmt-zixmtkozy-ivhz', 343)
        self.assertEqual(decrypted, 'very encrypted name')

if __name__ == '__main__':
    unittest.main()
