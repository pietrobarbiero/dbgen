import os

from dbgen import dbgen


def main():

    try:
        os.chdir("./examples")
    except:
        pass

    dbgen.run()

    return


if __name__ == "__main__":
    main()
