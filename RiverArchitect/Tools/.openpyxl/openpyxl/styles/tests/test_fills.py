from __future__ import absolute_import
# Copyright (c) 2010-2018 openpyxl

import pytest

from openpyxl.styles.colors import BLACK, WHITE, Color
from openpyxl.xml.functions import tostring, fromstring

from openpyxl.tests.helper import compare_xml

@pytest.fixture
def GradientFill():
    from openpyxl.styles.fills import GradientFill
    return GradientFill


@pytest.fixture
def Stop():
    from openpyxl.styles.fills import Stop
    return Stop


class TestGradientFill:

    def test_empty_ctor(self, GradientFill):
        gf = GradientFill()
        assert gf.type == 'linear'
        assert gf.degree == 0
        assert gf.left == 0
        assert gf.right == 0
        assert gf.top == 0
        assert gf.bottom == 0
        assert gf.stop == []


    def test_ctor(self, GradientFill):
        gf = GradientFill(degree=90, left=1, right=2, top=3, bottom=4)
        assert gf.degree == 90
        assert gf.left == 1
        assert gf.right == 2
        assert gf.top == 3
        assert gf.bottom == 4


    @pytest.mark.parametrize("colors",
                             [
                                 [Color(BLACK), Color(WHITE)],
                                 [BLACK, WHITE],
                             ]
                             )
    def test_stop_sequence(self, GradientFill, Stop, colors):
        gf = GradientFill(stop=[Stop(colors[0], 0), Stop(colors[1], .5)])
        assert gf.stop[0].color.rgb == BLACK
        assert gf.stop[1].color.rgb == WHITE
        assert gf.stop[0].position == 0
        assert gf.stop[1].position == .5


    @pytest.mark.parametrize("colors,rgbs,positions", [
        ([Color(BLACK), Color(WHITE)], [BLACK, WHITE], [0, 1]),
        ([BLACK, WHITE], [BLACK, WHITE], [0, 1]),
        ([BLACK, WHITE, BLACK], [BLACK, WHITE, BLACK], [0, .5, 1]),
        ([WHITE], [WHITE], [0]),
    ])
    def test_color_sequence(self, Stop, colors, rgbs, positions):
        from ..fills import _assign_position

        stops = _assign_position(colors)

        assert [stop.color.rgb for stop in stops] == rgbs
        assert [stop.position for stop in stops] == positions


    def test_invalid_stop_color_mix(self, Stop):
        from ..fills import _assign_position
        with pytest.raises(ValueError):
            _assign_position([Stop(BLACK, .1), WHITE])


    def test_duplicate_position(self, Stop):
        from ..fills import _assign_position

        with pytest.raises(ValueError):
            _assign_position([Stop(BLACK, 0.5), Stop(BLACK, 0.5)])


    def test_dict_interface(self, GradientFill):
        gf = GradientFill(degree=90, left=1, right=2, top=3, bottom=4)
        assert dict(gf) == {'bottom': "4", 'degree': "90", 'left':"1",
                            'right': "2", 'top': "3", 'type': 'linear'}


    def test_serialise(self, GradientFill, Stop):
        gf = GradientFill(degree=90, left=1, right=2, top=3, bottom=4,
                          stop=[Stop(BLACK, 0), Stop(WHITE, 1)])
        xml = tostring(gf.to_tree())
        expected = """
        <fill>
        <gradientFill bottom="4" degree="90" left="1" right="2" top="3" type="linear">
           <stop position="0">
              <color rgb="00000000"></color>
            </stop>
            <stop position="1">
              <color rgb="00FFFFFF"></color>
            </stop>
        </gradientFill>
        </fill>
        """
        diff = compare_xml(xml, expected)
        assert diff is None, diff


    def test_create(self, GradientFill, Stop):
        src = """
        <fill>
        <gradientFill xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" degree="90">
        <stop position="0">
          <color theme="0"/>
        </stop>
        <stop position="1">
          <color theme="4"/>
        </stop>
        </gradientFill>
        </fill>
        """
        xml = fromstring(src)
        fill = GradientFill.from_tree(xml)
        assert fill.stop == [Stop(Color(theme=0), position=0),
                             Stop(Color(theme=4), position=1)]


