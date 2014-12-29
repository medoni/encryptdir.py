
import argparse
import os
import random
import shutil

from subprocess import call


INPUTDIR="./input"
OUTPUTDIR="./output"
TMPDIR="./tmp"

DEFAULT_KEY_FILE="./mykey.pem"
DEFAULT_PUB_KEY_FILE="./mykey.pem.pub"

AES_KEY_FILE_SIZE=256
RSA_KEY_SIZE=4096

#======================================================
def main():
	#encrypt()
	#_generate_priv_pub_key_pair()

	parser = argparse.ArgumentParser(prog='encryptdir.py')

	subparsers = parser.add_subparsers()
	subparsers.required = True
	subparsers.dest = 'command'

	clean_args = subparsers.add_parser('clean', help='cleans local tmp folder')
	clean_args.add_argument('--include-outdir', action='store_true', help='cleans also output folder')

	encrypt_args = subparsers.add_parser('encrypt', help='encrypts a folder')

	priv_pub_key_args = subparsers.add_parser('gen-keys', help='generates a rsa key pair')
	priv_pub_key_args.add_argument('-s', '--key-size', help='key size. Default {0}'.format(RSA_KEY_SIZE), default=RSA_KEY_SIZE, metavar='n', type=int, nargs='?')
	priv_pub_key_args.add_argument('-o', '--key-file', help='name of the output key filename. Default {0}'.format(DEFAULT_KEY_FILE), metavar='key.pem', type=str )

	gen_test_args = subparsers.add_parser('gen-test-files', help='generates some lorem ipsum test file')
	gen_test_args.add_argument('count', metavar='number', type=int, help='Count of test files should be created')

	args = parser.parse_args()
	#print(args)
	if args.command == 'clean':
		clean(include_outdir=args.include_outdir)
	elif args.command == 'encrypt':
		encrypt()
	elif args.command == 'gen-keys':
		_generate_priv_pub_key_pair(key_size=args.key_size, key_file=args.key_file)
	elif args.command == 'gen-test-files':
		_generate_test_data(number=args.count)
	else:
		raise Exception('Invalid command "{0}"'.format(args.command))



#======================================================
def _generate_test_data(number=5):

	lorem_words = [
		'Lorem', 'ipsum', 'dolor', 'sit', 'amet,', 'consectetur', 'adipiscing', 'elit.', 'Donec', 'a', 'diam', 'lectus.', 'Sed', 'sit', 'amet', 'ipsum', 'mauris.', 'Maecenas', 'congue', 'ligula', 'ac', 'quam', 'viverra', 'nec', 'consectetur', 'ante', 'hendrerit.', 'Donec', 'et', 'mollis', 'dolor.', 'Praesent', 'et', 'diam', 'eget', 'libero', 'egestas', 'mattis', 'sit', 'amet', 'vitae', 'augue.', 'Nam', 'tincidunt', 'congue', 'enim,', 'ut', 'porta', 'lorem', 'lacinia', 'consectetur.', 'Donec', 'ut', 'libero', 'sed', 'arcu', 'vehicula', 'ultricies', 'a', 'non', 'tortor.', 'Lorem', 'ipsum', 'dolor', 'sit', 'amet,', 'consectetur', 'adipiscing', 'elit.', 'Aenean', 'ut', 'gravida', 'lorem.', 'Ut', 'turpis', 'felis,', 'pulvinar', 'a', 'semper', 'sed,', 'adipiscing', 'id', 'dolor.', 'Pellentesque', 'auctor', 'nisi', 'id', 'magna', 'consequat', 'sagittis.', 'Curabitur', 'dapibus', 'enim', 'sit', 'amet', 'elit', 'pharetra', 'tincidunt', 'feugiat', 'nisl', 'imperdiet.', 'Ut', 'convallis', 'libero', 'in', 'urna', 'ultrices', 'accumsan.', 'Donec', 'sed', 'odio', 'eros.', 'Donec', 'viverra', 'mi', 'quis', 'quam', 'pulvinar', 'at', 'malesuada', 'arcu', 'rhoncus.', 'Cum', 'sociis', 'natoque', 'penatibus', 'et', 'magnis', 'dis', 'parturient', 'montes,', 'nascetur', 'ridiculus', 'mus.', 'In', 'rutrum', 'accumsan', 'ultricies.', 'Mauris', 'vitae', 'nisi', 'at', 'sem', 'facilisis', 'semper', 'ac', 'in', 'est.', 'Vivamus', 'fermentum', 'semper', 'porta.', 'Nunc', 'diam', 'velit,', 'adipiscing', 'ut', 'tristique', 'vitae,', 'sagittis', 'vel', 'odio.', 'Maecenas', 'convallis', 'ullamcorper', 'ultricies.', 'Curabitur', 'ornare,', 'ligula', 'semper', 'consectetur', 'sagittis,', 'nisi', 'diam', 'iaculis', 'velit,', 'id', 'fringilla', 'sem', 'nunc', 'vel', 'mi.', 'Nam', 'dictum,', 'odio', 'nec', 'pretium', 'volutpat,', 'arcu', 'ante', 'placerat', 'erat,', 'non', 'tristique', 'elit', 'urna', 'et', 'turpis.', 'Quisque', 'mi', 'metus,', 'ornare', 'sit', 'amet', 'fermentum', 'et,', 'tincidunt', 'et', 'orci.', 'Fusce', 'eget', 'orci', 'a', 'orci', 'congue', 'vestibulum.', 'Ut', 'dolor', 'diam,', 'elementum', 'et', 'vestibulum', 'eu,', 'porttitor', 'vel', 'elit.', 'Curabitur', 'venenatis', 'pulvinar', 'tellus', 'gravida', 'ornare.', 'Sed', 'et', 'erat', 'faucibus', 'nunc', 'euismod', 'ultricies', 'ut', 'id', 'justo.', 'Nullam', 'cursus', 'suscipit', 'nisi,', 'et', 'ultrices', 'justo', 'sodales', 'nec.', 'Fusce', 'venenatis', 'facilisis', 'lectus', 'ac', 'semper.', 'Aliquam', 'at', 'massa', 'ipsum.', 'Quisque', 'bibendum', 'purus', 'convallis', 'nulla', 'ultrices', 'ultricies.', 'Nullam', 'aliquam,', 'mi', 'eu', 'aliquam', 'tincidunt,', 'purus', 'velit', 'laoreet', 'tortor,', 'viverra', 'pretium', 'nisi', 'quam', 'vitae', 'mi.', 'Fusce', 'vel', 'volutpat', 'elit.', 'Nam', 'sagittis', 'nisi', 'dui.'
	]
	
	for i in range(number):
		filename="test-{0}".format(i)
		with open('{0}/{1}'.format(INPUTDIR, filename), 'w') as myfile:
			for word in lorem_words:
				myfile.write('{0}{1} '.format(word, str(int(random.random() * 99)) ))

			myfile.write('\n')
				

