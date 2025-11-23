# -*- coding: utf-8 -*-
"""
Beer rating Dash app
Created on Sun Nov 23 13:24:19 2025

@author: mikkel
"""
import os
import pandas as pd
import plotly.express as px
import dash
from dash import html, dcc
from dash.dependencies import Input, Output, State
import dash.dash_table as dt

# ---------- File storage settings ----------
# This will create/use beer_ratings.csv in the same folder as this .py file
DATA_FILE = os.path.join(os.path.dirname(__file__), "beer_ratings.csv")

COLUMNS = ['Dato', 'Øl', 'Navn', 'Smag', 'Duft', 'Helhedsoplevelse', 'Booster']

def load_data():
    """Load ratings from CSV, or return empty DataFrame if file does not exist."""
    if os.path.exists(DATA_FILE):
        df = pd.read_csv(DATA_FILE)
        # Make sure all expected columns exist
        missing = [c for c in COLUMNS if c not in df.columns]
        for c in missing:
            df[c] = None
        return df[COLUMNS]
    else:
        # No file yet -> start empty
        return pd.DataFrame(columns=COLUMNS)


def save_data(df: pd.DataFrame):
    """Save ratings to CSV."""
    df.to_csv(DATA_FILE, index=False)

# --------- Hardcoded allowed values (choices) ---------
Date = list(range(1, 25))
Øl = ['Øl1', 'Øl2', 'Øl3', 'Øl4']
Navn = ['Tejl', 'Stein', 'Ems', 'Miks']
Smag = [1, 2, 3, 4, 5]
Duft = [1, 2, 3, 4, 5]
Helhedsoplevelse = [1, 2, 3, 4, 5]
Booster = [0, 2]

# --------- empty df (for reference / debugging) ---------
initial_df = load_data()

# --------- Build Dash app ---------
app = dash.Dash(__name__)

server = app.server  # <- this is what PythonAnywhere will use

