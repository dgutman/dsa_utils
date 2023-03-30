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
