def ss_error(first_function, second_function):
    """
    Calculates the squared error to another function
    :param other_function:
    :return: the ss error
    """
    Calculate_distances = second_function - first_function
    Calculate_distances["y"] = Calculate_distances["y"] ** 2
    total_deviation_forFunction = sum(Calculate_distances["y"])
    return total_deviation_forFunction

