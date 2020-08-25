from abc import ABC, abstractmethod
from typing import List, Dict, Optional, Union
from datetime import datetime, time, timedelta
from dateutil.parser import parse
from voluptuous.error import Error
from alarmy import WakeApp

from const import *


class SourceRule:
    def __init__(
        self,
        alarm_time: time,
        before: Optional[time] = None,
        after: Optional[time] = None,
        **kwargs,
    ) -> None:
        self.alarm_time = alarm_time

        self.before = before
        self.after = after

    def apply(self, source_time: datetime) -> Union[bool, datetime]:

        if self.after is not None:
            if source_time.time() < self.after:
                return False

        if self.before is not None:
            if source_time.time() > self.before:
                return False

        return source_time.replace(
            hour=self.alarm_time.hour, minute=self.alarm_time.minute
        )


class Source(ABC):
    def __init__(
        self,
        entity_id: str,
        app: "WakeApp",
        weekdays: Optional[List[int]] = None,
        rules: Optional[List[Dict]] = None,
        **kwargs,
    ) -> None:
        self.entity_id = entity_id
        self.app = app
        self.weekdays = [parse(w).weekday() for w in weekdays] if weekdays else list(range(6))
        self.rules = [SourceRule(**r) for r in rules] if rules else None

        self.init_source(**kwargs)

    @abstractmethod
    def init_source(self, **kwargs) -> None:
        """Performs further initialization of the source."""
        pass

    def apply_rules(self, source_time: datetime) -> Optional[datetime]:
        for r in self.rules:
            if t := r.apply(source_time):
                return t

        return None

    def get_alarm_time(self) -> datetime:
        alarm_time = self.get_source_time()

        if self.rules is not None:
            alarm_time = self.apply_rules(alarm_time)

        return alarm_time

    @abstractmethod
    def get_source_time(self) -> datetime:
        pass


class CalendarSource(Source):
    def init_source(self, **kwargs) -> None:
        pass

    def get_source_time(self) -> Optional[datetime]:
        try:
            return parse(
                self.app.get_state(self.entity_id, attribute=CALENDAR_ATTR_START_TIME)
            )
        except Exception as e:
            self.app.log(f"Could not parse time from calendar {self.entity_id}: {e}")

            return None


class SensorSource(Source):
    def init_source(
        self,
        attribute: Optional[str] = None,
        date_format: str = "%Y-%M-%D %H:%M",
        timezone: Optional[str] = None,
    ) -> None:
        self.attribute = attribute
        self.date_format = date_format
        self.timezone = timezone

    def get_source_time(self) -> datetime:
        sensor_time = parse(
            self.app.get_state(self.entity_id, attribute=self.attribute)
        )

        if sensor_time < datetime.now():
            sensor_time = sensor_time + timedelta(days=1)

        return sensor_time


class InputDatetimeSource(Source):
    def init_source(self, **kwargs) -> None:
        pass

    def get_source_time(self) -> datetime:
        sensor_time = parse(
            self.app.get_state(self.entity_id)
        )

        if sensor_time < datetime.now():
            sensor_time = sensor_time + timedelta(days=1)

        return sensor_time
