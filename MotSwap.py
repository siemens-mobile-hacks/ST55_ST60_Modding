#!/usr/bin/env python3

import sys
import argparse

def swap_bytes(input_path, output_path):
	'''Reads a binary file and swaps every pair of bytes.'''
	try:
		with open(input_path, 'rb') as f:
			data = f.read()

		if len(data) % 2 != 0:
			print('Warning: File size is odd. The final byte will be skipped.', file=sys.stderr)

		# Create a bytearray to store the swapped data
		swapped = bytearray(data)

		# Iterate through the data in steps of 2 and swap
		for i in range(0, len(data) - 1, 2):
			swapped[i] = data[i + 1]
			swapped[i + 1] = data[i]

		with open(output_path, 'wb') as f:
			f.write(swapped)

		print(f'Successfully wrote swapped data to: {output_path}')

	except FileNotFoundError:
		print(f'Error: File {input_path} not found.', file=sys.stderr)
		sys.exit(1)
	except Exception as e:
		print(f'An unexpected error occurred: {e}', file=sys.stderr)
		sys.exit(1)

def main():
	parser = argparse.ArgumentParser(
		description='Swap bytes in a binary file (e.g., conversion between Big-Endian and Little-Endian RGB565).'
	)
	parser.add_argument('input', help='Path to the source raw/binary file')
	parser.add_argument('output', help='Path to save the byte-swapped output file')

	args = parser.parse_args()

	swap_bytes(args.input, args.output)

if __name__ == '__main__':
	main()
