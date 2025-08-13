import sys

def main(file_path):
    with open(file_path, "r") as f:
        code = f.read()
    print("File contents:")
    print(code, flush=True)
    return {"lines": len(code.splitlines())}

if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(sys.argv[1])
