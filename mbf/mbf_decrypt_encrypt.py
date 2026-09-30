#!/usr/bin/env python3
"""
Written by OpenAI GPT-5.6 Luna & EXL, 30-Sep-2026

Decrypt/encrypt the MBF firmware format recovered from:
040720_RA1.PAC_C042_CN0M0802_LPCL1201mf.mbf

The transform is byte-wise modular addition with a repeating 256-byte mask.

For absolute file offset p:
	encrypted[p] = (plain[p] + KEY[(p - PHASE_OFFSET) & 0xff]) & 0xff
	plain[p]     = (encrypted[p] - KEY[(p - PHASE_OFFSET) & 0xff]) & 0xff

The key below is the mask recovered from the 256-byte erased (0xff) block
at PHASE_OFFSET = 0x9e9e0c:
	KEY[i] = encrypted_erased_block[i] + 1 (mod 256)

Do NOT reset the key index at the beginning of a chunk unless the chunk
starts at the same phase. For partial/chunked processing, pass the absolute
file offset.
"""
import argparse
from pathlib import Path

PHASE_OFFSET = 0x9E9E0C

KEY = bytes.fromhex("""
0B 07 0D 0D 03 0C 04 0F 05 08 01 11 10 0E 12 03
06 0A 00 00 05 07 13 0B 06 13 07 0F 03 0B 00 11
0C 09 04 09 06 13 00 0A 06 0D 09 0A 0D 0D 09 0D
0B 00 00 02 01 02 07 09 01 04 04 09 05 02 12 10
06 0D 03 0B 0A 08 00 11 00 07 0E 05 0E 0A 08 13
03 0B 05 0B 01 0F 06 04 0A 11 09 13 06 09 00 0E
03 01 13 0B 13 12 00 06 0B 06 12 11 13 0C 03 13
03 0A 0B 02 0F 09 12 00 07 10 08 0B 0D 03 07 01
04 01 0F 02 11 06 0D 08 07 10 05 08 02 03 0C 0E
0C 01 12 0B 00 00 0D 00 09 0B 10 0F 07 02 13 06
07 08 00 0B 02 03 00 07 02 06 0D 0B 09 07 0C 01
13 11 00 11 04 0A 0D 02 0F 05 13 0C 0A 08 00 01
0E 07 0C 05 0F 0B 07 01 0A 12 04 04 09 0F 0C 05
04 10 03 0C 13 04 04 02 04 08 08 0C 00 02 0F 10
0A 07 10 0B 07 0D 04 0E 01 09 0A 00 10 05 0F 0E
0A 0F 04 0D 05 06 06 02 0D 07 13 09 0E 12 00 0D
""")

assert len(KEY) == 256

def transform(src, dst, start_offset=0, decrypt=True):
	# Process in chunks so the whole firmware need not be held in RAM.
	with open(src, "rb") as fi, open(dst, "wb") as fo:
		pos = start_offset
		while True:
			b = fi.read(1024 * 1024)
			if not b:
				break
			out = bytearray(len(b))
			for j, c in enumerate(b):
				k = KEY[(pos + j - PHASE_OFFSET) & 0xff]
				out[j] = (c - k) & 0xff if decrypt else (c + k) & 0xff
			fo.write(out)
			pos += len(b)

def main():
	ap = argparse.ArgumentParser()
	ap.add_argument("input")
	ap.add_argument("output")
	ap.add_argument("-e", "--encrypt", action="store_true",
					help="encrypt instead of decrypt")
	ap.add_argument("--offset", type=lambda x: int(x, 0), default=0,
					help="absolute file offset of input data (default: 0)")
	args = ap.parse_args()
	transform(args.input, args.output, args.offset, decrypt=not args.encrypt)

if __name__ == "__main__":
	main()
