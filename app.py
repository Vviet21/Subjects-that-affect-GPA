from flask import Flask, render_template, request, jsonify,  url_for ,redirect,send_file
import sqlite3
import pandas as pd 
import seaborn as sns
import matplotlib.pyplot as plt
from draw import create_df,create_datamerged
import numpy as np
import os
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split




df_moi,mon_hoc_theo_nganh = create_df()

app = Flask(__name__)

stored_data = {}

def get_db_connection():
    conn = sqlite3.connect('my_database.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/nhapdiem')
def nhapdiem():
    return render_template('nhapdiem.html')

@app.route('/upload_excel', methods=['POST'])
def upload_excel():
    global stored_data
    data = request.get_json()
    excel_data = data.get('monHocDetails')
    nganh_hoc = data.get('nganh')
    khoa = data.get('nienkhoa')
    gpa = data.get('gpa')
   
    df = pd.DataFrame(excel_data)
    stored_data = {
        'nganh_hoc': nganh_hoc,
        'khoa': khoa,
        'gpa': gpa,
        'df': df
    }
    
    
    print('Nganh : ',nganh_hoc,'Khoa : ',khoa," GPA : ",gpa )
    print(df)
   
    return jsonify({'message': 'Excel data received and processed successfully'})


@app.route('/api/chuongtrinhdaotao', methods=['GET'])
def get_chuongtrinhdaotao():
    nganh = request.args.get('nganh')
    nienkhoa = request.args.get('nienkhoa')
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM my_table WHERE Ngành = ? AND Khóa = ?", (nganh, nienkhoa))
    rows = cursor.fetchall()
    conn.close()
    chuong_trinh_dao_tao = [dict(row) for row in rows]
    print(chuong_trinh_dao_tao)
    for i, item in enumerate(chuong_trinh_dao_tao):
        item['stt'] = i + 1
    return jsonify(chuong_trinh_dao_tao)


@app.route('/ketqua')
def ketqua():
    return render_template('ketqua.html')

@app.route('/vebieudo', methods=['GET'])
def vebieudo():
    global stored_data

    file_path1 = draw_grade(stored_data['nganh_hoc'])
    file_path2 = draw_gpa(stored_data['nganh_hoc'],float(stored_data['gpa']))
    return jsonify({'message': 'Biểu đồ đã được vẽ', 'file_path': [file_path1,file_path2]})

@app.route('/sosanh', methods=['POST'])
def sosanh():
    ma_mon_hoc = request.form['ma-mon-hoc']
    global stored_data
    df = pd.DataFrame(stored_data['df'])
    nganh = stored_data['nganh_hoc']

    row = df.loc[df['mamonHoc'] == ma_mon_hoc].values
    if len(row) == 0:
        return jsonify({'message': 'Không tìm thấy mã môn học'})

    ten_mon_hoc = row[0][1]
    diem_mon_hoc = row[0][2]
    tin_chi_ = row[0][3]

    print((nganh, ten_mon_hoc, tin_chi_, ma_mon_hoc, diem_mon_hoc))
    file_path = draw_hist_hp(nganh, ten_mon_hoc, tin_chi_, ma_mon_hoc, diem_mon_hoc)
    
    if (file_path )is None:
        return jsonify({'message': 'Lỗi khi vẽ biểu đồ'})

    return jsonify({'message': 'Biểu đồ đã được vẽ', 'file_path': file_path})

@app.route('/show_image')
def show_image():
    global stored_data

    nganh = stored_data['nganh_hoc']
    image_path = os.path.join('static', 'image', f'{nganh}_impact.png')  # Đường dẫn tới ảnh
    return send_file(image_path, mimetype='image/png')



# Vẽ biểu đồ tròn
def draw_grade(nganh):
    file_path = 'static/image_result/grade_plot.png'

    if os.path.exists(file_path):
        os.remove(file_path)
    df_moi,mon_hoc_theo_nganh = create_df()
    df = pd.concat([df_moi.iloc[:,[0,1,-2,-1]].loc[df_moi['Ngành']==nganh],df_moi.loc[df_moi['Ngành']==nganh].iloc[:,np.where(np.isin(df_moi.columns.get_level_values('Mã HP'),list(mon_hoc_theo_nganh[nganh])))[0]]],axis=1)

    labels = sorted(df.Grade.unique())
    sizes = df.Grade.value_counts().sort_index()

    plt.figure(figsize=(8, 8))
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
    plt.axis('equal')
    plt.title('Grade của ngành '+ nganh)
    plt.savefig(file_path,dpi=300)
    return file_path



