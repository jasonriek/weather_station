from flask import Flask, jsonify, redirect, send_from_directory
import board
import busio
import adafruit_bme680

app = Flask(__name__)

# Create I2C bus interface
i2c = busio.I2C(board.SCL, board.SDA)

# Create BME680 object with default I2C address (0x76 or 0x77)
sensor = adafruit_bme680.Adafruit_BME680_I2C(i2c, address=0x77)

# Optionally, you can change the sea level pressure (in hPa) to get more accurate altitude data
sensor.sea_level_pressure = 1013.25

def read_sensor():
    celsius = sensor.temperature
    fahrenheit = (celsius * 9 / 5) + 32
    meters = sensor.altitude
    feet = meters * 3.28084

    data = {
        "temperature": fahrenheit,
        "gas_resistance": sensor.gas,
        "humidity": sensor.humidity,
        "pressure": sensor.pressure,
        "altitude": feet
    }

    return data

@app.route('/', methods=['GET'])
def index():
    return redirect('/api/sensor')

@app.route('/api/sensor', methods=['GET'])
def get_sensor_data():
    data = read_sensor()
    return jsonify(data)

@app.route('/download/cert', methods=['GET'])
def download_cert():
    cert_directory = '/etc/ssl/weather_app'
    cert_file = 'weather.local.pfx'
    return send_from_directory(directory=cert_directory, path=cert_file, as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=52007)

