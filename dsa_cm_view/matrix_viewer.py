from sklearn import metrics
import json
from dash import Dash, dcc, html, dash_table
from dash.dependencies import Input, Output, State
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
import numpy as np
from collections import OrderedDict
import confMatrix_graph as cmg
import plotly.figure_factory as ff
from graphCallBackLayout import callBackOutputs
import get_dataset as gds


# Config Parameters, may move to a yaml or config.json file
dbName = "sqliteDb/confMatrixDB.db"
dsaBaseUrl = "https://styx.neurology.emory.edu/girder/api/v1"

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
df = gds.getConfusionMatrixData(dbName)


# imgViewer = html.Div(json.dumps(selectedData))


table = html.Div([
    dash_table.DataTable(
        id='datatable-interactivity',
        columns=[
            {"name": i, "id": i, "deletable": False, "selectable": True} for i in df.columns
        ],
        data=df.to_dict('records'),
        editable=True,
        filter_action="native",
        sort_action="native",
        sort_mode="multi",
        column_selectable="single",
        row_selectable="multi",
        row_deletable=True,
        selected_columns=[],
        selected_rows=[],
        page_action="native",
        page_current=0,
        page_size=10,
    ),
    dbc.Row([
        dbc.Col(html.Div(id='cur-hover-image'), width=3),
        dbc.Col(dbc.Row(id='datatable-interactivity-container'), width=9)])
])


@app.callback(
    Output('cur-hover-image', 'children'),
    [Input('datatable-interactivity', 'active_cell')],
    # (A) pass table as data input to get current value from active cell "coordinates"
    [State('datatable-interactivity', 'data')]
)
def display_click_data(active_cell, table_data):
    if active_cell:
        cell = json.dumps(active_cell, indent=2)
        row = active_cell['row']
        col = active_cell['column_id']
        value = table_data[row][col]
        out = '%s\n%s' % (cell, value)
        imgId = table_data[row]['imageId']
        # Create an Image From this as well
        thumbUrl = f'{dsaBaseUrl}/item/{imgId}/tiles/thumbnail'

    else:
        out = 'no cell selected'
    return [json.dumps(out, indent=2), html.Img(src=thumbUrl)]


# @app.callback(
#     Output('cur-hover-image', 'children'),
#     [Input('datatable-interactivity', 'active_cell')],

#     # Input('datatable-interactivity', 'selected_row_ids'),
#     [State('datatable-interactivity', 'data')]
# )
# def update_img_dataview(active_cell, table_data):
#     print(active_cell)
#     return json.dumps(active_cell)


@app.callback(
    Output('datatable-interactivity-container', "children"),
    Input('datatable-interactivity', "derived_virtual_data"),
    Input('datatable-interactivity', "derived_virtual_selected_rows"))
def update_graphs(rows, derived_virtual_selected_rows):
    # When the table is first rendered, `derived_virtual_data` and
    # `derived_virtual_selected_rows` will be `None`. This is due to an
    # idiosyncrasy in Dash (unsupplied properties are always None and Dash
    # calls the dependent callbacks when the component is first rendered).
    # So, if `rows` is `None`, then the component was just rendered
    # and its value will be the same as the component's dataframe.
    # Instead of setting `None` in here, you could also set
    # `derived_virtual_data=df.to_rows('dict')` when you initialize
    # the component.
    if derived_virtual_selected_rows is None:
        derived_virtual_selected_rows = []

    dff = df if rows is None else pd.DataFrame(rows)

    colors = ['#7FDBFF' if i in derived_virtual_selected_rows else '#0074D9'
              for i in range(len(dff))]

    histSet = []

    # Add in the image viewer window here

    for c in ["currentStain", "modelLabel"]:
        # Make sure the column is in the current dataframe
        if c in dff:
            fig = px.histogram(dff, x=c)
            fig.update_xaxes(tickangle=45, automargin=False, tickfont=dict(
                family='Rockwell', color='crimson', size=10))

            histSet.append(
                dbc.Col(dcc.Graph(figure=fig, id=c+'_hist'), width=3)
            )

    return histSet


# Now creating an image viewer

    # return [
    #     dbc.Col(dcc.Graph(
    #         id=column,
    #         figure=px.histogram(dff, x=column)

    #     ), width=3)
    #     # check if column exists - user may have deleted it
    #     # If `column.deletable=False`, then you don't
    #     # need to do this check.
    #     for column in ["currentStain", "modelLabel"] if column in dff
    # ]


# table = dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True)


# with open("imageSetForCm.json", "r") as fp:
#     imageSet = json.load(fp)

# image_df = pd.DataFrame(imageSet)
# with open("predictionSample.json", "r") as fp:
#     predictionSample = json.load(fp)
# Statistics regarding the main ADRC data set including current and predicted Stains.. this will evolve over time
pd_df = df
# pd.DataFrame(predictionSample)

currentStainHistogram = px.histogram(pd_df, x='currentStain')
predictedStainHistogram = px.histogram(pd_df, x='modelResponse')
dataSetDescriptors = [
    dbc.Col(dcc.Graph(figure=currentStainHistogram), width=3),
    dbc.Col(dcc.Graph(figure=predictedStainHistogram), width=3)
]
# figure={
#     "data": [
#         {
#             "x": dff["country"],
#             "y": dff[column],
#             "type": "bar",
#             "marker": {"color": colors},
#         }
#     ],
#     "layout": {
#         "xaxis": {"automargin": True},
#         "yaxis": {
#             "automargin": True,
#             "title": {"text": column}
#         },
#         "height": 250,
#         "margin": {"t": 10, "l": 10, "r": 10},
#     },
# },
# with open("predictionSample.json", "r") as fp:
#     preds = json.load(fp)

