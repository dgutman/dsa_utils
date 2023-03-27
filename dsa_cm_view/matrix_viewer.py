import json
from dash import Dash, dcc, html, dash_table
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
import numpy as np
from collections import OrderedDict
import plotly.figure_factory as ff
import confMatrix_graph as cmg



## TO REFACTOR
styles = {
    'pre': {
        'border': 'thin lightgrey solid',
        'overflowX': 'scroll'
    }
}

style = {
    "border": f"1px solid {dmc.theme.DEFAULT_COLORS['indigo'][4]}",
    "textAlign": "center",
    "width": 320
}


external_stylesheets = [
    'https://codepen.io/chriddyp/pen/bWLwgP.css', dbc.themes.BOOTSTRAP]
app = Dash(__name__, external_stylesheets=external_stylesheets)

####################### LOAD ADRC Data Table ##############################
df = pd.read_csv("./adrcThumbMetadata.csv")

dsaItemTable = dash_table.DataTable(
    data=df.to_dict('records'),
    columns=[{'id': c, 'name': c} for c in df.columns],
    page_size=10)

dsaBaseUrl = "https://styx.neurology.emory.edu/girder/api/v1"

with open("imageSetForCm.json", "r") as fp:
    imageSet = json.load(fp)

image_df = pd.DataFrame(imageSet)


data = [[1, 25, 30, 50, 1], [20, 1, 60, 80, 30], [30, 60, 1, 5, 20]]
hmap = px.imshow(data,
                 labels=dict(x="Day of Week", y="Time of Day",
                             color="Productivity"),
                 x=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'],
                 y=['Morning', 'Afternoon', 'Evening']
                 )
hmap.update_xaxes(side="top")

df = pd.DataFrame({
    "x": [1, 2, 1, 2],
    "y": [1, 2, 3, 4],
    "customdata": [1, 2, 3, 4],
    "fruit": ["apple", "apple", "orange", "orange"]
})

figf = px.scatter(df, x="x", y="y", color="fruit", custom_data=["customdata"])

figf.update_layout(clickmode='event+select')

figf.update_traces(marker_size=20)

dfm = px.data.medals_wide(indexed=True)
# fig = px.imshow(dfm)

dmcStuff = dmc.SimpleGrid(
    cols=4,
    spacing="lg",
    id="image-grid",
    breakpoints=[
        {"maxWidth": 980, "cols": 3, "spacing": "md"},
        {"maxWidth": 755, "cols": 2, "spacing": "sm"},
        {"maxWidth": 600, "cols": 1, "spacing": "sm"},
    ],
    children=[
        html.Div("", style=style),  # This is where the images get dumped
    ],
)

with open("predictionSample.json","r") as fp:
    predictionSample = json.load(fp)





iframeExample = 'https://computablebrain.emory.edu/histomics#?image=638147637f8a5e686a52dded&bounds=24400%2C51228%2C34733%2C56376%2C0'




### Statistics regarding the main ADRC data set including current and predicted Stains.. this will evolve over time
pd_df = pd.DataFrame(predictionSample)

currentStainHistogram = px.histogram(pd_df,x='currentStain')
predictedStainHistogram = px.histogram(pd_df,x='predictedStain')
dataSetDescriptors = dbc.Row([
    dbc.Col(dcc.Graph(figure=currentStainHistogram),width=3),
    dbc.Col(dcc.Graph(figure=predictedStainHistogram),width=3)
])

#    html.Iframe(src=iframeExample,
#                 style={"height": "600px", "width": "100%"}),
origIexample = "https://www.ons.gov.uk/visualisations/dvc914/map/index.html"

accordion = html.Div(
    dbc.Accordion(
        [
           
            
            dbc.AccordionItem(
    
               dataSetDescriptors,
                title="DSA Item Stats"            ),
            dbc.AccordionItem(
                [
                       dsaItemTable
                ],
                title="DSA Item Table",
            ),
            dbc.AccordionItem(
              [ dcc.Graph(figure=px.imshow(dfm))],
                title="Graph Set 3",
            ),
        ]        
    )
)

app.layout = html.Div([
    accordion,
    dcc.Graph(
        id='confusionMatrix-interactive',
        figure=hmap
    ),
    dmcStuff,
    html.Pre(id='hmap-selected-data', style=styles['pre']),
])

# using the z property from the current confusoin matrix, this will need to change



@app.callback(
    [Output('hmap-selected-data', 'children'),
     Output("image-grid", 'children')],
    Input('confusionMatrix-interactive', 'hoverData'))
def display_selected_data(selectedData):
    print(selectedData)
    ix = int(selectedData['points'][0]['z'])

    imageArray = []

    for i in range(1, 10):
        imgId = imageSet[ix+i]['_id']
        thumbUrl = f'{dsaBaseUrl}/item/{imgId}/tiles/thumbnail'
        imageArray.append(html.Img(src=thumbUrl, style=style))

    imgId = imageSet[ix]['_id']
    thumbUrl = f'{dsaBaseUrl}/item/{imgId}/tiles/thumbnail'
    print(thumbUrl)
    return (json.dumps(selectedData, indent=2), imageArray)


if __name__ == '__main__':
    app.run_server(debug=True)