app.layout = html.Div(
    style={
        "fontFamily": "Arial, sans-serif",
        "backgroundColor": "#f5f5f5",
        "minHeight": "100vh",
        "padding": "20px"
    },
    children=[
        # Header
        html.Div(
            style={
                "backgroundColor": "white",
                "padding": "15px 25px",
                "borderRadius": "10px",
                "boxShadow": "0 2px 6px rgba(0,0,0,0.1)",
                "marginBottom": "20px"
            },
            children=[
                html.H1("Øl Julekalender 2025!", style={"margin": 0}),
                html.P(
                    "Hvem løber med sejren, bliver det en sød julebryg, en hidsig stout, måske en mærkelig sour, eller en skøn IPA. Bliver det noget surt stats som Ems så godt kan lide. Og har Tejl ændret smagsløj. Hvad siger Stein til det hele, og vinder Mikkels øl med gran - følg med hele December!",
                    style={"marginTop": "5px", "color": "#555"}
                )
            ]
        ),

        # Main content: left = inputs, right = table + charts
        html.Div(
            style={
                "display": "flex",
                "gap": "20px",
                "alignItems": "flex-start"
            },
            children=[
                # LEFT: Input panel
                html.Div(
                    style={
                        "flex": "0 0 320px",
                        "backgroundColor": "white",
                        "padding": "20px",
                        "borderRadius": "10px",
                        "boxShadow": "0 2px 6px rgba(0,0,0,0.1)"
                    },
                    children=[
                        html.H3("Giv bedømmelse", style={"marginTop": 0}),

                        html.Div([
                            html.Label("Dato", style={"fontWeight": "bold"}),
                            dcc.Dropdown(
                                id='dato-input',
                                options=[{'label': x, 'value': x} for x in Date],
                                placeholder='Vælg dato',
                                style={"marginBottom": "12px"}
                            ),
                        ]),

                        html.Div([
                            html.Label("Øl", style={"fontWeight": "bold"}),
                            dcc.Dropdown(
                                id='ol-input',
                                options=[{'label': x, 'value': x} for x in Øl],
                                placeholder='Vælg øl',
                                style={"marginBottom": "12px"}
                            ),
                        ]),

                        html.Div([
                            html.Label("Ekspert", style={"fontWeight": "bold"}),
                            dcc.Dropdown(
                                id='navn-input',
                                options=[{'label': str(x), 'value': x} for x in Navn],
                                placeholder='Vælg ekspert',
                                style={"marginBottom": "12px"}
                            ),
                        ]),

                        html.Hr(),

                        html.Div([
                            html.Label("Smag", style={"fontWeight": "bold"}),
                            dcc.Dropdown(
                                id='smag-input',
                                options=[{'label': str(x), 'value': x} for x in Smag],
                                placeholder='Vælg smag (1–5)',
                                style={"marginBottom": "12px"}
                            ),
                        ]),

                        html.Div([
                            html.Label("Duft", style={"fontWeight": "bold"}),
                            dcc.Dropdown(
                                id='duft-input',
                                options=[{'label': str(x), 'value': x} for x in Duft],
                                placeholder='Vælg duft (1–5)',
                                style={"marginBottom": "12px"}
                            ),
                        ]),

                        html.Div([
                            html.Label("Helhedsoplevelse", style={"fontWeight": "bold"}),
                            dcc.Dropdown(
                                id='helhedsoplevelse-input',
                                options=[{'label': str(x), 'value': x} for x in Helhedsoplevelse],
                                placeholder='Vælg helhedsoplevelse (1–5)',
                                style={"marginBottom": "12px"}
                            ),
                        ]),

                        html.Hr(),

                        html.Div([
                            html.Label("BeerLicious Booster", style={"fontWeight": "bold"}),
                            dcc.Dropdown(
                                id='booster-input',
                                options=[{'label': str(x), 'value': x} for x in Booster],
                                placeholder='Skal den have en beerlicious booster?',
                                style={"marginBottom": "16px"}
                            ),
                        ]),

                        html.Button(
                            "Giv bedømmelse",
                            id='add-row',
                            n_clicks=0,
                            style={
                                "width": "100%",
                                "backgroundColor": "#2c7be5",
                                "color": "white",
                                "border": "none",
                                "padding": "10px 0",
                                "borderRadius": "6px",
                                "fontWeight": "bold",
                                "cursor": "pointer"
                            }
                        ),
                        html.Div(id="feedback", style={"marginTop": "8px", "color": "#b00020"})
                    ]
                ),

                # RIGHT: Table + charts STACKED
                html.Div(
                    style={
                        "flex": "1",
                        "display": "flex",
                        "flexDirection": "column",
                        "gap": "30px"
                    },
                    children=[

                        # ---- TABLE CARD ----
                        html.Div(
                            style={
                                "backgroundColor": "white",
                                "padding": "15px",
                                "borderRadius": "10px",
                                "boxShadow": "0 2px 6px rgba(0,0,0,0.1)"
                            },
                            children=[
                                html.H3("Bedømmelser:", style={"marginTop": 0}),
                                dt.DataTable(
                                    id='table',
                                    columns=[
                                        {'name': 'Dato', 'id': 'Dato'},
                                        {'name': 'Øl', 'id': 'Øl'},
                                        {'name': 'Navn', 'id': 'Navn'},
                                        {'name': 'Smag', 'id': 'Smag'},
                                        {'name': 'Duft', 'id': 'Duft'},
                                        {'name': 'Helhedsoplevelse', 'id': 'Helhedsoplevelse'},
                                        {'name': 'Booster', 'id': 'Booster'},
                                    ],
                                    data=initial_df.to_dict("records"),
                                    row_deletable=False,
                                    page_size=10,
                                    style_table={'overflowX': 'auto'},
                                    style_cell={
                                        'textAlign': 'center',
                                        'padding': '4px'
                                    },
                                    style_header={
                                        'backgroundColor': '#f0f0f0',
                                        'fontWeight': 'bold'
                                    }
                                )
                            ]
                        ),

                        # ---- CHART 1: Total Rating ----
                        html.Div(
                            style={
                                "backgroundColor": "white",
                                "padding": "20px",
                                "borderRadius": "10px",
                                "boxShadow": "0 2px 6px rgba(0,0,0,0.1)"
                            },
                            children=[
                                dcc.Graph(id='samlede_rating')
                            ]
                        ),

                        # ---- CHART 2: Smag ----
                        html.Div(
                            style={
                                "backgroundColor": "white",
                                "padding": "20px",
                                "borderRadius": "10px",
                                "boxShadow": "0 2px 6px rgba(0,0,0,0.1)"
                            },
                            children=[
                                dcc.Graph(id='smag_rating')
                            ]
                        ),

                        # ---- CHART 3: Duft ----
                        html.Div(
                            style={
                                "backgroundColor": "white",
                                "padding": "20px",
                                "borderRadius": "10px",
                                "boxShadow": "0 2px 6px rgba(0,0,0,0.1)"
                            },
                            children=[
                                dcc.Graph(id='duft_rating')
                            ]
                        ),

                        # ---- CHART 4: Helhedsoplevelse ----
                        html.Div(
                            style={
                                "backgroundColor": "white",
                                "padding": "20px",
                                "borderRadius": "10px",
                                "boxShadow": "0 2px 6px rgba(0,0,0,0.1)"
                            },
                            children=[
                                dcc.Graph(id='helhedsoplevelse_rating')
                            ]
                        ),
                    ]
                )
            ]
        )
    ]
)

