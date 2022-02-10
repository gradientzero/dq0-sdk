class InterfaceIterator:
    def __init__(self, interface):
        self.interface = interface
        self.index = -1

    def __iter__(self):
        return self

    def __next__(self):
        self.index += 1
        if len(self.interface) <= self.index:
            raise StopIteration
        if self.index == 0:
            return self.interface.dataset()
        else:
            raise Exception(f"this cannot happen: index {self.index} is out of bounds; len is {len(self.interface)}; "
                            "there should be an access function defined for each index and thus each element in interface")
