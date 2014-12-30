encryptdir.py
=============

a python script to encrypt all files in a directory with a public rsa key. 

## Usage
1. Generate a rsa key pair

    ```bash
    python encryptdir.py gen-keys
    ```

    This creates a 4096 rsa key file _mykey.pem_ and it's public key file is: _mykey.pem.pub_

1. Create your input folder if not exists

    ```bash
    mkdir input
    ```

1. Create some test data (optional)
    
    ```bash
    python encryptdir.py gen-test-files 5
    ```

1. Encrypting

    ```bash
    python encryptdir.py encrypt
    ```

    This encrypts all files in `./input/` to `./output/`. Files which are exists in output will be ignored. After encrypting, the output folder looks like:

    ```
    root@FreeBSD:~/encryptdir # ls -la output
    total 324015
    drwxr-xr-x  2 root  wheel         14 Dec 30 02:13 .
    drwxr-xr-x  7 root  wheel         14 Dec 30 02:11 ..
    -rw-r--r--  1 root  wheel  331375424 Dec 29 23:29 31c3-5960-en-Revisiting_SSL_TLS_Implementations_hd.mp4.gz.enc
    -rw-r--r--  1 root  wheel        512 Dec 29 23:27 31c3-5960-en-Revisiting_SSL_TLS_Implementations_hd.mp4.key.enc
    -rw-r--r--  1 root  wheel       1392 Dec 29 23:29 test-0.gz.enc
    -rw-r--r--  1 root  wheel        512 Dec 29 23:29 test-0.key.enc
    -rw-r--r--  1 root  wheel       1392 Dec 29 23:29 test-1.gz.enc
    -rw-r--r--  1 root  wheel        512 Dec 29 23:29 test-1.key.enc
    -rw-r--r--  1 root  wheel       1392 Dec 29 23:29 test-2.gz.enc
    -rw-r--r--  1 root  wheel        512 Dec 29 23:29 test-2.key.enc
    -rw-r--r--  1 root  wheel       1392 Dec 29 23:29 test-3.gz.enc
    -rw-r--r--  1 root  wheel        512 Dec 29 23:29 test-3.key.enc
    -rw-r--r--  1 root  wheel       1392 Dec 29 23:29 test-4.gz.enc
    -rw-r--r--  1 root  wheel        512 Dec 29 23:29 test-4.key.enc
    ```


1. Decrypting
    
    ```bash
    python encryptdir.py decrypt -in ./folder-with-encrypted-files/ -out ./target-folder/
    ```

1. Test encryption and decryption
    You can also test encryption and decryption.

    ```bash
    #mkdir input && insert some test files (optional)
    python encryptdir.py test
    ```

    This encrypts and decrypts your test files. If ```./input/``` does not exists, the folder will be automatically created and some test data will be inserted.

## Parameters
In *encryptdir.py* you can customize following parameters:
* Folders:

  ```python
  # default input folder only for encrypting
  INPUTDIR="./input"
  # default output folder only for encrypting
  OUTPUTDIR="./output"
  # default temp folder for en-/decrypting
  TMPDIR="./tmp"
  ```

* Key files
  
  ```python
  # location of rsa private key file. 
  # Keep this file save! only needed for decryption!
  DEFAULT_KEY_FILE="./mykey.pem"
  # location of rsa public key file.
  DEFAULT_PUB_KEY_FILE="./mykey.pem.pub"
  ```

* Key sizes

  ```python
  # File/key size for symmetric encryption
  AES_KEY_FILE_SIZE=256
  # RSA key size. Only needed for RSA key creation. (encryptdir.py gen-keys)
  RSA_KEY_SIZE=4096
  ```

* symmetric cipher routines
  Sym. cipher routines used for each file en-/decryption. [Support Types](https://www.openssl.org/docs/apps/enc.html#supported_ciphers)

  ```python
  # used symmetric cipher routines
  # see https://www.openssl.org/docs/apps/enc.html#supported_ciphers
  SYMMETRIC_ENCRYPTION_CASC = [
    'aes-256-cbc',
    'bf',
    'cast5-cbc'
  ]
  ```