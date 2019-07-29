"""Micropython code for my esp8266
Simple http server that doesnt even care
what is being send while making request
just sends 200 response with DHT sensor data
"""
import dht
import machine
import time
import socket


class DHT_DATA:
    def __init__(self, pin_num):
        """ Holds dht data values
        """
        self.pin_num = pin_num
        self.dht_pin = dht.DHT11(machine.Pin(self.pin_num))
        self.temp = None
        self.humidity = None
        self.head_index = None
        self.measure()

    def measure(self):
        self.dht_pin.measure()
        self.temp = self.dht_pin.temperature()
        self.humidity = self.dht_pin.humidity()
        self.head_index = self.heat_index_calc()

    def heat_index_calc(self):
        f_temp = self.temp * (9 / 5) + 32
        f_heat_index = (
            -42.379
            + 2.04901523 * f_temp
            + 10.14333127 * self.humidity
            - 0.22475541 * f_temp * self.humidity
            - 0.00683783 * f_temp ** 2
            - 0.05481717 * self.humidity ** 2
            + 0.00122874 * f_temp ** 2 * self.humidity
            + 0.00085282 * f_temp * self.humidity ** 2
            - 0.00000199 * (f_temp * self.humidity) ** 2
        )
        return (f_heat_index - 32) * (5 / 9)

    def __str__(self):
        return "DHT11 pin: {} temp: {} humidity: {} head index: {}".format(
            self.pin_num, self.temp, self.humidity, self.head_index
        )


def main():
    dht_data = DHT_DATA(pin_num=16)
    # virtual timer
    dht_timer = machine.Timer(-1)
    # measure after 2 every seconds
    dht_timer.init(
        period=2000, mode=machine.Timer.PERIODIC, callback=lambda _: dht_data.measure()
    )
    http_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    http_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    http_server.bind(("", 80))
    http_server.listen(1)
    pin = machine.Pin(2, machine.Pin.OUT)
    # just to see when it starts
    pin.off()
    time.sleep(1)
    pin.on()
    while True:
        client_socket, _ = http_server.accept()
        _ = client_socket.recv(1024)
        # lets ignore routes and request type
        http_body = """\
<!DOCTYPE html>
<html>
<head>
    <link rel="stylesheet" href="https://cdn.rawgit.com/kimeiga/bahunya/css/bahunya-0.1.3.css"/>
</head>
<body>
    <div style="margin: 10% auto 0; width: 20%; ">
        <table>
            <tr>
            <th>Temp(°C)</th><td>{}</td>
            </tr>
            <tr>
            <th>Humidity(%) </th><td>{}</td>
            </tr>
            <tr>
            <th>Heat Index(°C)</th><td>{}</td>
            </tr>
        </table>
    </div>
</body>
</html>
""".format(
            dht_data.temp, dht_data.humidity, dht_data.head_index
        )
        http_response = b"""\
HTTP/1.1 200 OK
Server: dht socket server 0.0.1
Content-Type: text/html; charset=utf-8
Content-Length: {}

{}
""".format(
            len(http_body), http_body
        )
        client_socket.sendall(http_response)
        client_socket.close()


main()
