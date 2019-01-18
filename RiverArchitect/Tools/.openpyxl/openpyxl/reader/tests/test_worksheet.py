from __future__ import absolute_import
# Copyright (c) 2010-2018 openpyxl

import pytest

import datetime
from io import BytesIO
from zipfile import ZipFile

from lxml.etree import iterparse, fromstring

from openpyxl import load_workbook
from openpyxl.compat import unicode
from openpyxl.xml.constants import SHEET_MAIN_NS
from openpyxl.utils.indexed_list import IndexedList
from openpyxl.worksheet import Worksheet
from openpyxl.worksheet.pagebreak import Break, PageBreak
from openpyxl.packaging.relationship import Relationship, RelationshipList


def test_get_xml_iter():
    #1 file object
    #2 stream (file-like)
    #3 string
    #4 zipfile
    from openpyxl.reader.worksheet import _get_xml_iter
    from tempfile import TemporaryFile

    FUT = _get_xml_iter
    s = b""
    stream = FUT(s)
    assert isinstance(stream, BytesIO), type(stream)

    u = unicode(s)
    stream = FUT(u)
    assert isinstance(stream, BytesIO), type(stream)

    f = TemporaryFile(mode='rb+', prefix='openpyxl.', suffix='.unpack.temp')
    stream = FUT(f)
    assert stream == f
    f.close()

    t = TemporaryFile()
    z = ZipFile(t, mode="w")
    z.writestr("test", "whatever")
    stream = FUT(z.open("test"))
    assert hasattr(stream, "read")

    try:
        z.close()
    except IOError:
        # you can't just close zipfiles in Windows
        z.close() # python 2.7


@pytest.fixture
def Workbook():
    from openpyxl.styles.styleable import StyleArray
    from openpyxl.styles import numbers

    class DummyStyle:
        number_format = numbers.FORMAT_GENERAL
        font = ""
        fill = ""
        border = ""
        alignment = ""
        protection = ""

        def copy(self, **kw):
            return self


    class DummyWorkbook:

        guess_types = False
        data_only = False
        _colors = []
        encoding = "utf8"

        def __init__(self):
            self._differential_styles = []
            self.shared_strings = IndexedList()
            self.shared_strings.add("hello world")
            self._fonts = IndexedList()
            self._fills = IndexedList()
            self._number_formats = IndexedList()
            self._borders = IndexedList()
            self._alignments = IndexedList()
            self._protections = IndexedList()
            self._cell_styles = IndexedList()
            self.vba_archive = None
            for i in range(29):
                self._cell_styles.add((StyleArray([i]*9)))
            self._cell_styles.add(StyleArray([0,4,6,0,0,1,0,0,0])) #fillId=4, borderId=6, alignmentId=1))
            self.sheetnames = []


        def create_sheet(self, title):
            return Worksheet(self)


    return DummyWorkbook()


@pytest.fixture
def WorkSheetParser(Workbook):
    """Setup a parser instance with an empty source"""
    from .. worksheet import WorkSheetParser
    ws = Workbook.create_sheet('sheet')
    return WorkSheetParser(ws, None, {0:'a'})


@pytest.fixture
def WorkSheetParserKeepVBA(Workbook):
    """Setup a parser instance with an empty source"""
    Workbook.vba_archive=True
    from .. worksheet import WorkSheetParser
    ws = Workbook.create_sheet('sheet')
    return WorkSheetParser(ws, {0:'a'}, {})


def test_col_width(datadir, WorkSheetParser):
    datadir.chdir()
    parser = WorkSheetParser
    ws = parser.ws

    with open("complex-styles-worksheet.xml", "rb") as src:
        cols = iterparse(src, tag='{%s}col' % SHEET_MAIN_NS)
        for _, col in cols:
            parser.parse_column_dimensions(col)
    assert set(ws.column_dimensions) == set(['A', 'C', 'E', 'I', 'G'])
    assert ws.column_dimensions['A'].style_id == 0
    assert dict(ws.column_dimensions['A']) == {'max': '1', 'min': '1',
                                               'customWidth': '1',
                                               'width': '31.1640625'}


