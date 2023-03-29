import json

from dash import Dash, dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
import numpy as np

def confusion_matrix(labelsTrue, labelsOutput, classCount):
    combined = np.asarray([labelsTrue, labelsOutput]).T
    uniqueVals, uniqueCounts = np.unique(combined, return_counts=True, axis=0)
    
    confusionMatrix = np.zeros((classCount, classCount))
    allUnique = np.sort(np.unique(combined.astype(int)))
    
    mapped = {uniqueVal: val for uniqueVal, val in zip(allUnique.tolist(), range(allUnique.size))}
    
    for (val, count) in zip(uniqueVals, uniqueCounts):
        confusionMatrix[mapped[int(val[0])], mapped[int(val[1])]] += count
        
    return confusionMatrix

style = {
    "border": f"1px solid {dmc.theme.DEFAULT_COLORS['indigo'][4]}",
    "textAlign": "center",
    "width": 160
}

dmcStuff = dmc.SimpleGrid(
    cols=4,
    spacing="sm",
    id="image-grid",
    breakpoints=[
        {"maxWidth": 980, "cols": 3, "spacing": "md"},
        {"maxWidth": 755, "cols": 2, "spacing": "sm"},
        {"maxWidth": 600, "cols": 1, "spacing": "sm"},
    ],
    children=[
        html.Div("", style=style), ### This is where the images get dumped
    ],
)


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css',dbc.themes.BOOTSTRAP]

app = Dash(__name__, external_stylesheets=external_stylesheets)

styles = {
    'pre': {
        'border': 'thin lightgrey solid',
        'overflowX': 'scroll'
    }
}


dsaBaseUrl = "https://styx.neurology.emory.edu/girder/api/v1"


with open("imageSetForCm.json","r") as fp:
    imageSet = json.load(fp)

image_df = pd.DataFrame(imageSet)


data=[[1, 25, 30, 50, 1], [20, 1, 60, 80, 30], [30, 60, 1, 5, 20]]
hmap = px.imshow(data,
                labels=dict(x="Day of Week", y="Time of Day", color="Productivity"),
                x=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'],
                y=['Morning', 'Afternoon', 'Evening']
               )
hmap.update_xaxes(side="top")

df = pd.DataFrame({
    "x": [1,2,1,2],
    "y": [1,2,3,4],
    "customdata": [1,2,3,4],
    "fruit": ["apple", "apple", "orange", "orange"]
})

fig = px.scatter(df, x="x", y="y", color="fruit", custom_data=["customdata"])

fig.update_layout(clickmode='event+select')

fig.update_traces(marker_size=20)

app.layout = html.Div([
    dcc.Graph(
        id='confusionMatrix-interactive',
        figure=hmap
    ),
    dmcStuff,

       html.Pre(id='hmap-selected-data', style=styles['pre']),
  
])



## using the z property from the current confusoin matrix, this will need to change

@app.callback(
    [Output('hmap-selected-data', 'children'),
     Output("image-grid",'children')],
    Input('confusionMatrix-interactive', 'hoverData'))
def display_selected_data(selectedData):
    print(selectedData)
    ix = int(selectedData['points'][0]['z'])


    imageArray =    []
    
    for i in range(1,10):
        imgId = imageSet[ix+i]['_id']
        thumbUrl = f'{dsaBaseUrl}/item/{imgId}/tiles/thumbnail'
        imageArray.append(html.Img(src=thumbUrl,style=style))
                                  

    imgId = imageSet[ix]['_id']
    thumbUrl = f'{dsaBaseUrl}/item/{imgId}/tiles/thumbnail'
    print(thumbUrl)
    return (json.dumps(selectedData, indent=2), imageArray)


if __name__ == '__main__':
    app.run_server(debug=True)

# @app.callback(
#     Output('relayout-data', 'children'),
#     Input('basic-interactions', 'relayoutData'))
# def display_relayout_data(relayoutData):
#     return json.dumps(relayoutData, indent=2)


# @app.callback(
#     Output('selected-data', 'children'),
#     Input('basic-interactions', 'selectedData'))
# def display_selected_data(selectedData):
#     return json.dumps(selectedData, indent=2)

# @app.callback(
#     Output('hover-data', 'children'),
#     Input('basic-interactions', 'hoverData'))
# def display_hover_data(hoverData):
#     return json.dumps(hoverData, indent=2)


# @app.callback(
#     Output('click-data', 'children'),
#     Input('basic-interactions', 'clickData'))
# def display_click_data(clickData):
#     return json.dumps(clickData, indent=2)
  # dcc.Graph(
    #     id='basic-interactions',
    #     figure=fig
    # ),

    # html.Div(className='row', children=[
    #     html.Div([
    #         dcc.Markdown("""
    #             **Hover Data**

    #             Mouse over values in the graph.
    #         """),
    #         html.Pre(id='hover-data', style=styles['pre'])
    #     ], className='three columns'),

    #     html.Div([
    #         dcc.Markdown("""
    #             **Click Data**

    #             Click on points in the graph.
    #         """),
    #         html.Pre(id='click-data', style=styles['pre']),
    #     ], className='three columns'),

    #     html.Div([
    #         dcc.Markdown("""
    #             **Selection Data**

    #             Choose the lasso or rectangle tool in the graph's menu
    #             bar and then select points in the graph.

    #             Note that if `layout.clickmode = 'event+select'`, selection data also
    #             accumulates (or un-accumulates) selected data if you hold down the shift
    #             button while clicking.
    #         """),
    #         html.Pre(id='selected-data', style=styles['pre']),
    #     ], className='three columns'),

    #     html.Div([
    #         dcc.Markdown("""
    #             **Zoom and Relayout Data**

    #             Click and drag on the graph to zoom or click on the zoom
    #             buttons in the graph's menu bar.
    #             Clicking on legend items will also fire
    #             this event.
    #         """),
    #         html.Pre(id='relayout-data', style=styles['pre']),
    #     ], className='three columns')
    # ])