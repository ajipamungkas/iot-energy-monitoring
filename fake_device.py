import paho.mqtt.client as mqtt
import json
import ssl
import time
import random

# ==========================================
# KONFIGURASI SAMA DENGAN CONSUMER
MQTT_SERVER = "kingfisher.lmq.cloudamqp.com"  # Hostname Anda
MQTT_PORT = 8883
MQTT_USER = "aqimgrci:aqimgrci"  # user:vhost
MQTT_PASS = "Sc4R0pLH85N05JYqDCwxFeNNkOh2FiJK"  # GANTI!
MQTT_TOPIC = "energy/telemetry"
# ==========================================

total_energy = 15.6  # kWh - accumulated

def generate():
    global total_energy
    
    voltage = round(random.uniform(218.0, 242.0), 1)
    current = round(random.uniform(1.0, 8.0), 1)
    power = round(voltage * current, 1)
    power_factor = round(random.uniform(0.85, 0.98), 2)
    frequency = round(random.uniform(49.8, 50.2), 1)
    
    # Accumulate
    total_energy += (power / 1000.0) * (5.0 / 3600.0)
    
    return {
        "device_id": "meter-001",
        "voltage": voltage,
        "current": current,
        "power": power,
        "energy": round(total_energy, 2),
        "power_factor": power_factor,
        "frequency": frequency
    }

def main():
    client = mqtt.Client(client_id="fake-device-001")
    client.username_pw_set(MQTT_USER, MQTT_PASS)
    client.tls_set(cert_reqs=ssl.CERT_NONE)
    client.tls_insecure_set(True)
    
    print(f"Connecting to {MQTT_SERVER}...")
    client.connect(MQTT_SERVER, MQTT_PORT, 60)
    client.loop_start()
    
    print("Device running... (Ctrl+C to stop)")
    
    try:
        while True:
            data = generate()
            payload = json.dumps(data)
            client.publish(MQTT_TOPIC, payload)
            print(f"[TX] {payload}")
            time.sleep(5)
    except KeyboardInterrupt:
        print("\nStopped")
        client.loop_stop()

if __name__ == "__main__":
    main()