# Import libraries
import psycopg2 as db 

import datetime as dt
from datetime import timedelta
import pandas as pd
import numpy as np

from airflow import DAG
from airflow.operators.python import PythonOperator

def getdata():
    '''
    This function is use to get data from PostgreSQL where PostgreSQL load from csv
    '''
    conn_string ="dbname='airflow' host='postgres' user='airflow' password='airflow'"           # Make connection form PostgreSQL 
    conn = db.connect(conn_string)                                                             

    df = pd.read_sql("select * from bank", conn)                                                # Read dataset 
    df.to_csv('/opt/airflow/data/bank_data.csv',index= False)                                                # Save to CSV
    print('-----Data Saved------')

def clean():
    '''
    This function is to use clean data from dataset and will save into bank_data_clean.csv
    '''
    df = pd.read_csv('/opt/airflow/data/P2M3_betara_candra_data_raw.csv',index_col=False)       # Read dataset
    # Drop index columns 
    df.drop(columns=['Unnamed: 0'], inplace=True)
    if df.isnull().sum().sum() > 0 :                                                            # Check missing value
        df.dropna(inplace=True)                                                                 # Drop missing value
    if df.duplicated().sum() > 0:                                                               # Check duplicated of data 
        df.drop_duplicates(inplace=True)    
    df['month'] = df['month'].replace(['oct', 'may', 'apr', 'jun', 'feb', 
                                   'aug', 'jan', 'jul', 'nov',
                                   'sep', 'mar', 'dec'],['october','may','april',
                                   'juny','february','august','january','july','november',
                                   'september','march','december'])                                                              
    df.rename({'y' :  'subscribed'}, axis = 1, inplace= True)                                  # Change column name target
    # Change column name for more easier to understand
    df.rename({'pdays' :  'days_passed'}, axis = 1, inplace= True)                             
    df.rename({'poutcome' :  'outcome_passed'}, axis = 1, inplace= True)
    df.rename({'housing' :  'housing_loan'}, axis = 1, inplace= True)
    df.rename({'default' :  'has_credit'}, axis = 1, inplace= True)

    df.to_csv('/opt/airflow/data/bank_data_clean.csv', index= False)                            # Save raw file



default_args = { 
    'owner':  'group2',
    'start_date': dt.datetime(2024, 1, 26, 12, 00, 0) - dt.timedelta(hours=7), 
}

with DAG('cleaning_data',
         default_args=default_args,
         schedule_interval= '0 0 1 * *', 
         catchup = False
         ) as dag:
    
    # Define Task 1 get data
    fetchdataformsql = PythonOperator(task_id='getdata',
                                      python_callable=getdata)
    # Define task 2 function clean data
    cleandata = PythonOperator(task_id='cleandata',
                               python_callable=clean)
    
    fetchdataformsql >> cleandata