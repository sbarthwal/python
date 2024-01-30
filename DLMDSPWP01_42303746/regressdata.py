from functionOp import IdealFunction

def find_point_on_ideal_fun(point, ideal_functions):
    """
    It computes if a point is within the tolerance of a ideal fun
    :param point: a point with x,y
    :param ideal_functions: list of IdealFunctions
    :return:a tuple containing the closest value if any, and the distance
    """
    current_lowest_val = None
    current_lowest_dist = None

    for ideal_function in ideal_functions:
        try:
            point_t_loc = ideal_function.locate_y_based_on_x(point["x"])
        except IndexError:
            print("point not found")
            raise IndexError

        # calculate distance
        distance = abs(point_t_loc - point["y"])

        if (abs(distance < ideal_function.tolerance)):

            #  find lowest distance
            if ((current_lowest_val == None) or (distance < current_lowest_dist)):
                current_lowest_val = ideal_function
                current_lowest_dist = distance

    return current_lowest_val, current_lowest_dist

def min_loss_ideal_function(training_function, list_of_candidate_functions, loss_function):
    """
    returns an IdealFunction based on a training function and a list of ideal functions
    :param training_function: training function
    :param list_of_candidate_functions: list of candidate ideal functions
    :param loss_function: the function use to minimise the error
    :return: a IdealFunction object
    """
    function_with_smallest_error = None
    smallest_error = None
    for function in list_of_candidate_functions:
        error = loss_function(training_function, function)
        if ((smallest_error == None) or error < smallest_error):
            smallest_error = error
            function_with_smallest_error = function

    ideal_function = IdealFunction(function=function_with_smallest_error, training_function=training_function,
                          error=smallest_error)
    return ideal_function