def _generate_priv_pub_key_pair(key_size=RSA_KEY_SIZE, key_file=None, key_pub_file=None):
	if key_file==None:
		key_file = DEFAULT_KEY_FILE

	if key_pub_file==None:
		key_pub_file = '{0}.pub'.format(key_file)

	# generate key pair
	call([ 'openssl', 'genrsa', '-out', key_file, str(key_size) ])

	# extract public key 
	with open(key_pub_file, 'w') as stdout:
		call([ 'openssl', 'rsa', '-in', key_file, '-pubout' ], stdout=stdout)


#======================================================
def prepair():

	# cleaning workspace
	clean()

	# check tmp dir
	if not os.path.exists(TMPDIR):
		print('Creating {0}'.format(TMPDIR))
		os.makedirs(TMPDIR)

	# check output dir
	if not os.path.exists(OUTPUTDIR):
		print("Creating {0}".format(OUTPUTDIR))
		os.makedirs(OUTPUTDIR)


#======================================================
def clean(include_outdir=False):
	if os.path.exists(TMPDIR):
		print("Deleting {0}".format(TMPDIR))
		shutil.rmtree(TMPDIR)

	if include_outdir and os.path.exists(OUTPUTDIR):
		print('Deleting {0}'.format(OUTPUTDIR))
		shutil.rmtree(OUTPUTDIR)

#======================================================
def encrypt():
	prepair()
	
	for file in getNewFiles():
		encrypt_file(file)

#======================================================
def encrypt_file(source):

	print('Encrypting file {0}'.format(source))

	# generate key file > TMPDIR/xyz.key
	keyfile = '{0}/{1}'.format(TMPDIR, getKeyFileName(source))

	with open(os.devnull, 'w') as devnull:
		call([ 'dd', 'if=/dev/random', 'of={0}'.format(keyfile), 'bs={0}'.format(AES_KEY_FILE_SIZE), 'count=1' ], stdout=devnull, stderr=devnull)

	# encrypt key file > OUTPUTDIR/xyz.key.enc
	enckeyfile = '{0}/{1}'.format(OUTPUTDIR, getEncryptedKeyFileName(source))

	call([ 'openssl', 'rsautl', '-encrypt', '-pubin', '-inkey', DEFAULT_PUB_KEY_FILE, '-in', keyfile, '-out', enckeyfile])
	
	# gz
	outfile = '{0}/{1}'.format(TMPDIR, getOutputFileName(source))

	with open(outfile, 'w') as stream:
		call([ 'gzip', '-9', '--keep', '{0}/{1}'.format(INPUTDIR, source), '--stdout' ], stdout=stream)
	
	# encrypt file
	encoutfile = '{0}/{1}'.format(OUTPUTDIR, getEncryptedOutputFileName(source))

	call([ 'openssl', 'aes-256-cbc', '-in', outfile, '-out', encoutfile, '-pass', 'file:{0}'.format(keyfile) ])

#======================================================
def getNewFiles():
	for sourcefile in os.listdir(INPUTDIR):
		if not os.path.exists(getEncryptedOutputFileName(sourcefile)):
			yield sourcefile


#======================================================
def getOutputFileName(input):
	return '{0}.gz'.format(input)

def getEncryptedOutputFileName(input):
	return '{0}.gz.enc'.format(input)

def getKeyFileName(input):
	return '{0}.key'.format(input)

def getEncryptedKeyFileName(input):
	return '{0}.key.enc'.format(input)





















#======================================================
if __name__ == '__main__':
    main()