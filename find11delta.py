import pandas as pd

class ExcelData:
    def __init__(self, file_path):
        self.file_path = file_path
        self.data = pd.read_excel(file_path)

    def calculate_delta(self, other):
        if not isinstance(other, ExcelData):
            raise ValueError("The other object must be an instance of ExcelData.")

        common_columns = self.data.columns.intersection(other.data.columns)
        delta_df = self.data[common_columns] - other.data[common_columns]
        return delta_df

# Example usage
data1 = ExcelData('file1.xlsx')
data2 = ExcelData('file2.xlsx')
delta = data1.calculate_delta(data2)
print(delta)