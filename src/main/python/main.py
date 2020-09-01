import sys
from gui import AppContext
from cli import CLI


def main(args):
    if len(args) > 0:
        cli = CLI()
        cli.run()
    else:
        appctxt = AppContext()         # 1. Instantiate ApplicationContext
        exit_code = appctxt.run()      # 2. Invoke appctxt.app.exec_()
        sys.exit(exit_code)


if __name__ == "__main__":
    main(sys.argv[1:])
