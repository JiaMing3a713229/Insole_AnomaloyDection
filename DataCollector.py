import paho.mqtt.client as mqtt
import time

mqtt_host = "broker.emqx.io"
mqtt_port = 1883
mqtt_topic_insole = "SmartInsole/RL"

    
def on_message(client, userdata, msg):
    print(f"Received message: {msg.payload.decode()} on topic {msg.topic}")




if __name__ == "__main__":

    client = mqtt.Client()
    client.on_publish = on_publish

    # 连接到MQTT代理（broker）
    client.connect(mqtt_host, mqtt_port, 60)
    

    # 发布消息
    # result = client.publish(topic, message)

    # 等待消息发布完成
    # result.wait_for_publish()

    # 断开连接
    client.disconnect()