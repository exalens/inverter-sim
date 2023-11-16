from enum import Enum
import random

class InverterMode(Enum):
    NORMAL = "NORMAL"
    MAINTENANCE = "MAINTENANCE"
    ERROR = "ERROR"

def get_enum_by_value(value):
    for recipe in InverterMode:
        if recipe.value == value:
            return recipe
    return None

def generate_cyclical_values(mode, time_step):
    # Define lists of possible values for each variable
    pv_current_values = [10.0, 10.408, 10.816, 11.224, 11.633, 12.041, 12.449, 12.857, 13.265, 13.673, 14.082, 14.49,
                      14.898, 15.306, 15.714, 16.122, 16.531, 16.939, 17.347, 17.755, 18.163, 18.571, 18.98, 19.388,
                      19.796]
    pv_amperage_values = [5.0, 5.204, 5.408, 5.612, 5.816, 6.02, 6.224, 6.429, 6.633, 6.837, 7.041, 7.245, 7.449, 7.653,
                       7.857, 8.061, 8.265, 8.469, 8.673, 8.878, 9.082, 9.286, 9.49, 9.694, 9.898]
    pv_voltage_values = [220.0, 220.612, 221.224, 221.837, 222.449, 223.061, 223.673, 224.286, 224.898, 225.51, 226.122,
                      226.735, 227.347, 227.959, 228.571, 229.184, 229.796, 230.408, 231.02, 231.633, 232.245, 232.857,
                      233.469, 234.082, 234.694]
    load_values = [50.0, 51.02, 52.041, 53.061, 54.082, 55.102, 56.122, 57.143, 58.163, 59.184, 60.204, 61.224, 62.245,
                   63.265, 64.286, 65.306, 66.327, 67.347, 68.367, 69.388, 70.408, 71.429, 72.449, 73.469, 74.49]
    pv_ac_power_values = [200.0, 202.041, 204.082, 206.122, 208.163, 210.204, 212.245, 214.286, 216.327, 218.367, 220.408,
                       222.449, 224.49, 226.531, 228.571, 230.612, 232.653, 234.694, 236.735, 238.776, 240.816, 242.857,
                       244.898, 246.939, 248.98]
    pv_dc_power_values = [180.0, 181.429, 182.857, 184.286, 185.714, 187.143, 188.571, 190.0, 191.429, 192.857, 194.286,
                       195.714, 197.143, 198.571, 200.0, 201.429, 202.857, 204.286, 205.714, 207.143, 208.571, 210.0,
                       211.429, 212.857, 214.286]
    pv_temperature_values = [25.0, 25.306, 25.612, 25.918, 26.224, 26.531, 26.837, 27.143, 27.449, 27.755, 28.061, 28.367,
                          28.673, 28.98, 29.286, 29.592, 29.898, 30.204, 30.51, 30.816, 31.122, 31.429, 31.735, 32.041,
                          32.347]
    status_code_values = [1]
    battery_temperature_values = [10.1, 12.3, 9.8, 15.2, 16.7, 15.3, 18.123, 22.324, 17.433, 11.98, 23.33]
    battery_health_values = ["High"]
    battery_state_of_charge_values = [99.12, 98.123, 97.34, 99.01, 96.22, 97.99, 99.111]
    operating_mode_values = ["NORMAL"]

    # Example cyclical value generation based on the time step
    values = {
        'PvCurrent': pv_current_values[time_step % len(pv_current_values)],
        'PvAmperage': pv_amperage_values[time_step % len(pv_amperage_values)],
        'PvVoltage': pv_voltage_values[time_step % len(pv_voltage_values)],
        'PvPower': pv_voltage_values[time_step % len(pv_voltage_values)] * pv_amperage_values[time_step % len(pv_amperage_values)],
        'Load': load_values[time_step % len(load_values)],
        'PvACPower': pv_ac_power_values[time_step % len(pv_ac_power_values)],
        'PvDCPower': pv_dc_power_values[time_step % len(pv_dc_power_values)],
        'PvTemperature': pv_temperature_values[time_step % len(pv_temperature_values)],
        'StatusCode': status_code_values[time_step % len(status_code_values)],
        'BatteryTemp': battery_temperature_values[time_step % len(battery_temperature_values)],
        'BatteryHealth': battery_health_values[time_step % len(battery_health_values)],
        'BatteryCharge': battery_state_of_charge_values[time_step % len(battery_state_of_charge_values)],
        'OperatingMode': operating_mode_values[time_step % len(operating_mode_values)]

    }

    # Adjust the values for different modes if necessary
    if mode == InverterMode.MAINTENANCE:
        # Adjust values for maintenance mode
        values['PvCurrent'] *= 0.1
        values['PvVoltage'] *= 0.1
        values['PvAmperage'] *= 0.1
        values['PvPower'] *= 0.1
        values['PvACPower'] *= 0.1
        values['PvDCPower'] *= 0.1
        values['PvTemperature'] *= 0.1
        values['StatusCode'] = 0
        values['BatteryHealth'] = "High"
        values['BatteryTemp'] *= 0.1
        values['BatteryCharge'] -= random.choice([5, 7, 8, 9, 10])
        values['OperatingMode'] = "MAINTENANCE"

        # Other adjustments as needed

    elif mode == InverterMode.ERROR:
        # Set values for error mode
        values = {key: 0 for key in values}
        values['PvTemperature'] = 100  # Static value in Error mode
        values['StatusCode'] = -1
        values['BatteryHealth'] = "Low"
        values['BatteryTemp'] = 90
        values['BatteryCharge'] = 0.01
        values['OperatingMode'] = "FAULT"

    return values
