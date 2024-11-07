class FortranModule:
    def __init__(self, name, file_path):
        self.name = name
        self.path = file_path

    def print_info(self):
        print(f"Module {self.name} is located at {self.path}")


    