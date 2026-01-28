import plotly.graph_objects as go
from dash import dcc, html, Dash
from dash.dash_table.Format import Group
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
import numpy as np
import webbrowser
from threading import Timer
from options import title, markdown, dropdown, radio_items, slider, range_slider


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = Dash(__name__, external_stylesheets=external_stylesheets)

server = app.server

csv_files = {
    "df": "data/players_20years_change.csv",
    "list_name_lower": "data/name_lower.csv",
    "df_stat": "data/stat_mean.csv",
    "final_note": "data/position_note_final_test.csv",
    "salary": "data/salary_notes.csv",
    "leaders_top": "data/leaders.csv",
    "teams": "data/team_season_comp.csv",
    "global_seas": "data/seasons_global.csv",
    "ml_pos": "data/ml_position.csv",
    "ml_predict": "data/ml_2001_results.csv"
}

# Lecture des CSV
data = {name: pd.read_csv(path) for name, path in csv_files.items()}

x1 = np.array([0, 2, 4, 6, 8, 10])
y1 = np.array([0, 8000000, 16000000, 24000000, 32000000, 40000000])


app.title = "20 Years of NBA Statistics"

# Markdown Text

markdown_text = """
This app is a data student project. Most of the informations for the statistics comes from an API named nba-api 1.1.8,
enriched with a scraping of the website www.basketball-reference.com. It contains the statistics of every players and every
teams from 2001 to 2020 season, which means that the stats of a players that plays before are not taken into consideration.
"""

explain_3d_pos = """
Choose 3 features to compute which ones are key features to determine the position of a player. You can select Position that
gives the 5 position or Generalized position that group in 3 categories (Front, Wing and Guard). You can also keep only players
that plays a minimum of time with the slider.
"""

explain_box_pos = """
Choose 1 stat category to see the evolution of this stat in function of th position.
"""

explain_player_choice = """
Write 1 to 5 player names and choose a stat category to compare their evolution.
"""

explain_notes = """
To get these notes, I splitted the computations in several steps :
First, for the (minutes, points, rebounds, assists, steals, blocks, turnovers, fouls) per games and the (field goals, 3 points field goals, free throws) percentage,
I did a MinMax scaler for each season and each position.\n
Then I added the results of points, rebounds, assists, steals, blocks, field goals, 3 points field goals and free throws minus the score of turnovers and fouls.
This result is then multiplied by the result for minutes per games to normalize in function of the time played for these stats.\n
Finally, I made a last MinMax scaler from these results to have a final note from 0 to 10.
"""

age_range_explain = """
You can adapt the range of the players' age with the slider below.
"""

explain_ml_pos = """
To perform this Machine Learning exploration, for each players, I scaled all the datas with a MinMax scaler for the stats Points per games, Field Goals percentage,
3 points percentage, Free Throws percentage, Rebounds per games, Assists per games, Steals per games, Blocks per games, Turnovers per games and Fouls per games,
doing this for each season.\n
We will try to do this for the 5 positions (Point Guard, Shooting Guard, Small Forward, Power Forward and center) and for a generalisation of them
(Guard = point + shooting, Wing = Small Forward, Front = Center and Power Forward). \n
I tried these computations with and without Height and Weight, these stats being directly linked with the position.\n
Note : The Logistic regression is performed with a max_iter = 500 due to the size of the data.
"""

explain_ml_predict = """
To perform this Machine Learning exploration, for each players, I scaled all the datas with a MinMax scaler for the stats Height, Weight, Age,  Points per games,
Field Goals percentage, 3 points percentage, Free Throws percentage, Rebounds per games, Assists per games, Steals per games, Blocks per games, Turnovers per games
and Fouls per games, doing this for the 2001 season.\n
Then I have sorted these data by Teams, Minutes played per games (descending), number of games started (descending) and number of games played(descending).
For each Teams, I only keep the 10 "best" players sorted and, by team, I sort them again by generalized position (Guard, Wing, Front), and by minutes played per games
(descending). \n
The assertion of the machine learning process will be "The home team wins". So for each of the stats of the 10 players per team, I made a substraction of the home teams
player minus the away team player. I have here 10 "oppositions" with all the stats categories. \n
"""


# ===================== Players Options =====================

