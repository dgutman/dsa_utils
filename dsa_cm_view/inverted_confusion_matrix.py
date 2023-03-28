import plotly.figure_factory as ff

z = [[0.1, 0.3, 0.5, 0.2],
     [1.0, 0.8, 0.6, 0.1],
     [0.1, 0.3, 0.6, 0.9],
     [0.6, 0.4, 0.2, 0.2]]

# invert z idx values
z = z[::-1]

x = ['healthy', 'multiple diseases', 'rust', 'scab']
y = x[::-1].copy()  # invert idx values of x

# change each element of z to type string for annotations
z_text = [[str(y) for y in x] for x in z]

# set up figure
fig = ff.create_annotated_heatmap(
    z, x=x, y=y, annotation_text=z_text, colorscale='Viridis')

# add title
fig.update_layout(title_text='<i><b>Confusion matrix</b></i>',
                  # xaxis = dict(title='x'),
                  # yaxis = dict(title='x')
                  )

# add custom xaxis title
fig.add_annotation(dict(font=dict(color="black", size=14),
                        x=0.5,
                        y=-0.15,
                        showarrow=False,
                        text="Predicted value",
                        xref="paper",
                        yref="paper"))

# add custom yaxis title
fig.add_annotation(dict(font=dict(color="black", size=14),
                        x=-0.35,
                        y=0.5,
                        showarrow=False,
                        text="Real value",
                        textangle=-90,
                        xref="paper",
                        yref="paper"))

# adjust margins to make room for yaxis title
fig.update_layout(margin=dict(t=50, l=200))f
