import sys

try:
    # somewhat gracefully load the local build
    import plotly
except ImportError:
    sys.path.append('/mnt/usmp-data3/scratch/Labs/Kristofor/python/plotly')
    import plotly

from plotly.tools import FigureFactory as FF
from plotly.graph_objs import *
from plotly.offline import download_plotlyjs, plot


def _plot_accuracy_vs_readlength(dsets_kpis):
    """
    Generate plotly subplot structure of accuracy vs readlength for each condition.
    Return plot structure.
    """

    traces = []; titles = []; max_rl = 0
    for key in dsets_kpis.keys():
        rl = dsets_kpis[key]['readlength']
        acc = dsets_kpis[key]['accuracy']
        if max(rl) > max_rl:
            max_rl = max(rl)
        trace = Scatter(
                x = rl,
                y = acc,
                mode='markers'
        )
        traces.append( trace )
        titles.append( str(key) )
    rows = len( traces )
    fig = plotly.tools.make_subplots(rows=rows, cols=1,
                                     subplot_titles=tuple(titles))
    fig['layout']['font']['size'] = 16
    fig['layout'].update(showlegend=False)
    for row,trace in enumerate(traces):
        fig.append_trace(trace, row+1, 1) # convert from zero-based to one-based indexing
        fig['layout']['xaxis'+str(row+1)]['tickfont'].update(size=24)
        fig['layout']['yaxis'+str(row+1)]['tickfont'].update(size=24)
        fig['layout']['xaxis'+str(row+1)].update(range=[0,max_rl])

    fig['layout']['yaxis'+str(rows/2+1)].update(title='accuracy')
    fig['layout']['yaxis'+str(rows/2+1)]['titlefont'].update(size=24)
    fig['layout']['xaxis'+str(rows)].update(title='readlength (bases)')
    fig['layout']['xaxis'+str(rows)]['titlefont'].update(size=24)

    return fig

def _plot_accuracy_distribution(dsets_kpis):
    """
    Generate plotly histogram of accuracy distributions, overlaid
    Return a plot structure
    """

    data = []
    for key in dsets_kpis.keys():
        accuracy = dsets_kpis[key]['accuracy']
        data.append(accuracy)

    group_labels = dsets_kpis.keys()

    fig = FF.create_distplot(data, group_labels, show_hist=False)
    fig['layout']['xaxis'].update(title='Accuracy')
    fig['layout']['xaxis']['tickfont'].update(size=24)
    fig['layout']['xaxis']['titlefont'].update(size=24)
    fig['layout']['yaxis'].update(title='density')
    fig['layout']['yaxis']['tickfont'].update(size=24)
    fig['layout']['yaxis']['titlefont'].update(size=24)
    fig['layout']['font']['size'] = 20

    return fig

def _plot_accuracy_boxplots(dsets_kpis):
    """
    Generate plotly boxplots of accuracy distributions, side-by-side
    Return a plot structure
    """
    traces = []
    for key in dsets_kpis.keys():
        trace = Box(
            name = key,
            y = dsets_kpis[key]['accuracy'],
            boxpoints = 'all',
            jitter = 0.2,
            marker=dict(
                size=4,
                opacity=0.25
            ),
            boxmean=True
        )
        traces.append(trace)

    layout = Layout(
        font=dict(
            size=20
        ),
        yaxis=dict(
            autorange=True,
            showgrid=True,
            gridwidth=2,
            tickfont=dict(
                size=24
            )
        ),
        xaxis=dict(
            autorange=True,
            tickfont=dict(
                size=24
            )
        ),
        paper_bgcolor='rgb(243, 243, 243)',
        plot_bgcolor='rgb(243, 243, 243)',
        showlegend=True
    )

    fig = Figure(data=traces, layout=layout)

    return fig