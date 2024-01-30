import pandas as pd
from sqlalchemy import create_engine


class Function:

    def __init__(self, name):
        """
        :param name: the name the function should have
        """
        self._name = name
        self.dataframe = pd.DataFrame()

    def locate_y_based_on_x(self, x):
        """
        find a Y-Value
        :param x: the x val
        :return: the y val
        """
        # use panda iloc function to find the x and return the corresponding y
        # If it is not found, an exception is raised
        search_key = self.dataframe["x"] == x
        try:
            return self.dataframe.loc[search_key].iat[0, 1]
        except IndexError:
            raise IndexError

    @property
    def name(self):
        """
        fun name
        :return: name as string
        """
        return self._name

    def __iter__(self):
        return self

    _index = 0

    def __next__(self):
        if self._index < len(self.dataframe):
            values = (self.dataframe.iloc[self._index])
            point = {"x": values.x, "y": values.y}
            self._index += 1
            return point
        self._index = 0
        raise StopIteration

    def __sub__(self, other):
        """
        Sub 2 fun
        :rtype: object
        """
        diff = self.dataframe - other.dataframe
        return diff

    @classmethod
    def from_dataframe(cls, name, dataframe):
        """
        create a fun
        with "x" and "y"
        :rtype: a Function
        """
        function = cls(name)
        function.dataframe = dataframe
        function.dataframe.columns = ["x", "y"]
        return function

    def __repr__(self):
        return "Function for {}".format(self.name)

class IdealFunction(Function):
    def __init__(self, function, training_function, error):
        """
        stores ideal function details
        :param function: the ideal function
        :param training_function: the training data the classifying data is based upon
        :param squared_error: the beforehand calculated regression
        """
        super().__init__(function.name)
        self.dataframe = function.dataframe

        self.training_function = training_function
        self.error = error
        self._tolerance_value = 1
        self._tolerance = 1

    def _determine_largest_deviation(self, ideal_function, train_function):
        # Accepts an two functions and substracts them
        # From the resulting dataframe, it finds the one which is largest
        dist = train_function - ideal_function
        dist["y"] = dist["y"].abs()
        largest_deviation = max(dist["y"])
        return largest_deviation

    @property
    def tolerance(self):
        """
        :return: the tolerance
        """
        self._tolerance = self.tolerance_factor * self.largest_deviation
        return self._tolerance

    @tolerance.setter
    def tolerance(self, value):
        self._tolerance = value

    @property
    def tolerance_factor(self):
        """
        Set the factor of the largest_deviation to determine the tolerance
        :return:
        """
        return self._tolerance_value

    @tolerance_factor.setter
    def tolerance_factor(self, value):
        self._tolerance_value = value

    @property
    def largest_deviation(self):
        """
        Retrieves the largest deviation with training function it is based upon
        :return: the largest deviation
        """
        largest_deviation = self._determine_largest_deviation(self, self.training_function)
        return largest_deviation
class FunctionOperator:

    def __init__(self, path_of_csv):
        """
        Parses a local .csv as a list of Functions.
        :param path_of_csv: local path of the csv
        """
        self._functions = []

        # get the data frame
        try:
            self._function_data = pd.read_csv(path_of_csv)
        except FileNotFoundError:
            print("Error in file reading {}".format(path_of_csv))
            raise

        # Get the x value.
        x_values = self._function_data["x"]

        # Read remaining.
        for name_of_column, data_of_column in self._function_data.items():
            if "x" in name_of_column:
                continue
            # We already stored the x column, we now have the y colum. We can stick them together with the concat function
            subset = pd.concat([x_values, data_of_column], axis=1)
            function = Function.from_dataframe(name_of_column, subset)
            self._functions.append(function)

    def save_to_sql_db(self, file_name, suffix):
        """
        save into sql db

        :param file_name: name of the db as a file
        :param suffix: will be added to the columns
        """

        engine = create_engine('sqlite:///{}.db'.format(file_name), echo=True)

        function_data_for_db = self._function_data.copy()
        function_data_for_db.columns = [name.capitalize() + suffix for name in function_data_for_db.columns]
        function_data_for_db.set_index(function_data_for_db.columns[0], inplace=True)

        function_data_for_db.to_sql(
            file_name,
            engine,
            # if file exists replace it.
            if_exists="replace",
            index=True,
        )

    @property
    def functions(self):
        """
        :rtype: object
        """
        return self._functions

    def __iter__(self):
        return self

    _index = 0

    def __next__(self):

        self._function_manager = self.functions
        if self._index < len(self._function_manager):
            value_requested = self._function_manager[self._index]
            self._index = self._index + 1
            return value_requested
        self._index = 0
        raise StopIteration

    def __repr__(self):
        return "Total {} number of functions".format(len(self.functions))





