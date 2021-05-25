    # function
def build_lineup(df):
        # imports
        import pandas as pd
        # clean up fd to match column list above
        df.drop(columns=['First Name', 'Last Name', 'FPPG', 'Played', 'Injury Details', 'Tier', 'Batting Order', 'Roster Position'], inplace=True)

        # filling nulls for probable pitcher
        df['Probable Pitcher'].fillna('No', inplace=True)

        # fill nulls for injury indicator
        df['Injury Indicator'].fillna('Healthy', inplace=True)

        # renaming nickname column
        df.rename(columns={'Nickname': 'Name'}, inplace=True)

        # fitler to only healthy players
        df = df.loc[df['Injury Indicator'] == 'Healthy']

        # split using .loc by position and make new dataframe for pitchers
        pitchers = df.loc[df['Position']=='P']

        # split using .loc by position and make new dataframe for batters
        batters = df.loc[df['Position']!='P']

        # pitcher dataframe steps
        # save pitchers df to only starting pitchers
        pitchers = pitchers.loc[pitchers['Probable Pitcher']=='Yes']

        # read in pitcher projections
        pitcher_proj = pd.read_csv('pitcher_projections_2021.csv')

        # merge attempt
        pitcher_projections = pitchers.merge(pitcher_proj, how='left', on='Name')

        # drop nulls if any
        pitcher_projections.dropna(inplace=True)

        # overwrite df with only the columns needed
        pitcher_projections = pitcher_projections[['Id', 'Position', 'Name', 'Salary', 'Team_x', 'Opponent', 'Projected_FPPG']]

        # rename team column
        pitcher_projections.rename(columns={'Team_x' : 'Team'}, inplace=True)

        # batter dataframe steps
        # read in projections file
        batter_21 = pd.read_csv('batter_projections_2021.csv')

        # merge projections with batter df, creating new df
        batters_projections = batters.merge(batter_21, how='left', on='Name')

        # dropping batters with no projections
        batters_projections.dropna(inplace=True)

        # drop unneeded columns for merge with pitcher, overwrite current df
        batters_projections = batters_projections[['Id', 'Position', 'Name', 'Salary', 'Team_x', 'Opponent','Projected_FPPG']]
        
        # rename team column
        batters_projections.rename(columns={'Team_x' : 'Team'}, inplace=True)

        # following are steps for creating a line up
        # set cap for fanduel
        salary_cap = 35_000

        # sort pitcher by fppg projections
        pitcher_projections.sort_values(by='Projected_FPPG', ascending=False, inplace=True, ignore_index=True)

        # create a player list to 
        lineup = []
        lineup.append(pitcher_projections.values[0])

        # need to update remaining salary
        salary_cap -= pitcher_projections['Salary'][0]

        # with updated salary fill remaining roster based on position and highest fppg
        # create position list for remaining roster spots
        position_list = ['C', '1B', '2B', '3B', 'SS', 'OF', 'OF', 'OF']
        # sort batters by FPPG
        batters_projections.sort_values(by='Projected_FPPG', ascending=False, inplace=True, ignore_index=True)

        # create count based on remaining positions
        sal_count = 8

        # create average salary variable for remaining players
        avg_sal = salary_cap/sal_count

        # create for loop for each position in list to take highest fppg
        for pos in position_list:
            # setting counter to increase if player is already in list
            # this is inside the for loop beacuse it needs to be per position
            counter = 0
            # if salary greater than average move to next player
            for salary in batters_projections.loc[batters_projections['Position'] == pos]['Salary']:
                # test if salary is greater than average if it is increase counter
                if batters_projections.loc[batters_projections['Position'] == pos]['Salary'].values[counter] > avg_sal:
                    counter += 1
                else:
                    # if less than average add player to list
                    lineup.append(batters_projections.loc[batters_projections['Position'] == pos].values[counter])
                    # drop player so no duplicates are added
                    batters_projections.drop(batters_projections.loc[batters_projections['Position'] == pos].index.values[counter], inplace=True)
                    # decrease sal_count
                    sal_count -= 1
                    # decrease salary cap
                    salary_cap -= batters_projections.loc[batters_projections['Position'] == pos]['Salary'].values[counter]
                    # create new average salary
                    avg_sal = salary_cap/sal_count
                    break
        # create dataframe of lineup
        df_lineup = pd.DataFrame(lineup, columns=['Id', 'Position', 'Name', 'Salary', 'Team', 'Opponent','Projected_FPPG'])

        # return dataframe
        return df_lineup

