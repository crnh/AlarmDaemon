import hassapi as hass
from voluptuous import Schema, Optional, Required, All, ALLOW_EXTRA, In, Any
from datetime import datetime, timedelta

from sources import CalendarSource

from const import *

CONFIG_SCHEMA = Schema(
    {
        Required(CONF_SOURCES): All([{
            Required(CONF_ENTITY_ID): str,
            # Optional(CONF_RULES): All([{
            #     Any([{
            #         Required(CONF_RULE_BEFORE): str
            #     },
            #     {
            #         Required(CONF_RULE_AFTER): str
            #     }]),
            #     Required(CONF_RULE_TIME): str
            # }])
        }]),
        Required(CONF_SERVICES): All(
            [{
                Required(CONF_SERVICE): str,
                Required(CONF_SERVICE_DATA): dict,
                Optional(CONF_OFFSET): int
            }]
        ),
    },
    extra=ALLOW_EXTRA
)


class AlarmyApp(hass.Hass):
    def initialize(self):
        self.cfg = CONFIG_SCHEMA(self.args)
        self.log(self.cfg)

        # # c = self.parse_datetime(self.get_state(self.cfg[CONF_SOURCES][0][CONF_ENTITY_ID], attribute=CALENDAR_START_TIME))
        # d = self.get_state("sensor.corne_next_alarm")

        # # self.log(c)
        # self.log(self.parse_datetime(d))