@pytest.fixture
def PatternFill():
    from ..fills import PatternFill
    return PatternFill


class TestPatternFill:

    def test_ctor(self, PatternFill):
        pf = PatternFill()
        assert pf.patternType is None
        assert pf.fgColor == Color()
        assert pf.bgColor == Color()


    def test_dict_interface(self, PatternFill):
        pf = PatternFill(fill_type='solid')
        assert dict(pf) == {'patternType':'solid'}


    def test_serialise(self, PatternFill):
        pf = PatternFill('solid', 'FF0000', 'FFFF00')
        xml = tostring(pf.to_tree())
        expected = """
        <fill>
        <patternFill patternType="solid">
            <fgColor rgb="00FF0000"/>
            <bgColor rgb="00FFFF00"/>
        </patternFill>
        </fill>
        """
        diff = compare_xml(xml, expected)
        assert diff is None, diff

    @pytest.mark.parametrize("src, args",
                             [
                                 ("""
                                 <fill>
                                 <patternFill xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" patternType="solid">
                                   <fgColor theme="0" tint="-0.14999847407452621"/>
                                   <bgColor indexed="64"/>
                                 </patternFill>
                                 </fill>
                                 """,
                                dict(patternType='solid',
                                     start_color=Color(theme=0, tint=-0.14999847407452621),
                                     end_color=Color(indexed=64)
                                     )
                                ),
                                 ("""
                                 <fill>
                                 <patternFill xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" patternType="solid">
                                   <fgColor theme="0"/>
                                   <bgColor indexed="64"/>
                                 </patternFill>
                                 </fill>
                                 """,
                                dict(patternType='solid',
                                     start_color=Color(theme=0),
                                     end_color=Color(indexed=64)
                                     )
                                ),
                                 ("""
                                 <fill>
                                 <patternFill xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" patternType="solid">
                                   <fgColor indexed="62"/>
                                   <bgColor indexed="64"/>
                                 </patternFill>
                                 </fill>
                                 """,
                                dict(patternType='solid',
                                     start_color=Color(indexed=62),
                                     end_color=Color(indexed=64)
                                     )
                                ),
                             ]
                             )
    def test_create(self, PatternFill, src, args):
        xml = fromstring(src)
        assert PatternFill.from_tree(xml) == PatternFill(**args)


def test_create_empty_fill():
    from ..fills import Fill

    src = fromstring("<fill/>")
    assert Fill.from_tree(src) is None


class TestStop:

    def test_ctor(self, Stop):
        stop = Stop('999999', .5)
        xml = tostring(stop.to_tree())
        expected = """
        <stop position="0.5">
              <color rgb="00999999"></color>
        </stop>
        """
        diff = compare_xml(xml, expected)
        assert diff is None, diff


    def test_from_xml(self, Stop):
        src = """
        <stop position=".5">
              <color rgb="00999999"></color>
        </stop>
        """
        node = fromstring(src)
        stop = Stop.from_tree(node)
        assert stop == Stop('999999', .5)


    @pytest.mark.parametrize('position', [0, .5, 1])
    def test_position_valid(self, Stop, position):
        # smoke test
        Stop('999999', position)


    @pytest.mark.parametrize('position,exception', [
        (-.1, ValueError),
        (1.1, ValueError),
        (None, TypeError)
    ])
    def test_position_invalid(self, Stop, position, exception):
        with pytest.raises(exception):
            Stop('999999', position)



def test_read_fills():
    # Make sure we pass the right class

    from ..fills import Fill
    s = """
    <fills count="3" xmlns:x="http://schemas.openxmlformats.org/spreadsheetml/2006/main">
    <fill>
      <patternFill patternType="none" />
    </fill>
    <fill>
      <patternFill patternType="gray125" />
    </fill>
    <fill>
      <gradientFill type="path" left="0.5" right="0.5" top="0.5" bottom="0.5">
        <stop position="0">
          <color theme="0" tint="-5.0935392315439317E-2" />
        </stop>
        <stop position="1">
          <color theme="0" tint="-0.25098422193060094" />
        </stop>
      </gradientFill>
    </fill>
    </fills>
    """
    xml = fromstring(s)
    for node in xml:
        fill = Fill.from_tree(node)
