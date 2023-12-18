import streamlit as st
import pandas as pd
import pydeck as pdk

st.title(":blue[Maps of Boston for Data Visualization]:world_map:")
path = "C:/Users/cdhim/OneDrive - Bentley University/CS230/final/"
df = pd.read_csv(path + "bostoncrime2023_7000_sample.csv", index_col="INCIDENT_NUMBER")
pd.set_option("display.max_rows", None, "display.max_columns", None, 'display.width', None, 'max_colwidth', None)
df = df.dropna()
df.rename(columns={"Lat": 'lat', "Long": "lon"}, inplace=True)
zoom_level = st.sidebar.slider("Please select the zoom level", 0.0, 15.0, 10.0)

color_dict = {
    'ASSAULT - SIMPLE': [255, 0, 0],
    'INVESTIGATE PERSON': [60, 179, 113],
    'INVESTIGATE PROPERTY': [255, 165, 0],
    'LARCENY SHOPLIFTING': [0, 0, 255],
    'LARCENY THEFT FROM BUILDING': [238, 130, 238],
    'M/V - LEAVING SCENE - PROPERTY DAMAGE': [106, 90, 205],
    'PROPERTY - LOST/ MISSING': [255, 103, 71],
    'SICK ASSIST': [0, 139, 168],
    'TOWED MOTOR VEHICLE': [196, 211, 255],
    'VANDALISM': [56, 117, 155]
}

Hour = 18
district = []
Districts = [district.append(x) for x in df["DISTRICT"] if x not in district]
district.pop(-1)


def filter_data(Hour, District, sel_days_week=["Friday", "Saturday", "Sunday"]):
    df1 = df.loc[df["DAY_OF_WEEK"].isin(sel_days_week)]
    df1 = df1.loc[df["DISTRICT"].isin(District)]
    df1 = df1.loc[df["HOUR"] >= Hour]

    return df1


df1 = filter_data(Hour, district)


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

    crimedf = new_df(df1, top10_list)

    crimedf = crimedf[['OCCURRED_ON_DATE', "OFFENSE_DESCRIPTION", "DAY_OF_WEEK", "STREET", "lat", "lon"]].copy()

    return crimedf.sort_values(by=['DAY_OF_WEEK', 'OFFENSE_DESCRIPTION']), top10_list


crime, top10_list = topcrime(df)

crime['Color'] = [color_dict[offense] for offense in crime['OFFENSE_DESCRIPTION']]

sel_crime = st.sidebar.multiselect("Choose a crime", top10_list, default=top10_list)


def filter_data2(sel_crime):
    df2 = crime.loc[crime['OFFENSE_DESCRIPTION'].isin(sel_crime)]
    return df2


sel_crime_data = filter_data2(sel_crime)
st.title("Scatterplot")
scatterplot = pdk.Layer(
    "ScatterplotLayer",
    data=sel_crime_data,
    get_position=["lon", "lat"],
    get_color="Color",
    get_radius=100,
    pickable=True,
)


view_state = pdk.ViewState(
    latitude=sel_crime_data['lat'].mean(),
    longitude=sel_crime_data['lon'].mean(),
    zoom=zoom_level,
    pitch=0
)


st.pydeck_chart(pdk.Deck(
    map_style="mapbox://styles/mapbox/light-v9",
    initial_view_state=view_state,
    layers=[scatterplot],
    tooltip={
        "html": "<b>Crime:</b> {OFFENSE_DESCRIPTION}</b>",
    }
))
with st.expander("Caption"):
    st.caption("The following map displays the marked location of offenses in Boston Friday through Sunday."
               " When hovering over the marker it will display the type of offense")


st.title("Heat Map")
view_state = pdk.ViewState(
    latitude=sel_crime_data["lat"].mean(),
    longitude=sel_crime_data["lon"].mean(),
    zoom=zoom_level,
    pitch=0
)

layer1 = pdk.Layer(type='HeatmapLayer',
                   data=sel_crime_data,
                   get_position='[lon,lat]',
                   get_radius=100,
                   get_color=[0, 200, 0],
                   pickable=True)
layer2 = pdk.Layer('HeatmapLayer',
                   data=sel_crime_data,
                   get_position='[lon,lat]',
                   get_radius=.5,
                   get_color=[0, 0, 255],
                   pickable=True)
map = pdk.Deck(
    map_style='mapbox://styles/mapbox/dark-v11',
    initial_view_state=view_state,
    layers=[layer1, layer2],
)

st.pydeck_chart(map)
with st.expander("Caption"):
    st.caption("The following map is a heatmap displaying the location of offenses in Boston Friday through Sunday."
               "This is using the same data as the map above")