def encrypt_caesar(plaintext):
    """
    >>> encrypt_caesar("PYTHON")
    'SBWKRQ'
    >>> encrypt_caesar("python")
    'sbwkrq'
    >>> encrypt_caesar("Python3.6")
    'Sbwkrq3.6'
    >>> encrypt_caesar("")
    ''
    """
    # PUT YOUR CODE HERE
    ciphertext = ""
    for char in plaintext:
        if char.islower():
            ciphertext += chr((ord(char) + 3 - ord('a')) % 26 + ord('a'))
        if char.isupper():
            ciphertext += chr((ord(char) + 3 - ord('A')) % 26 + ord('A'))
        if not char.isalpha():
            ciphertext += char
    return ciphertext


def decrypt_caesar(ciphertext):
    """
    Decrypts a ciphertext using a Caesar cipher.
    »> decrypt_caesar("SBWKRQ")
    'PYTHON'
    »> decrypt_caesar("sbwkrq")
    'python'
    »> decrypt_caesar("Sbwkrq3.6")
    'Python3.6'
    »> decrypt_caesar("")
    ''
    """
    # PUT YOUR CODE HERE
    plaintext = ''
    for char in plaintext:
        if char.islower():
            plaintext += chr((ord(char) + 3 - ord('a')) % 26 + ord('a'))
        if char.isupper():
            plaintext += chr((ord(char) + 3 - ord('A')) % 26 + ord('A'))
        if not char.isalpha():
            plaintext += char
    return plaintext
