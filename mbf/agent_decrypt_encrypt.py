#!/usr/bin/env python3

import argparse


def transform_byte(byte):
	'''
	Swap the high and low nibbles of one byte.

	3D -> D3
	00 -> 00
	0A -> A0
	3E -> E3
	'''
	return (byte >> 4) | ((byte & 0x0F) << 4)


def process_file(input_file, output_file):
	with open(input_file, 'rb') as f:
		data = f.read()

	result = bytes(
		transform_byte(byte)
		for byte in data
	)

	with open(output_file, 'wb') as f:
		f.write(result)


def main():
	parser = argparse.ArgumentParser(
		description='Swap high and low nibbles of every byte in a file.'
	)

	parser.add_argument(
		'input',
		help='Input file'
	)

	parser.add_argument(
		'output',
		help='Output file'
	)

	args = parser.parse_args()

	process_file(args.input, args.output)


if __name__ == '__main__':
	main()
