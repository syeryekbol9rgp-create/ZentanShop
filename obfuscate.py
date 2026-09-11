import base64
import zlib
import marshal
import sys
import os


def obfuscate(input_file, output_file=None):
    if not os.path.exists(input_file):
        print(f"[!] File not found: {input_file}")
        return

    if output_file is None:
        base, _ = os.path.splitext(input_file)
        output_file = f"{base}_obf.py"

    with open(input_file, "r", encoding="utf-8") as f:
        source = f.read()

    code_obj = compile(source, input_file, "exec")
    marshalled = marshal.dumps(code_obj)
    compressed = zlib.compress(marshalled, 9)
    encoded = base64.b64encode(compressed).decode("ascii")

    loader = (
        "import base64,zlib,marshal\n"
        f"exec(marshal.loads(zlib.decompress(base64.b64decode('{encoded}'))))\n"
    )

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(loader)

    print(f"[✓] Obfuscated: {input_file}")
    print(f"    → {output_file}")
    print(f"    Original : {os.path.getsize(input_file):,} bytes")
    print(f"    Obfusc.  : {os.path.getsize(output_file):,} bytes")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python obfuscate.py <file.py> [output.py]")
        sys.exit(1)

    infile = sys.argv[1]
    outfile = sys.argv[2] if len(sys.argv) > 2 else None
    obfuscate(infile, outfile)