def build_lineup_stack(df):
        # imports 
        import pandas as pd
        # clean up fd to match column list above
        df.drop(columns=['First Name', 'Last Name', 'FPPG', 'Played', 'Injury Details', 'Tier', 'Batting Order', 'Roster Position'], inplace=True)

        # filling nulls for probable pitcher
        df['Probable Pitcher'].fillna('No', inplace=True)

        # fill nulls for injury indicator
        df['Injury Indicator'].fillna('Healthy', inplace=True)

        # renaming nickname column
        df.rename(columns={'Nickname': 'Name'}, inplace=True)

        # fitler to only healthy players
        df = df.loc[df['Injury Indicator'] == 'Healthy']

        # split using .loc by position and make new dataframe for pitchers
        pitchers = df.loc[df['Position']=='P']

        # split using .loc by position and make new dataframe for batters
        batters = df.loc[df['Position']!='P']

        # pitcher dataframe steps
        # save pitchers df to only starting pitchers
        pitchers = pitchers.loc[pitchers['Probable Pitcher']=='Yes']

        # read in pitcher projections
        pitcher_proj = pd.read_csv('pitcher_projections_2021.csv')

        # merge attempt
        pitcher_projections = pitchers.merge(pitcher_proj, how='left', on='Name')

        # drop nulls if any
        pitcher_projections.dropna(inplace=True)

        # overwrite df with only the columns needed
        pitcher_projections = pitcher_projections[['Id', 'Position', 'Name', 'Salary', 'Team_x', 'Opponent', 'AVG', 'Projected_FPPG']]

        # rename team column
        pitcher_projections.rename(columns={'Team_x' : 'Team'}, inplace=True)

        # batter dataframe steps
        # read in projections file
        batter_21 = pd.read_csv('batter_projections_2021.csv')

        # merge projections with batter df, creating new df
        batters_projections = batters.merge(batter_21, how='left', on='Name')

        # dropping batters with no projections
        batters_projections.dropna(inplace=True)

        # drop unneeded columns for merge with pitcher, overwrite current df
        batters_projections = batters_projections[['Id', 'Position', 'Name', 'Salary', 'Team_x', 'Opponent','Projected_FPPG']]
        
        # rename team column
        batters_projections.rename(columns={'Team_x' : 'Team'}, inplace=True)

        # following are steps for creating a line up
        # set cap for fanduel
        salary_cap = 35_000
        
        # sort by avg
        pitcher_projections.sort_values(by='AVG', ascending=False, inplace=True, ignore_index=True)
        # create list of teams to filter batters
        team_list = []
        for x in range(0,4):
            team_list.append(pitcher_projections['Opponent'][x])
        # drop avg
        pitcher_projections.drop(columns='AVG', inplace=True)
        
        # create team filter 
        team_filter = (batters_projections['Team'] == team_list[0]) | (batters_projections['Team'] == team_list[1]) |(batters_projections['Team'] == team_list[2]) |(batters_projections['Team'] == team_list[3])
        # new batter dataframe with team filter
        batters_projections = batters_projections[team_filter]
        # reset index
        batters_projections.reset_index(drop=True, inplace=True)

        # sort pitcher by fppg projections
        pitcher_projections.sort_values(by='Projected_FPPG', ascending=False, inplace=True, ignore_index=True)

        # create a player list to 
        lineup = []
        lineup.append(pitcher_projections.values[0])

        # need to update remaining salary
        salary_cap -= pitcher_projections['Salary'][0]

        # with updated salary fill remaining roster based on position and highest fppg
        # create position list for remaining roster spots
        position_list = ['C', '1B', '2B', '3B', 'SS', 'OF', 'OF', 'OF']
        # clean position
        pos_list = [pos[:2] for pos in batters_projections['Position']]
        batters_projections['Position'] = pos_list
        # sort batters by FPPG
        batters_projections.sort_values(by='Projected_FPPG', ascending=False, inplace=True, ignore_index=True)

        # create count based on remaining positions
        sal_count = 8

        # create average salary variable for remaining players
        avg_sal = salary_cap/sal_count

        # create for loop for each position in list to take highest fppg
        for pos in position_list:
            # setting counter to increase if player is already in list
            # this is inside the for loop beacuse it needs to be per position
            counter = 0
            # if salary greater than average move to next player
            for salary in batters_projections.loc[batters_projections['Position'] == pos]['Salary']:
                # test if salary is greater than average if it is increase counter
                if batters_projections.loc[batters_projections['Position'] == pos]['Salary'].values[counter] > avg_sal:
                    counter += 1
                else:
                    # if less than average add player to list
                    lineup.append(batters_projections.loc[batters_projections['Position'] == pos].values[counter])
                    # drop player so no duplicates are added
                    batters_projections.drop(batters_projections.loc[batters_projections['Position'] == pos].index.values[counter], inplace=True)
                    # decrease sal_count
                    sal_count -= 1
                    # decrease salary cap
                    salary_cap -= batters_projections.loc[batters_projections['Position'] == pos]['Salary'].values[counter]
                    # create new average salary
                    avg_sal = salary_cap/sal_count
                    break
        # create dataframe of lineup
        df_lineup = pd.DataFrame(lineup, columns=['Id', 'Position', 'Name', 'Salary', 'Team', 'Opponent','Projected_FPPG'])

        # return dataframe
        return df_lineup, pd.DataFrame(team_list)   
    
def make_template(df):
    template = df[['Position', 'Id']]
    template = template.set_index('Position').T
    template.rename(columns={'C':'C/1B', '1B':'UTIL'}, inplace=True)
    return template