from sklearn import metrics
import json
from dash import Dash, dcc, html, dash_table
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
import numpy as np
from collections import OrderedDict
import confMatrix_graph as cmg
import plotly.figure_factory as ff
from graphCallBackLayout import callBackOutputs

# TO REFACTOR
styles = {
    'pre': {
        'border': 'thin lightgrey solid',
        'overflowX': 'scroll'
    }
}

style = {
    "border": f"1px solid {dmc.theme.DEFAULT_COLORS['indigo'][4]}",
    "textAlign": "center",
    "width": 200,
    "height": 200
}

external_stylesheets = [
    'https://codepen.io/chriddyp/pen/bWLwgP.css', dbc.themes.BOOTSTRAP]

app = Dash(__name__, external_stylesheets=external_stylesheets)

####################### LOAD ADRC Data Table ##############################
df = pd.read_csv("./adrcThumbMetadata.csv")

dsaBaseUrl = "https://styx.neurology.emory.edu/girder/api/v1"

with open("imageSetForCm.json", "r") as fp:
    imageSet = json.load(fp)

image_df = pd.DataFrame(imageSet)

with open("predictionSample.json", "r") as fp:
    predictionSample = json.load(fp)

# Statistics regarding the main ADRC data set including current and predicted Stains.. this will evolve over time
pd_df = pd.DataFrame(predictionSample)

currentStainHistogram = px.histogram(pd_df, x='currentStain')
predictedStainHistogram = px.histogram(pd_df, x='predictedStain')
dataSetDescriptors = dbc.Row([
    dbc.Col(dcc.Graph(figure=currentStainHistogram), width=3),
    dbc.Col(dcc.Graph(figure=predictedStainHistogram), width=3)
])

with open("predictionSample.json", "r") as fp:
    preds = json.load(fp)

df_pred = pd.DataFrame(preds)

lblSet = ['HE', 'Tau', 'Syn', 'aBeta', 'pTDP', 'Biels']
df1 = df_pred[df_pred['currentStain'].map(
    df_pred['currentStain'].value_counts()) > 100]

df1.replace({"Abeta": "aBeta", "Ptdp": "pTDP", "He": "HE"}, inplace=True)
df1.drop(columns=['allPredictions'])
cm = metrics.confusion_matrix(list(df1.currentStain.values), list(
    df1.predictedStain.values), labels=df1.currentStain.unique())

# cmfig = metrics.ConfusionMatrixDisplay(cm,display_labels=lblSet)
print(df1.currentStain.unique())
print(df1.predictedStain.unique())

print(df_pred)

df = pd.read_json("predictionSample.json")
df = df.drop(columns='allPredictions')


dsaItemTable = dash_table.DataTable(
    data=df.to_dict('records'),
    columns=[{'id': c, 'name': c} for c in df.columns],
    page_size=10)

z = cm
x = lblSet
y = lblSet
print(cm)
cmfig = ff.create_annotated_heatmap(cm, x=x, y=y, colorscale='Viridis')

dmcStuff = dmc.SimpleGrid(
    cols=8,
    spacing="lg",
    id="image-grid",
    breakpoints=[
        {"maxWidth": 980, "cols": 3, "spacing": "md"},
        {"maxWidth": 755, "cols": 2, "spacing": "sm"},
        {"maxWidth": 600, "cols": 1, "spacing": "sm"},
    ],
    children=[
        # This is where the images get dumped
        html.Div(" ", style=style),
    ],
)

mancordion = dmc.AccordionMultiple(
    children=[
        dmc.AccordionItem(
            [
                dmc.AccordionControl("DSA Item DataTable"),
                dmc.AccordionPanel(
                    dsaItemTable
                ),
            ],
            value="DSA Datatable",
        ),
        dmc.AccordionItem(
            [
                dmc.AccordionControl("Confusion Matrix"),
                dmc.AccordionPanel(
                    dbc.Row(
                        [dbc.Col(dcc.Graph(figure=cmfig, id='confusionMatrix-interactions'), width=5),
                         dbc.Col(
                         html.Div(id='matrixSelectionInfo',  children=[]), width=3)
                         ])
                ),
            ],
            value="Confusion Matrix",
        ),     dmc.AccordionItem(
            [
                dmc.AccordionControl("callBacks"),
                dmc.AccordionPanel(callBackOutputs)
            ],
            value="callBacks",
        ),
        dmc.AccordionItem(
            [
                dmc.AccordionControl("imageGrid"),
                dmc.AccordionPanel(
                ),
            ],
            value="image View",
        ),
    ],
)

app.layout = html.Div([
    mancordion,
    dmcStuff
])


@ app.callback(

    Output("image-grid", 'children'),
    Output("matrixSelectionInfo", "children"),
    Input('confusionMatrix-interactions', 'hoverData'))
def display_selected_data(selectedData):
    print(selectedData)
    if selectedData:
        ix = int(selectedData['points'][0]['z'])
        imageArray = []

        for i in range(1, 9):
            imgId = imageSet[ix+i]['_id']
            thumbUrl = f'{dsaBaseUrl}/item/{imgId}/tiles/thumbnail'
            imageArray.append(html.Img(src=thumbUrl, style=style))
        # imgId = imageSet[ix]['_id']
        # thumbUrl = f'{dsaBaseUrl}/item/{imgId}/tiles/thumbnail'
        # print(thumbUrl)
        return (imageArray, html.Div(json.dumps(selectedData)))
    # Dash ism... have to return two null arrays or callback fxn gets confused on the first run
    return ([], [])


if __name__ == '__main__':
    app.run_server(debug=True)

# @app.callback(
#     Output('hover-data', 'children'),
#     Input('confusionMatrix-interactions', 'hoverData'))
# def display_hover_data(hoverData):
#     return json.dumps(hoverData, indent=2)


# # using the z property from the current confusoin matrix, this will need to change