def test_hidden_col(datadir, WorkSheetParser):
    datadir.chdir()
    parser = WorkSheetParser
    ws = parser.ws

    with open("hidden_rows_cols.xml", "rb") as src:
        cols = iterparse(src, tag='{%s}col' % SHEET_MAIN_NS)
        for _, col in cols:
            parser.parse_column_dimensions(col)
    assert 'D' in ws.column_dimensions
    assert dict(ws.column_dimensions['D']) == {'customWidth': '1', 'hidden':
                                               '1', 'max': '4', 'min': '4'}


def test_styled_col(datadir, WorkSheetParser):
    datadir.chdir()
    parser = WorkSheetParser
    ws = parser.ws

    with open("complex-styles-worksheet.xml", "rb") as src:
        cols = iterparse(src, tag='{%s}col' % SHEET_MAIN_NS)
        for _, col in cols:
            parser.parse_column_dimensions(col)
    assert 'I' in ws.column_dimensions
    cd = ws.column_dimensions['I']
    assert cd.style_id == 28
    assert dict(cd) ==  {'customWidth': '1', 'max': '9', 'min': '9', 'width': '25', 'style':'28'}


def test_hidden_row(datadir, WorkSheetParser):
    datadir.chdir()
    parser = WorkSheetParser
    ws = parser.ws

    with open("hidden_rows_cols.xml", "rb") as src:
        rows = iterparse(src, tag='{%s}row' % SHEET_MAIN_NS)
        for _, row in rows:
            parser.parse_row(row)
    assert 2 in ws.row_dimensions
    assert dict(ws.row_dimensions[2]) == {'hidden': '1'}


def test_styled_row(datadir, WorkSheetParser):
    datadir.chdir()
    parser = WorkSheetParser
    ws = parser.ws
    parser.shared_strings = dict((i, i) for i in range(30))

    with open("complex-styles-worksheet.xml", "rb") as src:
        rows = iterparse(src, tag='{%s}row' % SHEET_MAIN_NS)
        for _, row in rows:
            parser.parse_row(row)
    assert 23 in ws.row_dimensions
    rd = ws.row_dimensions[23]
    assert rd.style_id == 28
    assert dict(rd) == {'s':'28', 'customFormat':'1'}


def test_sheet_protection(datadir, WorkSheetParser):
    datadir.chdir()
    parser = WorkSheetParser
    ws = parser.ws

    with open("protected_sheet.xml", "rb") as src:
        tree = iterparse(src, tag='{%s}sheetProtection' % SHEET_MAIN_NS)
        for _, tag in tree:
            parser.parse_sheet_protection(tag)
    assert dict(ws.protection) == {
        'autoFilter': '0', 'deleteColumns': '0',
        'deleteRows': '0', 'formatCells': '0', 'formatColumns': '0', 'formatRows':
        '0', 'insertColumns': '0', 'insertHyperlinks': '0', 'insertRows': '0',
        'objects': '0', 'password': 'DAA7', 'pivotTables': '0', 'scenarios': '0',
        'selectLockedCells': '0', 'selectUnlockedCells': '0', 'sheet': '1', 'sort':
        '0'
    }


def test_formula_without_value(WorkSheetParser):
    parser = WorkSheetParser
    ws = parser.ws

    src = """
      <x:c r="A1" xmlns:x="http://schemas.openxmlformats.org/spreadsheetml/2006/main">
        <x:f>IF(TRUE, "y", "n")</x:f>
        <x:v />
      </x:c>
    """
    element = fromstring(src)

    parser.parse_cell(element)
    assert ws['A1'].data_type == 'f'
    assert ws['A1'].value == '=IF(TRUE, "y", "n")'


