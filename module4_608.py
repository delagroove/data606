import pandas as pd
import numpy as np
import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html

app = dash.Dash()

theurl = ('https://data.cityofnewyork.us/resource/nwxe-4ae8.json?' +\
        '$select=boroname,spc_common,count(tree_id)' +\
        '&$group=boroname,spc_common').replace(' ', '%20')
the_json = pd.read_json(theurl)

boroughs = the_json['boroname'].unique()
species = the_json['spc_common'].unique()

app.layout = html.Div([
    html.Div([
        dcc.Dropdown(id='boro',
                     options=[{'label': i, 'value': i} for i in boroughs],
                     placeholder='Borough: '),
        dcc.Graph(id='health_prop'),
        dcc.Dropdown(id='spc',
                     options=[{'label': i, 'value': i} for i in species],
                     placeholder='Species: '),

        dcc.Graph(id='steward')],
        style={'columnCount': 2}),

    # Hidden div inside the app that stores the intermediate value
    html.Div(id='value-holder', style={'display': 'none'})
])

@app.callback(
    dash.dependencies.Output('value-holder', 'children'),
    [dash.dependencies.Input('boro', 'value'),
     dash.dependencies.Input('spc', 'value')])



def get_data(boro,spc):
    if spc is None:
        url = ('https://data.cityofnewyork.us/resource/nwxe-4ae8.json?' +\
            '$select=steward,health,count(tree_id)' +\
            '&$where=boroname=\'' + boro + '\'' +
            '&$group=steward,health' +\
            '&$order=steward,health').replace(' ', '%20')
    else:
        url = ('https://data.cityofnewyork.us/resource/nwxe-4ae8.json?' +\
            '$select=steward,health,count(tree_id)' +\
            '&$where=boroname=\'' + boro + '\'&spc_common=\'' + spc + '\'' +
            '&$group=steward,health' +\
            '&$order=steward,health').replace(' ', '%20')

    df = pd.read_json(url)
    print df['steward']
    categories = []
    # map the names to the current value in the db and sort them
    if None in df['steward']:
        df['steward'] = df['steward'].replace({'None':'None'})
        categories.push('None');
    if '1or2' in df['steward']:
        df['steward'] = df['steward'].replace({'1or2':'1 or 2'})
        categories.push('1 or 2');
    if '3or4' in df['steward']:
        df['steward'] = df['steward'].replace({'3or4':'3 or 4'})
        categories.push('3 or 4');
    if '4orMore' in df['steward']:
        df['steward'] = df['steward'].replace({'4orMore':'4 or More'})
        categories.push('4 or More');
    print df['steward']
    df['steward'] = df['steward'].astype('category')
    df['steward'] = df['steward'].cat.reorder_categories(categories, ordered=True)

    return df.to_json(orient='split')

@app.callback( #1
    Output('health_prop', 'figure'),
    [Input('value-holder', 'children')])
def update_graph1(cleaned_data):
    df = pd.read_json(cleaned_data, orient='split')

    df['health'] = df['health'].astype('category')
    df['health'] = df['health'].cat.reorder_categories(['Poor','Fair','Good'], ordered=True)

    tmp = df.groupby('health')['count_tree_id'].sum().reset_index()

    return{
    'data':[
        {'x':['Poor','Fair','Good'],
         'y':tmp['count_tree_id']/sum(tmp['count_tree_id']),
         'type':'bar'},
    ],
    'layout':{
        'title':'Health condition proportion'
    }
}

@app.callback( #2
    Output('steward', 'figure'),
    [Input('value-holder', 'children')])
def update_graph2(cleaned_data):
    df = pd.read_json(cleaned_data, orient='split')

    tmp = df.pivot(index='health', columns='steward', values='count_tree_id')
    columns = ['None', '1 or 2', '3 or 4', '4 or More']
    rows = ['Poor', 'Fair', 'Good']
    tmp = tmp.reindex_axis(columns, axis=1).reindex_axis(rows, axis=0)

    return{
        'data': [
            {'x': columns,
             'y': rows,
             'z': tmp.values.tolist(),
             'type':'heatmap'}
        ],
        'layout': {
            'title':'Stewardship impact on trees'
    }
}

if __name__ == '__main__':
    app.run_server(debug=True)
