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
    __does_loop__: bool
    __current_loop__: int
    __loop_time__: float
    __loop_time_does_change__: bool
    __loop_times__: list[float] | list[int]
    __time_scale__: TimeScale

    def __init__(
        self,
        n: float | list[float] | list[int],
        func: Callable[[T], None] | Callable[[], None],
        params: T = None,
        time_scale: TimeScale = TimeScale.MILLISECONDS,
        loops: bool = True,
    ) -> None:
        if isinstance(n, list):
            assert len(n) > 0, "Must present at least one `n` value in the list."
            self.__loop_time_does_change__ = True
            self.__loop_time__ = self.__to_seconds__(n[0], time_scale)
            self.__loop_times__ = n
        else:
            self.__loop_time_does_change__ = False
            self.__loop_time__ = self.__to_seconds__(n, time_scale)
            self.__loop_times__ = []

        self.__time_scale__ = time_scale
        self.__does_loop__ = loops
        self.__current_loop__ = 0
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
        self.__current_loop__ += 1

        if type(self.executable) is type(Callable[[T], None]):
            cast(Callable[[T], None], self.executable)(self.params)
        else:
            cast(Callable[[], None], self.executable)()

        if not self.__loop_time_does_change__ and not self.__does_loop__:
            # We don't loop and we don't have a dynamic loop count so we only run once
            self.stop()
            return

        if self.__loop_time_does_change__ and self.__current_loop__ >= len(
            self.__loop_times__
        ):
            # We've reached the end of the dynamic loop times, check if we start again
            if self.__does_loop__:
                self.__current_loop__ = 0
            else:
                self.stop()
                return

        self.is_running = False
        timer = Timer(self.__loop_time__, self.__run_loop__)
        timer.daemon = True

        if self.__loop_time_does_change__:
            self.__loop_time__ = self.__to_seconds__(
                self.__loop_times__[self.__current_loop__], self.__time_scale__
            )

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
