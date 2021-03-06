import sys
import argparse
from fbs_runtime.application_context.PyQt5 import ApplicationContext
from logging import getLogger, StreamHandler, INFO, WARNING
from transformer import TableTransformer, get_extractors, MaxLevelFilter


class AppContext(ApplicationContext):
    pass


class CLI():
    def __init__(self):
        self.ctx = AppContext()
        self.APPNAME = self.ctx.build_settings['app_name']
        self.APPVERSION = self.ctx.build_settings['version']
        self.APPAUTHOR = self.ctx.build_settings['author']
        self.logger = self.configure_root_logger()
        self.parser = self.configure_parser()

    def configure_root_logger(self):
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

    def configure_parser(self):
        description = ('Extract measurements or summaries to new csv tables. '
                       'To run in gui mode specify no arguments.')
        epilog = (f'{self.APPNAME} {self.APPVERSION} Copyright (C) 2020 '
                  f'{self.APPAUTHOR} This program comes with ABSOLUTELY NO '
                  'WARRANTY. This is free software, and you are welcome to '
                  'redistribute it under certain conditions. See '
                  '<https://www.gnu.org/licenses/gpl-3.0>.')

        parser = argparse.ArgumentParser(prog=self.APPNAME,
                                         description=description,
                                         epilog=epilog)

        parser.add_argument('-i',
                            '--input',
                            metavar='file',
                            type=str,
                            nargs=1,
                            help=('Process specified file in command line '
                                  'mode.'))
        parser.add_argument('-s',
                            '--summaries',
                            action='store_true',
                            help='Export summaries to csv.')
        parser.add_argument('-m',
                            '--measurements',
                            action='store_true',
                            help='Export measurements to csv.')
        parser.add_argument('-o',
                            '--output',
                            metavar='dir',
                            nargs=1,
                            help=('Write output files to the specified '
                                  'directory.'))
        parser.add_argument('--version', action='version',
                            version=f'{self.APPNAME} {self.APPVERSION}')

        return parser

    def run(self):
        args = self.parser.parse_args()
        extractors = get_extractors(measurements=args.measurements,
                                    summaries=args.summaries)
        transformer = TableTransformer(args.input[0], *extractors)
        transformer.run()
