import paho.mqtt.client as mqtt
import time

host_url = "localhost"
port = 1883
topic = "cmd/Light"

class Subscriber:
    def __init__(self, on_message):
        self.mqttc = None
        self.set_client(on_message)

    def set_client(self, on_message):
        self.mqttc = mqtt.Client()
        self.mqttc.on_connect = self._connect
        self.mqttc.on_disconnect = self._disconnect
        self.mqttc.on_subscribe = self._subscribe
        self.mqttc.on_message = on_message

    def _connect(self, client, userdata, flags, rc):
        if rc == 0:
            print("subscriber connected")
        else:
            print("bad connection return code = ", rc)

    def _disconnect(self, client, userdata, flags, rc=0):
        print(str(rc))

    def _subscribe(self, client, userdata, mid, granted_qos):
        print("subscribed: " + str(mid) + " " + str(granted_qos))

    def start(self):
        self.mqttc.connect(host_url, port)
        self.mqttc.subscribe(topic, 1)
        self.mqttc.loop_forever()

    def stop(self):
        self.mqttc.disconnect()


class Publisher:
    def __init__(self):
        self.mqttc = None
        self.set_client()

    def set_client(self):
        self.mqttc = mqtt.Client()
        self.mqttc.on_connect = self._connect
        self.mqttc.on_disconnect = self._disconnect
        self.mqttc.on_publish = self._publish

    def _connect(self, client, userdata, flags, rc):
        if rc == 0:
            print("publisher connected")
        else:
            print("bad connection return code = ", rc)

    def _disconnect(self, client, userdata, flags, rc=0):
        print(str(rc))

    def _publish(self, client, userdata, mid):
        print("publish success, callback mid = ", mid)

    def start(self):
        self.mqttc.connect(host_url, port)
        #self.mqttc.loop_start()

    def stop(self):
        self.mqttc.loop_stop()
        self.mqttc.disconnect()

    def publish(self, data):
        self.mqttc.publish(topic, data, 1)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print('test mqtt using python')

    def on_message(client, userdata, msg):
        rx_message = str(msg.payload.decode("utf-8"))
        print(rx_message)
        if rx_message == 'q':
            print('stop subscriber')
            subscriber.stop()
        elif rx_message == '1':
            publisher = Publisher()
            publisher.start()
            publisher.publish('ccc')
            #time.sleep(1)
        # print(str(msg.payload.decode("utf-8")))

    subscriber = Subscriber(on_message)
    subscriber.start()



# See PyCharm help at https://www.jetbrains.com/help/pycharm/
