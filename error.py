class Error:
    def __init__(self):
        pass

    def no_verb(self):
        print(
            "------\n"
            "[ERROR]:"
            "Requested verb is not in dictionary!\n"
            "Try to add new verbs following the README.md file instructions\n"
        )

    def no_file(self, param):
        print(
            "------\n"
            "[ERROR]: "
            "Bad verb's definition for \"" + param + "\"! Check the dictionary!\n"
        )

    def bad_definition(self):
        print(
            "[ERROR]:"
            "Bad definition of requested verb in dictionary!\n"
            "Check the order of parameter definition\n"
        )
