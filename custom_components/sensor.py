from . import KiaUvoEntity
from .const import DOMAIN, VEHICLE_DATA, VEHICLE_ACCOUNT

async def async_setup_entry(hass, config_entry, async_add_entities):
    vehicle_data = hass.data[DOMAIN][config_entry.entry_id][VEHICLE_ACCOUNT].vehicle_data

    async_add_entities([BatterySoC(hass, config_entry, vehicle_data)], True)
    async_add_entities([BatteryChargeTime(hass, config_entry, vehicle_data)], True)
   


class BatterySoC(KiaUvoEntity):
    def __init__(self, hass, config_entry, vehicle_data):
        super().__init__(hass, config_entry, vehicle_data)
        
    @property
    def icon(self):
        """Return the icon."""
        #return "mdi:battery"
        return "mdi:battery-charging" if self._vehicle_data.status["evStatus"]["batteryCharge"] else "mdi:battery"
    @property
    def state(self):
        return self._vehicle_data.status["evStatus"]["batteryStatus"]

    @property
    def state_attributes(self):
        return {
            'unit_of_measurement': '%',
            'minutes_to_charged': self._vehicle_data.status["evStatus"]["remainTime2"]["atc"]["value"],
        }

    @property
    def device_class(self):
        """Return the device class."""
        return "battery"

    @property
    def name(self):
        return f'{self._vehicle_data.vehicle["nickName"]} SoC'

    @property
    def unique_id(self):
        return f'kiauvo-SoC-{self._vehicle_data.vehicle["vehicleId"]}'


class BatteryChargeTime(KiaUvoEntity):
    def __init__(self, hass, config_entry, vehicle_data):
        super().__init__(hass, config_entry, vehicle_data)
        
    @property
    def icon(self):
        """Return the icon."""
        return "mdi:battery"
        #return "mdi:battery-charging" if self._vehicle_data.status["evStatus"]["batteryCharge"] else "mdi:battery"
    @property
    def state(self):
        return self._vehicle_data.status["evStatus"]["remainTime2"]["atc"]["value"]

    @property
    def state_attributes(self):
        return {
            'unit_of_measurement': 'min',
        }

    @property
    def device_class(self):
        """Return the device class."""
        return "battery"

    @property
    def name(self):
        return f'{self._vehicle_data.vehicle["nickName"]} Charge Time'

    @property
    def unique_id(self):
        return f'kiauvo-Charge-Time-{self._vehicle_data.vehicle["vehicleId"]}'

