# -*- coding: utf-8 -*-
"""Utils package contains helper functions for the SDK API

Copyright 2020, Gradient Zero
All rights reserved
"""

from dq0sdk.errors import DQ0SDKError


def check_signature(code, name):
    """check method signatures. Used by set_code functions."""
    if code is None:
        return None
    wrong_signature_error = 'Wrong function signature. '\
                            'Should start with "def {}():" '\
                            'or "def {}(self). '\
                            '(Static function will be changed to '\
                            'member function automatically.)"'\
                            .format(name, name)
    try:
        def_start_index = code.index('def {}('.format(name))
        if def_start_index != 0:
            raise DQ0SDKError('{}. {}'.format(name, wrong_signature_error))
        def_end_index = code.index(':')
        code = code.replace(code[:def_end_index], 'def {}(self)'.format(name))
    except ValueError:
        raise DQ0SDKError('{}. {}'.format(name, wrong_signature_error))
    return code


def replace_function(lines, code):  # noqa: C901
    """Replace functions code. Used my set_code functions."""
    search = code[:code.index(':')]
    new_lines = []
    code_lines = code.split('\n')
    code_lines_index = 1  # skip signature
    in_function = False
    indent = -1
    line_index = 0
    filling = False
    for line in lines:
        line_index = line_index + 1
        if indent == -1:
            try:
                indent = line.index(search)
                # if search was not found ValueError is thrown.
                space_char = '\t' if line[:1] == '\t' else ' '
                in_function = True
                # use original function signature
                new_lines.append(line)
            except ValueError:
                pass
        else:
            if in_function:
                len_indent = len(line) - len(line.lstrip())
                if line_index == len(lines) or (len(line) > 1 and len_indent == indent):
                    in_function = False
            filling = False
            while True:
                # replace function
                if code_lines_index < len(code_lines):
                    code_line = code_lines[code_lines_index]
                    num_code_spaces = len(code_line) - len(code_line.lstrip())
                    if space_char == '\t':
                        if code_line[:1] == ' ':
                            num_code_spaces = int(num_code_spaces / 4)
                        num_code_spaces = num_code_spaces + 1
                    else:
                        num_code_spaces = num_code_spaces + 4
                    code_spaces = space_char.join(['' for i in range(num_code_spaces + 1)])
                    new_lines.append(code_spaces + code_line.lstrip() + '\n')
                    code_lines_index = code_lines_index + 1
                if in_function or code_lines_index == len(code_lines):
                    break
                else:
                    filling = True
        if not filling and not in_function:
            # keep other code
            new_lines.append(line)
    if len(new_lines) == 0 or code_lines_index == 1:
        raise DQ0SDKError('Function to replace not found in py file')
    return new_lines


def replace_model_parent_class(lines, parent_class_name):
    """Replace parent class. Used my set_code functions."""
    new_lines = []
    for line in lines:
        try:
            index = line.index('from dq0sdk.models')
            if index == 0:
                line = 'from dq0sdk.models.tf.neural_network import NeuralNetwork\n'
        except ValueError:
            pass
        try:
            line.index('class UserModel(')
            line = 'class UserModel(NeuralNetwork):\n'
        except ValueError:
            pass
        new_lines.append(line)
    return new_lines


def replace_data_parent_class(lines, parent_class_name):
    """Replace parent class. Used my set_code functions."""
    new_lines = []
    for line in lines:
        try:
            index = line.index('from dq0sdk.data')
            if index == 0:
                line = 'from dq0sdk.data.csv.csv_source import CSVSource\n'
        except ValueError:
            pass
        try:
            line.index('class UserSource(')
            line = 'class UserSource(CSVSource):\n'
        except ValueError:
            pass
        new_lines.append(line)
    return new_lines
