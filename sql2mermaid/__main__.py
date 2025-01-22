from . import cli
import sys
if __name__ == "__main__":
    cli = cli.CLI()
    cli.run(argv=sys.argv[1:])
