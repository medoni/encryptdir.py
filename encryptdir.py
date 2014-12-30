
import argparse
import hashlib
import os
import random
import re
import shutil

from subprocess import call


# default input folder only for encrypting
INPUTDIR="./input"
# default output folder only for encrypting
OUTPUTDIR="./output"
# default temp folder for en-/decrypting
TMPDIR="./tmp"

# location of rsa private key file. 
# Keep this file save! only needed for decryption!
DEFAULT_KEY_FILE="./mykey.pem"
# location of rsa public key file.
DEFAULT_PUB_KEY_FILE="./mykey.pem.pub"

# File/key size for symmetric encryption
AES_KEY_FILE_SIZE=256
# RSA key size. Only needed for RSA key creation. (encryptdir.py gen-keys)
RSA_KEY_SIZE=4096

# used symmetric cipher routines
# see https://www.openssl.org/docs/apps/enc.html#supported_ciphers
SYMMETRIC_ENCRYPTION_CASC = [
    'aes-256-cbc',
    'bf',
    'cast5-cbc'
]

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

    decrypt_args = subparsers.add_parser('decrypt', help='decrypts an encrypted folder')
    decrypt_args.add_argument('-in', metavar='input-folder', help='input folder', dest='input_folder')
    decrypt_args.add_argument('-out', metavar='output-folder', help='output folder', dest='output_folder')


    priv_pub_key_args = subparsers.add_parser('gen-keys', help='generates a rsa key pair')
    priv_pub_key_args.add_argument('-s', '--key-size', help='key size. Default {0}'.format(RSA_KEY_SIZE), default=RSA_KEY_SIZE, metavar='n', type=int, nargs='?')
    priv_pub_key_args.add_argument('-o', '--key-file', help='name of the output key filename. Default {0}'.format(DEFAULT_KEY_FILE), metavar='key.pem', type=str )

    gen_test_args = subparsers.add_parser('gen-test-files', help='generates some lorem ipsum test file')
    gen_test_args.add_argument('count', metavar='number', type=int, help='Count of test files should be created')

    test_args = subparsers.add_parser('test', help='Tests encrypting and decrypting')

    args = parser.parse_args()
    #print(args)
    if args.command == 'clean':
        clean(include_outdir=args.include_outdir)
    elif args.command == 'encrypt':
        encrypt()
    elif args.command == 'decrypt':
        decrypt(args.input_folder, args.output_folder)
    elif args.command == 'gen-keys':
        _generate_priv_pub_key_pair(key_size=args.key_size, key_file=args.key_file)
    elif args.command == 'gen-test-files':
        _generate_test_data(number=args.count)
    elif args.command == 'test':
        test()
    else:
        raise Exception('Invalid command "{0}"'.format(args.command))



#======================================================
def _generate_test_data(number=5):

    if not os.path.exists(INPUTDIR):
        print('Input dir "{0}" not found'.format(INPUTDIR))
        exit(1)

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
def prepair(out_dir=OUTPUTDIR):

    # cleaning workspace
    clean()

    # check tmp dir
    if not os.path.exists(TMPDIR):
        print('Creating {0}'.format(TMPDIR))
        os.makedirs(TMPDIR)

    # check output dir
    if not os.path.exists(out_dir):
        print("Creating {0}".format(out_dir))
        os.makedirs(out_dir)


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

    # clean tmp
    shutil.rmtree(TMPDIR)

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

    sym_inc_file = '{0}.in'.format(outfile)
    sym_out_file = '{0}.out'.format(outfile)

    shutil.move(outfile, sym_inc_file)

    for sym_alg in SYMMETRIC_ENCRYPTION_CASC:
        call([ 'openssl', sym_alg, '-in', sym_inc_file, '-out', sym_out_file, '-pass', 'file:{0}'.format(keyfile) ])
        shutil.move(sym_out_file, sym_inc_file)

    # move to ./output/xyz.gz.enc
    shutil.move(sym_inc_file, encoutfile)

    # clean tmp
    removeFile(keyfile)

