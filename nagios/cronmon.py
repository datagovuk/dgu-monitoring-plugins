#!/usr/bin/env python
"""
    cronmon is a nagios plugin that checks syslog to make sure that specific
    cron jobs ran within the last X minutes. For this specific use the status
    is dependant of how many multiples of X have passed since the last run of
    the process. We'll add a buffer of a minute to the times we will allow.

     * Ran in last X minutes STATE_OK
     * Ran in last X * 3 minutes STATE_WARNING
     * Otherwise STATE_CRITICAL

    The process works by jumping to the end of the file, and then jumping
    backwards 4Kb at a time until we find a line that is before the warning
    time. From there we iterate through the lines until we can be sure that
    the task ran within a given time window.
 """
import os
import sys
from optparse import OptionParser
from datetime import datetime, timedelta
from dateutil import parser

STATE_OK = 0
STATE_WARNING  = 1
STATE_CRITICAL = 2
BUFFER_SIZE = 4096

debug = False
options = None

# Setup testing data if test is passed as a command line arg
debug = len(sys.argv) == 2 and sys.argv[1] == 'test'
if debug:
    syslog_file = "./testlog"

def read_date(line):
    if not line:
        return None
    dt = " ".join(line.split(' ')[0:3])
    return parser.parse(dt)


def seek_back_until(when, filesize, f, offset=1):
    """
        Seeks back from the end of the file in 8k chunks until if finds a line that
        is older than time_now - (time_span * 3)
    """
    d = datetime(1900, 1, 1)

    while d:
        to = BUFFER_SIZE * offset
        if f.tell() - to  < 0 and offset > 1:
            # If we have done at least one iteration and then next takes us back
            # before the start of the file, just process the whole file.
            return

        # Seek buffer size back from end of file
        f.seek(-to, 2)

        # Throw away the next line, it is more than likely a partial and
        # of no use.
        f.readline()
        d = read_date(f.readline())
        if d and d < when:
            return

        offset += 1

def process_log(time_now=datetime.now(), log="/var/syslog"):
    """ Run the process against the specified log file """
    when_warning = time_now - timedelta(minutes=options.time_span * 3)
    when_ok = time_now - timedelta(minutes=options.time_span)
    size = os.stat(log).st_size
    msg = "CRITICAL: Task has not run in last 30 minutes"
    state = STATE_CRITICAL
    with open(log, "r") as f:
        seek_back_until(when_warning, size, f)
        for line in f:
            date_on_line = read_date(line)
            if date_on_line > when_ok and options.match_line in line:
                state = STATE_OK
                msg = "OK: Task ran %d minutes ago" % ((time_now - date_on_line).seconds / 60)
            elif date_on_line > when_warning and options.match_line in line:
                state = STATE_WARNING
                msg = "WARNING: Task last ran %d minutes ago" % ((time_now - date_on_line).seconds / 60)
    return state, msg

def test():
    """ Tail of test log (not in repo) is
            Last entry in log Apr 22 10:46:20
            Last harvest run at Apr 22 10:40:01
    """
    print "Running some tests against 'testlog' ... "
    # 36 minutes after last run
    state, msg = process_log(time_now=datetime(2013, 4, 22, 11, 16, 20), log="./testlog")
    print msg
    assert state == STATE_CRITICAL

    state, msg = process_log(time_now=datetime(2013, 4, 22, 10, 56, 20), log="./testlog")
    # 16 minutes after last run
    print msg
    assert state == STATE_WARNING, state

    state, msg = process_log(time_now=datetime(2013, 4, 22, 10, 48, 20), log="./testlog")
    # 8 minutes after last run
    print msg
    assert state == STATE_OK


if __name__ == "__main__":
    p = OptionParser()
    p.add_option("-d", "--debug", dest="debug", default=False, action="store_true",
        help="Specifies that tests should be run")
    p.add_option("-f", "--file", dest="filename", help="Location of syslog file",
        default="/var/log/syslog")
    p.add_option("-l", "--line", dest="match_line", help="The line to match",
        default="--plugin=ckanext-harvest harvester run")
    p.add_option("-t", "--time", dest="time_span", default=10, type="int",
        help="Specify the time period that is allowable, in minutes")

    (options, args) = p.parse_args()

    if options.debug:
        test()
        sys.exit(0)

    state, msg = process_log(log=options.filename)
    print msg
    sys.exit(state)
