from __future__ import absolute_import
# Copyright (c) 2010-2018 openpyxl

import pytest

from openpyxl.utils.indexed_list import IndexedList
from ..named_styles import (
    NamedStyleList,
    NamedStyle,
)


def test_descriptor(Worksheet):
    from ..styleable import StyleDescriptor
    from ..cell_style import StyleArray
    from ..fonts import Font

    class Styled(object):

        font = StyleDescriptor('_fonts', "fontId")

        def __init__(self):
            self._style = StyleArray()
            self.parent = Worksheet

    styled = Styled()
    styled.font = Font()
    assert styled.font == Font()


@pytest.fixture
def Workbook():

    class DummyWorkbook:

        _fonts = IndexedList()
        _fills = IndexedList()
        _borders = IndexedList()
        _protections = IndexedList()
        _alignments = IndexedList()
        _number_formats = IndexedList()
        _named_styles = NamedStyleList()

        def add_named_style(self, style):
            self._named_styles.append(style)
            style.bind(self)

    return DummyWorkbook()


@pytest.fixture
def Worksheet(Workbook):

    class DummyWorksheet:

        parent = Workbook

    return DummyWorksheet()


@pytest.fixture
def StyleableObject(Worksheet):
    from .. styleable import StyleableObject
    so = StyleableObject(sheet=Worksheet, style_array=list(range(9)))
    return so


def test_has_style(StyleableObject):
    so = StyleableObject
    so._style = None
    assert not so.has_style
    so.number_format= 'dd'
    assert so.has_style


class TestNamedStyle:

    def test_assign_name(self, StyleableObject):
        so = StyleableObject
        wb = so.parent.parent
        style = NamedStyle(name='Standard')
        wb.add_named_style(style)

        so.style = 'Standard'
        assert so._style.xfId == 0


    def test_assign_style(self, StyleableObject):
        so = StyleableObject
        wb = so.parent.parent
        style = NamedStyle(name='Standard')

        so.style = style
        assert so._style.xfId == 0


    def test_unknown_style(self, StyleableObject):
        so = StyleableObject

        with pytest.raises(ValueError):
            so.style = "Financial"


    def test_read(self, StyleableObject):
        so = StyleableObject
        wb = so.parent.parent

        red = NamedStyle(name='Red')
        wb.add_named_style(red)
        blue = NamedStyle(name='Blue')
        wb.add_named_style(blue)

        so._style.xfId = 1
        assert so.style == "Blue"


    def test_builtin(self, StyleableObject):
        so = StyleableObject
        so.style = "Hyperlink"
        assert so.style == "Hyperlink"


    def test_copy_not_share(self, StyleableObject):
        s1 = StyleableObject
        wb = s1.parent.parent

        from copy import copy
        s2 = copy(s1)
        s1.style = "Hyperlink"
        s2.style = "Hyperlink"
        assert s1._style is not s2._style
