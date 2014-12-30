encryptdir.py
=============

a python script to encrypt all files in a directory with public rsa key. 

## Usage
1. Generate a rsa key pair

	```
	python encryptdir.py gen-keys
	```

	This creates a 4096 rsa key file _mykey.pem_ and it's public key file is: _mykey.pem.pub_

1. Create your input folder if not exists

	```
	mkdir input
	```

1. Create some test data (optional)
	
	```
	python encryptdir.py gen-test-files 5
	```

1. Encrypting

	```
	python encryptdir.py encrypt
	```

	This encrypts all files in ```./input/``` to ```./output/```. Files which are exists in output will be ignored. After encrypting, the output folder looks like:

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
	
	```
	python encryptdir.py decrypt -in ./folder-with-encrypted-files/ -out ./target-folder/
	```


