import streamlit as st
import pydeck as pdk
import pandas as pd

st.set_option('deprecation.showPyplotGlobalUse', False)


# this is how streamlit refreshes data

@st.cache
def load_data(nrows, price_max):
    data = pd.read_csv('airbnb_cambridge_listings_20201123.csv', nrows=nrows)
    df = pd.DataFrame(data, columns=["name", "neighbourhood", "latitude", "longitude", "price", "number_of_reviews",
                                     "availability_365"])
    # the filtering by price
    data_filter = df['price'] < price_max
    filter_data = df[data_filter]
    return filter_data


def print_raw_data(price_max):
    data = pd.read_csv('airbnb_cambridge_listings_20201123.csv')

    pd.set_option('display.max_rows', 700)
    pd.set_option('display.max_columns', 20)
    pd.set_option('display.width', 1000)

    info_data = load_data(10000, price_max)

    st.subheader('Raw data')
    st.write(info_data)


def print_bar_chart():
    data = pd.read_csv('airbnb_cambridge_listings_20201123.csv')
    newdf = data.set_index(["neighbourhood", "id"]).count(level="neighbourhood")
    df2 = newdf['name']
    df2.plot.bar()
    st.pyplot()

def print_map(price_max):
    df = load_data(700, price_max)
    MAPKEY = "pk.eyJ1IjoiY2hlY2ttYXJrIiwiYSI6ImNrOTI0NzU3YTA0azYzZ21rZHRtM2tuYTcifQ.6aQ9nlBpGbomhySWPF98DApk.eyJ1IjoiY2hlY2ttYXJrIiwiYSI6ImNrOTI0NzU3YTA0azYzZ21rZHRtM2tuYTcifQ.6aQ9nlBpGbomhySWPF98DA"
    locations = [
        ("SunsplashedSerenity walk to Harvard & Fresh Pond", "West Cambridge", 42.38329, -71.13617, 150, 36, 164)]

    view_state = pdk.ViewState(
        latitude=df["latitude"].mean(),
        longitude=df["longitude"].mean(),
        zoom=11,
        pitch=0)

    layer1 = pdk.Layer('ScatterplotLayer',
                       data=load_data(10000, price_max),
                       get_position='[longitude, latitude]',
                       get_radius='scaled_radius',
                       radius_scale=1,
                       radius_min_pixels=3,
                       radius_max_pixels=10,
                       get_color=[255, 0, 255],
                       pickable=True
                       )

    tool_tip = {"html": "Cambridge Listing:<br/> <b>{name}</b> <br/><b>Price:${price}</b> ",
                "style": {"backgroundColor": "crimson",
                          "color": "white"}
                }

    "# Map of cambridge"
    map = pdk.Deck(
        map_style='mapbox://styles/mapbox/light-v9',
        initial_view_state=view_state,
        mapbox_key=MAPKEY,
        layers=layer1,
        tooltip=tool_tip
    )

    st.pydeck_chart(map)


def print():
    st.title("Cambridge Listings")
    price_max = st.slider('Price Range', 30, 3000, 100)
    if st.checkbox("Show Raw Data"):
        print_raw_data(price_max)
    print_map(price_max)
    print_bar_chart()

print()

# list holding neighbourhood
# dic holding avg price/avg availability/avg # of reviews
# all of printing stuff

neighbourhoods = ["Agassiz", "Area 2/MIT", "Cambridge Highlands", "Cambridgeport", "East Cambridge", "Mid-Cambridge",
                  " Neighborhood Nine", "North Cambridge", "Riverside", "Strawberry Hill", "The Port",
                  "Wellington-Harrington", "West Cambridge"]
