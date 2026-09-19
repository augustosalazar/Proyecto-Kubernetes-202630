import sys

if len(sys.argv) == 4 and sys.argv[1] == "suma":
    print(int(sys.argv[2]) + int(sys.argv[3]))
else:
    print("Uso: suma <entero-a> <entero-b>", file=sys.stderr)
    raise SystemExit(2)
