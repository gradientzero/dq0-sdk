class StrUtils:
    @staticmethod
    def str_from(object, quoted=False):
        if object is None:
            return 'null'
        string = str(object)
        return "'" + string + "'" if quoted else string

    @staticmethod
    def restricted_str_from(object, quoted=False, request_uuids=None):
        if object is None:
            return 'null'
        string = object.__str__(request_uuids=request_uuids)
        return "'" + string + "'" if quoted else string

    @staticmethod
    def str_from_list(list, sort=False):
        if list is None:
            return " null"
        if len(list) == 0:
            return " []"
        return_string = ''
        tmp_list = [StrUtils.str_from(tmp_elem, quoted=False) for tmp_elem in list]
        if sort:
            tmp_list.sort()
        for tmp_elem in tmp_list:
            return_string += '\n' + tmp_elem
        return return_string

    @staticmethod
    def restricted_str_from_list(list, sort=False, request_uuids=None):
        if list is None:
            return " null"
        if len(list) == 0:
            return " []"
        return_string = ''
        tmp_list = [StrUtils.restricted_str_from(tmp_elem, quoted=False, request_uuids=request_uuids) for tmp_elem in list]
        if sort:
            tmp_list.sort()
        for tmp_elem in tmp_list:
            return_string += '\n' + tmp_elem
        return return_string
