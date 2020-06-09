class Error:
    def __init__(self):
        pass

    def no_verb(self):
        print("[ERROR]:\n"
              "Requested verb is not in dictionary!\n"
              "Try to add new verbs following the README.md file instructions"
        )

    def no_file(self, module):
        print(
            "[ERROR]: "
            "Bad verb's definition. Check the dictionary!"
        )
