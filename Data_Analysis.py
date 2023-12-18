import matplotlib.pyplot as plt
import streamlit as st
import pandas as pd
from PIL import Image
st.markdown('<span style="font-family: Times New Roman; font-size: 50px;">Data Analysis of Crime Rate</span>',
            unsafe_allow_html=True)
path = "C:/Users/cdhim/OneDrive - Bentley University/CS230/final/"
df = pd.read_csv(path + "bostoncrime2023_7000_sample.csv", index_col="INCIDENT_NUMBER")
df = df.dropna()
st_image = Image.open("C:/Users/cdhim/OneDrive - Bentley University/CS230/final/shutterstock_216617104.0.jpg")
st_image2 = Image.open("C:/Users/cdhim/OneDrive - Bentley University/CS230/final/Boston-MA-Crime-Rate.jpg")
col1, col2 = st.columns(2)

with col1:
    st.image(st_image)
with col2:
    st.image(st_image2)
st.subheader(":blue[The following chart shows the most frequent hours when crime occurs in Boston Friday-Sunday.]",divider="green")


Hour = 18
district = []
Districts = [district.append(x) for x in df["DISTRICT"] if x not in district]
district.pop(-1)


def filter_data(Hour, District, sel_days_week=["Friday", "Saturday", "Sunday"]):
    df1 = df.loc[df["DAY_OF_WEEK"].isin(sel_days_week)]
    df1 = df1.loc[df["DISTRICT"].isin(District)]
    df1 = df1.loc[df["HOUR"] >= Hour]

    return df1


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

    crimedf = new_df(filter_data(Hour, district), top10_list)

    crimedf = crimedf[
        ['OCCURRED_ON_DATE', "OFFENSE_DESCRIPTION", "DAY_OF_WEEK", "STREET", "Lat", "Long", "HOUR"]].copy()

    return crimedf.sort_values(by=['DAY_OF_WEEK', 'OFFENSE_DESCRIPTION'])


crime_df = topcrime(filter_data(Hour, district))

df = crime_df.groupby(["HOUR", "DAY_OF_WEEK"]).size().reset_index(name='COUNT')


pivot_df = df.pivot(index='HOUR', columns='DAY_OF_WEEK', values='COUNT')

pivot_df.plot(kind='line', marker='o', figsize=(10, 6))


plt.xlabel("Hour of the Day")
plt.ylabel("Number of Incidents")
plt.title('Incidents per Hour for Each Day of the Week')

plt.legend(title='Day of the Week')
plt.tight_layout()

tab1, tab2 = st.tabs(["📈 Chart", "🗃 Data"])
with tab1:
    st.pyplot()
with tab2:
    st.dataframe(df)

st.markdown('<span style="font-family: Times New Roman; font-size: 50px;">Conclusion</span>',
            unsafe_allow_html=True)
container = st.container(border=True)
container.subheader(":blue[Is Boston safe during the weekend?]")
container.write("Boston is generally safe as indicated by the frequency of top 10 crimes. Boston is a relatively "
                "small city"
                " and does not have the same crime rate as larger cities such as New York and Chicago."
                " The maps also shows that crime rate is somewhat spread out in Boston besides in the financial district."
                "Therefore, you may want to avoid this area if going out at night.")