#======================================================
def decrypt(in_dir, out_dir):
    if in_dir == None:
        print('No input folder given.')
        exit(1)

    if out_dir == None:
        print('No output folder given')
        exit(1)

    if not os.path.exists(in_dir):
        print('Input folder "{0}" does not exists'.format(in_dir))
        exit(1)

    prepair(out_dir=out_dir)

    for file, file_key, org_name in getDecryptingFiles(in_dir):
        decrypt_file(file, file_key, org_name, in_dir, out_dir)
    
    # clean tmp
    shutil.rmtree(TMPDIR)

#======================================================
def decrypt_file(file, file_key, org_name, in_dir, out_dir):
    print('Decrypting {0}'.format(file))

    source_file = '{0}/{1}'.format(in_dir, file)
    source_file_key = '{0}/{1}'.format(in_dir, file_key)

    output_file = '{0}/{1}'.format(out_dir, org_name)

    #print('\tDecrypting key file {0}'.format(file_key))
    tmp_file_key = '{0}/{1}.key'.format(TMPDIR, org_name)

    call([ 'openssl', 'rsautl', '-decrypt', '-inkey', DEFAULT_KEY_FILE, '-in', source_file_key, '-out', tmp_file_key])

    #print('\tDecrypting file with symmetric cascade')
    sym_inc_file = '{0}/{1}.in'.format(TMPDIR, file)
    sym_out_file = '{0}/{1}.out'.format(TMPDIR, file)

    shutil.copyfile(source_file, sym_inc_file)
    for sym_alg in reversed(SYMMETRIC_ENCRYPTION_CASC):
        call([ 'openssl', sym_alg, '-d', '-in', sym_inc_file, '-out', sym_out_file, '-pass', 'file:{0}'.format(tmp_file_key) ])
        shutil.move(sym_out_file, sym_inc_file)

    #Ungzip file
    with open(output_file, 'w') as stream:
        call([ 'gzip', '-d', sym_inc_file, '--stdout' ], stdout=stream)

    # clean tmp
    removeFile(tmp_file_key)
    removeFile(sym_inc_file)
    
#======================================================
def test():
    if not os.path.exists(INPUTDIR):
        os.makedirs(INPUTDIR)
        _generate_test_data(5)

    if not os.path.exists(DEFAULT_KEY_FILE):
        _generate_priv_pub_key_pair()

    encrypt_in = INPUTDIR
    encrypt_out = OUTPUTDIR

    decrypt_in = OUTPUTDIR
    decrypt_out = 'output2'

    encrypt()
    decrypt(decrypt_in, decrypt_out)

    #compare encrypt_in with decrypt_out
    for file in os.listdir(encrypt_in):
        en_file = '{0}/{1}'.format(encrypt_in, file)
        de_file = '{0}/{1}'.format(decrypt_out, file)

        if not os.path.exists(de_file):
            print('File "{0} does not exists in "{1}"'.format(en_file, decrypt_out))
            exit(1)


        sha_in = _getHashFromFile(en_file)
        sha_out = _getHashFromFile(de_file)
        
        if not sha_in == sha_out:
            print('Input file: "{0}" are not equal with {1}"'.format(en_file, de_file))


    print('All files matched successfully')

#======================================================
def _getHashFromFile(file):
    with open(file, 'r') as file:
        return hashlib.sha256(file.read().encode('utf-8')).hexdigest()



#======================================================
def getNewFiles():
    for sourcefile in os.listdir(INPUTDIR):
        if not os.path.exists('{0}/{1}'.format(OUTPUTDIR, getEncryptedOutputFileName(sourcefile))):
            yield sourcefile

#======================================================
def getDecryptingFiles(dir):
    for item in os.listdir(dir):
        mtch = re.match(r'(.*)\.key\.enc$', item)
        if mtch:
            file_key = mtch.group(0)
            file = '{0}.gz.enc'.format(mtch.group(1))

            if os.path.exists('{0}/{1}'.format(dir, file)):
                yield file, file_key, mtch.group(1)

#======================================================
def getOutputFileName(input):
    return '{0}.gz'.format(input)

def getEncryptedOutputFileName(input):
    return '{0}.gz.enc'.format(input)

def getKeyFileName(input):
    return '{0}.key'.format(input)

def getEncryptedKeyFileName(input):
    return '{0}.key.enc'.format(input)

def removeFile(file):
    os.remove(file)



















#======================================================
if __name__ == '__main__':
    main()