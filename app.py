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
                    "Hvem løber med sejren, bliver det en sød julebryg, en hidsig stout, måske en mærkelig sour, eller en skøn IPA. "
                    "Bliver det noget surt stats som Ems så godt kan lide. Og har Tejl ændret smagsløj. Hvad siger Stein til det hele, "
                    "og vinder Mikkels øl med gran - følg med hele December!",
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
                            html.Label("Connoisseur", style={"fontWeight": "bold"}),
                            dcc.Dropdown(
                                id='navn-input',
                                options=[{'label': str(x), 'value': x} for x in Navn],
                                placeholder='Vælg connoisseur',
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
                                    data=load_data().to_dict("records"),
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

                        # ---- CHART 5: Person details ----
                        html.Div(
                            style={
                                "backgroundColor": "white",
                                "padding": "20px",
                                "borderRadius": "10px",
                                "boxShadow": "0 2px 6px rgba(0,0,0,0.1)"
                            },
                            children=[
                                html.H3("Vurderinger fra valgt øl connoisseur",
                                        style={"marginTop": 0, "marginBottom": "10px"}),

                                html.Div(
                                    style={"maxWidth": "250px", "marginBottom": "10px"},
                                    children=[                                    
                                        dcc.Dropdown(
                                            id='navn-filter',
                                            options=[{'label': str(x), 'value': x} for x in Navn],
                                            placeholder='Vælg øl connoisseur',
                                            clearable=True
                                        ),
                                    ]
                                ),

                                dcc.Graph(id='navn_detail')
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


# --- Graph 1: Total rating (stacked by Navn, ordered by total) ---
@app.callback(
    Output('samlede_rating', 'figure'),
    Input('table', 'data')
)
def update_bar_chart_1(rows):
    if not rows:
        fig = px.bar()
        fig.update_layout(template='simple_white',
                          title='Den samlede vurdering')
        return fig

    df = pd.DataFrame(rows)

    # Compute total score per row
    df['TotalScore'] = df[['Smag', 'Duft', 'Helhedsoplevelse', 'Booster']].sum(axis=1)

    # Sum total score per øl + navn
    grouped = df.groupby(['Øl', 'Navn'], as_index=False)['TotalScore'].sum()

    # Total per øl for sorting
    total_per_ol = grouped.groupby('Øl', as_index=False)['TotalScore'].sum()
    total_per_ol = total_per_ol.sort_values('TotalScore', ascending=False)
    ol_order = total_per_ol['Øl'].tolist()

    fig = px.bar(
        grouped,
        x='Øl',
        y='TotalScore',
        color='Navn',
        barmode='stack',
        category_orders={'Øl': ol_order},
        labels={'TotalScore': 'Samlet score', 'Øl': 'Øl', 'Navn': 'Navn'},
        color_discrete_sequence=px.colors.qualitative.Pastel1
    )

    fig.update_layout(
        title='Den samlede vurdering',
        template='simple_white',
        margin=dict(t=60, l=40, r=20, b=60),
        legend_title_text=''
    )

    return fig


# --- Graph 2: Smag (stacked by Navn, ordered by total Smag) ---
@app.callback(
    Output('smag_rating', 'figure'),
    Input('table', 'data')
)
def update_bar_chart_2(rows):
    if not rows:
        fig = px.bar()
        fig.update_layout(template='simple_white',
                          title='Smags-vurdering')
        return fig

    df = pd.DataFrame(rows)

    # Sum Smag per øl + navn
    grouped = df.groupby(['Øl', 'Navn'], as_index=False)['Smag'].sum()

    # Total Smag per øl for sorting
    total_smag = grouped.groupby('Øl', as_index=False)['Smag'].sum()
    total_smag = total_smag.sort_values('Smag', ascending=False)
    ol_order = total_smag['Øl'].tolist()

    fig = px.bar(
        grouped,
        x='Øl',
        y='Smag',
        color='Navn',
        barmode='stack',
        category_orders={'Øl': ol_order},
        labels={'Smag': 'Smag', 'Øl': 'Øl'},
        color_discrete_sequence=px.colors.qualitative.Pastel1
    )

    fig.update_layout(
        title='Smags-vurdering',
        template='simple_white',
        margin=dict(t=60, l=40, r=20, b=60),
        legend_title_text=''
    )

    return fig


# --- Graph 3: Duft (stacked by Navn, ordered by total Duft) ---
@app.callback(
    Output('duft_rating', 'figure'),
    Input('table', 'data')
)
def update_bar_chart_3(rows):
    if not rows:
        fig = px.bar()
        fig.update_layout(template='simple_white',
                          title='Duft-vurdering')
        return fig

    df = pd.DataFrame(rows)

    # Sum Duft per øl + navn
    grouped = df.groupby(['Øl', 'Navn'], as_index=False)['Duft'].sum()

    # Total Duft per øl for sorting
    total_duft = grouped.groupby('Øl', as_index=False)['Duft'].sum()
    total_duft = total_duft.sort_values('Duft', ascending=False)
    ol_order = total_duft['Øl'].tolist()

    fig = px.bar(
        grouped,
        x='Øl',
        y='Duft',
        color='Navn',
        barmode='stack',
        category_orders={'Øl': ol_order},
        labels={'Duft': 'Duft', 'Øl': 'Øl'},
        color_discrete_sequence=px.colors.qualitative.Pastel1
    )

    fig.update_layout(
        title='Duft-vurdering',
        template='simple_white',
        margin=dict(t=60, l=40, r=20, b=60),
        legend_title_text=''
    )

    return fig


# --- Graph 4: Helhedsoplevelse (stacked by Navn, ordered by total) ---
@app.callback(
    Output('helhedsoplevelse_rating', 'figure'),
    Input('table', 'data')
)
def update_bar_chart_4(rows):
    if not rows:
        fig = px.bar()
        fig.update_layout(template='simple_white',
                          title='Helhedsvurdering')
        return fig

    df = pd.DataFrame(rows)

    # Sum Helhedsoplevelse per øl + navn
    grouped = df.groupby(['Øl', 'Navn'], as_index=False)['Helhedsoplevelse'].sum()

    # Total Helhedsoplevelse per øl for sorting
    total_helhed = grouped.groupby('Øl', as_index=False)['Helhedsoplevelse'].sum()
    total_helhed = total_helhed.sort_values('Helhedsoplevelse', ascending=False)
    ol_order = total_helhed['Øl'].tolist()

    fig = px.bar(
        grouped,
        x='Øl',
        y='Helhedsoplevelse',
        color='Navn',
        barmode='stack',
        category_orders={'Øl': ol_order},
        labels={'Helhedsoplevelse': 'Helhedsoplevelse', 'Øl': 'Øl'},
        color_discrete_sequence=px.colors.qualitative.Pastel1
    )

    fig.update_layout(
        title='Helhedsvurdering',
        template='simple_white',
        margin=dict(t=60, l=40, r=20, b=60),
        legend_title_text=''
    )

    return fig


# --- Graph 5: Detaljer for valgt ekspert ---
@app.callback(
    Output('navn_detail', 'figure'),
    Input('table', 'data'),
    Input('navn-filter', 'value')
)
def update_navn_detail(rows, selected_navn):
    # No data or no name selected -> empty-ish figure
    if not rows or selected_navn is None:
        fig = px.bar()
        fig.update_layout(
            template='simple_white',
            title='Vælg en øl connoisseur'
        )
        return fig

    df = pd.DataFrame(rows)

    # Filter for the chosen name
    df = df[df['Navn'] == selected_navn]

    if df.empty:
        fig = px.bar()
        fig.update_layout(
            template='simple_white',
            title=f'Ingen data for connoisseur {selected_navn}'
        )
        return fig

    # Sum components per øl for this person
    grouped = df.groupby('Øl', as_index=False)[['Smag', 'Duft', 'Helhedsoplevelse', 'Booster']].sum()

    # Total per øl for ordering
    grouped['Total'] = grouped[['Smag', 'Duft', 'Helhedsoplevelse', 'Booster']].sum(axis=1)
    grouped = grouped.sort_values('Total', ascending=False)
    ol_order = grouped['Øl'].tolist()

    # Long format for stacked bar
    plot_df = grouped.melt(
        id_vars='Øl',
        value_vars=['Smag', 'Duft', 'Helhedsoplevelse', 'Booster'],
        var_name='Kategori',
        value_name='Score'
    )

    fig = px.bar(
        plot_df,
        x='Øl',
        y='Score',
        color='Kategori',
        barmode='stack',
        category_orders={'Øl': ol_order},
        labels={'Score': 'Score', 'Øl': 'Øl', 'Kategori': 'Bidrag'},
        color_discrete_sequence=px.colors.qualitative.Pastel1
    )

    fig.update_layout(
        title=f'Vurderinger for øl connoisseur {selected_navn}',
        template='simple_white',
        margin=dict(t=60, l=40, r=20, b=60),
        legend_title_text=''
    )

    return fig


if __name__ == "__main__":
    app.run_server(debug=True)
