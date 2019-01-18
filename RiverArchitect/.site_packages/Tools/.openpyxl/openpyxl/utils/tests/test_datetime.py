from __future__ import absolute_import
# Copyright (c) 2010-2018 openpyxl

# Python stdlib imports
from datetime import (
    datetime,
    date,
    timedelta,
    time,
    tzinfo
)

import pytest


def test_to_iso():
    from ..datetime import to_ISO8601
    assert to_ISO8601(datetime(2013, 7, 15, 6, 52, 33)) == "2013-07-15T06:52:33Z"


@pytest.mark.parametrize("value, group, expected",
                         [
                             ("2011-06-30", "date", "2011-06-30"),
                             ("12:19:01", "time", "12:19:01"),
                         ]
                         )
def test_iso_regex(value, group, expected):
    from ..datetime import ISO_REGEX
    match = ISO_REGEX.match(value)
    assert match is not None
    assert match.groupdict()[group] == expected


@pytest.mark.parametrize("value, expected",
                         [
                             ("2011-06-30T13:35:26Z", datetime(2011, 6, 30, 13, 35, 26)),
                             ("2013-03-04T12:19:01.00Z", datetime(2013, 3, 4, 12, 19, 1)),
                             ("2011-06-30", date(2011, 6, 30)),
                             ("12:19:01", time(12, 19, 1)),
                         ]
                         )
def test_from_iso(value, expected):
    from ..datetime  import from_ISO8601
    assert from_ISO8601(value) == expected


@pytest.mark.parametrize("value, expected",
                         [
                             (date(1899, 12, 31), 0),
                             (date(1900, 1, 15), 15),
                             (date(1900, 2, 28), 59),
                             (date(1900, 3, 1), 61),
                             (datetime(2010, 1, 18, 14, 15, 20, 1600), 40196.5939815),
                             (date(2009, 12, 20), 40167),
                             (datetime(1506, 10, 15), -143618.0),
                         ])
def test_to_excel(value, expected):
    from ..datetime import to_excel
    FUT = to_excel
    assert FUT(value) == expected


@pytest.mark.parametrize("value, expected",
                         [
                             (date(1904, 1, 1), 0),
                             (date(2011, 10, 31), 39385),
                             (datetime(2010, 1, 18, 14, 15, 20, 1600), 38734.5939815),
                             (date(2009, 12, 20), 38705),
                             (datetime(1506, 10, 15), -145079.0)
                         ])
def test_to_excel_mac(value, expected):
    from ..datetime import to_excel, CALENDAR_MAC_1904
    FUT = to_excel
    assert FUT(value, CALENDAR_MAC_1904) == expected


@pytest.mark.parametrize("value, expected",
                         [
                             (40167, datetime(2009, 12, 20)),
                             (21980, datetime(1960,  3,  5)),
                             (59, datetime(1900, 2, 28)),
                             (-25063, datetime(1831, 5, 18, 0, 0)),
                             (40372.27616898148, datetime(2010, 7, 13, 6, 37, 41)),
                             (40196.5939815, datetime(2010, 1, 18, 14, 15, 20, 1600)),
                             (0.125, time(3, 0)),
                             (42126.958333333219, datetime(2015, 5, 2, 22, 59, 59, 999990)),
                             (42126.999999999884, datetime(2015, 5, 3, 0, 0, 0)),
                             (None, None),
                         ])
def test_from_excel(value, expected):
    from ..datetime import from_excel
    FUT = from_excel
    assert FUT(value) == expected


@pytest.mark.parametrize("value, expected",
                         [
                             (39385, datetime(2011, 10, 31)),
                             (21980, datetime(1964,  3,  6)),
                             (0, datetime(1904, 1, 1)),
                             (-25063, datetime(1835, 5, 19))
                         ])
def test_from_excel_mac(value, expected):
    from ..datetime import from_excel, CALENDAR_MAC_1904
    FUT = from_excel
    assert FUT(value, CALENDAR_MAC_1904) == expected


def test_time_to_days():
    from ..datetime  import time_to_days
    FUT = time_to_days
    t1 = time(13, 55, 12, 36)
    assert FUT(t1) == 0.5800000004166667
    t2 = time(3, 0, 0)
    assert FUT(t2) == 0.125


def test_timedelta_to_days():
    from ..datetime import timedelta_to_days
    FUT = timedelta_to_days
    td = timedelta(days=1, hours=3)
    assert FUT(td) == 1.125


def test_days_to_time():
    from ..datetime import days_to_time
    td = timedelta(0, 51320, 1600)
    FUT = days_to_time
    assert FUT(td) == time(14, 15, 20, 1600)


class CET(tzinfo):

    def utcoffset(self, dt):
        return timedelta(hours=1) + self.dst(dt)

    def dst(self, dt):
        # DST starts last Sunday in March
        d = datetime(dt.year, 4, 1)   # ends last Sunday in October
        self.dston = d - timedelta(days=d.weekday() + 1)
        d = datetime(dt.year, 11, 1)
        self.dstoff = d - timedelta(days=d.weekday() + 1)
        if self.dston <=  dt.replace(tzinfo=None) < self.dstoff:
            return timedelta(hours=1)
        else:
            return timedelta(0)

    def tzname(self,dt):
        return "CET +1"


def test_localised_time():

    from ..datetime import time_to_days, GMT

    dt1 = datetime(2015, 7, 24, tzinfo=GMT())
    dt2 = datetime(2015, 7, 24, 2, tzinfo=CET())
    assert dt2 - dt2 == timedelta(0)

    e1 = time_to_days(dt1)
    e2 = time_to_days(dt2)

    assert e1 == 0
    assert e2 == 0
