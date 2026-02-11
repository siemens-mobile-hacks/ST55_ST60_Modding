#!/usr/bin/env python3

import sys
import argparse

def generate_srec(input_path, start_address, chunk_size=16):
	try:
		with open(input_path, 'rb') as f:
			address = start_address

			while True:
				data = f.read(chunk_size)
				if not data:
					break

				# S3 Record: Type(1) + Count(1) + Addr(4) + Data(N) + Checksum(1).
				# Byte count = Address bytes (4) + Data bytes + Checksum byte (1).
				byte_count = 4 + len(data) + 1

				# Build the byte list for checksum calculation.
				# Checksum is the least significant byte of the one's complement
				# of the sum of the values of the byte count, address, and data bytes.
				payload = []
				payload.append(byte_count)
				payload.append((address >> 24) & 0xFF)
				payload.append((address >> 16) & 0xFF)
				payload.append((address >> 8) & 0xFF)
				payload.append(address & 0xFF)
				payload.extend(data)

				checksum = 0xFF - (sum(payload) & 0xFF)

				# Format components into hex strings.
				count_hex = f'{byte_count:02X}'
				addr_hex = f'{address:08X}'
				data_hex = ''.join(f'{b:02X}' for b in data)
				chk_hex = f'{checksum:02X}'

				# Output the S3 record.
				print(f'S3{count_hex}{addr_hex}{data_hex}{chk_hex}')

				address += len(data)

	except FileNotFoundError:
		print(f'Error: File {input_path} not found.', file=sys.stderr)
		sys.exit(1)

def main():
	parser = argparse.ArgumentParser(description='Convert binary file to S-Record (S3) format.')
	parser.add_argument('input', help='Path to the input binary file')
	parser.add_argument('--address', '-a',
						type=lambda x: int(x, 0),
						default=0x01000000,
						help='Starting address in hex (e.g., 0x01000000)')
	parser.add_argument('--size', '-s', 
						type=int,
						default=16,
						help='Number of bytes per line (default: 16)')

	args = parser.parse_args()

	generate_srec(args.input, args.address, args.size)

if __name__ == '__main__':
	main()
