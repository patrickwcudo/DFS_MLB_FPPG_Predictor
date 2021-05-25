import streamlit as st
import pandas as pd
from LineupBuilderFunction import build_lineup, build_lineup_stack
import base64
from bokeh.plotting import figure
from bokeh.models import LabelSet, Label, ColumnDataSource
from bokeh.io import show
from bokeh.transform import factor_cmap
from pathlib import Path



page = st.sidebar.selectbox(
    'Select a page:',
    ('Home', 'Position Analysis', 'Create Lineup', 'Create Lineup Stack'))

if page == 'Home':
    st.title('MLB Fantasy Points Per Game Predictor')

    st.header('About')
    st.write('This site will predict FPPG for players and produce a FanDuel lineup based on those prediction.  All you need is a player list from FanDuel.')
    st.write('The predictor uses machine learning to predict FPPG based on the previous two years. \n'
            'Click the link to check out more about the project.')
    st.write("Link to Project [link](https://github.com/patrickwcudo/DFS_MLB_FPPG_Predictor)")

    st.write('Click the links in the menu to the left to find out more about the predictor.')

if page == 'Position Analysis':
    st.title("Position Analysis")
    st.header('Below is a plot showing all positions and their actual vs projected FPPG.')
    st.write('')
    file_path = Path('data')
    st.write(file_path)
    players = pd.read_csv('data/all_players.csv')
    #st.write('Pick a Position below to gain more insight.')
    pos_input = st.selectbox(label='Pick a Position below to gain more insight.  Interact with features on right of plot to zoom and save.', 
    options=['All', 'SP', 'C', '1B', '2B', 'SS', '3B', 'OF'])

    # conditional for all players, if no position selected print all positions on one chart
    if pos_input == 'All':
        # create factor cmap
        pos_cmap = factor_cmap('Pos', palette=['green', 'red', 'blue', 'yellow', 'orange', 'black', 'grey'],
                         factors=sorted(players['Pos'].unique()))
        # create plot
        all_plot = figure(plot_width=750, plot_height=450, title='FPPG vs Projected FPPG by Position')
        all_plot.scatter('Projected_FPPG', 'FPPG', source=players, fill_alpha=0.6, fill_color=pos_cmap,
                   size=10, legend='Pos')
        all_plot.xaxis.axis_label = 'Projected FPPG'
        all_plot.yaxis.axis_label = 'Actual FPPG'
        all_plot.legend.location = 'top_left'

        # show plot
        st.bokeh_chart(all_plot)

    # once position is selected
    else:
        # attempt for scatter plot with names
        # create series based on user input
        pos_series = players.loc[players['Pos']==pos_input.upper()]
        # convert series to data source 
        pos_source = ColumnDataSource(data=pos_series)
        # retry
        pos_plot = figure(plot_width=750, plot_height=450, title=f'{pos_input.upper()}: FPPG vs Projected FPPG')
        pos_plot.scatter('Projected_FPPG', 'FPPG', source=pos_source, fill_alpha=0.6, size=10)
        pos_plot.xaxis.axis_label = 'Projected FPPG'
        pos_plot.yaxis.axis_label = 'Actual FPPG'
        # create labels
        labels = LabelSet(x='Projected_FPPG', y='FPPG', text='Name', 
                    text_font_size='7pt', text_color='blue', x_offset=5, y_offset=5,
                    source=pos_source, render_mode='canvas')
        pos_plot.add_layout(labels)
        # display plot 
        st.bokeh_chart(pos_plot)


if page == 'Create Lineup':
    st.title('Import player list from FanDuel.')
    file = st.file_uploader('Upload file', type=['csv'])
    # read file in as df in try except form
    try:
        df = pd.read_csv(file)
        # rewrite df with lineup built from LineupBuilder
        df = build_lineup(df)
        # describe lineup
        st.write('Lineup below is based on the highest predicted FPPG per position while staying under the salary cap.')
        # show lineup on screen
        st.dataframe(df)
        # create lineup for template to download
        template = df[['Position', 'Id']]
        template = template.set_index('Position').T
        template.rename(columns={'C':'C/1B', '1B':'UTIL'}, inplace=True)
        template = template[['P', 'C/1B', '2B', '3B', 'SS', 'OF', 'UTIL']]

        def get_table_download_link(df):
            """Generates a link allowing the data in a given panda dataframe to be downloaded
            in:  dataframe
            out: href string
            """
            csv = df.to_csv(index=False)
            b64 = base64.b64encode(
                csv.encode()
            ).decode()  # some strings <-> bytes conversions necessary here
            return f'<a href="data:file/csv;base64,{b64}" download="lineup_template.csv">Download Template as csv file</a>'

        st.markdown(get_table_download_link(template), unsafe_allow_html=True)
        #get_table_download_link(template)
    except:
        st.title('No file imported.')

if page == 'Create Lineup Stack':
    st.title('Import player list from FanDuel.')
    st.header('This will create a stacked lineup based on pitching match up.')
    st.write('')
    file = st.file_uploader('Upload file', type=['csv'])
    # read file in as df in try except form
    try: 
        df = pd.read_csv(file)
        # rewrite df with lineup built from LineupBuilder
        df, team = build_lineup_stack(df)
        # describe output
        st.write('The four teams below have the best pitching match ups based on projections.')
        # show team on screen 
        st.dataframe(team)
            # describe lineup
        st.write('Lineup below is based on the highest predicted FPPG per position while staying under the salary cap.')
        # show lineup on screen
        st.dataframe(df)
        # create lineup for template to download
        template = df[['Position', 'Id']]
        template = template.set_index('Position').T
        template.rename(columns={'C':'C/1B', '1B':'UTIL'}, inplace=True)
        template = template[['P', 'C/1B', '2B', '3B', 'SS', 'OF', 'UTIL']]

        def get_table_download_link(df):
            """Generates a link allowing the data in a given panda dataframe to be downloaded
            in:  dataframe
            out: href string
            """
            csv = df.to_csv(index=False)
            b64 = base64.b64encode(
                csv.encode()
            ).decode()  # some strings <-> bytes conversions necessary here
            return f'<a href="data:file/csv;base64,{b64}" download="lineup_template.csv">Download Template as csv file</a>'

        st.markdown(get_table_download_link(template), unsafe_allow_html=True)
        #get_table_download_link(template)
    except: 
        st.title('No file imported.')