# Vẽ biểu đồ cột



def draw_gpa(nganh,my_gpa):
    file_path = 'static/image_result/gpa_plot.png'

    if os.path.exists(file_path):
        os.remove(file_path)
    df_moi,mon_hoc_theo_nganh = create_df() 
    df = pd.concat([df_moi.iloc[:,[0,1,-2,-1]].loc[df_moi['Ngành']==nganh],df_moi.loc[df_moi['Ngành']==nganh].iloc[:,np.where(np.isin(df_moi.columns.get_level_values('Mã HP'),list(mon_hoc_theo_nganh[nganh])))[0]]],axis=1)
    

    plt.figure(figsize=(8, 8))
    sns.histplot(df['GPA'], bins=15, kde=True, color='blue', label='GPA của toàn bộ sinh viên')

    plt.axvline(my_gpa, color='red', linestyle='--', linewidth=2, label=f'GPA của bạn: {my_gpa}')

    plt.title('Phân phối GPA của toàn bộ sinh viên trong ngành'+ nganh)
    plt.xlabel('GPA')
    plt.ylabel('Số lượng sinh viên')
    plt.legend()
    plt.savefig(file_path)
    return file_path


# Biểu đồ scatter điểm môn học và GPA của ngành
# def draw_scatter_hp(nganh,tenhp,tinchi,mahp):
#     df_moi,mon_hoc_theo_nganh = create_df()
#     df = pd.concat([df_moi.iloc[:,[0,1,-2,-1]].loc[df_moi['Ngành']==nganh],df_moi.loc[df_moi['Ngành']==nganh].iloc[:,np.where(np.isin(df_moi.columns.get_level_values('Mã HP'),list(mon_hoc_theo_nganh[nganh])))[0]]],axis=1)
#     file_path = 'static/image_result/scatter_tenhp_plot.png'

#     if os.path.exists(file_path):
#         os.remove(file_path)

#     z = (tenhp,tinchi,mahp)

#     plt.figure(figsize=(8, 8))
#     sns.scatterplot(data=df, x=df.columns[df.columns.get_level_values('Mã HP')==mahp], y='GPA')

#     plt.title(f'{tenhp} {nganh} vs GPA')
#     plt.xlabel(f'Điểm môn {tenhp}')
#     plt.ylabel('GPA')
#     plt.savefig(file_path,dpi=300)
#     plt.close()
#     return file_path
# Biểu đồ cột điểm môn học của sinh viên với điểm của cả ngành
def draw_hist_hp(nganh,tenhp,tinchi,mahp,diem):
    df_moi,mon_hoc_theo_nganh = create_df()
    df = pd.concat([df_moi.iloc[:,[0,1,-2,-1]].loc[df_moi['Ngành']==nganh],df_moi.loc[df_moi['Ngành']==nganh].iloc[:,np.where(np.isin(df_moi.columns.get_level_values('Mã HP'),list(mon_hoc_theo_nganh[nganh])))[0]]],axis=1)
    file_path = 'static/image_result/hist_tenhp_plot.png'

    if os.path.exists(file_path):
        os.remove(file_path)

    plt.figure(figsize=(8, 8))
    sns.histplot(df[tenhp], bins=10, kde=True, color='blue', label='Điểm của toàn bộ sinh viên')

    plt.axvline(diem, color='red', linestyle='--', linewidth=2, label=f'Điểm của bạn: {diem}')

    plt.title(f'{tenhp} của toàn bộ sinh viên trong ngành'+nganh)
    plt.xlabel('Điểm')
    plt.ylabel('Số lượng sinh viên')
    plt.legend()
    plt.savefig(file_path,dpi=300)
    plt.close()
    return file_path
if __name__ == '__main__':
    app.run(debug=True)
