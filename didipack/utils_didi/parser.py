import sys
import pandas as pd

class Argument(pd.Series):
    def get_value(self, v: str):
        if v in self.index:
            return self[v]
        else:
            return 0

    def __getattr__(self, name: str):
        return self.get_value(name)

def didi_parse():
    # Default values for positional arguments
    first_pos = 0
    second_pos = 0
    third_pos = 0

    # Dictionary to hold named arguments with default value 0
    named_args = {}

    # List to hold remaining positional arguments
    positional_args = []

    # Parse through command-line arguments
    iterator = iter(sys.argv[1:])
    for arg in iterator:
        if arg.startswith('--'):
            # Remove leading '--' and split at the '=' to get key and value
            key, value = arg[2:].split('=')
            named_args[key] = value
        else:
            positional_args.append(arg)

    # Fill in positional arguments if they exist
    if len(positional_args) >= 1:
        first_pos = positional_args[0]
    if len(positional_args) >= 2:
        second_pos = positional_args[1]
    if len(positional_args) >= 3:
        third_pos = positional_args[2]

    # Combine positional and named arguments in one dictionary
    all_args = {'first': first_pos, 'second': second_pos, 'third': third_pos}
    all_args.update(named_args)

    # Create an arguemnt to output
    args = Argument(all_args)

    return args

if __name__ == "__main__":
    result = didi_parse()
