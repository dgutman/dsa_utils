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


## So for a confusion Matrix, we need two rows to compare..
## These map to x and y
## x= currentLabel,  y=modelLabel  i.e. what the model is producing...
trueLabel = "currentStain"
predLabel = "modelLabel"


### Generate the confusion matrix based on the data frame that was just loaded..
lblSetToGraph = ["HE", "Tau", "Syn", "aBeta", "pTDP", "Biels"]
## Very frequently I have other stains in my initial data set I am not interetsted in running through the model or wnat to hide.. at least for now


# print(df)
# print(list(df.currentStain.values))
# print(df.modelLabel.values)
cm = metrics.confusion_matrix(list(df[trueLabel].values), list(df[predLabel].values), labels=lblSetToGraph)
cmfig = dbc.Col(
    dcc.Graph(figure=px.imshow(cm, x=lblSetToGraph, y=lblSetToGraph, text_auto=True), id="basicGraphInteractions"),
    width=3,
)

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

    for c in [trueLabel, predLabel]:
        # Make sure the column is in the current dataframe
        if c in dff:
            fig = px.histogram(dff, x=c)
            fig.update_xaxes(
                tickangle=45, automargin=False, tickfont=dict(family="Rockwell", color="crimson", size=10)
            )
            histSet.append(dbc.Col(dcc.Graph(figure=fig, id=c + "_hist"), width=6))
    ### To do perhaps make the width of this part iterable.. this width is a percentage of the base container

    return histSet


### Possibly clean this up, but it's cleaner this way..
currentStainHistogram = px.histogram(df, x=trueLabel, title="Current Image Label")
predictedStainHistogram = px.histogram(df, x=predLabel, title="Predicted Image Label")
dataSetDescriptors = [
    dbc.Col(dcc.Graph(figure=currentStainHistogram)),
    dbc.Col(dcc.Graph(figure=predictedStainHistogram)),
]


imgGridId = "image-grid"
img_grid_dataview = dvc.generate_dataview_components(componentId=imgGridId)


callbackArea = dbc.Row(
    [
        dbc.Col(
            html.Div(
                [
                    dcc.Markdown(
                        """
                **Hover Data**

                Mouse over values in the graph.
            """
                    ),
                    html.Pre(id="hover-data"),
                ]
            ),
            width=1,
        ),
        dbc.Col(img_grid_dataview, width=11),
    ]
)
app.layout = html.Div([table, html.Div(id="cmi", children=[]), callbackArea, html.Div(id="debugarea", children=[])])

style = {
    "border": f"1px solid {dmc.theme.DEFAULT_COLORS['indigo'][4]}",
    "textAlign": "center",
    "width": 160,
    "height": 160,
}


## TO DO... think about call back logic... need to reset the page to 1... and also set the max value..


@app.callback(
    Output("debugarea", "children"),
    Input("image-grid-pager", "active_page"),
)
def updatedebug(active_page):
    print(active_page)
    return ("Active page should be", active_page)


## For this call back, the active paeg should be 0..
@app.callback(
    [
        Output("hover-data", "children"),
        Output("image-grid", "children"),
        Output("image-grid-pager", "max_value"),
        Output("image-grid-pager", "style"),
    ],
    [Input("basicGraphInteractions", "hoverData")],
)
def display_hover_data(hoverData):
    ## Hover data returns the x/y of the grid... in my case this wuld be
    ## currentStain and modelLabel
    ## TO DO is make these axis into columns
    activePage = 0

    ## maxPage is the maximum number of pages that should be shown in the pager, which adjusts per data set
    maxPage = 0

    pagerCss = {}

    if hoverData:
        ## Verify I didn't invert this..
        modelLabel = hoverData["points"][0]["x"]
        currentStain = hoverData["points"][0]["y"]
        imageArray = []

        dataForGrid = df[(df["modelLabel"] == modelLabel) & (df["currentStain"] == currentStain)].to_dict("records")

        pageSize = 6

        if activePage:
            offSet = pageSize * activePage  ## Need to add pageSize
        else:
            offSet = 0

        # print(activePage)
        ## TO DO.. NEED TO ADD IN THE PAGER LOGIC
        curIdx = offSet
        imgCounter = 0

        maxPage = len(dataForGrid) // pageSize

        if not dataForGrid:
            pagerCss = {"visibility": "hidden"}

        while curIdx < len(dataForGrid) and imgCounter < pageSize:
            imgId = dataForGrid[curIdx]["_id"]
            imgName = dataForGrid[curIdx]["name"]
            thumbUrl = f"{dsaBaseUrl}/item/{imgId}/tiles/thumbnail"
            imageArray.append(dmc.Image(src=thumbUrl, width=160, style=style, caption=imgName))
            imgCounter += 1
            curIdx += 1

        return (json.dumps(hoverData, indent=2), imageArray, maxPage, pagerCss)

    else:
        return ("", [], maxPage, pagerCss)


if __name__ == "__main__":
    app.run_server(debug=True)
