import unittest

from day7 import does_address_support_tls, does_address_support_ssl

class Day7TlsTests(unittest.TestCase):

    def test_example1(self):
        # abba[mnop]qrst supports TLS (abba outside square brackets).
        result = does_address_support_tls('abba[mnop]qrst')
        self.assertEqual(result, True)


    def test_example2(self):
        # abcd[bddb]xyyx does not support TLS (bddb is within square brackets, even though xyyx is outside square brackets).
        result = does_address_support_tls('abcd[bddb]xyyx')
        self.assertEqual(result, False)

    def test_example3(self):
        # aaaa[qwer]tyui does not support TLS (aaaa is invalid; the interior characters must be different).
        result = does_address_support_tls('aaaa[qwer]tyui')
        self.assertEqual(result, False)

    def test_example4(self):
        # ioxxoj[asdfgh]zxcvbn supports TLS (oxxo is outside square brackets, even though it's within a larger string).
        result = does_address_support_tls('ioxxoj[asdfgh]zxcvbn')
        self.assertEqual(result, True)

    def test_multibracket_example1(self):
        # there may be multiple bracketed parts: kjghsdf[kghaf]asddssd[werkjr]ljuwht is valid
        result = does_address_support_tls('kjghsdf[kghaf]asddssd[werkjr]ljuwht')
        self.assertEqual(result, True)

    def test_multibracket_example2(self):
        # there may be multiple bracketed parts: kjghsdf[kghaf]aasdsd[werjjr]ljuwht is not valid
        result = does_address_support_tls('kjghsdf[kghaf]aasdsd[werjjr]ljuwht')
        self.assertEqual(result, False)

    def test_bracketed_abba_after_plain_abba(self):
        # addresses where the abba sequence occurs in any odd part is always invalid, even if an earlier part
        # e.g. 'abba[abba]abba' is not valid
        result = does_address_support_tls('abba[abba]abba')
        self.assertEqual(result, False)


class Day7SslTests(unittest.TestCase):

    def test_example1(self):
        # aba[bab]xyz supports SSL (aba outside square brackets with corresponding bab within square brackets).
        result = does_address_support_ssl('aba[bab]xyz')
        self.assertEqual(result, True)

    def test_example2(self):
        # xyx[xyx]xyx does not support SSL (xyx, but no corresponding yxy)
        result = does_address_support_ssl('xyx[xyx]xyx')
        self.assertEqual(result, False)

    def test_example3(self):
        # aaa[kek]eke supports SSL (eke in supernet with corresponding kek in hypernet; the aaa sequence is not related, because the interior character must be different).
        result = does_address_support_ssl('aaa[kek]eke')
        self.assertEqual(result, True)

    def test_example4(self):
        # zazbz[bzb]cdb supports SSL (zaz has no corresponding aza, but zbz has a corresponding bzb, even though zaz and zbz overlap).
        result = does_address_support_ssl('zazbz[bzb]cdb')
        self.assertEqual(result, True)


if __name__ == '__main__':
    unittest.main()
