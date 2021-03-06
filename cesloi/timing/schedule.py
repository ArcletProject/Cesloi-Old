import asyncio
from datetime import datetime, timedelta
from typing import Optional, List
from .timers import Timer

from ..delegatesystem import EventDelegate
from .task import TimingTask


class Toconada:
    """
    托可娜达,莱恩家的姐姐，与妹妹一起住在Cesloi隔壁

    用于非事件订阅器的调度器

    Args:
        delegate: 事件系统的实例
    """
    delegate: EventDelegate
    loop: asyncio.AbstractEventLoop
    schedule_tasks: List[TimingTask]

    def __init__(self, delegate: EventDelegate):
        self.delegate = delegate
        self.loop = self.delegate.loop
        self.schedule_tasks = []

    def timing(self, timer: Timer, is_disposable: Optional[bool] = False):
        """定时一个函数/方法

        Args:
            timer : 时间器实例, 参考timing.timers
            is_disposable: 是否只执行一次该函数/方法
        """
        def wrapper(func):
            task = TimingTask(
                func, timer, self.delegate, is_disposable
            )
            self.schedule_tasks.append(task)
            task.set_task()
            return func

        return wrapper


class Toconado:
    """
    托可娜多,莱恩家的妹妹,与Cesloi玩得更好

    用于事件订阅器的调度器

    Args:
            timer : 时间器实例, 参考timing.timers
    """
    timer: Timer
    last_run: Optional[datetime]

    def __init__(self, timer: Timer):
        self.timer = timer
        self.last_run = None

    def should_run(self):
        if not self.last_run:
            self.last_run = datetime.now()
            return True
        for interval in self.timer.get_delta():
            now = datetime.now()
            if self.last_run + (interval - now) <= now:
                self.last_run = now - timedelta(microseconds=now.microsecond / 1000000)
                return True
            return False
