
import cryptography



class Transcryptor(object):
    """ Helper class for encrypting and decrypting files safely with a symmetric cipher and  user provided  
    password (user pass, is the pass b4 kdf applied). 
    """

    def __init__(self, usr_pass, salt, progress_callback=None):
        """ Init a new Transcryptor object. Applies the key derivation function to user password, and 
        saves it this object for future encrypt, decrypt operations. 
        
        To lose the key simply destroy this object from memory. 
        
        Since the key derivation function is intentionally compute-intensive this init call might take 
        a while to return. 
        
        """
        super(Transcryptor, self).__init__()


    def encrypt_file(self, src, dst):
        """ Given the pathname to a source file, encrypt it and save it into another file whose pathname is dst.  """


        pass

    def decrypt_file(self, src, dst):
        """ Given the pathname to a source file, decrypt it and save it into another file whose pathname is dst.  """


        pass

