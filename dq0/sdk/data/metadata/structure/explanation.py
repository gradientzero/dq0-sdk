class Explanation:
    @staticmethod
    def dynamic_add_message(explanation=None, message=None):
        if not isinstance(explanation, Explanation) or not isinstance(message, str):
            return
        explanation.add_message(message=message)

    def __init__(self, stack=[]):
        if not isinstance(stack, list):
            raise Exception(f"stack is not of type list, is of type {type(stack)} instead")
        for message in stack:
            if not isinstance(message, str):
                raise Exception(f"message is not of type str, is of type {type(message)} instead")
        self.stack = stack

    def __str__(self):
        return_string = 'Explanation:'
        for index, message in enumerate(self.stack):
            return_string += "\n  " + f"({index}): " + message.replace('\n', "\n  ")
        return return_string

    def __repr__(self):
        return f"Explanation(stack={repr(self.stack)})"

    def add_message(self, message):
        if not isinstance(message, str):
            raise Exception(f"message is not of type str, is of type {type(message)} instead")
        self.stack.append(message)
