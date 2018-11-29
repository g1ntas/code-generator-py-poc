import argparse
from accio.commands.root import Root


def main():
    parser = argparse.ArgumentParser(prog="accio", description="Process some integers.")
    Root(parser)
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
