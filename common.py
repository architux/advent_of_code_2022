def get_input_data(file_name: str):
    with open(file_name) as input_file:
        return [
            line.rstrip("\n") for line in input_file.readlines()
        ]