# --- Callback: add a row when button is clicked ---
@app.callback(
    Output('table', 'data'),
    Input('add-row', 'n_clicks'),
    State('table', 'data'),
    State('dato-input', 'value'),
    State('ol-input', 'value'),
    State('navn-input', 'value'),
    State('smag-input', 'value'),
    State('duft-input', 'value'),
    State('helhedsoplevelse-input', 'value'),
    State('booster-input', 'value'),
    prevent_initial_call=True
)
def add_row(n_clicks, current_rows, dato,
            ol, navn, smag, duft, helhed, booster):

    rows = current_rows or []

    # Enforce: nothing may be NULL
    if not all(v is not None for v in [dato, ol, navn, smag, duft, helhed, booster]):
        return rows

    new_row = {
        'Dato': dato,
        'Øl': ol,
        'Navn': navn,
        'Smag': smag,
        'Duft': duft,
        'Helhedsoplevelse': helhed,
        'Booster': booster
    }

    rows.append(new_row)

    df = pd.DataFrame(rows, columns=COLUMNS)
    save_data(df)   

    return rows

# --- Graph 1: Total rating ---
@app.callback(
    Output('samlede_rating', 'figure'),
    Input('table', 'data')
)
def update_bar_chart_1(rows):
    if not rows:
        return px.bar()

    df = pd.DataFrame(rows)
    df['TotalScore'] = df[['Smag', 'Duft', 'Helhedsoplevelse', 'Booster']].sum(axis=1)
    df = df.sort_values('Dato')

    grouped = df.groupby(['Øl', 'Navn'], as_index=False)['TotalScore'].sum()

    fig = px.bar(
        grouped,
        x='Øl',
        y='TotalScore',
        color='Navn',
        barmode='stack',
        labels={'TotalScore': 'Samlet score', 'Øl': 'Øl'}
    )

    fig.update_layout(
        title='Samlet rating pr. øl (stacked efter navn)',
        margin=dict(t=60, l=40, r=20, b=40)
    )

    return fig


# --- Graph 2: Smag ---
@app.callback(
    Output('smag_rating', 'figure'),
    Input('table', 'data')
)
def update_bar_chart_2(rows):
    if not rows:
        return px.bar()

    df = pd.DataFrame(rows)
    df = df.sort_values('Dato')
    grouped = df.groupby(['Øl', 'Navn'], as_index=False)['Smag'].sum()

    fig = px.bar(
        grouped,
        x='Øl',
        y='Smag',
        color='Navn',
        barmode='stack',
        labels={'Smag': 'Smag', 'Øl': 'Øl'}
    )

    fig.update_layout(
        title='Rating – Smag',
        margin=dict(t=60, l=40, r=20, b=40)
    )

    return fig


# --- Graph 3: Duft ---
@app.callback(
    Output('duft_rating', 'figure'),
    Input('table', 'data')
)
def update_bar_chart_3(rows):
    if not rows:
        return px.bar()

    df = pd.DataFrame(rows)
    df = df.sort_values('Dato')
    grouped = df.groupby(['Øl', 'Navn'], as_index=False)['Duft'].sum()

    fig = px.bar(
        grouped,
        x='Øl',
        y='Duft',
        color='Navn',
        barmode='stack',
        labels={'Duft': 'Duft', 'Øl': 'Øl'}
    )

    fig.update_layout(
        title='Rating – Duft',
        margin=dict(t=60, l=40, r=20, b=40)
    )

    return fig


# --- Graph 4: Helhedsoplevelse ---
@app.callback(
    Output('helhedsoplevelse_rating', 'figure'),
    Input('table', 'data')
)
def update_bar_chart_4(rows):
    if not rows:
        return px.bar()

    df = pd.DataFrame(rows)
    df = df.sort_values('Dato')
    grouped = df.groupby(['Øl', 'Navn'], as_index=False)['Helhedsoplevelse'].sum()

    fig = px.bar(
        grouped,
        x='Øl',
        y='Helhedsoplevelse',
        color='Navn',
        barmode='stack',
        labels={'Helhedsoplevelse': 'Helhedsoplevelse', 'Øl': 'Øl'}
    )

    fig.update_layout(
        title='Rating – Helhedsoplevelse',
        margin=dict(t=60, l=40, r=20, b=40)
    )

    return fig


if __name__ == "__main__":
    app.run_server(debug=True)
