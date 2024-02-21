import pandas as pd

class DataDifference:
    def calculate(self, df1, df2):
        common_columns = df1.columns.intersection(df2.columns)
        delta_df = df1[common_columns] - df2[common_columns]
        return delta_df

class ExcelData:
    def __init__(self, file_path):
        self.file_path = file_path
        self.data = pd.read_excel(file_path)
        self.difference_calculator = DataDifference()

    def calculate_delta(self, other):
        if not isinstance(other, ExcelData):
            raise ValueError("The other object must be an instance of ExcelData.")

        return self.difference_calculator.calculate(self.data, other.data)

# Example usage
data1 = ExcelData('file1.xlsx')
data2 = ExcelData('file2.xlsx')
delta = data1.calculate_delta(data2)
print(delta)