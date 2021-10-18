## custom imports 
import get_connected

import dash 
from dash import dash_table
from dash.dependencies import Input, Output, State
from dash import dcc
import dash_bootstrap_components as dbc
from dash import html
import plotly.express as px    

import pandas as pd             


## initilazing the app and adding bootstrap theme


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.COSMO],
                meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=1.0'}]
                )
server = app.server

## getting the data from NTG

host="mysql-prod-db2-rds.csxffbq6aqlg.us-west-2.rds.amazonaws.com"
port=4475
user="dvNZm538"
passwd="m53849"
database='NationalT_1009278'

main_db = get_connected.get_connection(host, port, user, passwd, database)
conn_check = get_connected.check_connection(main_db)

mycursor = main_db.cursor()

## Collecting  data 
query_1 = 'select * from AOL_Customer_Segmentation_Custom '

mycursor.execute(query_1)
result_data_1 = mycursor.fetchall()
query_2 = 'desc AOL_Customer_Segmentation_Custom'

mycursor.execute(query_2)
result_data_2 = mycursor.fetchall()


mycursor.close()
main_db.close()
conn_check = get_connected.check_connection(main_db)



## getting col names for out table
data_for_df = [record for record in result_data_2]

## creating df 
desc_df = pd.DataFrame(data_for_df, columns =['Field', 'Type', 'NULL', 'Key', 'Default', 'Extra'])

## converting our query results into df
data_for_df = [record for record in result_data_1] ## list of tuples for creating dataframe

# creating df 
col_names = desc_df.Field.unique().tolist()
main_df = pd.DataFrame(data_for_df, columns =col_names)


## creating the layout
table_cols = ['CUSTOMER', 'BRANCH', 'SALES REP', 'Avg Sales (Previous 3 Months)', 'Org Avg Sales (Previous 3 Months)', 'Last Mont Sales', 'Org Last Month Sales', 'Sales MTD', 
              'Avg Orders (Prv 3 Months)', 'Last Mont Orders', 'Orders MTD']

app.layout = dbc.Container([
    ## first row
    dbc.Row(
        dbc.Col(html.H1("Customer Spend Analysis", className="text-center text-primary mt-3 mb-5", style={"font-size":"40px"}), width=12)
    ), 

    ## second row
    dbc.Row(
        [
            dbc.Col(dcc.Dropdown(id="division_drpdwn", multi=False, value='',
                options=[{'label': x, 'value': x} for x in main_df.DIVISION.unique()], placeholder='Company Name'), width=2), 

            dbc.Col(dcc.Dropdown(id="branch_drpdwn", multi=False, value='',
                options=[{'label': x, 'value': x} for x in main_df.BRANCH.unique()], placeholder='Branch Name'), width=2),

            dbc.Col(dcc.Dropdown(id="rep_drpdwn", multi=False, value='',
                options=[{'label': x, 'value': x} for x in main_df.SALES_PERSON.unique()], placeholder='Sales Rep Name'), width=2), 

            dbc.Col(dcc.Dropdown(id="cust_drpdwn", multi=False, value='',
                options=[{'label': x, 'value': x} for x in main_df.CUSTOMER_NAME.unique()], placeholder='Customer Name'), width=2),

            dbc.Col(dcc.Dropdown(id="spending_less_drpdwn", multi=False, value='',
                options=[{'label': x, 'value': x} for x in ['YES', 'NO']], placeholder='Spending Less'), width=2),

            dbc.Col(dcc.Dropdown(id="spending_less_often_drpdwn", multi=False, value='',
                options=[{'label': x, 'value': x} for x in ['YES', 'NO']], placeholder='Spending Less Often'), width=2),

        ], className="mb-2 ml-2 mr-2", justify='center'),

    ## thrid row
    dbc.Row(
        [
            dbc.Col(dcc.Dropdown(id="new_cust_drpdwn", multi=False, value='',
                options=[{'label': x, 'value': x} for x in ['YES', 'NO']], placeholder='New Customers'), width=2),

            dbc.Col(dcc.Dropdown(id="reactivated_cust_drpdwn", multi=False, value='',
                options=[{'label': x, 'value': x} for x in ['YES', 'NO']], placeholder='Reactivated Customers'), width=2),

        ], className="mb-4 ml-2 mr-2", justify='start'),
    
    ## fourth row
    dbc.Row(
        [   ## card one
            dbc.Col(
                [
                    dbc.Card(
                        [
                            dbc.CardBody(
                                [
                                    html.H6('Customers Spending Less', className="card-title font-weight-bold text-primary card-header"),
                                    html.H2(id='Cust_Spending_Less_Card', children="0", style={"font-size":"70px"})
                                ], className="text-center")

                        ], style={"height": "250px"})

                ], width=3),

            ## card two
            dbc.Col(
                [
                    dbc.Card(
                        [
                            dbc.CardBody(
                                [
                                    html.H6('Customers Spending Less Often', className="card-title font-weight-bold text-primary card-header"),
                                    html.H2(id='Cust_Spending_Less_Often_Card', children="0", style={"font-size":"70px"})
                                ], className="text-center")

                        ], style={"height": "250px"})

                ], width=3), 

            ## card three
            dbc.Col(
                [
                    dbc.Card(
                        [
                            dbc.CardBody(
                                [
                                    html.H6('New Customers', className="card-title font-weight-bold text-primary card-header"),
                                    html.H2(id='New_Customers_Card', children="0", style={"font-size":"70px"})
                                ], className="text-center")

                        ], style={"height": "250px"})

                ], width=3), 

            ## card four
            dbc.Col(
                [
                    dbc.Card(
                        [
                            dbc.CardBody(
                                [
                                    html.H6('Reactivated Customers', className="card-title font-weight-bold text-primary card-header"),
                                    html.H2(id='Reactivated_Customers_Card', children="0", style={"font-size":"70px"})
                                ], className="text-center")

                        ], style={"height": "250px"})

                ], className="mb-2", width=3),

            ## card five
            dbc.Col(
                [
                    dbc.Card(
                        [
                            dbc.CardBody(
                                [
                                    html.H6('Sales Opportunity Lost Last Month', className="card-title font-weight-bold text-primary card-header"),
                                    html.H2(id='Sales_Lost_Card', children="0", style={"font-size":"70px"})
                                ], className="text-center")

                        ], style={"height": "250px"})

                ], width=12),

        ], className="mb-4 ml-2 mr-2", justify='center'),
    
    ## fifth row
    dbc.Row([
        dbc.Col(
            html.H6('Detailed Table', className='text-start text-primary font-weight-bold mb-2', style={"font-size":"20px"})
        ),
        dbc.Col(
            dash_table.DataTable(
                id='table',
                columns=[{"name": i, "id": i} for i in table_cols],
                style_cell={'textAlign': 'left', 'font-family':'sans-serif', 'padding':'5x'},
                style_as_list_view=False,
                style_header={
                    'textAlign': 'center',
                    'backgroundColor': 'light blue',
                    'fontWeight': 'bold',
                    'font-family':'sans-serif'},
                page_size=10,
            ), width=12
        )], className="mb-4 ml-2 mr-2", justify='center')


], fluid=True)




