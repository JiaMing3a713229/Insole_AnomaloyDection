from fastapi import FastAPI
from fastapi_mqtt import FastMQTT, MQTTConfig
from openpyxl import Workbook
import threading
import time

workbook = Workbook()
sheet = workbook.active

mqtt_host = "broker.emqx.io"
mqtt_port = 1883
topic_smartInsole = "SmartInsole/#" 
mqtt_topic_L = "SmartInsole/L"
mqtt_topic_R = "SmartInsole/R"
mqtt_topic_LR = "SmartInsole/RL"
result_r = ""
result_l = ""
result_lr = ""
message_arrived = False
isLogState = False

app = FastAPI()
message_payload = ""
mqtt_config = MQTTConfig(
    host = mqtt_host,
    port= mqtt_port,

)
mqtt = FastMQTT(
    config=mqtt_config
)

def write_to_excel():
    global result_r, result_l, message_arrived, result_lr, isLogState
    count = 0
    while True:
        time.sleep(0.1)
        print(isLogState)
        # print("Task1 work")
        # if(((len(result_l) > 10) and (len(result_r) > 10)) and message_arrived):
        #     count += 1
        #     print(f'write {count}th data')
        #     list_result_r = eval(result_r)
        #     list_result_l = eval(result_l)
        #     int_dataR = [int(x) for x in list_result_r]
        #     int_dataL = [int(x) for x in list_result_l]
        #     result_data = int_dataR + int_dataL
        #     sheet.append(result_data)
        #     # message_arrived = False
        #     if(count % 200 == 0):
        if((len(result_l) > 10) and (isLogState)):
            count += 1
            print(f'write {count}th data {result_l}')
            # list_result_lr = eval(result_lr)
            # int_dataLR = [int(x) for x in list_result_lr]
            # sheet.append(int_dataLR)
            # message_arrived = False
            list_result_l = eval(result_l)
            int_dataL = [int(x) for x in list_result_l]
            sheet.append(int_dataL)
            if(count % 200 == 0):
                workbook.save("NormalData_test.xlsx")

            

# 启动线程
thread = threading.Thread(target=write_to_excel)
thread.daemon = True
thread.start()


mqtt.init_app(app)
@app.get("/")
async def root():
    global message_payload
    return f"The Server Connect Broker:broker.emqx.io:1883 message:{message_payload}"

@app.get("/1")
async def start_log():
    global isLogState
    isLogState = True

@app.get("/0")
async def stop_log():
    global isLogState
    isLogState = False

@mqtt.on_connect()
def connect(client, flags, rc, properties):
    mqtt.client.subscribe(topic_smartInsole) #subscribing mqtt topic
    print("Connected: ", client, flags, rc, properties)
@mqtt.on_message()
async def message(client, topic, payload, qos, properties):
    global message_payload, result_r, result_l, message_arrived, result_lr
    message_payload = payload.decode()
    message_arrived = True
    if(topic == mqtt_topic_R):
        if(len(message_payload) > 10):
            result_r = message_payload
    elif(topic == mqtt_topic_L):
        if(len(message_payload) > 10):
            result_l = message_payload
    elif(topic == mqtt_topic_LR):
        if(len(message_payload) > 10):
            result_lr = message_arrived
    

