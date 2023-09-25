import sys,os

# create environment directory
os.system('mkdir -p ./certificate')


def main():
	os.system('clear')

	print('''
┌───────────────────────────────────────────────────────┐
│          Digital Certificate Manager Tools            │
└───────────────────────────────────────────────────────┘
┌───────────────────────────────────────────────────────┐
│ 1. Generate Certificate Authority (CA)                │
│ 2. Generate Intermediate Certificate Authority (ICA)  │
│ 3. Generate Certificate Signing Request (CSR)         │
│ 4. Signing Certificate Request                        │
│ 5. Exit                                               │
└───────────────────────────────────────────────────────┘
''')

	# get input from user
	choice = int(input('[?] : '))

	if choice == 1:
	# generate ca
		gen_ca()
		main()

	elif choice == 2:
	# generate ica
		gen_ica()
		main()

	elif choice == 3:
	# generate csr
		gen_csr()
		main()

	elif choice == 4:
	# signing cert
		sign_cert()
		main()

	else:
		sys.exit()

def gen_csr():
	# store input user
	name = input('\nInput name for output file (without extension):\t').replace(' ', '_')
	C = input('Input Country Name [ex: ID] : ')
	ST = input('Input State [ex: Jawa Timur] : ')
	L = input('Input Locality Name [ex: Sidoarjo] : ')
	O = input('Input Organization Name [ex: YLPM Walisongo Gempol] : ')
	OU = input('Input Organization Unit Name [ex: SMK Walisongo 2 Gempol] : ')
	CN = input('Input Common Name : ')


	# generate key for certificate request
	os.system('mkdir -p ./certificate/private')
	os.system(f"openssl genrsa -out ./certificate/private/{name}.key")

	# setup temp conf file
	os.system('cp ./openssl.cnf tmp.cnf')
	os.system(f'echo "[SAN]\nsubjectAltName = @alt_names\n\n[alt_names]\nDNS.1 = {CN}\nDNS.2 = *.{CN}" >> tmp.cnf')

	# generate certificate request
	os.system('mkdir -p ./certificate/request')
	os.system(f"openssl req -new -key ./certificate/private/{name}.key -out ./certificate/request/{name}.csr -subj '/C={C}/ST={ST}/L={L}/O={O}/OU={OU}/CN={CN}' -config ./tmp.cnf -reqexts SAN")

	# delete tmp conf file
	os.system('rm -f ./tmp.cnf')

	return name


def gen_ca():
	# store input user
	name = input('\nInput name for output file (without extension):\t').replace(' ', '_')
	C = input('Input Country Name [ex: ID] : ')
	ST = input('Input State [ex: Jawa Timur] : ')
	L = input('Input Locality Name [ex: Sidoarjo] : ')
	O = input('Input Organization Name [ex: YLPM Walisongo Gempol] : ')
	OU = input('Input Organization Unit Name [ex: SMK Walisongo 2 Gempol] : ')
	CN = input('Input Common Name : ')


	# generate key for certificate request
	os.system('mkdir -p ./certificate/private')
	os.system(f"openssl genrsa -out ./certificate/private/{name}.key")

	# generate certificate request
	os.system('mkdir -p ./certificate/authority')
	os.system(f"openssl req -new -x509 -key ./certificate/private/{name}.key -out ./certificate/authority/{name}.pem -subj '/C={C}/ST={ST}/L={L}/O={O}/OU={OU}/CN={CN}' -config ./openssl.cnf")


def gen_ica():
	name = gen_csr()

	# setup env directory for openssl
	os.system('mkdir -p ./certificate/.demoCA/newcerts && touch ./certificate/.demoCA/index.txt')

	# store input user
	print('\n[i] Select Certificate Authority for signing request\n')

	directory_path = "./certificate/authority"
	# List all files in the directory
	file_list = [f for f in os.listdir(directory_path) if os.path.isfile(os.path.join(directory_path, f))]

	# Print the list of files
	num = 1
	for file_name in file_list:
		print(f'{num}. {file_name}')
		num += 1

	cert = int(input('\n[?] : '))

	# signing certificate
	os.system(f"openssl ca -keyfile ./certificate/private/{file_list[cert-1].replace('pem', 'key')} -cert ./certificate/authority/{file_list[cert-1]} -extensions v3_ca -in ./certificate/request/{name}.csr -out ./certificate/authority/{name}.pem -rand_serial -config ./openssl.cnf")


def sign_cert():
	print('\n[i] Select Certificate Signing Request\n')

	csr_dir = "./certificate/request"
	# List all files in the directory
	csr_list = [f for f in os.listdir(csr_dir) if os.path.isfile(os.path.join(csr_dir, f))]

	# Print the list of files
	num = 1
	for csr_name in csr_list:
		print(f'{num}. {csr_name}')
		num += 1

	csr = int(input('\n[?] : '))

	print('\n[i] Select Certificate Authority\n')

	ca_dir = "./certificate/authority"
	# List all files in the directory
	ca_list = [f for f in os.listdir(ca_dir) if os.path.isfile(os.path.join(ca_dir, f))]

	# Print the list of files
	num = 1
	for ca_name in ca_list:
		print(f'{num}. {ca_name}')
		num += 1

	ca = int(input('\n[?] : '))

	# create env directory
	os.system('mkdir -p ./certificate/cert')
	os.system('mkdir -p ./certificate/.demoCA/newcerts && touch ./certificate/.demoCA/index.txt')

	# signing certificate
	os.system(f"openssl ca -in ./certificate/request/{csr_list[csr-1]} -cert ./certificate/authority/{ca_list[ca-1]} -keyfile ./certificate/private/{ca_list[ca-1].replace('pem', 'key')} -out ./certificate/cert/{csr_list[csr-1].replace('csr', 'crt')} -rand_serial -config ./openssl.cnf")


main()
