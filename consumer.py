import paho.mqtt.client as mqtt
import json
import ssl
from influxdb import InfluxDBClient

# ==========================================
# GANTI INI DENGAN DATA CLOUDAMQP ANDA
MQTT_SERVER = "kingfisher.lmq.cloudamqp.com"  # Hostname Anda
MQTT_PORT = 8883
MQTT_USER = "aqimgrci:aqimgrci"  # user:vhost
MQTT_PASS = "Sc4R0pLH85N05JYqDCwxFeNNkOh2FiJK"  # GANTI!
MQTT_TOPIC = "energy/telemetry"
# ==========================================

# ==========================================
# KONFIGURASI INFLUXDB CLOUD (BARU!)
INFLUX_URL = "https://ap-southeast-2-1.aws.cloud2.influxdata.com"  # Ganti sesuai region Anda
INFLUX_TOKEN = "TOKEN_ANDA_DISINI"  # GANTI! (All Access Token tadi)
INFLUX_ORG = "digitalskola"         # GANTI! (Organization name)
INFLUX_BUCKET = "energydb"          # Nama bucket
# ==========================================

# Setup InfluxDB Cloud Client (v2 API)
#influx_client = InfluxDBClient(url=INFLUX_URL, token=INFLUX_TOKEN, org=INFLUX_ORG)
#write_api = influx_client.write_api(write_options=SYNCHRONOUS)

# InfluxDB di localhost (dalam VM)
influx_client = InfluxDBClient(host='localhost', port=8086, database='energydb')

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("✓ Connected to CloudAMQP MQTT")
        client.subscribe(MQTT_TOPIC)
        print(f"✓ Subscribed to: {MQTT_TOPIC}")
    else:
        print(f"✗ Connection failed: {rc}")

def on_message(client, userdata, msg):
    try:
        data = json.loads(msg.payload.decode())
        
        # Validasi 7 field PDF
        required = ['device_id', 'voltage', 'current', 'power', 'energy', 'power_factor', 'frequency']
        if not all(field in data for field in required):
            print(f"⚠️ Missing fields: {data}")
            return
        
        json_body = [{
            "measurement": "energy_telemetry",
            "tags": {"device_id": data['device_id']},
            "fields": {
                "voltage": float(data['voltage']),
                "current": float(data['current']),
                "power": float(data['power']),
                "energy": float(data['energy']),
                "power_factor": float(data['power_factor']),
                "frequency": float(data['frequency'])
            }
        }]
        
        influx_client.write_points(json_body)
        print(f"✓ {data['device_id']}: {data['power']}W | {data['energy']}kWh")
        
    except Exception as e:
        print(f"✗ Error: {e}")

def main():
    try:
        influx_client.create_database('energydb')
    except:
        influx_client.switch_database('energydb')
    
    client = mqtt.Client(client_id="consumer-vm-001")
    client.on_connect = on_connect
    client.on_message = on_message
    client.username_pw_set(MQTT_USER, MQTT_PASS)
    client.tls_set(cert_reqs=ssl.CERT_NONE)
    client.tls_insecure_set(True)
    
    print(f"Connecting to {MQTT_SERVER}:{MQTT_PORT}...")
    client.connect(MQTT_SERVER, MQTT_PORT, 60)
    print("Consumer running... (Ctrl+C to stop)")
    client.loop_forever()

if __name__ == "__main__":
    main()