# df_pred = pd.DataFrame(preds)

# lblSet = ['HE', 'Tau', 'Syn', 'aBeta', 'pTDP', 'Biels']
# df1 = df_pred[df_pred['currentStain'].map(
#     df_pred['currentStain'].value_counts()) > 100]

# df1.replace({"Abeta": "aBeta", "Ptdp": "pTDP", "He": "HE"}, inplace=True)
# df1.drop(columns=['allPredictions'])
# cm = metrics.confusion_matrix(list(df1.currentStain.values), list(
#     df1.predictedStain.values), labels=df1.currentStain.unique())

# # cmfig = metrics.ConfusionMatrixDisplay(cm,display_labels=lblSet)
# print(df1.currentStain.unique())
# print(df1.predictedStain.unique())

# print(df_pred)

# df = pd.read_json("predictionSample.json")
# df = df.drop(columns='allPredictions')

# dsaItemTable = dash_table.DataTable(
#     data=df.to_dict('records'),
#     columns=[{'id': c, 'name': c} for c in df.columns],
#     page_size=10)

# z = cm
# x = lblSet
# y = lblSet
# print(cm)
# cmfig = ff.create_annotated_heatmap(cm, x=x, y=y, colorscale='Viridis')

# dmcStuff = dmc.SimpleGrid(
#     cols=8,
#     spacing="lg",
#     id="image-grid",
#     breakpoints=[
#         {"maxWidth": 980, "cols": 3, "spacing": "md"},
#         {"maxWidth": 755, "cols": 2, "spacing": "sm"},
#         {"maxWidth": 600, "cols": 1, "spacing": "sm"},
#     ],
#     children=[
#         # This is where the images get dumped
#         html.Div(" ", style=style),
#     ],
# )

# mancordion = dmc.AccordionMultiple(
#     children=[
#         dmc.AccordionItem(
#             [
#                 dmc.AccordionControl("DSA Item DataTable"),
#                 dmc.AccordionPanel(
#                     dsaItemTable
#                 ),
#             ],
#             value="DSA Datatable",
#         ),
#         dmc.AccordionItem(
#             [
#                 dmc.AccordionControl("Confusion Matrix"),
#                 dmc.AccordionPanel(
#                     dbc.Row(
#                         [dbc.Col(dcc.Graph(figure=cmfig, id='confusionMatrix-interactions'), width=5),
#                          dbc.Col(
#                          html.Div(id='matrixSelectionInfo',  children=[]), width=3)
#                          ])
#                 ),
#             ],
#             value="Confusion Matrix",
#         ),     dmc.AccordionItem(
#             [
#                 dmc.AccordionControl("callBacks"),
#                 dmc.AccordionPanel(callBackOutputs)
#             ],
#             value="callBacks",
#         ),
#         dmc.AccordionItem(
#             [
#                 dmc.AccordionControl("imageGrid"),
#                 dmc.AccordionPanel(
#                 ),
#             ],
#             value="image View",
#         ),
#     ],
# )


app.layout = html.Div([
    table
    # dmc.AccordionPanel(
    #     dbc.Row(
    #         [dbc.Col(dcc.Graph(figure=cmfig, id='confusionMatrix-interactions'), width=5),
    #             dbc.Col(
    #             html.Div(id='matrixSelectionInfo',  children=[]), width=3)
    #          ])
    # ),
    # mancordion,
    # dmcStuff
])


# def getSelectedItemSet(confMatrix_df, xCol, yCol):
#     """This expects the pandas dataframe which should be the data fed into the confusion matrix generation
#     and I want to filter this dataframe and return the rows that match the selected row/column / x/y grid
#     So for example, I may want to find the rows where x/true = aBeta and y/predicted=pTDP

#     xCol = current Stain,  y=predictedStain
#     """


# @ app.callback(

#     Output("image-grid", 'children'),
#     Output("matrixSelectionInfo", "children"),
#     Input('confusionMatrix-interactions', 'hoverData'))
# def display_selected_data(selectedData):
#     print(selectedData)
#     if selectedData:
#         ix = int(selectedData['points'][0]['z'])
#         imageArray = []

#         for i in range(1, 9):
#             imgId = imageSet[ix+i]['_id']
#             thumbUrl = f'{dsaBaseUrl}/item/{imgId}/tiles/thumbnail'
#             imageArray.append(html.Img(src=thumbUrl, style=style))
#         # imgId = imageSet[ix]['_id']
#         # thumbUrl = f'{dsaBaseUrl}/item/{imgId}/tiles/thumbnail'
#         # print(thumbUrl)
#         return (imageArray, html.Div(json.dumps(selectedData)))
#     # Dash ism... have to return two null arrays or callback fxn gets confused on the first run
#     return ([], [])


if __name__ == '__main__':
    app.run_server(debug=True)

# @app.callback(
#     Output('hover-data', 'children'),
#     Input('confusionMatrix-interactions', 'hoverData'))
# def display_hover_data(hoverData):
#     return json.dumps(hoverData, indent=2)


# # using the z property from the current confusoin matrix, this will need to change
# Markdown supports images with this syntax: ![alt](src) where alt refers to the image's alt text and src is the path to the image (the src property).
