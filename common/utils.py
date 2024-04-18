def get_last_serializer_error(errors) -> str:
    """ function to get the first error messg from a serializer errors """

    for key in errors:
        error_message =  key + errors[key][0][4:]
    return error_message