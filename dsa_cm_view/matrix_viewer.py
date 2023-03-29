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
import dsaDataTable as dtt
import dataViewComponent as dvc



# Config Parameters, may move to a yaml or config.json file
dbName = "sqliteDb/confMatrixDB.db"
dsaBaseUrl = "https://styx.neurology.emory.edu/girder/api/v1"


external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css", dbc.themes.BOOTSTRAP]

app = Dash(__name__, external_stylesheets=external_stylesheets)

####################### LOAD ADRC Data Table ##############################
df = gds.getConfusionMatrixData(dbName)

## I need to make sure that none of the values I feed into the confusion matrix are None or this fails

df.currentStain.fillna("Unk", inplace=True)
df.replace({"Abeta": "aBeta", "Ptdp": "pTDP", "He": "HE"}, inplace=True)


### Generate the confusion matrix based on the data frame that was just loaded..
lblSet = ["HE", "Tau", "Syn", "aBeta", "pTDP", "Biels"]
# print(df)
# print(list(df.currentStain.values))
# print(df.modelLabel.values)
cm = metrics.confusion_matrix(list(df.currentStain.values), list(df.modelLabel.values), labels=lblSet)
cmfig = dbc.Col(dcc.Graph(figure=px.imshow(cm, x=lblSet, y=lblSet),id='basicGraphInteractions'), width=3)

# , colorscale="Viridis"
table = dtt.gen_DSA_DataTable(
    df, columns_to_ignore=["modelResponse", "baseParentId", "description"], addlColSet=[cmfig]
)


@app.callback(
    Output("cur-hover-image", "children"),
    [Input("datatable-interactivity", "active_cell")],
    # (A) pass table as data input to get current value from active cell "coordinates"
    [State("datatable-interactivity", "data")],
)
def display_click_data(active_cell, table_data):
    thumbUrl = ""

    if active_cell:
        cell = json.dumps(active_cell, indent=2)
        row = active_cell["row"]
        col = active_cell["column_id"]
        value = table_data[row][col]
        out = "%s\n%s" % (cell, value)
        imgId = table_data[row]["imageId"]
        # Create an Image From this as well
        thumbUrl = f"{dsaBaseUrl}/item/{imgId}/tiles/thumbnail"
    else:
        out = "no cell selected"
    return [json.dumps(active_cell, indent=2), html.Img(src=thumbUrl)]


@app.callback(
    Output("datatable-interactivity-container", "children"),
    Input("datatable-interactivity", "derived_virtual_data"),
    Input("datatable-interactivity", "derived_virtual_selected_rows"),
)
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

    colors = ["#7FDBFF" if i in derived_virtual_selected_rows else "#0074D9" for i in range(len(dff))]
    histSet = []
    # Add in the image viewer window here

    for c in ["currentStain", "modelLabel"]:
        # Make sure the column is in the current dataframe
        if c in dff:
            fig = px.histogram(dff, x=c)
            fig.update_xaxes(
                tickangle=45, automargin=False, tickfont=dict(family="Rockwell", color="crimson", size=10)
            )
            histSet.append(dbc.Col(dcc.Graph(figure=fig, id=c + "_hist"),width=6))
    ### To do perhaps make the width of this part iterable.. this width is a percentage of the base container

    return histSet


currentStainHistogram = px.histogram(df, x="currentStain")
predictedStainHistogram = px.histogram(df, x="modelResponse")
dataSetDescriptors = [
    dbc.Col(dcc.Graph(figure=currentStainHistogram)),
    dbc.Col(dcc.Graph(figure=predictedStainHistogram)),
]


imgGridId='image-grid'
img_grid_dataview = dvc.generate_dataview_components(componentId=imgGridId)


callbackArea = dbc.Row(
    
    [
        dbc.Col(html.Div([
            dcc.Markdown("""
                **Hover Data**

                Mouse over values in the graph.
            """),
            html.Pre(id='hover-data'),
        ]),width=1),
    dbc.Col(   
            img_grid_dataview
            
        ,width=10 ),
      
    ])
# style=styles['pre']


app.layout = html.Div(
    [
             table,
             html.Div(id='cmi',  children=[]),
             callbackArea
    ]
)

style = {
    "border": f"1px solid {dmc.theme.DEFAULT_COLORS['indigo'][4]}",
    "textAlign": "center",
    "width": 200,
    "height": 200
}



@app.callback(
    [Output('hover-data', 'children'),
      Output("image-grid", 'children')],
    [Input('basicGraphInteractions', 'hoverData'),
    Input('image-grid-pager','active_page')])
