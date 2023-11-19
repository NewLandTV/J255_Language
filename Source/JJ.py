import os
import sys

if len(sys.argv) == 1 or __name__ != "__main__":
    print("Usage : JJ [Java Script File Path] [Output File Path]")

    try:
        sys.exit(0)
    except SystemExit:
        os._exit(0)

code: list[str] = list()

with open(sys.argv[1], "r", encoding = "utf-8") as file:
    for line in file.readlines():
        line = line[:len(line) - 1]

        if line.startswith("console.log(") and line.endswith(");"):
            result = line[13:]
            result = result[:len(result) - 3]
            result = result.replace(".", "^.")

            code.append(f"println {result}.\n")
    
    code.append("end")

with open(sys.argv[2], "w", encoding = "utf-8") as file:
    file.writelines(code)