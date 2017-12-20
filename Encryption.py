
#   Encryption Program    #

# =========================================================================== #
'''
Program for encrypting any files saved by the main program when writing to files
in any of the filders. Symmetric (private) key encryption method employed
because of speed of use. Comments are attempted to be written in accordance with 
PEP 8 Style Guide: 
http://legacy.python.org/dev/peps/pep-0008/#comments
https://google.github.io/styleguide/pyguide.html
'''
# =========================================================================== #



# ====== Imports (Python Native Modules and My Program Modules) ====== #

from base64 import b64encode
import random
import sys
import os



# ====== Encryption Algorithm ====== #        

class Encryption:
    '''Encryption class within which all of the (en/de)cryption tools reside.'''
    def __init__(self):
        '''Inits the class. Assigns all the object wide variables.'''
        self.cipherText = []
        self.plainText = []
        self.password = "encrypt"

    # == Encryption of Message == #
    
    def generate_key(self):
        '''Random key generator using HRNG from Python's os module.'''
        self.key = os.urandom(32)
        self.key = b64encode(self.key).decode('utf-8')

    def encrypt(self, message):
        '''Initial layer of encryption based on a randomly generated 32 byte
        (256 bit) key and variable modulo.

        Attributes:
            modulo: Random integer between 127 and 255
            key_: The changing encryption 'key' based on the symmetric key
        '''
        self.generate_key()
        modulo = random.randint(127, 255)
        list(message)
        for i in range(len(message)):
            key_ = ord(self.key[i % len(self.key)])
            self.cipherText.append(chr((ord(message[i]) + key_) % int(modulo)))
        self.cipherText = str(self.key)+"//%%//"+str(modulo)+"//%%//"+str((''.join(self.cipherText)))
        return self.password_encrypt()

    def password_encrypt(self):
        '''Second layer of encryption, using a less secure permanent key to
        encrypt the key, the modulus for the previous encryption and a second
        encryption of the message.

        Attributes:
            key_: The changing encryption 'key' based on the symmetric key

        Returns:
            String containing the encrypted key, modulus and message
        '''
        toReturn = []
        for i in range(len(self.cipherText)):
            key_ = ord(self.password[i % len(self.password)])
            # MOD 255 because it's the same as bitmask 11111111
            toReturn.append(chr((ord(self.cipherText[i]) + key_) % 255))
        return "".join(toReturn)

    # == Decryption of Message == #
    
    def decrypt(self, message):
        '''Decryptes the original layer, identifying the original plain text
        using the original mod and key.

        Attributes:
            key_: The changing encryption 'key' based on the symmetric key
        '''
        modulo, message = self.password_decrypt(message)
        self.plainText = []
        for i in range(len(message)):
            key_ = ord(self.key[i % len(self.key)])
            self.plainText.append(chr((ord(message[i]) - key_) % int(modulo)))
        return ''.join(self.plainText)

    def password_decrypt(self, message):
        '''Removes second layer of encryption to identify the key, modulus and
        encrypted message.

        Returns:
            Returns the identified modulus and message to the decrypt function
        '''
        self.cipherText = []
        for i in range(len(message)):
            key_ = ord(self.password[i % len(self.password)])
            self.cipherText.append(chr((ord(message[i]) - key_) % 255))

        self.cipherText = "".join(self.cipherText)
        self.key, modulo, message = self.cipherText.split("//%%//")
        return modulo, message
            

                                        
# ====== Encrypt Request ====== #

def encrypt(message):
    '''Function, externally called which encrypts the text'''
    E = Encryption()
    return E.encrypt(message)

# ====== Decrypt Request ====== #

def decrypt(message):
    '''Function, externally called which decrypts the text'''
    E = Encryption()
    return E.decrypt(message)



# ====== Python Boiler Plate ====== #

if __name__ == "__main__":
    try:
        message = str(input("Please enter the message you wish to have encrypted: "))
        E = Encryption()
        temp = E.encrypt(message)
        print("ENCRYPTED MESSAGE: "+temp)
        print("DECRYPTED MESSAGE: "+E.decrypt(temp))
    except Exception as e:
        print(e)
        input()
