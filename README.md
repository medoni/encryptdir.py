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

1. Maybe create some test data
	
	```
		python encryptdir.py gen-test-files 5
	``