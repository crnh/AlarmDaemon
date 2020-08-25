> :warning: **This app is currently under development and does not work yet. The docs below are my ideas about how it _should_ work and are regularly updated during the development process. As soon as the app works, I'll post about it on the Home Assistant Forums.** :warning: 

# WakeApp: Automatically set your alarm based on multiple sources

`WakeApp` is an AppDaemon app that automatically schedules alarms based on multiple sources, e.g. Home Assistant sensors, input_datetimes and calendars. It does currently only support Home Assistant entities as sources and I think that makes sense (since Home Assistant does a perfect job integrating a lot of services, why would I even want to write integrations for multiple calendar services myself?), but it shouldn't be too hard to add custom sources.

## How does it work?

`WakeApp` gets multiple alarm times from a list of sources, and then picks the earliest one, making sure you won't wake up too late. If `WakeApp` thinks you should wake up within 24 hours, it schedules one or more user defined service calls.

Three types of sources are currently supported: `calendar`, `sensor` and `input_datetime`. The source type is determined from the supplied entity ID.

Sometimes a source does not give the exact wake time; e.g. if you are using a calendar, you will probably want to have your alarm set some time _before_ an event begins :wink:. In this case, the source time can be mapped to an alarm time using [rules](#rules).

## Why would you want to use this?

Being a student, my life is more or less dictated by my university's schedule, so being able to schedule my alarms based on the university calendar makes life a little bit easier. Of course, I also want to be able to override this schedule, so it should also be able to use times I entered in Home Assistant. This functionality needs a lot of automations in order to get it working, and so `WakeApp` was born. Yes, it is complex and probably a niche case. But if it works for me, it's probably worth sharing.

## Configuration

Configuration is done using AppDaemon's `apps.yaml` file. An example is included below:

```yaml
wekker_crnh:
  module: wakeapp
  class: WakeApp
  sources:
    - entity_id: calendar.crnh
      rules:
        - after: 06:30
          before: 09:30
          alarm_time: 06:15
        - after: 09:30
          alarm_time: 06:45
  services:
    - service: light.turn_on
      offset: -600
      data:
        entity_id: light.corne_bed
        transition: 600
```

### General

option | type | default | description
:----- | :--- | :------ | :----------
`module` | string | Required | Must be `wakeapp`
`class` | string | Required | Must be `WakeApp`
`sources` | list | Required | List of `source` objects
`services` | list | Required | List of `service` objects


### Sources

The source object supports these configuration options:

option | type | default | description
:----- | :--- | :------ | :----------
`entity_id` | string | Required | Entity ID of the source, domain must be either `calendar`, `input_datetime` or `sensor`
`rules` | list | Optional | List of `rule` objects
`days` | list | Optional | List of days on which the source should be used. Allowed values are sun, mon, tue, wed, thu, fri, sat.
<!-- `date_format` | string | %Y-%M-%D %H:%M | Only used if the source is a sensor. Python strftime string to parse the sensor state to a (date)time object.
`timezone` | string | Optional | Only used if the source is a sensor. Python `dateutil` timezone string, this is needed if the time is not specified in the local timezone (e.g. UTC). -->

All time strings are parsed using `dateutil.parser.parse`, so most formats are supported without any configuration. If this does not work for your source, you can supply these extra arguments:

option | type | default | description
:----- | :--- | :------ | :----------
`dayfirst` | boolean | False | Whether to interpret the first value in an ambiguous 3-integer date (e.g. 01/05/09) as the day (`True`) or month (`False`).
`yearfirst` | boolean | False | Whether to interpret the first value in an ambiguous 3-integer date (e.g. 01/05/09) as the year. If `True`, the first number is taken to be the year, otherwise the last number is taken to be the year.
`fuzzy` | boolean | False | Whether to allow fuzzy parsing, allowing for string like "Today is January 1, 2047 at 8:21:00A".

For more information about these options, please consult the [`dateutil` docs](https://dateutil.readthedocs.io/en/stable/parser.html#dateutil.parser.parse).

### Rules

Rules are used to map a source time to an alarm time. They are parsed in the order in which they are specified and the first match is used to schedule the alarm. All options should be specified in the format `HH:MM:SS` or `HH:MM`. Examples:

```yaml
rules:
  # Returns 07:00 if the source time is before 06:00
  - before: 06:00
    alarm_time: 07:00
  # Returns 07:30 if the source time is between 06:00 and 08:00
  - after: 06:00
    before: 08:00
    alarm_time: 07:30
  # Returns 08:00 if the source time is after 08:00
  - after: 08:00
    alarm_time: 08:00
```


option | type | default | description
:----- | :--- | :------ | :----------
`before` | string | Optional | Matches if the time is before this value
`after` | string | Optional | Matches if the time is after this value
`alarm_time` | string | Required | Time that is returned on a match

### Services

The service object uses notation that is also used in automations and scripts, with some additional parameters. Although this app has been created with Home Assistant services in mind, you can of course also register your own AppDaemon services and call them from here.

option | type | default | description
:----- | :--- | :------ | :----------
`offset` | int | 0 | Offset in seconds to execute the service call before or after the scheduled alarm time. A negative offset means the service will be called before the scheduled alarm time.
`service` | string | Required | Name of the service that should be called. **Please note: if you supply the service name in Home Assistant notation (`script.my_fancy_script`) it will be automatically converted to AppDaemon notation (`script/my_fancy_script`).**
`data` | dict | Optional | Arguments that should be supplied to the script. This dictionary is passed directly into the service call, without any prior modifications.

 
