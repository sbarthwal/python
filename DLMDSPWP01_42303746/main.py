import math

from graphplot import (add_points_in_ideal_function_graph,create_graph_for_ideal_functions)
from functionOp import FunctionOperator
from difffunction import ss_error
from regressdata import min_loss_ideal_function,find_point_on_ideal_fun
from datautil import write_results_to_db

# This constant is the factor for the criterion
ALLOW_ERROR_FECTOR = math.sqrt(2)

if __name__ == '__main__':
    # Taking Data As input
    ideal_functions_file_path = "data/ideal2.csv"
    train_functions_file_path = "data/train2.csv"

    # Creating function object with data values
    ideal_function_data_manager = FunctionOperator(path_of_csv=ideal_functions_file_path)
    train_function_data_manager = FunctionOperator(path_of_csv=train_functions_file_path)
    print(ideal_function_data_manager)
    print(train_function_data_manager)
    # saving data into db
    train_function_data_manager.save_to_sql_db(file_name="output/training", suffix=" (training func)")
    ideal_function_data_manager.save_to_sql_db(file_name="output/ideal", suffix=" (ideal func)")

    # now find the ideal function and create a list of ideal function
    ideal_functions_array = []
    for single_train_function in train_function_data_manager:
        # minimise_loss is able to compute the best fitting function given the train function
        ideal_function = min_loss_ideal_function(training_function=single_train_function,
                                                 list_of_candidate_functions=ideal_function_data_manager.functions,
                                                 loss_function=ss_error)
        ideal_function.tolerance_factor = ALLOW_ERROR_FECTOR
        ideal_functions_array.append(ideal_function)

    # plot ideal graphs
    create_graph_for_ideal_functions(ideal_functions_array, "output/traningwithIdealFunction")

    #test points
    test_data_file_path = "data/test2.csv"
    test_function_op = FunctionOperator(path_of_csv=test_data_file_path)
    test_fun = test_function_op.functions[0]

    points_with_ideal_function = []
    for point in test_fun:
        ideal_function, delta_y = find_point_on_ideal_fun(point=point, ideal_functions=ideal_functions_array)
        result = {"point": point, "classification": ideal_function, "delta_y": delta_y}
        points_with_ideal_function.append(result)


    # plot the test points
    add_points_in_ideal_function_graph(points_with_ideal_function, "output/testWithIdealFunction")

    # Finally Save the results
    write_results_to_db(points_with_ideal_function)
    

    print("Completed successfully")



