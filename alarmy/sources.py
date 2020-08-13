from abc import ABC, abstractmethod
from typing import List, Dict, Optional, Union
from datetime import datetime, time
from alarmy import AlarmyApp

from const import *

class Source(ABC):
    rules: Optional[List[SourceRule]] = None

    def apply_rules(self, time: time) -> Optional[time]:
        try:
            alarm_time = [r.alarm_time for r in self.rules if r.check(time)][0]
        except IndexError:
            return None
        else:
            return alarm_time

    def get_alarm_time(self):
        source_time = self.get_source_time()
        alarm_time = self.apply_rules(source_time) if rules is not None else source_time

        return alarm_time

    @abstractmethod
    def get_source_time(self):
        pass


class CalendarSource(Source):
    def __init__(
        self,
        entity_id: str,
        app: "AlarmyApp",
        days: Optional[List[int]] = None,
        rules: Optional[List[Dict]] = None,
    ) -> None:
        self.entity_id = entity_id
        self.app = app
        self.days = day
        self.rules = [SourceRule(**r) for r in rules]
    
    def get_source_time(self):
        return self.app.parse_datetime(
            self.app.get_state(self.entity_id, attribute=)
        )


class SensorSource(Source):
    def __init__(
        self,
        entity_id: str,
        app: "AlarmyApp",
        days: Optional[List[int]] = None,
        rules: Optional[List[Dict]] = None,
        date_format: str = "%Y-%M-%D %H:%M",
    ) -> None:
        pass


class InputDatetimeSource(Source):
    def __init__(
        self,
        entity_id: str,
        app: "AlarmyApp",
        days: Optional[List[int]] = None,
        rules: Optional[List[Dict]] = None,
    ) -> None:
        pass


class SourceRule:
    def __init__(
        self,
        alarm_time: time,
        before: Optional[time] = None,
        after: Optional[time] = None,
    ) -> None:
        self.alarm_time = alarm_time

        self.before = before
        self.after = after

    def check(self, time: time):
        if self.after is not None:
            if time < self.after:
                return False

        if self.before is not None:
            if time > self.before:
                return False

        return True