## callbacks 
## updating cards based on input filters

@app.callback(
    [
        Output('Cust_Spending_Less_Card','children'),
        Output('Cust_Spending_Less_Often_Card','children'),
        Output('New_Customers_Card','children'),
        Output('Reactivated_Customers_Card','children'),
        Output('Sales_Lost_Card','children')
    ],
    [
        Input('division_drpdwn','value'),
        Input('branch_drpdwn','value'),
        Input('rep_drpdwn','value'),
        Input('cust_drpdwn','value'),
        Input('spending_less_drpdwn','value'),
        Input('spending_less_often_drpdwn','value'),
        Input('new_cust_drpdwn','value'),
        Input('reactivated_cust_drpdwn','value')
    ],
)

def update_cards(division, branch, sales_rep, customer, spending_less, spending_less_often, new_customers, reactivated_customers):
    ## Customers Spending Less
    df = main_df[(main_df['DIVISION'] == division) & (main_df['BRANCH'] == branch) & (main_df['SALES_PERSON'] == sales_rep) & (main_df['CUSTOMER_NAME'] == customer)]
    # num_cust_spending_less = df[(df['SPENDING_LESS_FLAG'] == spending_less) & (df['SPENDING_LESS_OFTEN_FLAG'] == spending_less_often) & (df['NEW_CUSTOMERS_FLAG'] == new_customers)
    #                                 & (df['REVISITING_CUSTOMERS_FLAG'] == reactivated_customers)].shape[0]

    if spending_less == 'YES':
        num_cust_spending_less = df[df['SPENDING_LESS_FLAG'] == 'YES'].shape[0]
    else:
        num_cust_spending_less = 0

    if spending_less_often == 'YES':
        num_cust_spending_less_often = df[df['SPENDING_LESS_OFTEN_FLAG'] == 'YES'].shape[0]
    else:
        num_cust_spending_less_often = 0

    if new_customers == 'YES':
        num_new_custs = df[df['NEW_CUSTOMERS_FLAG'] == 'YES'].shape[0]
    else:
        num_new_custs = 0

    if reactivated_customers == 'YES':
        num_reactivated_custs = df[df['REVISITING_CUSTOMERS_FLAG'] == 'YES'].shape[0]
    else:
        num_reactivated_custs = 0

    sales_lost = round(df['SALES_OPPORTUNITY_LAST_MONTH'].sum())

    
    return num_cust_spending_less, num_cust_spending_less_often, num_new_custs, num_reactivated_custs, sales_lost

@app.callback(
        Output('table','data'),
        Input('division_drpdwn','value'),
        Input('branch_drpdwn','value'),
        # Input('rep_drpdwn','value'),
        # Input('cust_drpdwn','value'),
        # Input('spending_less_drpdwn','value'),
        # Input('spending_less_often_drpdwn','value'),
        # Input('new_cust_drpdwn','value'),
        # Input('reactivated_cust_drpdwn','value'),
)

def update_table(division, branch):
    df = main_df[(main_df['DIVISION'] == division) & (main_df['BRANCH'] == branch)]
    df = df[['CUSTOMER_NAME', 'BRANCH', 'SALES_PERSON', 'LAST_3_MONTHS_AVERAGE_SPEND', 'ORG_LAST_3_MONTHS_AVERAGE_SPEND', 'LAST_MONTH_SALES', 'ORG_LAST_MONTH_SALES', 
            'SALES_MTD', 'LAST_3_MONTHS_AVERAGE_ORDERS', 'LAST_MONTH_ORDERS', 'ORDERS_MTD']]
    
    df = df.rename(columns={old_name: new_name for old_name, new_name in zip(df.columns, table_cols)})

    data = df.to_dict('records')
    
    
    return data


if __name__ == '__main__':
    app.run_server(debug=False)