def display_hover_data(hoverData,activePage):
    ## Hover data returns the x/y of the grid... in my case this wuld be
    ## currentStain and modelLabel
    ## TO DO is make these axis into columns

    ## Verify I didn't invert this..
    modelLabel = hoverData['points'][0]['x']
    currentStain = hoverData['points'][0]['y']
    print(modelLabel,currentStain)
    imageArray= []
    
    dataForGrid = df[(df['modelLabel']==modelLabel)].to_dict("records")


    if activePage:
        offSet = 10*activePage  ## Need to add pageSize
    else:
        offSet = 0

    print(activePage)
    ## TO DO.. NEED TO ADD IN THE PAGER LOGIC

    for i in range(1,10):
        imgId = dataForGrid[i+offSet]['_id']
        imgName = dataForGrid[i+offSet]['name']
        thumbUrl = f'{dsaBaseUrl}/item/{imgId}/tiles/thumbnail'
        imageArray.append(dmc.Image(src=thumbUrl,style=style,caption=imgName))


    return (json.dumps(hoverData, indent=2),imageArray)


# , style=style

# @ app.callback(
#     Output("image-grid", 'children'),
#     Output("matrixSelectionInfo", "children"),
#     Input('basicGraphInteractions', 'hoverData'))
# def display_selected_data(selectedData):
#     print(selectedData)
#     if selectedData:
#         ix = int(selectedData['points'][0]['z'])
#         imageArray = []

#         # for i in range(1, 9):
#         #     
#         # imgId = imageSet[ix]['_id']
#         # thumbUrl = f'{dsaBaseUrl}/item/{imgId}/tiles/thumbnail'
#         # print(thumbUrl)
#         return (imageArray, html.Div(json.dumps(selectedData)))
#     # Dash ism... have to return two null arrays or callback fxn gets confused on the first run
#     return ([], [])







# @app.callback(
#     Output('click-data', 'children'),
#     Input('basic-interactions', 'clickData'))
# def display_click_data(clickData):
#     return json.dumps(clickData, indent=2)


# @app.callback(
#     Output('selected-data', 'children'),
#     Input('basic-interactions', 'selectedData'))
# def display_selected_data(selectedData):
#     return json.dumps(selectedData, indent=2)


# @app.callback(
#     Output('relayout-data', 'children'),
#     Input('basic-interactions', 'relayoutData'))
# def display_relayout_data(relayoutData):
#     return json.dumps(relayoutData, indent=2)


if __name__ == "__main__":
    app.run_server(debug=True)



#   html.Div([
#             dcc.Markdown("""
#                 **Click Data**

#                 Click on points in the graph.
#             """),
#             html.Pre(id='click-data'), #style=styles['pre']
#         ], className='three columns'),

#         html.Div([
#             dcc.Markdown("""
#                 **Selection Data**

#                 Choose the lasso or rectangle tool in the graph's menu
#                 bar and then select points in the graph.

#                 Note that if `layout.clickmode = 'event+select'`, selection data also
#                 accumulates (or un-accumulates) selected data if you hold down the shift
#                 button while clicking.
#             """),
#             html.Pre(id='selected-data', ),#style=styles['pre']
#         ], className='three columns'),

#         html.Div([
#             dcc.Markdown("""
#                 **Zoom and Relayout Data**

#                 Click and drag on the graph to zoom or click on the zoom
#                 buttons in the graph's menu bar.
#                 Clicking on legend items will also fire
#                 this event.
#             """),
#             html.Pre(id='relayout-data', ),
#         ], className='three columns')

# @app.callback(
#     Output('hover-data', 'children'),
#     Input('confusionMatrix-interactions', 'hoverData'))
# def display_hover_data(hoverData):
#     return json.dumps(hoverData, indent=2)

   # dmc.AccordionPanel(
        #     dbc.Row(
        #         [dbc.Col(dcc.Graph(figure=cmfig, id='confusionMatrix-interactions'), width=5),
        #             dbc.Col(
        #             html.Div(id='matrixSelectionInfo',  children=[]), width=3)
        #          ])
        # ),
        # mancordion,
        # dmcStuff
# # using the z property from the current confusoin matrix, this will need to change
# Markdown supports images with this syntax: ![alt](src) where alt refers to the image's alt text and src is the path to the image (the src property).
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
# TO REFACTOR
# styles = {
#     'pre': {
#         'border': 'thin lightgrey solid',
#         'overflowX': 'scroll'
#     }
# }

# style = {
#     "border": f"1px solid {dmc.theme.DEFAULT_COLORS['indigo'][4]}",
#     "textAlign": "center",
#     "width": 200,
#     "height": 200
# }

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



# @app.callback(
#     Output('cur-hover-image', 'children'),
#     [Input('datatable-interactivity', 'active_cell')],

#     # Input('datatable-interactivity', 'selected_row_ids'),
#     [State('datatable-interactivity', 'data')]
# )
# def update_img_dataview(active_cell, table_data):
#     print(active_cell)
#     return json.dumps(active_cell)


# Now creating an image viewer



# table = dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True)


# with open("imageSetForCm.json", "r") as fp:
#     imageSet = json.load(fp)

# image_df = pd.DataFrame(imageSet)
# with open("predictionSample.json", "r") as fp:
#     predictionSample = json.load(fp)
# Statistics regarding the main ADRC data set including current and predicted Stains.. this will evolve over time
