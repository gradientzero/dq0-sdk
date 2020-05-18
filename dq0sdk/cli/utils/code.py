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
    try:
        search = code[:code.index(':')]
    except ValueError:
        raise DQ0SDKError('Wrong function definition')
    new_lines = []
    code_lines = code.split('\n')
    code_lines_index = 1  # skip signature
    in_function = False
    indent = -1
    line_index = 0
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
            while True:
                # replace function
                if code_lines_index < len(code_lines):
                    code_line = code_lines[code_lines_index]
                    code_spaces = _get_code_spaces(code_line, space_char)
                    new_lines.append(code_spaces + code_line.lstrip() + '\n')
                    code_lines_index = code_lines_index + 1
                if in_function or code_lines_index == len(code_lines):
                    break
        if not in_function:
            # keep other code
            new_lines.append(line)
    if len(new_lines) == 0 or code_lines_index == 1:
        raise DQ0SDKError('Function to replace not found in py file')
    return new_lines


def add_function(lines, code):
    """Add the given code to the end of lines."""
    new_lines = []
    try:
        search = code[:code.index(':')]
    except ValueError:
        raise DQ0SDKError('Wrong function definition')
    indent = -1
    space_char = ' '
    for line in lines:
        if indent == -1:
            try:
                indent = line.index(search)
                space_char = '\t' if line[:1] == '\t' else ' '
            except ValueError:
                pass
        new_lines.append(line)
    new_lines.append('\n')
    if indent == -1:
        indent = 0
    code_lines = code.split('\n')
    for code_line in code_lines:
        code_spaces = _get_code_spaces(code_line, space_char, number_of_leading_chars=indent)
        new_lines.append(code_spaces + code_line.lstrip() + '\n')
    return new_lines


def _get_code_spaces(code_line, space_char, number_of_leading_chars=0):
    """Helper function to get leading spaces."""
    num_code_spaces = len(code_line) - len(code_line.lstrip())
    num_code_spaces = num_code_spaces + number_of_leading_chars
    if space_char == '\t':
        if code_line[:1] == ' ':
            num_code_spaces = int(num_code_spaces / 4)
        num_code_spaces = num_code_spaces + 1
    else:
        num_code_spaces = num_code_spaces + 4
    return space_char.join(['' for i in range(num_code_spaces + 1)])


def replace_model_parent_class(lines, parent_class_name):  # noqa: C901
    """Replace parent class. Used my set_code functions."""
    new_lines = []
    for line in lines:
        try:
            index = line.index('from dq0sdk.models')
            if index == 0:
                if parent_class_name == 'NeuralNetwork':
                    line = 'from dq0sdk.models.tf.neural_network import NeuralNetwork\n'
                elif parent_class_name == 'NeuralNetworkClassification':
                    line = 'from dq0sdk.models.tf.neural_network_classification import NeuralNetworkClassification\n'
                elif parent_class_name == 'NeuralNetworkMultiClassClassification':
                    line = 'from dq0sdk.models.tf.neural_network_multiclass_classification import NeuralNetworkMultiClassClassification\n'
                elif parent_class_name == 'NeuralNetworkRegression':
                    line = 'from dq0sdk.models.tf.neural_network_regression import NeuralNetworkRegression\n'
                elif parent_class_name == 'NeuralNetworkYaml':
                    line = 'from dq0sdk.models.tf.neural_network_yaml import NeuralNetworkYaml\n'
        except ValueError:
            pass
        try:
            line.index('class UserModel(')
            line = 'class UserModel({}):\n'.format(parent_class_name)
        except ValueError:
            pass
        new_lines.append(line)
    return new_lines
