# -*- coding: utf-8 -*-
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.pylab import rcParams
import seaborn as sns
import numpy as np
from datetime import datetime
import os

def read_file(filename):
    df = pd.read_csv(os.path.join("./Data/", filename))
    return df

def convert_months(refer_date,clean_df,column):
    time_delta=refer_date-clean_df[column]
    months=(time_delta/np.timedelta64(1,'M')).astype(int)
    return months

def client_preparation(df):
    df_client[['date_activ','date_end','date_modif_prod','date_renewal']] = df_client[['date_activ','date_end','date_modif_prod','date_renewal']].apply(pd.to_datetime)
    df_client['has_gas'].replace({'f':0, 't':1}, inplace = True)
    return df_client

client_data = read_file("client_data.csv")
df_client = client_preparation(client_data)

price = read_file("price_data.csv")

def price_preparation(df):
       
    var_year = price.groupby(["id","price_date"]).mean().groupby(["id"]).var().reset_index() #yearly sensitivity feature
    var_year = var_year.rename(columns = {
                            'price_off_peak_var':'var_year_price_off_peak_var',
                            'price_peak_var':'var_year_price_peak_var', 
                            'price_mid_peak_var':'var_year_price_mid_peak_var',
                            'price_off_peak_fix':'var_year_price_off_peak_fix',
                            'price_peak_fix':'var_year_price_peak_fix',
                            'price_mid_peak_fix': 'var_year_price_mid_peak_fix'})


    var_year['var_year_price_off_peak'] = var_year['var_year_price_off_peak_var'] + var_year['var_year_price_off_peak_fix']
    var_year['var_year_price_peak'] = var_year['var_year_price_peak_var'] + var_year['var_year_price_off_peak_fix']
    var_year['var_year_price_mid_peak'] = var_year['var_year_price_mid_peak_var'] + var_year['var_year_price_mid_peak_fix']

    var_6m = price[price['price_date'] > '2015-05-01'].groupby(['id', 'price_date']).mean().groupby(['id']).var().reset_index()
    var_6m = var_6m.rename(columns={
                       'price_off_peak_var':'var_6m_price_off_peak_var',
                       'price_peak_var': 'var_6m_price_peak_var',
                       'price_mid_peak_var': 'var_6m_price_mid_peak_var',
                       'price_off_peak_fix' : 'var_6m_price_off_peak_fix',
                       'price_peak_fix' :'var_6m_price_peak_fix',
                       'price_mid_peak_fix' : 'var_6m_price_mid_peak_fix'  
                        })

    var_6m['var_6m_price_off_peak'] = var_6m['var_6m_price_off_peak_var'] + var_6m['var_6m_price_off_peak_fix']
    var_6m['var_6m_price_peak'] = var_6m['var_6m_price_peak_var'] + var_6m['var_6m_price_peak_fix']
    var_6m['var_6m_price_mid_peak'] = var_6m['var_6m_price_mid_peak_var'] + var_6m['var_6m_price_mid_peak_fix']

    price_sens = pd.merge(var_year, var_6m, on='id')
    price_an = pd.merge(price_sens, df_client[['id', 'churn']], on='id')
    
    clean_df = pd.merge(df_client.drop(columns=['churn']), price_an, on = 'id')
    
    ##FEATURE ENGINEERING
    #Group off-peak prices by comapnies and month
    monthly_price_by_id= price.groupby(["id","price_date"]).agg({"price_off_peak_var":'mean','price_off_peak_fix':'mean'}).reset_index()
    
    # to get jan and dec prices
    jan_price=monthly_price_by_id.groupby('id').first().reset_index()
    dec_price=monthly_price_by_id.groupby('id').last().reset_index()
    
    #restando la diferencia entre diciembre y enero anterior " diff['dec_1']-diff['price_off_peak_var']" - energy.
    #restando la diferencia entre diciembre y enero anterior diff['dec_2']-diff['price_off_peak_fix'] - power.
    #calculating the difference
    diff = pd.merge(dec_price.rename(columns={'price_off_peak_var':'dec_1','price_off_peak_fix':'dec_2'}),jan_price.drop(columns='price_date'),on='id')
    diff['offpeak_diff_dec_jan_energy']=diff['dec_1']-diff['price_off_peak_var']
    diff['offpeak_diff_dec_jan_power']=diff['dec_2']-diff['price_off_peak_fix']
    diff = diff[['id','offpeak_diff_dec_jan_energy','offpeak_diff_dec_jan_power']]
    
    clean_df = pd.merge(clean_df, diff, on='id')
    
    mean_prices= price.groupby(["id"]).agg({
    'price_off_peak_var':'mean',
    'price_peak_var':'mean',
    'price_mid_peak_var':'mean',
    'price_off_peak_fix':'mean',
    'price_peak_fix':'mean',
    'price_mid_peak_fix':'mean'
    }).reset_index()
    
    mean_prices['off_peak_peak_var_mean_diff']= mean_prices['price_off_peak_var']-mean_prices['price_peak_var']
    mean_prices['peak_mid_peak_var_mean_diff']= mean_prices['price_peak_var']-mean_prices['price_mid_peak_var']
    mean_prices['off_peak_mid_peak_var_mean_diff']= mean_prices['price_off_peak_var']-mean_prices['price_mid_peak_var']

    mean_prices['off_peak_peak_fix_mean_diff']= mean_prices['price_off_peak_fix']-mean_prices['price_peak_fix']
    mean_prices['peak_mid_peak_fix_mean_diff']= mean_prices['price_peak_fix']-mean_prices['price_mid_peak_fix']
    mean_prices['off_peak_mid_peak_fix_mean_diff']= mean_prices['price_off_peak_fix']-mean_prices['price_mid_peak_fix']
    
    columns=['id','off_peak_peak_var_mean_diff','peak_mid_peak_var_mean_diff','off_peak_mid_peak_var_mean_diff','off_peak_peak_fix_mean_diff',
        'peak_mid_peak_fix_mean_diff','off_peak_mid_peak_fix_mean_diff']
    
    clean_df=pd.merge(clean_df,mean_prices[columns],on='id')
    
    mean_prices_by_month= price.groupby(["id","price_date"]).agg({
    'price_off_peak_var':'mean',
    'price_peak_var':'mean',
    'price_mid_peak_var':'mean',
    'price_off_peak_fix':'mean',
    'price_peak_fix':'mean',
    'price_mid_peak_fix':'mean'
    }).reset_index()
    
    mean_prices_by_month['off_peak_peak_var_mean_diff']= mean_prices_by_month['price_off_peak_var']-mean_prices_by_month['price_peak_var']
    mean_prices_by_month['peak_mid_peak_var_mean_diff']= mean_prices_by_month['price_peak_var']-mean_prices_by_month['price_mid_peak_var']
    mean_prices_by_month['off_peak_mid_peak_var_mean_diff']= mean_prices_by_month['price_off_peak_var']-mean_prices_by_month['price_mid_peak_var']

    mean_prices_by_month['off_peak_peak_fix_mean_diff']= mean_prices_by_month['price_off_peak_fix']-mean_prices_by_month['price_peak_fix']
    mean_prices_by_month['peak_mid_peak_fix_mean_diff']= mean_prices_by_month['price_peak_fix']-mean_prices_by_month['price_mid_peak_fix']
    mean_prices_by_month['off_peak_mid_peak_fix_mean_diff']=mean_prices_by_month['price_off_peak_fix']-mean_prices_by_month['price_mid_peak_fix']

    max_diff_across_periods_months= mean_prices_by_month.groupby(['id']).agg({
    'off_peak_peak_var_mean_diff':'max',
    'peak_mid_peak_var_mean_diff':'max',
    'off_peak_mid_peak_var_mean_diff':'max',
    'off_peak_peak_fix_mean_diff':'max',
    'peak_mid_peak_fix_mean_diff':'max',
    'off_peak_mid_peak_fix_mean_diff':'max'
    }).reset_index().rename(
    columns={
    'off_peak_peak_var_mean_diff':'off_peak_peak_var_max_monthly_diff',
    'peak_mid_peak_var_mean_diff':'peak_mid_peak_var_max_monthly_diff',
    'off_peak_mid_peak_var_mean_diff':'off_peak_mid_peak_var_max_monthly_diff',
    'off_peak_peak_fix_mean_diff':'off_peak_peak_fix_max_monthly_diff',
    'peak_mid_peak_fix_mean_diff':'peak_mid_peak_fix_max_monthly_diff',
    'off_peak_mid_peak_fix_mean_diff':'off_peak_mid_peak_fix_max_monthly_diff'
    })
    
    columns=[
    'id',
    'off_peak_peak_var_max_monthly_diff',
    'peak_mid_peak_var_max_monthly_diff',
    'off_peak_mid_peak_var_max_monthly_diff',
    'off_peak_peak_fix_max_monthly_diff',
    'peak_mid_peak_fix_max_monthly_diff',
    'off_peak_mid_peak_fix_max_monthly_diff']
    
    clean_df = pd.merge(clean_df, max_diff_across_periods_months[columns], on='id')
    clean_df['tenure']=((clean_df['date_end']-clean_df['date_activ'])/np.timedelta64(1,'Y')).astype(int)
    
    # Transforming the dates into month
    refer_date= datetime(2016,1,1)
    clean_df['months_activ']=convert_months(refer_date, clean_df,'date_activ')
    clean_df['months_end']=convert_months(refer_date, clean_df,'date_end')
    clean_df['months_modif_prod']=convert_months(refer_date, clean_df, 'date_modif_prod')
    clean_df['months_renewal']=convert_months(refer_date,clean_df,'date_renewal')
    remove=['date_activ','date_end','date_modif_prod','date_renewal']
    clean_df=clean_df.drop(columns=remove)
    
    # transforming categorical features- Channel_sales & origin_up
    clean_df["channel_sales"]=clean_df["channel_sales"].astype('category')
    clean_df["origin_up"]=clean_df["origin_up"].astype('category')
    
    #dummies
    clean_df=pd.get_dummies(clean_df, columns=['channel_sales'], prefix='channel')
    clean_df=clean_df.drop(columns=['channel_sddiedcslfslkckwlfkdpoeeailfpeds','channel_epumfxlbckeskwekxbiuasklxalciiuu','channel_fixdbufsefwooaasfcxdxadsiekoceaa'])
    clean_df=pd.get_dummies(clean_df, columns=['origin_up'], prefix='origin')
    clean_df=clean_df.drop(columns=['origin_usapbepcfoloekilkwsdiboslwaxobdp','origin_ewxeelcelemmiwuafmddpobolfuxioce','origin_MISSING'])

    # transforming numerical data which are skewed
    skewed=['cons_12m', 'cons_gas_12m', 'cons_last_month', 'forecast_cons_12m', 'forecast_cons_year','forecast_discount_energy',
        'forecast_meter_rent_12m', 'forecast_price_energy_off_peak','forecast_price_energy_peak','forecast_price_pow_off_peak']
    
    # apply log10 transformation
    # log cannot be applied on 0 hence adding constant 1
    clean_df['cons_12m']=np.log10(clean_df['cons_12m']+1)
    clean_df['cons_gas_12m']=np.log10(clean_df['cons_gas_12m']+1)
    clean_df['cons_last_month']=np.log10(clean_df['cons_last_month']+1)
    clean_df['forecast_cons_12m']=np.log10(clean_df['forecast_cons_12m']+1)
    clean_df['forecast_cons_year']=np.log10(clean_df['forecast_cons_year']+1)
    clean_df['forecast_discount_energy']=np.log10(clean_df['forecast_discount_energy']+1)
    clean_df['forecast_meter_rent_12m']=np.log10(clean_df['forecast_meter_rent_12m']+1)
    clean_df['forecast_price_energy_off_peak']=np.log10(clean_df['forecast_price_energy_off_peak']+1)
    clean_df['forecast_price_energy_peak']=np.log10(clean_df['forecast_price_energy_peak']+1)
    clean_df['forecast_price_pow_off_peak']=np.log10(clean_df['forecast_price_pow_off_peak']+1)
    
    clean_df=clean_df.drop(columns=["margin_net_pow_ele", "num_years_antig","months_activ"])
    
    print("Transformacion de datos completa")
    return clean_df

def data_exporting(df, filename):
    df.to_excel(os.path.join('./procesado/', filename))
    print(filename, 'exportado correctamente en la carpeta processed')


      # Generamos las matrices de datos que se necesitan para la implementación

def main():
    # Matriz de Entrenamiento
    df1 = read_price('price_data.csv')
    tdf1 = price_preparation(df1)
    data_exporting(tdf1,'train.xlsx')
        
if __name__ == "__main__":
    main()