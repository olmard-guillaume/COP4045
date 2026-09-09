"""Unit tests for the Caesar cipher module.

This module contains comprehensive tests for the Caesar cipher encryption/decryption
functions and letter frequency analysis functionality.
"""
import unittest

from P5_Guillaume_Olmard import caesar_cipher, caesar_decipher, letter_frequency


class CaesarCipherTests(unittest.TestCase):
    """Test suite for Caesar cipher implementation.
    
    Tests the caesar_cipher, caesar_decipher, and letter_frequency functions
    to ensure they correctly encrypt, decrypt, and analyze text.
    """
    
    def test_cipher_preserves_case_spaces_and_punctuation(self):
        """Test that Caesar cipher preserves case, spaces, and punctuation.
        
        Verifies that uppercase and lowercase letters remain in their respective cases,
        and that non-alphabetic characters (spaces, punctuation) are not modified.
        """
        self.assertEqual(caesar_cipher("Hello, World!", 3), "Khoor, Zruog!")

    def test_cipher_wraps_and_supports_negative_shifts(self):
        """Test that cipher wraps around the alphabet and handles negative shifts.
        
        Verifies that characters wrap around the alphabet when shifted past 'z' or 'Z',
        and that negative shift values correctly shift backwards in the alphabet.
        """
        self.assertEqual(caesar_cipher("xyz XYZ", 3), "abc ABC")
        self.assertEqual(caesar_cipher("abc", -3), "xyz")

    def test_decipher_returns_original_text(self):
        """Test that decryption reverses encryption correctly.
        
        Verifies that applying caesar_decipher with the same shift value used in
        caesar_cipher returns the original plaintext message.
        """
        message = "Attack at Dawn!"
        encrypted = caesar_cipher(message, 7)
        self.assertEqual(caesar_decipher(encrypted, 7), message)

    def test_letter_frequency_ignores_case_and_nonletters(self):
        """Test that letter frequency analysis is case-insensitive and ignores non-letters.
        
        Verifies that uppercase and lowercase letters are counted together,
        that non-alphabetic characters (spaces, punctuation, digits) are ignored,
        and that the returned dictionary contains all 26 letters with correct counts.
        """
        frequencies = letter_frequency("Hello, HELLO! 123")
        self.assertEqual(frequencies["h"], 2)
        self.assertEqual(frequencies["e"], 2)
        self.assertEqual(frequencies["l"], 4)
        self.assertEqual(frequencies["o"], 2)
        self.assertEqual(frequencies["a"], 0)
        self.assertEqual(len(frequencies), 26)


if __name__ == "__main__":
    unittest.main()
