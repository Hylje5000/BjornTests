import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import altair as alt
import numpy as np

# define sheet GID
sheet_name_dict ={
    'Banana box test': 0,
    'Weight': 1865415711,
    'Noise': 2069101638,
    'Acceleration': 378787627,
    'Braking': 26964202,
    'Range': 735351678,
    '1000km Challenge': 15442336}
gsheetid = "1V6ucyFGKWuSQzvI8lMzvvWJHrBS82echMVJH37kwgjE"

#load sheets into dataframes
dfs = {}
for sheet_name, gid in sheet_name_dict.items():
    gsheet_url = f"https://docs.google.com/spreadsheets/d/{gsheetid}/export?format=csv&gid={gid}"
    dfs[sheet_name] = pd.read_csv(gsheet_url)

#banana box dataframe configuration
bananadf = dfs['Banana box test'][['Car', 'Trunk', 'Seats folded']]
split_index = bananadf[bananadf['Car'] == 'Van'].index[0]
bananadf = bananadf.drop(index=split_index)
bananadf = bananadf.drop(index=108)
df_car = bananadf.loc[:split_index-2]
df_van = bananadf.loc[split_index+1:]

#acceleration dataframe config
accelerationdf = dfs['Acceleration'][['Car','0-10','0-20','0-30','0-40','0-50','0-60','0-70','0-80','0-90','0-100']]



# RENDERED SITE START
st.title("Bjørn Nyland test results")
st.header("Search results by car🚗")
st.markdown("This page utilizes data provided by Bjørn Nyland, find his original spreadsheet <a href='https://docs.google.com/spreadsheets/d/1V6ucyFGKWuSQzvI8lMzvvWJHrBS82echMVJH37kwgjE/edit?gid=378787627#gid=378787627'> here</a>.", unsafe_allow_html=True)

car_options = ['None'] + bananadf['Car'].unique().tolist()
selected_car = st.selectbox('Select a car', car_options)