YEARS = [(str(y), str(y)) for y in range(2001, 2021)]
STAT_OPTIONS = [
    ('Minutes per games','MPG'), ('Points per games','PPG'), ('Field Goals percentage','FG_PCT'),
    ('3 points percentage','FG3_PCT'), ('Free Throws percentage','FT_PCT'), ('Rebounds per games','RPG'),
    ('Assists per games','APG'), ('Steals per games','SPG'), ('Blocks per games','BPG'),
    ('Turnovers per games','TPG'), ('Fouls per games','FPG')
]
POSITION_OPTIONS = [('Position','POSITION'),('Generalized Position','GEN_POST')]
POSITION_CATEGORY = [('General','general'), ('Center','C'), ('Power Forward','PF'), ('Small Forward','SF'),
                     ('Shooting Guard','SG'), ('Point Guard','PG')]
YEAR_SALARY_OPTIONS = [('2020','2020'), ('2021','2021'), ('2022','2022'), ('2023','2023')]


# ===================== Team Options =====================
TEAMS = [
    ('Atlanta','ATL'), ('Boston','BOS'), ('Charlotte/New Orleans','NOP'), ('Chicago','CHI'),
    ('Cleveland','CLE'), ('Dallas','DAL'), ('Denver','DEN'), ('Detroit','DET'),
    ('Golden State','GSW'), ('Houston','HOU'), ('LA Clippers','LAC'), ('LA Lakers','LAL'),
    ('Miami','MIA'), ('Milwaukee','MIL'), ('Minnesota','MIN'), ('New Jersey/Brooklyn','BKN'),
    ('New York','NYK'), ('Orlando','ORL'), ('Philadelphia','PHI'), ('Phoenix','PHX'),
    ('Portland','POR'), ('Sacramento','SAC'), ('San Antonio','SAS'), ('Seattle/Oklahoma City','OKC'),
    ('Toronto','TOR'), ('Vancouver/Memphis','MEM'), ('Washington','WAS'), ('Charlotte','CHA')
]

TEAM_STAT_OPTIONS = [
    ('Points per games','PPG'), ('Field Goals percentage','FG_PCT'), ('3 points percentage','FG3_PCT'),
    ('Free Throws percentage','FT_PCT'), ('Offensive Rebs per games','ORPG'), ('Defensive Rebs per games','DRPG'),
    ('Rebounds per games','RPG'), ('Assists per games','APG'), ('Steals per games','SPG'),
    ('Blocks per games','BPG'), ('Turnovers per games','TPG'), ('Fouls per games','FPG'),
    ('Win Percentage','WIN_PCT')
]

GAME_EVOLUTION_OPTIONS = [
    ('Points','PTS'), ('Fiels Goals Made','FGM'), ('Fiels Goals Attempts','FGA'), ('Field Goals percentage','FG_PCT'),
    ('3 points Made','FG3M'), ('3 points Attempts','FG3A'), ('3 points percentage','FG3_PCT'),
    ('Free Throws Made','FTM'), ('Free Throws Attempts','FTA'), ('Free Throws percentage','FT_PCT'),
    ('Offensive Rebounds','OREB'), ('Defensive Rebounds','DREB'), ('Rebounds','REB'),
    ('Assists','AST'), ('Steals','STL'), ('Blocks','BLK'), ('Turnovers','TOV'), ('Fouls','PF')
]

# ===================== Layout =====================

