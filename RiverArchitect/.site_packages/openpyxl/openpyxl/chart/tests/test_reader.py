from __future__ import absolute_import
# Copyright (c) 2010-2018 openpyxl

from zipfile import ZipFile

from openpyxl.xml.functions import fromstring

from .. line_chart import LineChart
from .. axis import NumericAxis, DateAxis
from .. chartspace import ChartSpace


def test_read(datadir):
    datadir.chdir()
    from .. reader import read_chart

    with open("chart1.xml") as src:
        xml = src.read()
    tree = fromstring(xml)
    cs = ChartSpace.from_tree(tree)
    chart = read_chart(cs)

    assert isinstance(chart, LineChart)
    assert chart.title.tx.rich.p[0].r[0].t == "Website Performance"

    assert isinstance(chart.y_axis, NumericAxis)
    assert chart.y_axis.title.tx.rich.p[0].r[0].t == "Time in seconds"

    assert isinstance(chart.x_axis, DateAxis)
    assert chart.x_axis.title is None

    assert len(chart.series) == 10


def test_read_drawing(datadir):
    datadir.chdir()

    archive = ZipFile("sample.xlsx")
    path = "xl/drawings/drawing1.xml"

    from ..reader import find_charts
    charts = find_charts(archive, path)
    assert len(charts) == 6
