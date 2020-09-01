import sys
import argparse
from gui import AppContext
from logging import getLogger, StreamHandler, INFO, WARNING
from transformer import TableTransformer, get_extractors, MaxLevelFilter


def configure_root_logger():
    logger = getLogger('')
    logger.setLevel(INFO)

    stdout_handler = StreamHandler(sys.stdout)
    stdout_handler.addFilter(MaxLevelFilter(WARNING))
    stdout_handler.setLevel(INFO)
    logger.addHandler(stdout_handler)

    stderr_handler = StreamHandler(sys.stderr)
    stderr_handler.setLevel(WARNING)
    logger.addHandler(stderr_handler)
    return logger


def main():
    description = """Extract measurements or summaries to new csv tables.
                     To run in gui mode specify no arguments.
                     """
    epilog = """DOCC  Copyright (C) 2020  Till Schröder
                This program comes with ABSOLUTELY NO WARRANTY.
                This is free software, and you are welcome to redistribute it
                under certain conditions.
                See <https://www.gnu.org/licenses/gpl-3.0>.
             """

    parser = argparse.ArgumentParser(prog='tocc',
                                     description=description,
                                     epilog=epilog)

    parser.add_argument('-c',
                        '--cli',
                        metavar='file',
                        type=str,
                        nargs=1,
                        help='Process specified file in command line mode.')
    parser.add_argument('-s',
                        '--summaries',
                        action='store_true',
                        help='Export summaries to csv.'
                        )
    parser.add_argument('-m',
                        '--measurements',
                        action='store_true',
                        help='Export measurements to csv.'
                        )
    parser.add_argument('-o',
                        '--output',
                        metavar='dir',
                        nargs=1,
                        help='Create output files in the specified directory.')

    args = parser.parse_args()

    if args.cli:
        configure_root_logger()
        extractors = get_extractors(measurements=args.measurements,
                                    summaries=args.summaries)
        transformer = TableTransformer(args.cli[0], *extractors)
        transformer.run()
    else:
        appctxt = AppContext()         # 1. Instantiate ApplicationContext
        exit_code = appctxt.run()      # 2. Invoke appctxt.app.exec_()
        sys.exit(exit_code)


if __name__ == "__main__":
    main()
