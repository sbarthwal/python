from bokeh.models import Band, ColumnDataSource
from bokeh.layouts import column
from bokeh.plotting import figure, show,output_file
from bokeh.models.widgets import Div


def add_points_in_ideal_function_graph(points_with_details, file_name):
    """
    :param points_with_details: point details
    :param file_name: final html file name.
    """
    div = Div(text=""" <a href="#">Matriculation Id: 42303746</a> Assignment programming with python using dataset 2 submitted by Saurabh Barthwal<b> </b> Used Dataset 2
     """, width=200, height=100)
    plots = []
    for item in points_with_details:
        if item["classification"] is not None:
            p = plot_from_classification_object(item["point"], item["classification"])
            plots.append(p)
    output_file("{}.html".format(file_name))

    show(column(div,*plots))

def create_graph_for_ideal_functions(ideal_functions_array_list, data_file_name):
    """
    Plots all ideal functions
    :param ideal_functions_array_list: all 50 functions
    :param data_file_name: final html file name.
    """
    div = Div(text=""" <a href="#">Matriculation Id: 42303746</a> Assignment programming with python using dataset 2 submitted by Saurabh Barthwal<b> </b> Used Dataset 2
         """, width=200, height=100)
    ideal_functions_array_list.sort(key=lambda ideal_function: ideal_function.training_function.name, reverse=False)
    plots = []
    for ideal_function in ideal_functions_array_list:
        graphP = plot_graph_from_two_functions(function_for_line_plot=ideal_function, function_for_scatter_plot=ideal_function.training_function,
                                          squared_error_for_plot=ideal_function.error)
        plots.append(graphP)

    output_file("{}.html".format(data_file_name))
    # Observe here how unpacking is used to provide the arguments
    show(column(div,*plots))

def plot_from_classification_object(point, ideal_function):
    """
    plot point with tolerance band
    :param point: var has x and y value
    :param ideal_function: function to check value fitting
    """
    if ideal_function is not None:
        classification_function_dataframe = ideal_function.dataframe

        point_value_string = "({},{})".format(point["x"], round(point["y"], 2))
        title_for_graph = "point {} with ideal function: {}".format(point_value_string, ideal_function.name)

        graphP = figure(title=title_for_graph, x_axis_label='x', y_axis_label='y')

        # draw the ideal function
        graphP.line(classification_function_dataframe["x"], classification_function_dataframe["y"],
                legend_label="ideal function", line_width=1, line_color='black')

  #show error margins
        criterion = ideal_function.tolerance
        classification_function_dataframe['upper'] = classification_function_dataframe['y'] + criterion
        classification_function_dataframe['lower'] = classification_function_dataframe['y'] - criterion
        source = ColumnDataSource(classification_function_dataframe.reset_index())
        band = Band(base='x', lower='lower', upper='upper', source=source, level='underlay',
            fill_alpha=0.2, line_width=1, line_color='purple', fill_color="purple")

        graphP.add_layout(band)

        # draw the point
        graphP.scatter([point["x"]], [round(point["y"], 5)], fill_color="orange", legend_label="Given test point", size=10)

        return graphP




def plot_graph_from_two_functions(function_for_scatter_plot, function_for_line_plot, squared_error_for_plot):
    """
    plots a scatter for the train_function and a line for the ideal_function
    :param function_for_scatter_plot: the train function
    :param function_for_line_plot: ideal function
    :param squared_error_for_plot: the squared error will be plotted in the title
    """
    df1 = function_for_scatter_plot.dataframe
    df1_name = function_for_scatter_plot.name

    df2 = function_for_line_plot.dataframe
    df2_name = function_for_line_plot.name

    squared_error_for_plot = round(squared_error_for_plot, 2)
    graphP = figure(title="train function {} vs ideal function {}. with SS Error = {}".format(df1_name, df2_name, squared_error_for_plot),
               x_axis_label='x', y_axis_label='y')
    graphP.scatter(df1["x"], df1["y"], fill_color="red", legend_label="Train")
    graphP.line(df2["x"], df2["y"], legend_label="Ideal", line_width=1)
    return graphP


