"""Scheduler class to schedule tasks."""

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
    is_stopping: bool
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
        self.is_stopping = False

    def run(self) -> None:
        """Run the scheduled task."""
        self.__run_loop__()

    def stop(self) -> None:
        """Stop the scheduled task at the end of the current loop."""
        self.is_stopping = True

    def __run_loop__(self) -> None:
        """Run the scheduled task."""
        if self.is_stopping:
            return

        self.is_running = True

        if type(self.executable) is type(Callable[[T], None]):
            cast(Callable[[T], None], self.executable)(self.params)
        else:
            cast(Callable[[], None], self.executable)()

        self.is_running = False
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

        if time_scale == TimeScale.MILLISECONDS:
            return n / 1000

        if time_scale == TimeScale.SECONDS:
            return n

        if time_scale == TimeScale.MINUTES:
            return n * 60

        if time_scale == TimeScale.HOURS:
            return n * 60 * 60
