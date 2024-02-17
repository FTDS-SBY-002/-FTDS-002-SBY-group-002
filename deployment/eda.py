import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
from PIL import Image

def run():
    # Show dataframe
    st.title('Data Overview')
    df = pd.read_csv('data_clean.csv')

    st.title('Exploratory DataAnalysis')
    plot = st.selectbox(label='Choose', 
                                  options=['Bank Client Personal Information', 
                                           'Current Campaign Information'])
    
    # Plot 1
    def plot_1():
        st.write('### Bank Client Personal Information')
        labels = [ 'Not Deposit', 'Deposit']

        #define Seaborn color palette to use
        colors = sns.color_palette('pastel')[0:5]

        #create pie chart
        fig_1, ax = plt.subplots()
        ax.pie(df["subscribed"].value_counts(), labels = labels, colors = colors, autopct='%.0f%%')
        st.pyplot(fig_1)
        st.markdown('Bank client age vary from 19 to 87, and to make it easier for us to understand about age data we will do data creation based on their generation')
        st.markdown('---')


    def plot_2():
        st.write('### Job')
        grouped_df = df.groupby(['job', 'subscribed']).size().reset_index(name='count')

        pivot_df = grouped_df.pivot(index='job', columns='subscribed', values='count').fillna(0)

        pivot_df['percentage_subscribed'] = (pivot_df['yes'] / (pivot_df['yes'] + pivot_df['no'])) * 100
        pivot_df['percentage_not_subscribed'] = (pivot_df['no'] / (pivot_df['yes'] + pivot_df['no'])) * 100


        print(pivot_df)
    
    def plot_3():
        sns.set_style('whitegrid')

        avg_duration = df['duration'].mean()

        df['duration_status'] = pd.cut(df['duration'], bins=[-float('inf'), avg_duration, float('inf')],
                               labels=['below_average', 'above_average'])

        pct_term = pd.crosstab(df['duration_status'], df['subscribed'], normalize='index') * 100

        fig, ax = plt.subplots()
        sns.barplot(data=pct_term, x=pct_term.index, y='yes', ax=ax, palette="Set2")

        ax.set_title("The Impact of Duration in Subscription", fontsize=18)
        ax.set_xlabel("Duration Status", fontsize=18)
        ax.set_ylabel("Percentage (%)", fontsize=18)

        for p in ax.patches:
            ax.annotate(f'{p.get_height():.2f}%', (p.get_x() * 1.02, p.get_height() * 1.02))

        st.pyplot(fig)
        st.markdown('Pada barplot antara duration diatas rata" dan dibawah rata" ternyata mereka yang memiliki durasi telepon diatas rata" atau diatas 264 detik cenderung untuk setuju untuk subscribe sedangkan mereka yang below average cenderung untuk menolak subscribe. Dari informasi itu maka untuk menaikkan persentase yang subscribe maka diperlukan peningkatan durasi telepon bagi tiap target customer diatas 264 detik')
        st.markdown('---')
        plt.clf()

    if plot == "Bank Client Personal Information":
        plot_1()

    elif plot == "Current Campaign Information":
        plot_3()

if __name__ == '__main__':
    run()   