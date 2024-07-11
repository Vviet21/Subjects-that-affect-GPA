from sqlalchemy import create_engine
import pandas as pd
import sqlite3
# Tạo kết nối tới cơ sở dữ liệu SQLite
engine = create_engine('sqlite:///my_database.db')

# df = pd.read_csv("CDTN-1\\tonghop.csv")
# bang3 = pd.read_csv("CDTN-1\\bang3.csv")

# #TA
# cot_tenmon = ['Logic, suy luận toán học và kỹ thuật đếm','Tin đại cương','Giải tích 1','Giải tích 2','Đại số tuyến tính','Xác suất','Thống Kê','Tối ưu hóa','Toán rời rạc','Cấu trúc dữ liệu','Ngôn ngữ lập trình','Kỹ thuật số'
#              ,'Lập trình hướng đối tượng','Kiến trúc máy tính','Cơ sở dữ liệu','Mạng máy tính','Phân tích và thiết kế thuật toán','Thống kê nâng cao','Các công cụ lập trình trí tuệ nhân tạo','Học máy','Học sâu','Hệ thống thông tin'
#              ,'Trí tuệ nhân tạo và công nghệ tri thức','An toàn thông tin','Dữ liệu lớn','Xử lý ngôn ngữ tự nhiên','Thị giác máy tính','Thực tập ngành Trí tuệ nhân tạo','KLTN ngành Trí tuệ nhân tạo','CĐTN: Ngành Trí tuệ nhân tạo']

# cot_ma    =  ['MA101','CS100','MA110','MA111','MA120','MA230','MA234','MI302', 'MI201' ,'CF212' ,'CS121' ,'CS110' ,'CS122' ,'CS212' ,'IS222' ,'NW212' ,'CF211'
#               ,'MA238' ,'AI220' ,'CS320' ,'AI310' ,'IS314' ,'MI322' ,'IS345' ,'IS330' ,'AI320' ,'AI321' ,'IP405' ,'AI499' ,'AI485']

# cot_tin   =  [3, 2, 3, 3, 3, 3, 2, 2, 3 ,3 ,3 ,2 ,3 ,3 ,3 ,2 ,2 ,3 ,3 ,3 ,3 ,3 ,3 ,3 ,2 ,3 ,3 ,3 ,6 ,6 ]
# cot_nganh =  ['TA'] * len(cot_tin)
# cot_khoa  =  [33] * len(cot_tin)
# cot_kieu  =  [1] * len(cot_tin)

# bang3_TA = pd.DataFrame({'Khóa':cot_khoa,'Mã HP':cot_ma,'Tên HP':cot_tenmon,'Số TC':cot_tin,'Ngành':cot_nganh,'Kiểu môn':cot_kieu})
# bang3_tonghop = pd.concat([bang3,bang3_TA]).reset_index(drop=True)



# df = df.drop(columns='Điểm').drop_duplicates(subset=['Mã HP', 'Tên HP', 'Ngành', 'Khóa'])

# data_merged = pd.merge(df, bang3_tonghop[['Mã HP', 'Ngành','Kiểu môn']], on=['Mã HP', 'Ngành'], how='left')
# if 'Kiểu môn_y' in data_merged.columns:
#     data_merged['Kiểu môn'] = data_merged['Kiểu môn_y'].combine_first(data_merged['Kiểu môn_x'])
#     data_merged = data_merged.drop(columns=['Kiểu môn_x', 'Kiểu môn_y'])
# data_merged = data_merged.drop_duplicates(subset=['Mã HP', 'Tên HP', 'Ngành', 'Khóa'])

# data_merged.to_sql('my_table', con=engine, if_exists='replace', index=False)
# nganh = input("Nhập ngành: ")
# khoa = input("Nhập khóa: ")

conn = sqlite3.connect('my_database.db')
cur = conn.cursor()

query = "SELECT * FROM my_table WHERE Ngành = 'TT' "
cur.execute(query)

rows = cur.fetchall()

for row in rows:
    print(row)

conn.close()
