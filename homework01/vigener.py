def encrypt_vigenere(plaintext, keyword):
    """
    >>> encrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> encrypt_vigenere("python", "a")
    'python'
    >>> encrypt_vigenere("ATTACKATDAWN", "LEMON")
    'LXFOPVEFRNHR'
    """
    # PUT YOUR CODE HERE
    ciphertext = ""
    for j in plaintext:
        if not (char.islower() or char.isupper()):
            ciphertext += j
    if len(plaintext) > len(keyword):
        keyword += keyword*((len(plaintext) // len(keyword))-1)
        keyword += keyword[:(len(plaintext) % len(keyword))]
    number = 0
    for char in plaintext:
        if keyword[number].isupper():
            value = ord(keyword[number])-65
        else:
            value = ord(keyword[number])-97
        if char.isupper():
            ciphertext += chr((ord(char) + value - 'А') % 26 + 'А')
        else:
            ciphertext += chr((ord(char) + value - 'а') % 26 + 'а')
        number += 1
    return ciphertext


def decrypt_vigenere(ciphertext, keyword):
    """
    >>> decrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> decrypt_vigenere("python", "a")
    'python'
    >>> decrypt_vigenere("LXFOPVEFRNHR", "LEMON")
    'ATTACKATDAWN'
    """
    # PUT YOUR CODE HERE
    plaintext = ''
    for j in ciphertext:
        if not (char.islower() or char.isupper()):
            plaintext += j
    if len(ciphertext) > len(keyword):
        keyword += keyword*((len(ciphertext) // len(keyword))-1)
        keyword += keyword[:(len(ciphertext) % len(keyword))]
    number = 0
    for char in ciphertext:
        if keyword[number].isupper():
            value = ord(keyword[number]) - 65
        elif keyword[number].islower():
            value = ord(keyword[number]) - 97 
        if char.isupper():
            plaintext += chr((ord(char) - value - 'А') % 26 + 'А')
        elif char.islower():
            plaintext += chr((ord(char) - value - 'а') % 26 + 'а')
        number += 1  

    return plaintext