# Iteration start
for sheet_name, df in dfs.items():
    st.divider()
    

    #Banana Box
    if sheet_name == 'Banana box test':
        st.header(sheet_name + '🍌')
        if selected_car == 'None':
            st.dataframe(bananadf)
        else:
            selected_car_data = df[df['Car'].str.contains(selected_car, na=False)]
            for index, row in selected_car_data.iterrows():
                car_name = row['Car']
                trunk = row['Trunk']
                folded = row['Seats folded']
            
                st.subheader(car_name)
                col1, col2 = st.columns(2)
                col1.metric("Trunk", str(trunk) + "📦")
                col2.metric("Seats folded", str(folded) + "📦")
                

    #Weight
    elif sheet_name == 'Weight':
        st.header(sheet_name + '⚖️')
        if selected_car == 'None':
            st.dataframe(df)
        else:
            selected_car_data = df[df['Car'].str.contains(selected_car, na=False)]
            for index, row in selected_car_data.iterrows():
                car_name = row['Car']
                total_weight = row['Total']
                front = row['Front']
                rear = row['Rear']
                distribution = row['Distribution']
                battery = row['Battery']
            
                st.subheader(car_name)
                col1, col2, col3 = st.columns(3)
                col1.metric("Total weight", str(total_weight) + "kg")
                col2.metric("Front", str(front) + "kg")
                col3.metric("Rear", str(rear) + "kg")
                col4, col5 = st.columns([1,2])
                col4.metric("Distribution", str(distribution))
                col5.metric("Battery", str(battery))
            

    #Acceleration
    elif sheet_name == 'Acceleration':
        st.header(sheet_name + '💨')
        if selected_car == 'None':
            st.dataframe(accelerationdf)
        else:
            selected_car_data = accelerationdf[accelerationdf['Car'].str.contains(selected_car, na=False)]
            chart_data = selected_car_data.melt(id_vars='Car', var_name='Acceleration', value_name='Seconds')
            chart_data['Acceleration'] = chart_data['Acceleration'].str.replace('0-', '').astype(int)
            chart_data['Seconds'] = chart_data['Seconds'].str.replace(',', '.').astype(float)
            max_seconds = chart_data['Seconds'].max()
            tick_values = np.arange(0, np.ceil(max_seconds)+0.5, 0.5)
            chart = alt.Chart(chart_data).mark_line().encode(
                x=alt.X('Seconds:Q', title='Seconds',
                        scale=alt.Scale(domain=(0, np.ceil(max_seconds)),
                                        clamp=True),
                        axis=alt.Axis(values=list(tick_values))),
                y=alt.Y('Acceleration:N', sort='descending', title='Acceleration'),
                color=alt.Color('Car', legend=alt.Legend(orient='bottom', direction='vertical'))
                
            )
            col1, col2 = st.columns([2,1])

            col1.altair_chart(chart, use_container_width=True)
            col2.subheader('0-100 acceleration')
            for car in selected_car_data['Car'].unique():
                col2.markdown(f"**{car}**: {selected_car_data.loc[selected_car_data['Car'] == car, '0-100'].values[0]}sec")
            

    # Braking  
    elif sheet_name == 'Braking':
        st.header(sheet_name + '🫸🏻')
        if selected_car == 'None':
            st.dataframe(df)
        else:
            selected_car_data = df[df['Car'].str.contains(selected_car, na=False)]
            for index, row in selected_car_data.iterrows():
                car_name = row['Car']
                surface = row['Surface']
                temp = row['Temp']
                tires = row['Tires']
                season = row['Season']
                distance = row['Distance']
                time = row['100-0 km/h']
            
                st.subheader(car_name)
                col1, col2, col3,  = st.columns([1,1,2])
                col1.metric("Distance", str(distance) + "m")
                col2.metric("Time", str(time) + "sec")
                col3.metric("Tires", str(tires))
    
                col4, col5, col6 = st.columns([1,1,2])  
                col4.metric("Season", str(season))
                col5.metric("Temperature", str(temp) + "°C")
                col6.metric("Surface", str(surface))

                #Styling
                st.markdown(
                        """
                    <style>
                    [data-testid="stMetricValue"] {
                        font-size: 1.5rem;
                        overflow-wrap: normal;
                    }
                    </style>
                    """,
                        unsafe_allow_html=True,
                    )
                
    # Noise
    elif sheet_name == 'Noise':
        st.header(sheet_name + '📢')
        if selected_car == 'None':
            st.dataframe(df)
        else:
            selected_car_data = df[df['Car'].str.contains(selected_car, na=False)]
            for index, row in selected_car_data.iterrows():
                car_name = row['Car']
                average = row['Average']
                tires = row['Tires']
                season = row['Season']
                noise80 = row['80 km/h']
                noise100 = row['100 km/h']
                noise120 = row['120 km/h']
            
                st.subheader(car_name)
                col1, col2, col3,  = st.columns([1,1,2])
                col1.metric("Average", str(average) + "dB")
                col2.metric("Season", str(season))
                col3.metric("Tires", str(tires))
    
                col4, col5, col6 = st.columns([1,1,2])  
                col4.metric("80 km/h", str(noise80) + "dB")
                col5.metric("100 km/h", str(noise100) + "dB")
                col6.metric("120 km/h", str(noise120) + "dB")

    # Range
    elif sheet_name == 'Range':
        st.header(sheet_name + '🗺️')
        if selected_car == 'None':
            st.dataframe(df)
        else:
            selected_car_data = df[df['Car'].str.contains(selected_car, na=False)]
            for index, row in selected_car_data.iterrows():
                car_name = row['Car']
                surface = row['Surface']
                temp = row['Temp']
                tires = row['Tires']
                season = row['Season']
                speed = row['Speed']
                distance = row['km']
                consumption = row['Wh/km']
            
                st.subheader(car_name)
                col1, col2, col3,  = st.columns([1,1,2])
                col1.metric("Range", str(distance) + "km")
                col2.metric("Speed", str(speed) + "km/h")
                col3.metric("Tires", str(tires))
    
                col4, col5, col6, col7 = st.columns(4)  
                col4.metric("Consumption", str(consumption) + "Wh/km")
                col5.metric("Season", str(season))
                col6.metric("Temperature", str(temp) + "°C")
                col7.metric("Surface", str(surface))

    # 1000km
    elif sheet_name == '1000km Challenge':
        st.header(sheet_name + '🏅')
        if selected_car == 'None':
            st.dataframe(df)
        else:
            selected_car_data = df[df['Car'].str.contains(selected_car, na=False)]
            for index, row in selected_car_data.iterrows():
                car_name = row['Car']
                time = row['Time']
                temp = row['Temp']
                notes = row['Notes']
                consumption = row['Wh/km']
            
                st.subheader(car_name)
                col1, col2, col3  = st.columns(3)
                col1.metric("Time", str(time))
                col2.metric("Consumption", str(consumption) + "Wh/km")
                col3.metric("Temperature", str(temp) + "°C")
                
                if pd.isna(notes):
                    st.metric("Notes", "-")
                else:
                    st.metric("Notes", notes)
    else:
        if selected_car == 'None':
            st.dataframe(df)
        else:
            selected_car_data = df[df['Car'].str.contains(selected_car, na=False)]
            st.table(selected_car_data)
