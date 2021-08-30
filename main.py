# For mpush pressure testing with multithreading
from util import loadtest

def main():
    print("Testing start...")
    loadtest.start()

if __name__ == "__main__" :
    main()