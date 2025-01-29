import argparse
from . import mermaid_generator, open_sql_file


class CLI:
    """CLI for sql2mermaid module"""

    @staticmethod
    def parse_cli(argv):
        parser = argparse.ArgumentParser(description=__doc__)

        parser.add_argument(
            "--input",
            "--input_file",
            type=str,
            help="Path to the .sql file",
            required=False,
        )
        parser.add_argument(
            "--query",
            type=str,
            help="Query you want to convert to mermaid",
            required=False
        )
        return parser.parse_args(argv)

    def run(self, argv):
        """Main function"""
        args = self.parse_cli(argv)
        input_file = args.input
        query = args.query
        if query:
            output = mermaid_generator(query)
            print("output : ", output)
        elif input_file:
            input_query = open_sql_file(input_file)
            output = mermaid_generator(input_query)
            print("output :", output)
        else:
            raise argparse.ArgumentError(
                "You need to specify at least one argument")
