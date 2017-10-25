#  -*- coding: utf-8 -*-

# This file is part of Cockpit.
#
# Copyright (C) 2016 Red Hat, Inc.
#
# Cockpit is free software; you can redistribute it and/or modify it
# under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation; either version 2.1 of the License, or
# (at your option) any later version.
#
# Cockpit is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with Cockpit; If not, see <http://www.gnu.org/licenses/>.
# Author: Miloš Prchlík (https://gist.github.com/happz/d50897af8a2e90cce8c7)
#         Jan Scotka <jscotka@redhat.com>

import signal
import time

class Timeout(object):
    def __init__(self, retry, timeout):
        self.retry = retry
        self.timeout = timeout

    def __enter__(self):
        def timeout_handler(signum, frame):
            if __debug__:
                self.retry.timeouts_triggered += 1

            raise Exception()

        self.orig_sighand = signal.signal(signal.SIGALRM, timeout_handler)
        signal.alarm(self.timeout)

    def __exit__(self, type, value, traceback):
        signal.alarm(0)
        signal.signal(signal.SIGALRM, self.orig_sighand)


class NOPTimeout(object):
    def __init__(self, *args, **kwargs):
        pass

    def __enter__(self):
        pass

    def __exit__(self, *args, **kwargs):
        pass


class Retry(object):
    def __init__(self, attempts=1, timeout=None, exceptions=(Exception,), error=None, inverse=False, delay=None):
        """
        Try to run things ATTEMPTS times, at max, each attempt must not exceed TIMEOUT seconds.
        Restart only when one of EXCEPTIONS is raised, all other mtfexceptions will just bubble up.
        When the maximal number of attempts is reached, raise ERROR. Wait DELAY seconds between
        attempts.
        When INVERSE is True, successfull return of wrapped code is considered as a failure.
        """

        self.attempts = attempts
        self.timeout = timeout
        self.exceptions = exceptions
        self.error = error or Exception('Too many retries!')
        self.inverse = inverse
        self.timeout_wrapper = Timeout if timeout is not None else NOPTimeout
        self.delay = delay if delay is not None else timeout

        # some accounting, for testing purposes
        if __debug__:
            self.failed_attempts = 0
            self.timeouts_triggered = 0

    def handle_failure(self, start_time):
        if __debug__:
            self.failed_attempts += 1

        self.attempts -= 1
        if self.attempts == 0:
            raise self.error

        # Before the next iteration sleep $delay seconds. It's the
        # remaining time to the $timeout Since it makes not much sense
        # to feed time.sleep() with negative delays, return None.

        if self.delay is None:
            return None

        delay = self.delay - (time.time() - start_time)
        return delay if delay > 0 else None

    def __call__(self, fn):
        def __wrap(*args, **kwargs):
            # This is not an endless loop. It will be broken by
            # 1) first "successfull" return of fn() - taking self.inverse into account, of course - or
            # 2) by decrementing self.attempts to zero, or
            # 3) when unexpected exception is raised by fn().

            output = None
            delay = None  # no delay yet

            while True:
                if delay is not None:
                  time.sleep(delay)

                with self.timeout_wrapper(self, self.timeout):
                    start_time = time.time()

                    try:
                        output = fn(*args, **kwargs)
                        if not self.inverse:
                            return output

                    except self.exceptions as e:
                        if self.inverse:
                            return True

                        # Handle mtfexceptions we are expected to catch, by logging a failed
                        # attempt, and checking the number of attempts.
                        delay = self.handle_failure(start_time)
                        continue

                    except Exception as e:
                        # Handle all other mtfexceptions, by logging a failed attempt and
                        # re-raising the exception, effectively killing the loop.
                        if __debug__:
                            self.failed_attempts += 1
                        raise e

                delay = self.handle_failure(start_time)

        return __wrap
