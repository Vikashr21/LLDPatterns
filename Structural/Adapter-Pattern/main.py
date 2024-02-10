# Define the CelsiusTemperatureSensor class
class CelsiusTemperatureSensor:
    def __init__(self, temperature):
        self.temperature = temperature

    def get_temperature(self):
        return self.temperature

# Define the FahrenheitTemperatureSensor class
class FahrenheitTemperatureSensor:
    def __init__(self, temperature):
        self.temperature = temperature

    def get_temperature(self):
        return self.temperature

# Define the Adapter class
class TemperatureSensorAdapter:
    def __init__(self, fahrenheit_sensor):
        self.fahrenheit_sensor = fahrenheit_sensor

    def get_temperature(self):
        temperature_in_fahrenheit = self.fahrenheit_sensor.get_temperature()
        return (temperature_in_fahrenheit - 32) * 5 / 9

# Demonstration
if __name__ == "__main__":
    # Existing system sensor
    celsius_sensor = CelsiusTemperatureSensor(25)
    print(f"Celsius Sensor Reading: {celsius_sensor.get_temperature()}°C")

    # New sensor that requires an adapter
    fahrenheit_sensor = FahrenheitTemperatureSensor(77)  # Equivalent to 25°C
    adapter = TemperatureSensorAdapter(fahrenheit_sensor)
    print(f"Adapted Fahrenheit Sensor Reading: {adapter.get_temperature()}°C")
