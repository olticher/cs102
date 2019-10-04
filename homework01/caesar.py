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
    symbols = '1234567890.,-=<>?|+_)(*&^%$#@!'
    for char in plaintext:
        if char in symbols:
            ciphertext += char
        elif char.islower():
            ciphertext += chr((ord(char) + 3 - 97) % 26 + 97)
        elif char.isupper():
            ciphertext += chr((ord(char) + 3 - 65) % 26 + 65)

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
    symbols = '1234567890.,/!@#$%^&*()_-+={[] ' 
    for char in ciphertext: 
        if char in symbols: 
            plaintext += char
        elif char.isupper(): 
            plaintext += chr((ord(char) - 3 - 65) % 26 + 65) 
        elif char.islower(): 
            plaintext += chr((ord(char) - 3 - 97) % 26 + 97) 

    return plaintext