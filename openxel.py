import openpyxl

# 創建一個新的 Excel 檔案
workbook = openpyxl.Workbook()

# 選擇活動的工作表
sheet = workbook.active

# 你的浮點數陣列
float_array = [1.1, 2.2, 3.3, 4.4, 5.5, 6.6, 7.7, 8.8, 9.9, 10.0]

# 寫入浮點數到一行中的連續單元格
sheet.append(float_array)

# 將數據保存到文件
workbook.save('float_array_example.xlsx')

# 關閉 Excel 文件
workbook.close()