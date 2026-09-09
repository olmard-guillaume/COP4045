def caesar_cipher(text, shift):
	"""Encrypt text using Caesar cipher with given shift value.
	
	Shifts each alphabetic character by the specified number of positions in the alphabet.
	Preserves case (uppercase/lowercase), spaces, punctuation, and non-alphabetic characters.
	Shift value wraps around the alphabet (e.g., shift of 26 is equivalent to shift of 0).
	
	Args:
		text (str): The plaintext message to encrypt.
		shift (int): The number of positions to shift each character. Can be positive or negative.
	
	Returns:
		str: The encrypted text with characters shifted and non-alphabetic characters unchanged.
	
	Example:
		>>> caesar_cipher("Hello, World!", 3)
		'Khoor, Zruog!'
	"""
	alphabet_lower = "abcdefghijklmnopqrstuvwxyz"
	alphabet_upper = alphabet_lower.upper()
	encrypted_text = ""
	shift %= 26

	for character in text:
		if character in alphabet_lower:
			index = alphabet_lower.index(character)
			encrypted_text += alphabet_lower[(index + shift) % 26]
		elif character in alphabet_upper:
			index = alphabet_upper.index(character)
			encrypted_text += alphabet_upper[(index + shift) % 26]
		else:
			encrypted_text += character

	return encrypted_text


def caesar_decipher(cyphertext, shift):
	"""Decrypt text that was encrypted with a Caesar cipher.
	
	Reverses the Caesar cipher encryption by shifting in the opposite direction.
	
	Args:
		cyphertext (str): The encrypted text to decrypt.
		shift (int): The original shift value used to encrypt the text.
	
	Returns:
		str: The original plaintext message.
	
	Example:
		>>> encrypted = caesar_cipher("Hello", 5)
		>>> caesar_decipher(encrypted, 5)
		'Hello'
	"""
	return caesar_cipher(cyphertext, -shift)


def letter_frequency(text):
	"""Calculate the frequency of each letter in the given text.
	
	Counts the occurrences of each lowercase letter (a-z) in the text.
	Case-insensitive (uppercase letters are converted to lowercase).
	Non-alphabetic characters (spaces, punctuation, numbers) are ignored.
	
	Args:
		text (str): The text to analyze for letter frequency.
	
	Returns:
		dict: A dictionary with all 26 lowercase letters as keys and their occurrence 
			  counts as values. Letters not in the text have a count of 0.
	
	Example:application menu.
	
	Displays a menu-driven interface that allows users to:
	1. Encrypt a message using Caesar cipher
	2. Analyze the letter frequency of the original message
	3. Decrypt the encrypted message back to the original
	4. Exit the program
	
	The user is prompted to enter a message and a shift value. The application then
	displays the encrypted text, letter frequency analysis, and the decrypted text.
	
	Returns:
		None
	
		>>> letter_frequency("Hello World")
		{'a': 0, 'b': 0, 'c': 0, ..., 'd': 1, 'e': 1, 'h': 1, 'l': 3, 'o': 2, ...}
	"""
	frequencies = {}
	for character in "abcdefghijklmnopqrstuvwxyz":
		frequencies[character] = 0

	for character in text.lower():
		if character in frequencies:
			frequencies[character] += 1

	return frequencies


def main():
	"""Run the interactive Caesar cipher menu."""
	while True:
		print("\nCaesar Cipher Menu")
		print("1. Encrypt, analyze, and decrypt a message")
		print("2. Exit")
		choice = input("Choose an option: ")

		if choice == "2":
			print("Goodbye!")
			break
		if choice != "1":
			print("Invalid option. Please choose 1 or 2.")
			continue

		text = input("Enter a message: ")
		while True:
			try:
				shift = int(input("Enter the shift value: "))
				break
			except ValueError:
				print("Please enter an integer shift value.")

		encrypted_text = caesar_cipher(text, shift)
		frequencies = letter_frequency(text)
		decrypted_text = caesar_decipher(encrypted_text, shift)

		print("Ciphered text:", encrypted_text)
		print("Letter frequency:")
		for letter in frequencies:
			print(f"{letter}: {frequencies[letter]}")
		print("Deciphered text:", decrypted_text)


if __name__ == "__main__":
	main()
