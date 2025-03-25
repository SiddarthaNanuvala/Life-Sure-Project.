import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import traceback

try:
    # Load the dataset
    print("Loading dataset...")
    df = pd.read_csv(r'S:\Esilv sem 2\Explanability AI Project\insurance.csv')
    print("Dataset loaded successfully!")

    # Add a 'risk_category' column
    def classify_risk(row):
        if row['smoker'] == 'yes':
            return 'High Risk'
        elif row['bmi'] >= 30:
            return 'Medium Risk'
        else:
            return 'Low Risk'

    print("Adding risk category column...")
    df['risk_category'] = df.apply(classify_risk, axis=1)
    print("Risk category column added successfully!")

    # Initialize the Dash app
    print("Initializing Dash app...")
    app = dash.Dash(__name__)
    print("Dash app initialized successfully!")

    # Define styles
    CARD_STYLE = {
        'padding': '20px',
        'margin': '10px',
        'border-radius': '5px',
        'box-shadow': '0 4px 6px rgba(0, 0, 0, 0.1)',
        'background-color': 'white'
    }

    METRIC_CARD_STYLE = {
        'textAlign': 'center',
        'padding': '20px',
        'margin': '10px',
        'border-radius': '5px',
        'box-shadow': '0 4px 6px rgba(0, 0, 0, 0.1)',
        'background-color': '#f8f9fa'
    }

    # App layout
    app.layout = html.Div([
        # Header
        html.Div([
            html.H1("LifeSure Insurance Dashboard", style={'textAlign': 'center', 'color': '#2c3e50', 'marginBottom': '30px'})
        ]),

        # Filters Section
        html.Div([
            html.Div([
                # Region Filter
                html.Div([
                    html.Label("Select Region:", style={'fontWeight': 'bold'}),
                    dcc.Dropdown(
                        id='region-dropdown',
                        options=[{'label': region, 'value': region} for region in df['region'].unique()],
                        value='southeast',
                        multi=False,
                        placeholder="Select a Region"
                    )
                ], style={'flex': 1, 'marginRight': '20px'}),

                # Age Range Filter
                html.Div([
                    html.Label("Select Age Range:", style={'fontWeight': 'bold'}),
                    dcc.RangeSlider(
                        id='age-slider',
                        min=df['age'].min(),
                        max=df['age'].max(),
                        step=1,
                        marks={i: str(i) for i in range(df['age'].min(), df['age'].max() + 1, 10)},
                        value=[df['age'].min(), df['age'].max()]
                    )
                ], style={'flex': 2}),

                # Smoker Status Filter
                html.Div([
                    html.Label("Filter by Smoker Status:", style={'fontWeight': 'bold'}),
                    dcc.Checklist(
                        id='smoker-checklist',
                        options=[{'label': 'Smoker', 'value': 'yes'}, {'label': 'Non-Smoker', 'value': 'no'}],
                        value=['yes', 'no'],
                        inline=True
                    )
                ], style={'flex': 1})
            ], style={'display': 'flex', 'gap': '20px', 'marginBottom': '20px'})
        ], style=CARD_STYLE),

        # Key Metrics Section
        html.Div([
            html.Div([
                html.Div(id='total-customers', style=METRIC_CARD_STYLE),
                html.Div(id='avg-charges', style=METRIC_CARD_STYLE),
                html.Div(id='smoker-ratio', style=METRIC_CARD_STYLE),
                html.Div(id='high-risk-percentage', style=METRIC_CARD_STYLE)
            ], style={'display': 'flex', 'justifyContent': 'space-between'})
        ], style=CARD_STYLE),

        # Charts Section
        html.Div([
            # First Row of Charts
            html.Div([
                html.Div([
                    dcc.Graph(id='charges-by-region')
                ], style={'flex': 1}),
                html.Div([
                    dcc.Graph(id='age-vs-charges')
                ], style={'flex': 1})
            ], style={'display': 'flex', 'gap': '20px', 'marginBottom': '20px'}),

            # Second Row of Charts
            html.Div([
                html.Div([
                    dcc.Graph(id='charges-by-risk')
                ], style={'flex': 1}),
                html.Div([
                    dcc.Graph(id='customer-distribution')
                ], style={'flex': 1})
            ], style={'display': 'flex', 'gap': '20px', 'marginBottom': '20px'}),

            # Third Row - Correlation Heatmap
            html.Div([
                dcc.Graph(id='correlation-heatmap')
            ])
        ], style=CARD_STYLE)
    ], style={'padding': '20px', 'backgroundColor': '#f0f2f5'})

    # Callbacks for interactivity
    @app.callback(
        [Output('charges-by-region', 'figure'),
         Output('age-vs-charges', 'figure'),
         Output('charges-by-risk', 'figure'),
         Output('customer-distribution', 'figure'),
         Output('correlation-heatmap', 'figure'),
         Output('total-customers', 'children'),
         Output('avg-charges', 'children'),
         Output('smoker-ratio', 'children'),
         Output('high-risk-percentage', 'children')],
        [Input('region-dropdown', 'value'),
         Input('age-slider', 'value'),
         Input('smoker-checklist', 'value')]
    )
    def update_graphs(selected_region, selected_age_range, selected_smokers):
        # Filter data based on inputs
        filtered_df = df[
            (df['region'] == selected_region) &
            (df['age'] >= selected_age_range[0]) &
            (df['age'] <= selected_age_range[1]) &
            (df['smoker'].isin(selected_smokers))
        ]
        
        # Calculate metrics
        total_customers = len(filtered_df)
        avg_charges = filtered_df['charges'].mean()
        smoker_percentage = (filtered_df['smoker'] == 'yes').mean() * 100
        high_risk_percentage = (filtered_df['risk_category'] == 'High Risk').mean() * 100

        # Bar chart: Average charges by region
        avg_charges_df = filtered_df.groupby('region')['charges'].mean().reset_index()
        bar_fig = px.bar(avg_charges_df, x='region', y='charges', 
                        title="Average Charges by Region",
                        color_discrete_sequence=['#2ecc71'])
        
        # Scatter plot: Age vs Charges
        scatter_fig = px.scatter(filtered_df, x='age', y='charges', color='smoker',
                             title="Age vs Insurance Charges (Smoker vs Non-Smoker)",
                             color_discrete_map={'yes': '#e74c3c', 'no': '#2ecc71'})
        
        # Boxplot: Charges by risk category
        box_fig = px.box(filtered_df, x='risk_category', y='charges', 
                        title="Insurance Charges by Risk Category",
                        color='risk_category', 
                        color_discrete_map={
                            'High Risk': '#e74c3c',
                            'Medium Risk': '#f39c12',
                            'Low Risk': '#2ecc71'
                        })
        
        # Pie chart: Customer distribution by region
        customer_distribution = filtered_df['region'].value_counts().reset_index()
        customer_distribution.columns = ['region_name', 'count']
        pie_fig = px.pie(customer_distribution, names='region_name', values='count',
                        title="Customer Distribution by Region",
                        color_discrete_sequence=px.colors.qualitative.Set3)
        
        # Heatmap: Correlation matrix
        corr_matrix = filtered_df[['age', 'bmi', 'children', 'charges']].corr()
        heatmap_fig = px.imshow(corr_matrix, text_auto=True, 
                               title="Correlation Matrix",
                               color_continuous_scale='RdBu')

        # Format metric cards
        metric_cards = [
            html.Div([
                html.H4("Total Customers"),
                html.H2(f"{total_customers:,}")
            ]),
            html.Div([
                html.H4("Average Charges"),
                html.H2(f"${avg_charges:,.2f}")
            ]),
            html.Div([
                html.H4("Smoker Ratio"),
                html.H2(f"{smoker_percentage:.1f}%")
            ]),
            html.Div([
                html.H4("High Risk Customers"),
                html.H2(f"{high_risk_percentage:.1f}%")
            ])
        ]
        
        return bar_fig, scatter_fig, box_fig, pie_fig, heatmap_fig, *metric_cards

    # Run the app
    if __name__ == '__main__':
        print("Starting the server...")
        app.run(debug=True)
except Exception as e:
    print("An error occurred:")
    print(traceback.format_exc())