app.layout = html.Div([

    title("20 Years of NBA Statistics", 1),
    markdown(markdown_text),
    html.Br(),

    dcc.Tabs([

        # ----------------- Tab 1 : Players Statistics -----------------
        dcc.Tab(label="Players statistics", children=[

            # --- Top Players per year ---
            html.Div([
                title("Top Players for each year"),
                html.Br(),
                title("Select the year to check", 5),
                dropdown("year_stat1", YEARS, default='2001')
            ], className="two columns"),

            html.Div([], className="ten columns", id='output-container-button6'),
            html.Br(), html.Br(),

            # --- Observation of statistics by position ---
            html.Div([
                html.Div([
                    markdown(explain_3d_pos),
                    title("Position to predict", 5),
                    dropdown("position_to_predict", POSITION_OPTIONS, default='POSITION'),
                    title("Choose your stat categories", 5),
                    dropdown("stat_category", STAT_OPTIONS, default=['FG3_PCT','FT_PCT','BPG'], multi=True),
                    title("Minimum minutes played", 5),
                    slider("my_slider", 0, 30, 10, 20)
                ], className="four columns"),

                html.Div([], className="eight columns", id='output-container-button1')
            ], className="row"),
            html.Br(), html.Br(),

            # --- Boxplot of stats by position ---
            html.Div([
                html.Div([
                    markdown(explain_box_pos),
                    title("Position to predict", 5),
                    dropdown("position_to_predict2", POSITION_OPTIONS, default='POSITION'),
                    title("Choose your stat category", 5),
                    radio_items("stat_category2", STAT_OPTIONS, default='PPG')
                ], className="four columns"),

                html.Div([], className="eight columns", id='output-container-button2')
            ], className="row"),
            html.Br(), html.Br(),

            # --- Comparison of players stats ---
            html.Div([
                title("Comparison of players stats during their careers"),
                markdown(explain_player_choice),
                html.Br(), html.Br(),

                # Input players
                dcc.Input(id="input1", type="text", placeholder="Write Name"),
                dcc.Input(id="input2", type="text", placeholder="Write Name"),
                dcc.Input(id="input3", type="text", placeholder="Write Name"),
                dcc.Input(id="input4", type="text", placeholder="Write Name"),
                dcc.Input(id="input5", type="text", placeholder="Write Name"),

                html.Div([
                    html.Div([
                        title("Choose your stat category", 5),
                        radio_items("stat_category3", STAT_OPTIONS, default='PPG')
                    ], className="four columns"),

                    html.Div([], className="eight columns", id='output-container-button3')
                ], className="row")
            ]),
            html.Br(), html.Br(),

            # --- General notes ---
            html.Div([
                title("Experimentation : Give a general note for players to see the evolution over time"),
                markdown(explain_notes),
                html.Br(),

                html.Div([
                    html.Div([
                        title("Choose your Position", 5),
                        radio_items("position_category", POSITION_CATEGORY, default='general'),
                        html.Br(),
                        title("Minimum minutes played", 5),
                        slider("time_slider", 0, 30, 10, 0)
                    ], className="four columns"),

                    html.Div([], className="eight columns", id='output-container-button4')
                ], className="row")
            ]),
            html.Br(), html.Br(),

            # --- Notes vs Salary ---
            html.Div([
                title("Comparison of the notes with the salary"),
                html.Br(),

                html.Div([
                    html.Div([
                        title("Choose the year of the salary", 5),
                        radio_items("Year", YEAR_SALARY_OPTIONS, default='2020'),
                        html.Br(), html.Br(),
                        markdown(age_range_explain)
                    ], className="four columns"),

                    html.Div([], className="eight columns", id='output-container-button5')
                ], className="row"),

                html.Div([
                    title("Age Range", 5),
                    range_slider("age_slider", 17, 45, [22, 37])
                ]),
                html.Br(), html.Br()
            ])

        ]), # end Tab Players Statistics ###############################################

        dcc.Tab(label="Teams statistics", children=[

            # --- Teams stats over time ---
            title("Teams stats during time"),
            html.Br(),

            html.Div([
                html.Div([
                    title("Select the team", 5),
                    dropdown("team_select", TEAMS, default='ATL'),
                    radio_items("stat_select", TEAM_STAT_OPTIONS, default='PPG')
                ], className="four columns"),

                html.Div([], className="eight columns", id='output-container-button7')
            ], className="row"),
            html.Br(), html.Br(),

            # --- General evolution of the game ---
            title("General evolution of the game"),
            html.Br(),

            html.Div([
                html.Div([
                    title("Select the stat category", 5),
                    dropdown("stat_select2", GAME_EVOLUTION_OPTIONS, default='PTS')
                ], className="four columns"),

                html.Div([], className="eight columns", id='output-container-button8')
            ], className="row")
        ])

    ]) # end of the Tabs ##########################################################################################

], style={'width': '75%', 'textAlign': 'center', 'margin-left':'12.5%', 'margin-right':'0'})

@app.callback(
    Output('output-container-button1', 'children'),
    [Input('position_to_predict', 'value'),
     Input('stat_category', 'value'),
     Input('my_slider', 'value')]
)
def pos_predict(position, stats, min_mpg):
    if len(stats) != 3:
        return html.Div("Please select exactly 3 stats for 3D plot", style={'color':'red', 'textAlign':'center'})

    df_filtered = data["df_stat"][data["df_stat"]["MPG"] > min_mpg]
    fig = px.scatter_3d(df_filtered, x=stats[0], y=stats[1], z=stats[2], color="POSITION")
    fig.update_layout(title_text='3D plot of stats in function of position', title_x=0.5)

    return html.Div([html.Br(), dcc.Graph(id='g1', figure=fig)])

@app.callback(
    Output('output-container-button2', 'children'),
    [Input('position_to_predict2', 'value'), Input('stat_category2', 'value')])
def pos_predict2(value1, value2):

            fig2 = px.box(data["df_stat"], y=value2, color=value1, points="all")
            fig2.update_layout(title_text='Stat Category in function of position', title_x=0.5)
            return html.Div([
            html.Br(),
            dcc.Graph(id='g2', figure=fig2)
        ])

