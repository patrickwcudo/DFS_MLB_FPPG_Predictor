import streamlit as st
import pickle
import pandas as pd

page = st.sidebar.selectbox(
    'Select a page:',
    ('Home', 'About Predictor', 'Create Lineup', 'Test'))

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
    st.title('Welcome to DFS MLB Lineup Generator')
    st.header('Predictor')
    st.write('Import the player list from game you are entering.')
    # now try to predict some comments
    # import model reading binary
    model = pickle.load(open('model.p', 'rb'))
    # import tfidf feature extraction
    tvec = pickle.load(open('tfidf.p', 'rb'))
    # get user input
    user_text = st.text_input('Input a comment: ')
    # convert user input to list
    test_list = list(user_text.split(sep=' '))
    # convert list to tfidf sparse matrix
    test_tvec = tvec.transform(test_list)
    # get mean of predictions
    str_mean = model.predict(test_tvec).mean()
    # condictional for mean to classify subreddit
    if str_mean >= .5:
        st.write('The comment you enter is more likely to be found on the sportsbooks subreddit.')
    else:
        st.write('The comment you enter is more likely to be found on the dfsports subreddit.')

if page == 'Test':
    st.title('Test for file import.')
    file = st.file_uploader('Upload file', type=['csv'])
    # read file in as df
    df = pd.read_csv(file)
    st.dataframe(df.head(5))
