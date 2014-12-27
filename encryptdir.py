
import argparse
import os
import shutil

from subprocess import call


INPUTDIR="./input"
OUTPUTDIR="./output"
TMPDIR="./tmp"

KEY_FILE="./mykey.pem"
PUB_KEY_FILE="./mykey.pem.pub"

AES_KEY_FILE_SIZE=256

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

	args = parser.parse_args()
	#print(args)
	if args.command == 'clean':
		clean(include_outdir=args.include_outdir)
	elif args.command == 'encrypt':
		encrypt()
	else:
		raise Exception('Invalid command "{0}"'.format(args.command))



#======================================================
def _generate_test_data():
	
	for i in range(5):
		filename="test-{0}".format(i)
		with open('{0}/{1}'.format(INPUTDIR, filename), 'w') as myfile:
			myfile.write('lorem ipsum {0}\n'.format(i))

def _generate_priv_pub_key_pair():
	# generate key pair
	#call([ 'openssl', 'genrsa', '-out', KEY_FILE, '4096' ])

	# extract public key 
	with open(PUB_KEY_FILE, 'w') as stdout:
		call([ 'openssl', 'rsa', '-in', KEY_FILE, '-pubout' ], stdout=stdout)


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

	call([ 'openssl', 'rsautl', '-encrypt', '-pubin', '-inkey', PUB_KEY_FILE, '-in', keyfile, '-out', enckeyfile])
	
	# gz
	
	outfile = '{0}/{1}'.format(TMPDIR, getOutputFileName(source))
	print('TODO gzipping {0}'.format(outfile))
	call([ 'cp', '{0}/{1}'.format(INPUTDIR, source), outfile ])
	
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