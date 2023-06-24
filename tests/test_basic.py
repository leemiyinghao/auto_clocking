from datetime import datetime, timedelta

import pytest
from auto_clocking.models import Clock
from auto_clocking.utils import dump_activities, log_activity


@pytest.fixture(scope="function")
def db_fixture():
    Clock.setup_database(":memory:")
    yield
    Clock._db_inited = False


def test_simple_log_dump(db_fixture):
    now = datetime.now()
    log_activity(now - timedelta(hours=1))
    log_activity(now - timedelta(minutes=55))
    log_activity(now - timedelta(minutes=51))

    dumps = dump_activities(1)
    assert len(dumps) == 2
    ats, ips, clocks = zip(*dumps)
    assert ats == (now - timedelta(hours=1), now - timedelta(minutes=51))
    assert clocks == ("clock-in", "clock-out")
