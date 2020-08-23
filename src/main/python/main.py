import sys
import argparse
from gui import AppContext
from table_transformer import TableTransformer

def main():
    description = """Extract measurements or summaries to new csv tables.
                     To run in gui mode specify no arguments.
                     """
    epilog = """"""
    parser = argparse.ArgumentParser(prog='DOCC',
                                     description=description,
                                     epilog=epilog)

    parser.add_argument('-c',
                        '--cli',
                        metavar='file',
                        type=str,
                        nargs=1,
                        help='Process the specified file in command line mode.')
    parser.add_argument('-o',
                        '--output',
                        metavar='dir',
                        nargs=1,
                        help='Create output files in the specified directory.')

    args = parser.parse_args()

    if args.cli:
        transformer = TableTransformer(args.cli[0])
        transformer.main()
    else:
        appctxt = AppContext()       # 1. Instantiate ApplicationContext
        exit_code = appctxt.run()      # 2. Invoke appctxt.app.exec_()
        sys.exit(exit_code)


if __name__ == "__main__":
    main()
