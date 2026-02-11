#!/usr/bin/env python3

import sys
import argparse

def process_srecord_line(line, delta):
	line = line.strip()
	if not line or not line.startswith('S3'):
		return line

	# Parse the S-Record line.
	type = line[0:2]
	len_hex = line[2:4]
	addr_hex = line[4:12]
	data_hex = line[12:-2]
	chk_hex = line[-2:]

	# Convert to integers.
	len_byte = int(len_hex, 16)
	data_bytes = [int(data_hex[i:i+2], 16) for i in range(0, len(data_hex), 2)]

	# Modify data bytes.
	for pos in range(len(data_bytes)):
		data_bytes[pos] = (data_bytes[pos] + delta * pos) % 256

	# Build new data hex.
	new_data_hex = ''.join(f'{b:02X}' for b in data_bytes)

	if delta == 1:  # Encrypt, keep original checksum.
		new_chk_hex = chk_hex
	else:  # Decrypt, recompute checksum.
		addr_bytes = [int(addr_hex[j:j+2], 16) for j in range(0, 8, 2)]
		sum_bytes = len_byte + sum(addr_bytes) + sum(data_bytes)
		new_chk = 0xFF - (sum_bytes & 0xFF)
		new_chk_hex = f'{new_chk:02X}'

	# Build new S-Record line.
	new_line = f'{type}{len_hex}{addr_hex}{new_data_hex}{new_chk_hex}'
	return new_line

def main():
	parser = argparse.ArgumentParser(description='Encrypt or decrypt S-Record file')
	parser.add_argument('input_file', help='Input S-Record file')
	parser.add_argument('output_file', help='Output S-Record file')
	parser.add_argument('mode', choices=['encrypt', 'decrypt'], help='Mode: encrypt or decrypt')

	args = parser.parse_args()

	if args.mode == 'encrypt':
		delta = 1
	else:
		delta = -1

	with open(args.input_file, 'r') as in_f:
		lines = in_f.readlines()

	with open(args.output_file, 'w', newline="") as out_f:
		for line in lines:
			new_line = process_srecord_line(line, delta)
			out_f.write(f'{new_line}\n')

if __name__ == '__main__':
	main()
