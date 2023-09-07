import sys
import pandas as pd

def convert_to_int(value):
    if isinstance(value, int):
        return value
    elif isinstance(value, str):
        if value.isdigit():
            return int(value)
    return value


class Argument(pd.Series):
    def get_value(self, v: str):
        if v in self.index:
            return self[v]
        else:
            return 0

    def __getattr__(self, name: str):
        return self.get_value(name)

def parse():
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
            named_args[key] = convert_to_int(value)
        else:
            positional_args.append(arg)

    # Fill in positional arguments if they exist
    if len(positional_args) >= 1:
        first_pos = convert_to_int(positional_args[0])
    if len(positional_args) >= 2:
        second_pos = convert_to_int(positional_args[1])
    if len(positional_args) >= 3:
        third_pos = convert_to_int(positional_args[2])

    # Combine positional and named arguments in one dictionary
    all_args = {'a': first_pos, 'b': second_pos, 'c': third_pos}
    all_args.update(named_args)

    # Create an arguemnt to output
    args = Argument(all_args)

    return args

if __name__ == "__main__":
    result = parse()
