"""Scheduler class to schedule tasks."""

import sys
from threading import Timer
from typing import Callable, cast, TypeVar
from scheduler.timer_scale import TimeScale

T = TypeVar("T")


class Scheduler[T]:
    """Scheduler class to schedule tasks."""

    timer: Timer
    executable: Callable[[T], None] | Callable[[], None]
    params: T
    is_running: bool
    __loop_time__: float

    def __init__(
        self,
        n: float,
        func: Callable[[T], None] | Callable[[], None],
        params: T = None,
        time_scale: TimeScale = TimeScale.MILLISECONDS,
    ) -> None:
        self.__loop_time__ = self.__to_seconds__(n, time_scale)
        self.executable = func
        self.params = params
        self.is_running = False

    def run(self) -> None:
        """Run the scheduled task."""
        self.is_running = True
        self.__run_loop__()

    def stop(self) -> None:
        """Stop the scheduled task at the end of the current loop."""
        self.is_running = False

    def __run_loop__(self) -> None:
        """Run the scheduled task."""
        if not self.is_running:
            return

        if type(self.executable) is type(Callable[[T], None]):
            cast(Callable[[T], None], self.executable)(self.params)
        else:
            cast(Callable[[], None], self.executable)()

        timer = Timer(self.__loop_time__, self.__run_loop__)
        timer.daemon = True
        try:
            timer.start()
        except:
            print("New thread not started. Exiting...")

    def __to_seconds__(self, n: float, time_scale: TimeScale) -> float:
        """Convert time to milliseconds."""
        if time_scale == TimeScale.NANOSECONDS:
            return n / 1000000000
        elif time_scale == TimeScale.MILLISECONDS:
            return n / 1000
        elif time_scale == TimeScale.SECONDS:
            return n
        elif time_scale == TimeScale.MINUTES:
            return n * 60
        elif time_scale == TimeScale.HOURS:
            return n * 60 * 60