def test_formula(WorkSheetParser):
    parser = WorkSheetParser
    ws = parser.ws

    src = """
    <x:c r="A1" t="str" xmlns:x="http://schemas.openxmlformats.org/spreadsheetml/2006/main">
        <x:f>IF(TRUE, "y", "n")</x:f>
        <x:v>y</x:v>
    </x:c>
    """
    element = fromstring(src)

    parser.parse_cell(element)
    assert ws['A1'].data_type == 'f'
    assert ws['A1'].value == '=IF(TRUE, "y", "n")'


def test_formula_data_only(WorkSheetParser):
    parser = WorkSheetParser
    ws = parser.ws
    parser.data_only = True

    src = """
    <x:c r="A1" xmlns:x="http://schemas.openxmlformats.org/spreadsheetml/2006/main">
        <x:f>1+2</x:f>
        <x:v>3</x:v>
    </x:c>
    """
    element = fromstring(src)

    parser.parse_cell(element)
    assert ws['A1'].data_type == 'n'
    assert ws['A1'].value == 3


def test_string_formula_data_only(WorkSheetParser):
    parser = WorkSheetParser
    ws = parser.ws
    parser.data_only = True

    src = """
    <x:c r="A1" t="str" xmlns:x="http://schemas.openxmlformats.org/spreadsheetml/2006/main">
        <x:f>IF(TRUE, "y", "n")</x:f>
        <x:v>y</x:v>
    </x:c>
    """
    element = fromstring(src)

    parser.parse_cell(element)
    assert ws['A1'].data_type == 's'
    assert ws['A1'].value == 'y'


def test_number(WorkSheetParser):
    parser = WorkSheetParser
    ws = parser.ws

    src = """
    <x:c r="A1" xmlns:x="http://schemas.openxmlformats.org/spreadsheetml/2006/main">
        <x:v>1</x:v>
    </x:c>
    """
    element = fromstring(src)

    parser.parse_cell(element)
    assert ws['A1'].data_type == 'n'
    assert ws['A1'].value == 1



def test_datetime(WorkSheetParser):
    parser = WorkSheetParser
    ws = parser.ws

    src = """
    <x:c r="A1" t="d" xmlns:x="http://schemas.openxmlformats.org/spreadsheetml/2006/main">
        <x:v>2011-12-25T14:23:55</x:v>
    </x:c>
    """
    element = fromstring(src)

    parser.parse_cell(element)
    assert ws['A1'].data_type == 'd'
    assert ws['A1'].value == datetime.datetime(2011, 12, 25, 14, 23, 55)


def test_string(WorkSheetParser):
    parser = WorkSheetParser
    ws = parser.ws

    src = """
    <x:c r="A1" t="s" xmlns:x="http://schemas.openxmlformats.org/spreadsheetml/2006/main">
        <x:v>0</x:v>
    </x:c>
    """
    element = fromstring(src)

    parser.parse_cell(element)
    assert ws['A1'].data_type == 's'
    assert ws['A1'].value == "a"


def test_boolean(WorkSheetParser):
    parser = WorkSheetParser
    ws = parser.ws

    src = """
    <x:c r="A1" t="b" xmlns:x="http://schemas.openxmlformats.org/spreadsheetml/2006/main">
        <x:v>1</x:v>
    </x:c>
    """
    element = fromstring(src)

    parser.parse_cell(element)
    assert ws['A1'].data_type == 'b'
    assert ws['A1'].value is True


def test_inline_string(WorkSheetParser, datadir):
    parser = WorkSheetParser
    ws = parser.ws
    datadir.chdir()

    with open("Table1-XmlFromAccess.xml") as src:
        sheet = fromstring(src.read())

    element = sheet.find("{%s}sheetData/{%s}row/{%s}c" % (SHEET_MAIN_NS, SHEET_MAIN_NS, SHEET_MAIN_NS))
    parser.parse_cell(element)
    assert ws['A1'].data_type == 's'
    assert ws['A1'].value == "ID"


