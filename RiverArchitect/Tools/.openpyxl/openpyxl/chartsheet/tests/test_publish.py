from __future__ import absolute_import
# Copyright (c) 2010-2018 openpyxl

import pytest

from openpyxl.xml.functions import fromstring, tostring
from openpyxl.tests.helper import compare_xml

@pytest.fixture
def WebPublishItem():
    from ..publish import WebPublishItem

    return WebPublishItem


class TestWebPulishItem:
    def test_read(self, WebPublishItem):
        src = r"""
        <webPublishItem id="6433" divId="Views_6433" sourceType="chart" sourceRef=""
            sourceObject="Chart 1" destinationFile="D:\Publish.mht" autoRepublish="0"/>
        """
        xml = fromstring(src)
        webPulishItem = WebPublishItem.from_tree(xml)
        assert webPulishItem.id == 6433
        assert webPulishItem.sourceObject == "Chart 1"

    def test_write(self, WebPublishItem):
        webPublish = WebPublishItem(id=6433, divId="Views_6433", sourceType="chart", sourceRef="",
                                    sourceObject="Chart 1", destinationFile=r"D:\Publish.mht", title="First Chart",
                                    autoRepublish=False)
        expected = r"""
        <webPublishItem id="6433" divId="Views_6433" sourceType="chart" sourceRef=""
        sourceObject="Chart 1" destinationFile="D:\Publish.mht" title="First Chart" autoRepublish="0"/>
        """
        xml = tostring(webPublish.to_tree())
        diff = compare_xml(xml, expected)
        assert diff is None, diff


@pytest.fixture
def WebPublishItems():
    from ..publish import WebPublishItems

    return WebPublishItems


class TestWebPublishItems:
    def test_read(self, WebPublishItems):
        src = r"""
        <webPublishItems count="1">
            <webPublishItem id="6433" divId="Views_6433" sourceType="chart" sourceRef=""
            sourceObject="Chart 1" destinationFile="D:\Publish.mht" autoRepublish="0"/>
        </webPublishItems>
        """
        xml = fromstring(src)
        webPublishItems = WebPublishItems.from_tree(xml)
        assert webPublishItems.count == 1
        assert webPublishItems.webPublishItem[0].sourceObject == "Chart 1"

    def test_write(self, WebPublishItems):
        from ..publish import WebPublishItem

        webPublish_6433 = WebPublishItem(id=6433, divId="Views_6433", sourceType="chart", sourceRef="",
                                         sourceObject="Chart 1", destinationFile=r"D:\Publish.mht", title="First Chart",
                                         autoRepublish=False)
        webPublish_64487 = WebPublishItem(id=64487, divId="Views_64487", sourceType="chart", sourceRef="Ref_545421",
                                          sourceObject="Chart 15", destinationFile=r"D:\Publish_12.mht",
                                          title="Second Chart",
                                          autoRepublish=True)
        webPublishItems = WebPublishItems(webPublishItem=[webPublish_6433, webPublish_64487])
        expected = r"""
        <WebPublishItems count="2">
            <webPublishItem id="6433" divId="Views_6433" sourceType="chart" sourceRef=""
            sourceObject="Chart 1" destinationFile="D:\Publish.mht" title="First Chart" autoRepublish="0"/>
            <webPublishItem id="64487" divId="Views_64487" sourceType="chart" sourceRef="Ref_545421"
            sourceObject="Chart 15" destinationFile="D:\Publish_12.mht" title="Second Chart" autoRepublish="1"/>
        </WebPublishItems>
        """
        xml = tostring(webPublishItems.to_tree())
        diff = compare_xml(xml, expected)
        assert diff is None, diff
