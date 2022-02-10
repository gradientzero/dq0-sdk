class EntityIterator:
    def __init__(self, entity):
        self.entity = entity
        self.index = -1

    def __iter__(self):
        return self

    def __next__(self):
        self.index += 1
        if len(self.entity) <= self.index:
            raise StopIteration
        return self.entity.get_child_entity(index=self.index)
