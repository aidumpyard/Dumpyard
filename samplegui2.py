# your_script.py

def main(file1, file2, directory):
    print("File 1:", file1)
    print("File 2:", file2)
    print("Directory:", directory)
    # Your original code logic here

if __name__ == "__main__":
    import sys
    main(sys.argv[1], sys.argv[2], sys.argv[3])