@app.callback(
    Output('output-container-button3', 'children'),
    [Input(f'input{i}', 'value') for i in range(1,6)] + [Input('stat_category3', 'value')]
)
def players_career(*values_and_stat):
    stat = values_and_stat[-1]
    player_values = values_and_stat[:-1]

    fig = go.Figure()
    for val in player_values:
        if val and val.lower() in data["list_name_lower"].values:
            df_player = data["df"][data["df"]["LOWER_NAME"] == val.lower()]
            fig.add_trace(go.Scatter(x=df_player["AGE"], y=df_player[stat],
                                     mode='lines+markers', name=val))

    if not fig.data:
        return ""  # Aucun joueur valide

    fig.update_layout(title=dict(text='Comparison of players stats', x=0.5),
                      xaxis_title='Age', yaxis_title=stat)
    return html.Div([html.Br(), dcc.Graph(id='g3', figure=fig)])

@app.callback(
    Output('output-container-button4', 'children'),
    [Input('position_category', 'value'), Input('time_slider', 'value')]
)
def corr_notes(position, min_mpg):
    df_filtered = data["final_note"][data["final_note"]["MPG_REAL"] > min_mpg]
    if position != "general":
        df_filtered = df_filtered[df_filtered["POSITION"] == position]

    fig = px.box(df_filtered, x="AGE", y="NOTE_m_sc")
    fig.update_layout(title_text='Evolution of Players notes', xaxis_title='Age', yaxis_title='Notes', title_x=0.5)

    return html.Div([html.Br(), dcc.Graph(id='g4', figure=fig)])

@app.callback(
    Output('output-container-button5', 'children'),
    [Input('Year', 'value'), Input('age_slider', 'value')]
)
def salary_predict(year, age_range):
    df_filtered = data["salary"][(data["salary"][year] > 0) & (data["salary"]["AGE"].between(age_range[0], age_range[1]))]

    fig = px.scatter(df_filtered, x="NOTE_2020", y=year, color="PLAYER_NAME")
    fig.add_trace(go.Line(x=x1, y=y1, line=dict(color='red', width=4)))
    fig.update_layout(title_text="Player's salary in function of their notes", xaxis_title='Notes', yaxis_title='Salary', title_x=0.5)

    return html.Div([html.Br(), dcc.Graph(id='g5', figure=fig)])


@app.callback(
    Output('output-container-button6', 'children'),
    Input('year_stat1', 'value')
)
def leaders(year_selected):
    df_season = data["leaders_top"][data["leaders_top"]["SEASON"] == int(year_selected)]

    fig7 = go.Figure(data=[go.Table(
    header=dict(
        values=list(df_season.columns),
        align='center'
    ),
    cells=dict(
        values=[df_season[col] for col in df_season.columns],
        align='center'
    ),
    columnwidth=[70, 70, 70, 55, 55] + [40]*(len(df_season.columns)-5)
)])

    return html.Div([
        html.Br(),
        dcc.Graph(id='g6', figure=fig7, style={'height': 525})
    ])

@app.callback(
    Output('output-container-button7', 'children'),
    [Input('team_select', 'value'), Input('stat_select', 'value')])
def team_stats(value3, value4):

        fig8 = go.Figure()
        fig8.add_trace(go.Scatter(x=data["teams"][data["teams"]["TEAM"] == value3]["SEASON"], y=data["teams"][data["teams"]["TEAM"] == value3][value4],
                            mode='lines+markers', name=value3))
        fig8.update_layout(title=dict(text = 'Comparison of teams stats', x=0.5),
                           xaxis_title='Age', yaxis_title=value4)

        return html.Div([
        html.Br(),
        dcc.Graph(id='g7', figure=fig8)
        ])

@app.callback(
    Output('output-container-button8', 'children'),
    [Input('stat_select2', 'value')])
def global_team(value5):

        fig9 = go.Figure()
        fig9.add_trace(go.Scatter(x=data["global_seas"]["SEASON"], y=data["global_seas"][value5],
                        mode='lines+markers'))
        fig9.update_layout(title=dict(text = 'Evolution of the game', x=0.5),
                       xaxis_title='Season', yaxis_title=value5)

        return html.Div([
        html.Br(),
        dcc.Graph(id='g8', figure=fig9)
        ])

def open_browser():
    webbrowser.open_new("http://127.0.0.1:8050/")


if __name__ == '__main__':
    Timer(1, open_browser).start()
    app.run(debug=True, use_reloader=False)
