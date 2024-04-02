pivot_wb = excel.Workbooks.Open(temp_pivot_path, ReadOnly=False, UpdateLinks=0)
data_wb = excel.Workbooks.Open(pivot_config['data_file_path'], ReadOnly=True, UpdateLinks=0)