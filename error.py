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
            "Seems a motion is not defined for parameter: \"" + param +
            "\"! Check the dictionary and ./motions directory!\n"
        )

    def bad_definition(self):
        print(
            "[ERROR]:"
            "Bad definition of requested verb in dictionary!\n"
            "Check if all the parameters are defined and their order of definition\n"
        )

    def bad_time_definition(self):
        print(
            "[ERROR]:"
            "Bad TIME definition of requested verb in dictionary!\n"
            "Check \"speed\" parameter\n"
        )
