class ListUtils:
    @staticmethod
    def merge_list_of_dicts(list_of_dicts):
        if list_of_dicts is None:
            return None
        merged_dict = {}
        for element in list_of_dicts:
            merged_dict = {**merged_dict, **element}
        if len(merged_dict) == 0:
            return None
        return merged_dict

    @staticmethod
    def list_map_to_dict(list_to_map, request_uuids=None, full=True):
        mapped_list = None
        if list_to_map is not None:
            tmp_list = [tmp_elem.to_dict(request_uuids=request_uuids, full=full) for tmp_elem in list_to_map]
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
