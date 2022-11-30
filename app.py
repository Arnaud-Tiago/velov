import streamlit as st
import pandas as pd

import pydeck as pdk

import utils

st.write('Hello boys!')
st.write('Welcome to the Velo\'V prediction app')

# Pre-treatment
stations_info = utils.get_stations_info(source='local')
stations_info = stations_info[(stations_info['lng'] != 0)
                              & (stations_info['lng'] != 0)]

live_status = utils.get_live_status()

live_status['station_number'] = live_status['station_number'].astype(
    'int64', errors='raise')
cols = ['station_number', 'lat', 'lng', 'capacity']
stations_and_status = pd.merge(stations_info[cols],
                               live_status,
                               how='left',
                               on='station_number').dropna()


# Plotting the map

view_state = pdk.ViewState(
            latitude=45.7640,
            longitude=4.8357,
            zoom=13,
            pitch=40,
        )


scatter_layer_1 = pdk.Layer(
    'ScatterplotLayer',
    data=stations_info[['lng', 'lat']][:100],
    get_position=['lng', 'lat'],
    get_radius=50,
    get_fill_color=[0, 0, 200, 140])

scatter_layer = pdk.Layer(
    'ScatterplotLayer',
    data=stations_info[['lng', 'lat']][100:],
    get_position=['lng', 'lat'],
    get_radius=50,
    get_fill_color=[180, 0, 200, 140])

st.pydeck_chart(
    pdk.Deck(
        initial_view_state=view_state,
        layers=[
            #hexa_layer_1,
            scatter_layer,
            scatter_layer_1
        ],
    ))

pred_horizon = st.sidebar.slider(label="Prediction horizon",
                                 min_value=0,
                                 max_value=60,
                                 step=5)


#st.map(stations_info[['lat', 'lng']].rename(columns={'lng': 'lon'}))
#live_status = utils.get_live_status()

#chart_data = pd.DataFrame(np.random.randn(1000, 2) / [50, 50] +
#                          [37.76, -122.4],
#                          columns=['lat', 'lon'])

# hexa_layer_1 = pdk.Layer(
#     'HexagonLayer_1',
#     data=stations_info[['lng', 'lat']].rename(columns={'lng': 'lon'})[:100],
#     get_position=['lon', 'lat'],
#     get_elevation=['bikes'],
#     radius=20,
#     elevation_scale=1,
#     elevation_range=[0, 1000],
#     pickable=True,
#     extruded=True,
# )

# hexa_layer_2 = pdk.Layer(
#     'HexagonLayer_2',
#     data=stations_info[['lng', 'lat']].rename(columns={'lng': 'lon'})[100:],
#     get_position=['lon', 'lat'],
#     get_elevation=['bikes'],
#     radius=20,
#     elevation_scale=1,
#     elevation_range=[0, 1000],
#     pickable=True,
#     extruded=True,
#     get_fill_color=[180, 0, 200, 140]
# )

# fig = px.scatter_geo(
#     data_frame=stations_info,
#     #color="color_column",
#     lon="lng",
#     lat="lat",
#     projection="natural earth",
#     scope='europe',
#     #hover_name="hover_column",
#     #size="size_column",  # <-- Set the column name for size
#     #height=800,
# )

#st.plotly_chart(fig, use_container_width=True)
