from dq0.sdk.data.metadata.section.meta_section_type import MetaSectionType


class MetaSection:
    @staticmethod
    def merge_many(lst_a, lst_b):
        if lst_a is None:
            return lst_b
        if lst_b is None:
            return lst_a
        merged = []
        for elem_a in lst_a:
            elem_merged = elem_a.copy()
            for elem_b in lst_b:
                if elem_a.merge_precheck_with(elem_b):
                    lst_b.remove(elem_b)
                    elem_merged = elem_a.merge_with(elem_b)
                    break
            merged.append(elem_merged)
        for elem_b in lst_b:
            for elem_a in lst_a:
                if elem_b.merge_precheck_with(elem_a):
                    raise Exception("this can never happen")
            merged.append(elem_b.copy())
        return merged

    def __init__(
            self,
            type_name,
            name=None):
        if not MetaSectionType.isValidTypeName(type_name):
            raise Exception(f"invalid type_name {type_name if type_name is not None else 'None'}")
        self.type_name = type_name
        self.name = name

    def copy(self):
        return MetaSection(self.type_name, self.name)

    def to_dict(self):
        return {
            "type_name": self.type_name,
            "name": self.name,
        }

    def merge_precheck_with(self, other):
        if other is None or self.type_name != other.type_name or self.name != other.name:
            return False
        return True        

    def merge_with(self, other):
        if not self.merge_precheck_with(other):
            raise Exception("cannot merge sections that fail the precheck")
        return self.copy()