def test_inline_richtext(WorkSheetParser, datadir):
    parser = WorkSheetParser
    ws = parser.ws
    datadir.chdir()
    with open("jasper_sheet.xml", "rb") as src:
        sheet = fromstring(src.read())

    element = sheet.find("{%s}sheetData/{%s}row[2]/{%s}c[18]" % (SHEET_MAIN_NS, SHEET_MAIN_NS, SHEET_MAIN_NS))
    assert element.get("r") == 'R2'
    parser.parse_cell(element)
    cell = ws['R2']
    assert cell.data_type == 's'
    assert cell.value == "11 de September de 2014"


def test_legacy_drawing(datadir):
    datadir.chdir()
    wb = load_workbook("legacy_drawing.xlsm", keep_vba=True)
    sheet1 = wb['Sheet1']
    assert sheet1.legacy_drawing == 'xl/drawings/vmlDrawing1.vml'
    sheet2 = wb['Sheet2']
    assert sheet2.legacy_drawing == 'xl/drawings/vmlDrawing2.vml'


def test_cell_style(WorkSheetParser, datadir):
    datadir.chdir()
    parser = WorkSheetParser
    ws = parser.ws
    parser.shared_strings[1] = "Arial Font, 10"

    with open("complex-styles-worksheet.xml") as src:
        sheet = fromstring(src.read())

    element = sheet.find("{%s}sheetData/{%s}row[2]/{%s}c[1]" % (SHEET_MAIN_NS, SHEET_MAIN_NS, SHEET_MAIN_NS))
    assert element.get('r') == 'A2'
    assert element.get('s') == '2'
    parser.parse_cell(element)
    assert ws['A2']._style == parser.styles[2]
    assert ws['A2'].style_id == 2


def test_cell_exotic_style(WorkSheetParser, datadir):
    datadir.chdir()
    parser = WorkSheetParser
    ws = parser.ws
    parser.styles = [None, None, [0,0,0,0,0,0,1,1,0]]

    src = """
    <x:c xmlns:x="http://schemas.openxmlformats.org/spreadsheetml/2006/main" r="D4" s="2">
    </x:c>
    """

    sheet = fromstring(src)
    parser.parse_cell(sheet)
    assert ws['A1'].pivotButton is False

    cell = ws['D4']
    assert cell.pivotButton is True
    assert cell.quotePrefix is True


def test_sheet_views(WorkSheetParser, datadir):
    datadir.chdir()
    parser = WorkSheetParser

    with open("frozen_view_worksheet.xml") as src:
        sheet = src.read()

    parser.source = sheet
    parser.parse()
    ws = parser.ws
    view = ws.sheet_view

    assert view.zoomScale == 200
    assert len(view.selection) == 3


def test_legacy_document_keep(WorkSheetParserKeepVBA, datadir):
    parser = WorkSheetParserKeepVBA
    datadir.chdir()

    with open("legacy_drawing_worksheet.xml") as src:
        sheet = fromstring(src.read())

    element = sheet.find("{%s}legacyDrawing" % SHEET_MAIN_NS)
    parser.parse_legacy_drawing(element)
    assert parser.ws.legacy_drawing == 'rId3'


def test_legacy_document_no_keep(WorkSheetParser, datadir):
    parser = WorkSheetParser
    datadir.chdir()

    with open("legacy_drawing_worksheet.xml") as src:
        sheet = fromstring(src.read())

    element = sheet.find("{%s}legacyDrawing" % SHEET_MAIN_NS)
    parser.parse_legacy_drawing(element)
    assert parser.ws.legacy_drawing is None


@pytest.fixture
def Translator():
    from openpyxl.formula import translate
    return translate.Translator

