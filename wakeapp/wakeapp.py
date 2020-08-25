# import hassapi as hass
import appdaemon.plugins.hass as hass
import voluptuous as vol
from voluptuous import Schema, Optional, Required, All, ALLOW_EXTRA, In, Any
from datetime import datetime, timedelta

from .sources import *

from .const import *

def change_service_notation(service_name: str) -> str:
    """Changes HA service notation to AD service notation."""

    return service_name.replace(".", "/", 1)

# SOURCE_SCHEMA = vol.Schema(
#     {
#         vol.Required(CONF_ENTITY_ID): str,
#         vol.Optional(CONF_RULES): list,
#         vol.Optional(CONF_WEEKDAYS): vol.All([
#             vol.Any(["sun", "mon", "tue", "wed", "thu", "fri", "sat"]),
#             vol.Unique()
#         ])
#     }
# )

# CONFIG_SCHEMA = vol.Schema(
#     {
#         vol.Required(CONF_SOURCES): vol.All([]),
#         vol.Required(CONF_SERVICES): vol.All(
#             [{
#                 vol.Required(CONF_SERVICE): str,
#                 vol.Required(CONF_SERVICE_DATA): dict,
#                 vol.Optional(CONF_OFFSET): int
#             }]
#         ),
#     },
#     extra=ALLOW_EXTRA
# )


class WakeApp(hass.Hass):
    def initialize(self):
        self.sources: List[Source] = []
        self.cfg = self.args  # CONFIG_SCHEMA(self.args)
        self.log(self.cfg)

    def register_sources(self):
        """Registers alarm time sources."""

        sources = self.cfg["sources"]

        for s in sources:
            if s[CONF_ENTITY_ID].startswith(DOMAIN_CALENDAR):
                self.sources.append(CalendarSource(**s, app=self))
            elif s[CONF_ENTITY_ID].startswith(DOMAIN_INPUT_DATETIME):
                self.sources.append(InputDatetimeSource(**s, app=self))
            elif s[CONF_ENTITY_ID].startswith(DOMAIN_INPUT_DATETIME):
                self.sources.append(SensorSource(**s, app=self))

    def schedule_next_alarm(self, **kwargs) -> None:
        """Schedules the next alarm."""

        alarm_time = sorted(
            filter(lambda t: t is not None, [s.get_alarm_time() for s in self.sources])
        )[0]

        self.log(alarm_time)
