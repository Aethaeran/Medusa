# coding=utf-8
"""Provider test code for Generic Provider."""
from __future__ import unicode_literals

from datetime import datetime

from dateutil import tz

from medusa.providers.generic_provider import GenericProvider

import pytest


sut = GenericProvider('FakeProvider')


@pytest.mark.parametrize('p', [
    {  # p0: None
        'pubdate': None,
        'expected': None
    },
    {  # p1: date and time
        'pubdate': '2017-05-18 15:00:15',
        'expected': datetime(2017, 5, 18, 15, 0, 15, tzinfo=tz.gettz('UTC'))
    },
    {  # p2: date, time and timezone
        'pubdate': '2017-05-16 17:12:25+02:00',
        'expected': datetime(2017, 5, 16, 17, 12, 25, tzinfo=tz.tzoffset(None, 7200))
    },
    {  # p3: human time and minutes
        'pubdate': '12 minutes ago',
        'expected': 720,  # difference in seconds
        'human_time': True
    },
    {  # p4: human time and hours
        'pubdate': '3hours',
        'expected': 10800,  # difference in seconds
        'human_time': True
    },
    {  # p5: date, time and custom timezone
        'pubdate': '2017-05-18 16:19:33',
        'expected': datetime(2017, 5, 18, 16, 19, 33, tzinfo=tz.gettz('UTC')),
        'timezone': 'US/Eastern'
    },
    {  # p6: human time hours (full day)
        'pubdate': '24 hours ago',
        'expected': 86400,  # difference in seconds
        'human_time': True
    },
    {  # p7: human now variant
        'pubdate': 'right now',
        'expected': 0,  # difference in seconds
        'human_time': True
    },
    {  # p8: human now variant
        'pubdate': 'just now',
        'expected': 0,  # difference in seconds
        'human_time': True
    },
    {  # p9: human now variant
        'pubdate': 'Now',
        'expected': 0,  # difference in seconds
        'human_time': True
    },
    {  # p10: invalid human time string
        'pubdate': 'This is not a valid hum readable date format!',
        'expected': None,  # difference in seconds
        'human_time': True
    },
    {  # p11: human time 1 minute
        'pubdate': '1 minute ago',
        'expected': 60,  # difference in seconds
        'human_time': True
    },
    {  # p12: dayfirst
        'pubdate': '2017-04-10 01:36:00+00:00',
        'expected': datetime(2017, 10, 4, 1, 36, tzinfo=tz.gettz('UTC')),
        'dayfirst': True
    },
    {  # p13: yearfirst
        'pubdate': '07-04-10 12:54:00+00:00',
        'expected': datetime(2007, 4, 10, 12, 54, tzinfo=tz.gettz('UTC')),
        'yearfirst': True
    },
    {  # p14: dayfirst and yearfirst
        'pubdate': '07-04-10 17:22:00+00:00',
        'expected': datetime(2007, 10, 4, 17, 22, tzinfo=tz.gettz('UTC')),
        'dayfirst': True,
        'yearfirst': True
    },
])
def test_parse_pubdate(p):
    # Given
    parsed_date = p['pubdate']
    expected = p['expected']
    ht = p.get('human_time', False)
    tzone = p.get('timezone')
    df = p.get('dayfirst', False)
    yf = p.get('yearfirst', False)

    # When
    actual = sut.parse_pubdate(parsed_date, human_time=ht, timezone=tzone,
                               dayfirst=df, yearfirst=yf)

    # Calculate the difference for human date comparison
    if ht and actual:
        actual = int((datetime.now(tz.tzlocal()) - actual).total_seconds())

    # Then
    assert expected == actual