def test_shared_formula(WorkSheetParser, Translator):
    parser = WorkSheetParser
    src = """
    <x:c r="A9" t="str" xmlns:x="http://schemas.openxmlformats.org/spreadsheetml/2006/main">
      <x:f t="shared" si="0"/>
      <x:v>9</x:v>
    </x:c>
    """
    element = fromstring(src)
    parser.shared_formula_masters['0'] = Translator("=A4*B4", "A1")
    parser.parse_cell(element)
    assert parser.ws['A9'].value == "=A12*B12"


import warnings
warnings.simplefilter("always") # so that tox doesn't suppress warnings.

def test_extended_conditional_formatting(WorkSheetParser, datadir, recwarn):
    datadir.chdir()
    parser = WorkSheetParser

    with open("extended_conditional_formatting_sheet.xml") as src:
        sheet = fromstring(src.read())

    element = sheet.find("{%s}extLst" % SHEET_MAIN_NS)
    parser.parse_extensions(element)
    w = recwarn.pop()
    assert issubclass(w.category, UserWarning)


def test_row_dimensions(WorkSheetParser):
    src = """<row r="2" spans="1:6" x14ac:dyDescent="0.3" xmlns:x14ac="http://schemas.microsoft.com/office/spreadsheetml/2009/9/ac" />"""
    element = fromstring(src)

    parser = WorkSheetParser
    parser.parse_row(element)

    assert 2 not in parser.ws.row_dimensions


def test_shared_formulae(WorkSheetParser, datadir):
    datadir.chdir()
    parser = WorkSheetParser
    ws = parser.ws
    parser.shared_strings = ["Whatever"] * 7

    with open("worksheet_formulae.xml") as src:
        parser.source = src.read()

    parser.parse()

    assert set(ws.formula_attributes) == set(['C10'])

    # Test shared forumlae
    assert ws['B7'].data_type == 'f'
    assert ws['B7'].value == '=B4*2'
    assert ws['C7'].value == '=C4*2'
    assert ws['D7'].value == '=D4*2'
    assert ws['E7'].value == '=E4*2'

    # Test array forumlae
    assert ws['C10'].data_type == 'f'
    assert ws.formula_attributes['C10']['ref'] == 'C10:C14'
    assert ws['C10'].value == '=SUM(A10:A14*B10:B14)'


def test_cell_without_coordinates(WorkSheetParser, datadir):
    datadir.chdir()
    with open("worksheet_without_coordinates.xml", "rb") as src:
        xml = src.read()

    sheet = fromstring(xml)

    el = sheet.find(".//{%s}row" % SHEET_MAIN_NS)

    parser = WorkSheetParser
    parser.shared_strings = ["Whatever"] * 10
    parser.parse_row(el)

    assert parser.ws.max_row == 1
    assert parser.ws.max_column == 5


def test_external_hyperlinks(WorkSheetParser):
    src = """
    <sheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">
      <hyperlink xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"
       display="http://test.com" r:id="rId1" ref="A1"/>
    </sheet>
    """
    from openpyxl.packaging.relationship import Relationship, RelationshipList

    r = Relationship(type="hyperlink", Id="rId1", Target="../")
    rels = RelationshipList()
    rels.append(r)

    parser = WorkSheetParser
    parser.source = src
    parser.ws._rels = rels

    parser.parse()

    assert parser.ws['A1'].hyperlink.target == "../"


def test_local_hyperlinks(WorkSheetParser):
    src = """
    <sheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" >
      <hyperlinks>
        <hyperlink ref="B4:B7" location="'STP nn000TL-10, PKG 2.52'!A1" display="STP 10000TL-10"/>
      </hyperlinks>
    </sheet>
    """
    parser = WorkSheetParser
    parser.source = src
    parser.parse()

    assert parser.ws['B4'].hyperlink.location == "'STP nn000TL-10, PKG 2.52'!A1"


