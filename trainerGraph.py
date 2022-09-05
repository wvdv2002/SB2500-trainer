import plotly as py
import plotly.graph_objs as go
from pprint import pprint
from plotly.graph_objs import Scatter, Figure, Layout
import datetime
import os

dateFormat = "%Y-%m-%d %H-%M-%S"
dir_plots = './plots/'



def doPlot(data):
    if dir_plots and not os.path.exists(dir_plots):
        os.makedirs(dir_plots)

    listData = {}
    if len(data)>0:
        for point in data[0].__dict__.keys():
            listData[point] = []
        for line in data:
            for (key,val) in line.__dict__.items():
                listData[key].append(val)
        pprint(listData)
        traceList = []
        for (key,val) in listData.items():
            print(key)
            trace = go.Scatter(x=list(range(0,len(val))),y=val,mode = 'lines',name=key)
            traceList.append(trace)
        plotName = dir_plots + "plot-" + datetime.datetime.now().strftime(dateFormat) + ".html"
        py.offline.plot(traceList,auto_open=True,filename=plotName)

