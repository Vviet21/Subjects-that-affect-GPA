from flask import Flask, render_template, request, jsonify,  url_for
import sqlite3
import pandas as pd 
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import os



# Đọc dữ liệu 
def create_df():
    df_moi =  pd.read_csv("data\\data_moi_moi.csv",header=[0,1,2],index_col=0)
    nganh_pop = df_moi.pop('Ngành')
    df_moi.insert(0,'Ngành',nganh_pop)

    khoa_pop = df_moi.pop('Khóa')
    df_moi.insert(1,'Khóa',khoa_pop)

    grade_pop = df_moi.pop('Grade')
    df_moi['Grade'] = grade_pop

    gpa_pop = df_moi.pop('GPA')
    df_moi['GPA'] = gpa_pop

    df_moi['Khóa'] = (df_moi['Khóa']).astype(int)
    df_moi = (df_moi.sort_values(by='Khóa'))
    df_moi = df_moi.reset_index(drop=True)


    # Tìm ra môn theo ngành 
    ma_mon_tong_hop = pd.read_csv('data\\tonghop.csv')
    ma_mon_tong_hop = ma_mon_tong_hop.sort_values('Khóa')

    mon_hoc_theo_nganh = {}
    cac_nganh = ma_mon_tong_hop['Ngành'].unique()
    for nganh in cac_nganh:
        mon_hoc_theo_nganh[nganh] = set(ma_mon_tong_hop[ma_mon_tong_hop['Ngành'] == nganh]['Mã HP'])
    
    return df_moi,mon_hoc_theo_nganh


def create_datamerged():
    
    df = pd.read_excel("data\\data_merged.xlsx")
    return df

# Phân chia các ngành 

# TI = pd.concat([df_moi.iloc[:,[0,1,-2,-1]].loc[df_moi['Ngành']=='TI'],df_moi.loc[df_moi['Ngành']=='TI'].iloc[:,np.where(np.isin(df_moi.columns.get_level_values('Mã HP'),list(mon_hoc_theo_nganh['TI'])))[0]]],axis=1)

# TT = pd.concat([df_moi.iloc[:,[0,1,-2,-1]].loc[df_moi['Ngành']=='TT'],df_moi.loc[df_moi['Ngành']=='TT'].iloc[:,np.where(np.isin(df_moi.columns.get_level_values('Mã HP'),list(mon_hoc_theo_nganh['TT'])))[0]]],axis=1)

# TE = pd.concat([df_moi.iloc[:,[0,1,-2,-1]].loc[df_moi['Ngành']=='TE'],df_moi.loc[df_moi['Ngành']=='TE'].iloc[:,np.where(np.isin(df_moi.columns.get_level_values('Mã HP'),list(mon_hoc_theo_nganh['TE'])))[0]]],axis=1)

# TC = pd.concat([df_moi.iloc[:,[0,1,-2,-1]].loc[df_moi['Ngành']=='TC'],df_moi.loc[df_moi['Ngành']=='TC'].iloc[:,np.where(np.isin(df_moi.columns.get_level_values('Mã HP'),list(mon_hoc_theo_nganh['TC'])))[0]]],axis=1)

# TA = pd.concat([df_moi.iloc[:,[0,1,-2,-1]].loc[df_moi['Ngành']=='TA'],df_moi.loc[df_moi['Ngành']=='TA'].iloc[:,np.where(np.isin(df_moi.columns.get_level_values('Mã HP'),list(mon_hoc_theo_nganh['TA'])))[0]]],axis=1)

# TM = pd.concat([df_moi.iloc[:,[0,1,-2,-1]].loc[df_moi['Ngành']=='TM'],df_moi.loc[df_moi['Ngành']=='TM'].iloc[:,np.where(np.isin(df_moi.columns.get_level_values('Mã HP'),list(mon_hoc_theo_nganh['TM'])))[0]]],axis=1)




