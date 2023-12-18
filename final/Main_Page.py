"""
Name:       Costas Dhimogjini
CS230:      Section 5
Data:       Boston Crime 2023
URL:        Link to your web application on Streamlit Cloud (if posted)

Description: This program: Uses crime data from Boston as of 2023 and consists of a sample of 7000 cases. For this project I used various functions to filter data and
focused on friday-sunday as the data when mapped was too clustered if I did not do so. I also wanted to focus on a specific aspect of the data which was weekends. I wanted to
solve the question of where should you hang-out in Boston for the weekend. I created three charts: line_chart,Bar_Chart, and a pie chart. I used various streamlit widgets to customize the look and used different widgets to also select certain data for the charts.
I also used altair which was used for one of my charts this is a package that we did not use within class.I used many python applications such as list comprehnsion,dictionaires,and functions to manipulate data frames and filter data.
Overall, this project created a unique dashboard in streamlit displaying different data to get a picture of bosotn crime on the weekends for 2023.
"""
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import altair as alt

st.title(":blue[Where to spend your weekend night out in Boston] :night_with_stars:")
st.header(
    ":gray[This web page is meant inform you of dangerous areas in Boston. Additionally, the data for this page was collected from a sample of 7000 crime reports in Boston as of 2023.]",
    divider='green')
st.subheader(
    ":blue[Below is the raw data used for all of the metrics, graphs, and maps that are displayed throughout the webpage. I hope that this is helpful for planning your weekend get away!]",
    divider="green")
st.sidebar.markdown('<p style="font-size: 25px; color: light blue; font-family: Times New Roman, sans-serif;">Data Customization</p><hr style="border-top: .01px solid green;">', unsafe_allow_html=True)


pd.set_option("display.max_rows", None, "display.max_columns", None, 'display.width', None, 'max_colwidth', None)
column_names = ["INCIDENT_NUMBER", "OFFENSE_CODE", "OFFENSE_DESCRIPTION", "DISTRICT", "REPORTING_AREA", "SHOOTING",
                "OCCURRED_ON_DATE", "YEAR", "MONTH", "DAY_OF_WEEK", "HOUR", "STREET", "Lat", "Long", "Location"]
path = "C:/Users/cdhim/OneDrive - Bentley University/CS230/final/"
df = pd.read_csv( path +"bostoncrime_2023_7000_sample.csv", index_col="INCIDENT_NUMBER")
df = df.dropna()
st.dataframe(df)

Hour = 18
district = []
Districts = [district.append(x) for x in df["DISTRICT"] if x not in district]
district.pop(-1)

select_districts = st.sidebar.multiselect('Select Districts',district,default=district)
if len(select_districts) < 2:
    st.warning('Please select at least two districts.')



def filter_data(Hour, District, sel_days_week=["Friday", "Saturday", "Sunday"]):
    df1 = df.loc[df["DAY_OF_WEEK"].isin(sel_days_week)]
    df1 = df1.loc[df["DISTRICT"].isin(District)]
    df1 = df1.loc[df["HOUR"] >= Hour]

    return df1


def count_districts(district, data):
    lst = [data[data['DISTRICT'] == DISTRICT].shape[0] for DISTRICT in district]
    return lst
def count_offnses(offense,data):
    lst = [data[data['OFFENSE_DESCRIPTION'] == Offense].shape[0] for Offense in offense]
    return lst

# pie chart
def pie_chart(lst, sel_d):
    st.set_option('deprecation.showPyplotGlobalUse', False)

    plt.figure()
    explodes = [0 for i in range(len(lst))]
    maximum = lst.index(np.max(lst))
    explodes[maximum] = .25
    colors = ["#B9DDF1", "#9FCAE6", "#73A4CA", "#497AA7", "#2E5B88"]
    plt.pie(lst, labels=sel_d, explode=explodes, autopct="%.2f%%", counterclock=False, pctdistance=.95, colors=colors)
    plt.title(f"% Criminal Offenses in 2023 Friday-Sunday after 6:00pm by District")

    return plt


st.pyplot(pie_chart(count_districts(select_districts, filter_data(Hour, select_districts)),select_districts))

def topcrime(df):

    top10_df = df.groupby(["OFFENSE_DESCRIPTION"]).count().sort_values(by='DAY_OF_WEEK', ascending=False).reset_index()


    top10_list = []

    for i in top10_df["OFFENSE_DESCRIPTION"].head(10):
        top10_list.append(i)


    def new_df(df, val_list):
        new_df = pd.DataFrame()
        for i in val_list:
            new_df = pd.concat([new_df, df[(df['OFFENSE_DESCRIPTION'] == i)]])
        return new_df

    crimedf = new_df(filter_data(Hour,district),top10_list)

    crimedf = crimedf[['OCCURRED_ON_DATE',"OFFENSE_DESCRIPTION","DAY_OF_WEEK","STREET","Lat","Long"]].copy()

    return crimedf.sort_values(by=['DAY_OF_WEEK','OFFENSE_DESCRIPTION'])

crimedf = topcrime(df)

st.subheader(f':blue[Below is the data for the top 10 crimes in Boston sorted by the days of the week from Friday-Sunday and the type of Offense]',divider="green")
st.dataframe(crimedf)
tracked_val = st.selectbox("Before proceeding, select a crime to track:", crimedf['OFFENSE_DESCRIPTION'].unique())

alt_chart = (
    alt.Chart(crimedf, title="Most Recent Crime Count by Incident Type")
    .mark_bar()
    .encode(x=alt.Y('count(*):Q', title='Numer of Incidents'),
            y=alt.X('OFFENSE_DESCRIPTION', title="Incident Type").sort('-x'),
            color=alt.condition(
                alt.datum.OFFENSE_DESCRIPTION == tracked_val,
                alt.value('orange'),
                alt.value('steelblue'),
                )
            )
    .interactive().properties(width=900)
    )

st.altair_chart(alt_chart, use_container_width=False)

with st.expander("See explanation"):
    st.subheader(':yellow[The chart above is a bar chart displaying the top 10 crime rates in Boston.'
                 ' Additionally, it displays the total number of incidents for each offense and the select box highlights which offense you have chosen.]'
                 )