from unittest import TestCase
import pandas as pd
from functionOp import Function
from difffunction import ss_error

class Test(TestCase):
    def setUp(self):

        data1 = {"x":[10.0,11.0,12.0],"y":[13.0,14.0,15.0]}
        self.dataframe1 = pd.DataFrame(data=data1)

        data2 = {"x":[10.0,11.0,12.0], "y":[13.0,14.0,15.0]}
        self.dataframe2 = pd.DataFrame(data=data2)

        self.function1 = Function("name")
        self.function1.dataframe = self.dataframe1

        self.function2 = Function("name")
        self.function2.dataframe = self.dataframe2



    def tearDown(self):
        pass

    def test_squared_error(self):
        # case 1: simple test if loss function computes correct value
        self.assertEqual(ss_error(self.function1, self.function2), 00.0)
        # case 2: simple test if loss function is associative
        self.assertEqual(ss_error(self.function2, self.function1), 00.0)
        # case 3: check if regression of two equal functions is 0
        self.assertEqual(ss_error(self.function1, self.function1), 00.0)


