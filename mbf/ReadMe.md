# MBF firmware decrypt/encrypt

Reverse-engineered by OpenAI GPT-5.6 Luna & EXL, 30-Sep-2026 for Panasonic EB-X300 firmware.

## Usage

```sh
# Firmware files decription & encryption:
python mbf_decrypt_encrypt.py encrypted.mbf decrypted.bin
python mbf_decrypt_encrypt.py decrypted.mbf encrypted.bin --encrypt

# Agent.bin decription & encryption:
python agent_decrypt_encrypt.py Agent.bin Agent_dec.bin
python agent_decrypt_encrypt.py Agent_dec.bin Agent_enc.bin

md5sum *.bin
1916e222dce331125e0d294c044a7639 *Agent.bin
52db0c8d2ec16386ee54a87ac93b5894 *Agent_dec.bin
1916e222dce331125e0d294c044a7639 *Agent_enc.bin
```

## Information

01. [ChatGPT discussions](https://chatgpt.com/share/6abca5d5-2f74-83ec-a3ce-e3475c8fc49e)
