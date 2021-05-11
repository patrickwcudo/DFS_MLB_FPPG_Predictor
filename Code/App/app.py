import streamlit as st
import pickle
import pandas as pd
from LineupBuilder import build_lineup
import base64



page = st.sidebar.selectbox(
    'Select a page:',
    ('Home', 'About Predictor', 'Create Lineup'))

if page == 'Home':
    st.title('Welcome to DFS MLB Lineup Generator')

    st.header('This site will predict FPPG for players and produce a lineup based on those prediction.')
    st.header("All you need to do is import the player list from the game you are entering.")
    st.header('')
    st.text('Click the links in the menu to the left to find out more about the predictor.')

if page == 'About Predictor':
    st.title('Welcome to DFS MLB Lineup Generator')
    st.header('About')
    st.write('The predictor uses linear regression model to predict FPPG based on the previous two years. \n'
            'Click the link to check out more about the project.')
    st.write("Link to Project [link](https://github.com/patrickwcudo/DFS_MLB_FPPG_Predictor)")


if page == 'Create Lineup':
    st.title('Import player list from FanDuel.')
    file = st.file_uploader('Upload file', type=['csv'])
    # read file in as df in try except form
    try: 
        df = pd.read_csv(file)
        # rewrite df with lineup built from LineupBuilder
        df = build_lineup(df)
        # show lineup on screen
        st.dataframe(df)
        # create lineup for template to download
        template = df[['Position', 'Id']]
        template = template.set_index('Position').T
        template.rename(columns={'C':'C/1B', '1B':'UTIL'}, inplace=True)

        def get_table_download_link(df):
            """Generates a link allowing the data in a given panda dataframe to be downloaded
            in:  dataframe
            out: href string
            """
            csv = df.to_csv(index=False)
            b64 = base64.b64encode(
                csv.encode()
            ).decode()  # some strings <-> bytes conversions necessary here
            return f'<a href="data:file/csv;base64,{b64}" download="lineup_template.csv">Download csv file</a>'

        st.markdown(get_table_download_link(template), unsafe_allow_html=True)
        #get_table_download_link(template)
    except: 
        st.title('No file imported.')