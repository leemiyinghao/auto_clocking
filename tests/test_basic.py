import pytest
from utils import log_activity, dump_activities
from models import Clock
from datetime import datetime, timedelta


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
