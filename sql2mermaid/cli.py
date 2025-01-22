import argparse
from . import sql2mermaid, open_sql_file


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
            required=True,
        )
        return parser.parse_args(argv)

    def run(self, argv):
        """Main function"""
        args = self.parse_cli(argv)
        input_file = args.input
        input_query = open_sql_file(input_file)
        output = sql2mermaid(input_query)
        print("output :", output)
