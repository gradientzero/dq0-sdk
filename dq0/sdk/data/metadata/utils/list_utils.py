class ListUtils:
    @staticmethod
    def list_map_to_dict(list, request_uuids=None):
        mapped_list = None
        if list is not None:
            tmp_list = [tmp_elem.to_dict(request_uuids=request_uuids) for tmp_elem in list]
            tmp_list = [tmp_elem for tmp_elem in tmp_list if tmp_elem is not None]
            if len(tmp_list) != 0:
                mapped_list = tmp_list
        return mapped_list

    @staticmethod
    def list_equals_unordered(list_a, list_b):
        if list_a is None and list_b is None:
            return True
        if list_a is None or list_b is None:
            return False
        tmp_list = list_b.copy()
        for elem in list_a:
            found_match = False
            for tmp_elem in tmp_list:
                if elem == tmp_elem:
                    found_match = True
                    tmp_list.remove(tmp_elem)
                    break
            if not found_match:
                return False
        return len(tmp_list) == 0
