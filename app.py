import sys
from van_emde_boas import VanEmdeBoas


def process_commands_from_file(input_filename, output_filename, tree):
    output_lines = []

    with open(input_filename, "r") as file:
        for line in file:
            parts = line.strip().split()
            if not parts:
                continue
            command = parts[0]
            if command == "INC" and len(parts) == 2:
                value = int(parts[1])
                tree.insert(value)
                output_lines.append(f"INC {value}")
            elif command == "REM" and len(parts) == 2:
                value = int(parts[1])
                tree.delete(value)
                output_lines.append(f"REM {value}")
            elif command == "SUC" and len(parts) == 2:
                value = int(parts[1])
                succ = tree.successor(value)
                output_lines.append(f"SUC {value}")
                output_lines.append(str(succ))
            elif command == "PRE" and len(parts) == 2:
                value = int(parts[1])
                pred = tree.predecessor(value)
                output_lines.append(f"PRE {value}")
                output_lines.append(str(pred))
            elif command == "IMP" and len(parts) == 1:
                output_lines.append("IMP")
                output_lines.append(str(tree))

            else:
                print(f"Invalid command: {line.strip()}")

    with open(output_filename, "w") as out_file:
        out_file.write("\n".join(output_lines))


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python app.py <input_file.txt> <output_file.txt>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    tree = VanEmdeBoas(32)
    process_commands_from_file(input_file, output_file, tree)