def test_merge_cells(WorkSheetParser):
    src = """
    <sheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">
      <mergeCells>
        <mergeCell ref="C2:F2"/>
        <mergeCell ref="B19:C20"/>
        <mergeCell ref="E19:G19"/>
      </mergeCells>
    </sheet>
    """

    parser = WorkSheetParser
    parser.source = src

    parser.parse()

    assert parser.ws.merged_cells == "C2:F2 B19:C20 E19:G19"


def test_conditonal_formatting(WorkSheetParser):
    src = """
    <sheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">
      <conditionalFormatting sqref="S1:S10">
        <cfRule type="top10" dxfId="25" priority="12" percent="1" rank="10"/>
    </conditionalFormatting>
    <conditionalFormatting sqref="T1:T10">
      <cfRule type="top10" dxfId="24" priority="11" bottom="1" rank="4"/>
    </conditionalFormatting>
    </sheet>
    """
    from openpyxl.styles.differential import DifferentialStyle

    parser = WorkSheetParser
    dxf = DifferentialStyle()
    parser.differential_styles = [dxf] * 30
    parser.source = src

    parser.parse()

    assert parser.ws.conditional_formatting['T1:T10'][-1].dxf == dxf


def test_sheet_properties(WorkSheetParser):
    src = """
    <sheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">
    <sheetPr codeName="Sheet3">
      <tabColor rgb="FF92D050"/>
      <outlinePr summaryBelow="1" summaryRight="1"/>
      <pageSetUpPr/>
    </sheetPr>
    </sheet>
    """
    parser = WorkSheetParser
    parser.source = src
    parser.parse()

    assert parser.ws.sheet_properties.tabColor.rgb == "FF92D050"
    assert parser.ws.sheet_properties.codeName == "Sheet3"


def test_sheet_format(WorkSheetParser):

    src = """
    <sheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">
      <sheetFormatPr defaultRowHeight="14.25" baseColWidth="15"/>
    </sheet>
    """
    parser = WorkSheetParser
    parser.source = src
    parser.parse()

    assert parser.ws.sheet_format.defaultRowHeight == 14.25
    assert parser.ws.sheet_format.baseColWidth == 15


def test_tables(WorkSheetParser):
    src = """
    <sheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"
      xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">
      <tableParts count="1">
        <tablePart r:id="rId1"/>
      </tableParts>
    </sheet>
    """

    parser = WorkSheetParser
    r = Relationship(type="table", Id="rId1", Target="../tables/table1.xml")
    rels = RelationshipList()
    rels.append(r)
    parser.ws._rels = rels

    parser.source = src
    parser.parse()

    assert parser.tables == ["../tables/table1.xml"]


def test_auto_filter(WorkSheetParser):
    src = """
    <sheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">
      <autoFilter ref="A1:AK3237">
        <sortState ref="A2:AM3269">
            <sortCondition ref="B1:B3269"/>
        </sortState>
      </autoFilter>
    </sheet>
    """

    parser = WorkSheetParser
    parser.source = src
    parser.parse()
    ws = parser.ws

    assert ws.auto_filter.ref == "A1:AK3237"
    assert ws.auto_filter.sortState.ref == "A2:AM3269"
    assert ws.sort_state.ref is None


@pytest.mark.xfail
def test_sort_state(WorkSheetParser):
    src = """
    <sheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">
    <sortState ref="A2:AM3269">
        <sortCondition ref="B1:B3269"/>
    </sortState>
    </sheet>
    """

    parser = WorkSheetParser
    parser.source = src
    parser.parse()
    ws = parser.ws

    assert ws.sort_state.ref == "A2:AM3269"


def test_page_break(WorkSheetParser):
    src = """
    <sheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">
        <rowBreaks count="1" manualBreakCount="1">
            <brk id="15" man="1" max="16383" min="0"/>
        </rowBreaks>
    </sheet>
    """
    expected_pagebreak = PageBreak()
    expected_pagebreak.append(Break(id=15))

    parser = WorkSheetParser
    parser.source = src
    parser.parse()
    ws = parser.ws

    assert ws.page_breaks == expected_pagebreak
