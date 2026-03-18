Berikut **README.md lengkap** siap copy-paste:

```markdown
# IoT Energy Monitoring Pipeline - DigitalSkola

Project ini mengimplementasikan IoT pipeline untuk monitoring parameter listrik (voltage, current, power, energy, power factor, frequency) sesuai dengan spesifikasi tugas DigitalSkola Cloud Engineering.

## 🏗️ Architecture
```
![arsitektur - Copy](https://github.com/user-attachments/assets/45a4dee8-9eb0-4371-b752-0bd525099601)




**Komponen:**
- **Fake Device**: Simulator meter listrik menggunakan Python + Paho-MQTT
- **Message Broker**: CloudAMQP/LavinMQ (Cloud SaaS) dengan protokol MQTT over SSL
- **Ingestion Service**: Python consumer yang subscribe topic dan write ke database
- **Time-Series DB**: InfluxDB 1.8 running di Docker lokal
- **Dashboard**: Grafana untuk visualisasi real-time parameter electrical

## 📋 Prerequisites

- Python 3.9+
- Docker & Docker Compose
- Akun CloudAMQP/LavinMQ (free tier)
- OS: Linux/Windows (VM atau Native dengan VirtualBox)

## 🚀 Quick Start

### 1. Clone & Setup
```bash
git clone https://github.com/ajipamungkas/iot-energy-monitoring.git
cd iot-energy-monitoring
```

### 2. Konfigurasi Environment
Edit `consumer.py` dan `fake_device.py` dengan kredensial CloudAMQP Anda:
```python
MQTT_SERVER = "kingfisher.lmq.cloudamqp.com"  # Ganti dengan host Anda
MQTT_PORT = 8883
MQTT_USER = "aqimgrci:aqimgrci"        # Format: user:vhost
MQTT_PASS = "YOUR_PASSWORD_HERE"       # Ganti password asli
MQTT_TOPIC = "energy/telemetry"
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Jalankan Database (InfluxDB + Grafana)
```bash
docker-compose up -d
```
Akses:
- Grafana: http://localhost:3000 (admin/admin123)
- InfluxDB: http://localhost:8086

### 5. Jalankan Consumer (Terminal 1)
```bash
python3 consumer.py
```
Output yang diharapkan:
```
✓ Connected to CloudAMQP MQTT
✓ Subscribed to: energy/telemetry
Consumer running...
```

### 6. Jalankan Device Simulator (Terminal 2)
```bash
python3 fake_device.py
```
Output yang diharapkan:
```
[TX] {"device_id": "meter-001", "voltage": 230.5, "current": 4.2, "power": 967.3, ...}
```

## 📊 Data Format (Sesuai Tugas PDF)

Device mengirimkan telemetry dengan 7 field sesuai spesifikasi:

```json
{
  "device_id": "meter-001",
  "voltage": 230.5,
  "current": 4.2,
  "power": 967.3,
  "energy": 15.61,
  "power_factor": 0.94, l
  "frequency": 50.0
}
```

**Catatan Penting:**
- Field `energy` adalah **accumulated energy usage** (kWh), bukan random. Nilai bertambah sedikit setiap interval (5 detik) sesuai dengan rumus: `Energy = Power(kW) × Time(hours)`
- Power dihitung dengan rumus `P = V × I` sesuai AC electrical systems di dokumen tugas
- Semua parameter realistis untuk standar PLN (Voltage 218-242V, Frequency 49.8-50.2Hz)

## 📈 Grafana Dashboard

Dashboard menampilkan 4 panel visualisasi real-time:

1. **Voltage Monitoring**: Tegangan listrik (220-240V)
2. **Power Consumption**: Daya aktif dalam Watt (fluctuatif sesuai beban)
3. **Accumulated Energy**: Energi terakumulasi dalam kWh (grafik naik terus/monoton)
4. **Current Load**: Arus listrik (A)

**Query Example (InfluxQL):**
```sql
-- Power Consumption
SELECT mean("power") FROM "energy_telemetry" WHERE $timeFilter GROUP BY time($__interval)

-- Accumulated Energy (penting: last, bukan mean)
SELECT last("energy") FROM "energy_telemetry" WHERE $timeFilter GROUP BY time($__interval)
```

## 📸 Screenshots

Lihat folder `docs/` untuk bukti sistem berjalan:
- `screenshot-broker.png`: CloudAMQP management console
- `screenshot-consumer.png`: Terminal consumer menerima data
- `screenshot-device.png`: Terminal fake device mengirim JSON
- `screenshot-influxdb.png`: Query result di InfluxDB CLI
- `screenshot-grafana.png`: Dashboard real-time lengkap 4 panel
![run consumer py](https://github.com/user-attachments/assets/7d03107b-91a3-4631-8c68-c5c62eabc1e7)

![GRAFANA](https://github.com/user-attachments/assets/c44dfeed-1b04-4ea2-8f88-f44cb9d6f112)

  

## 🔧 Troubleshooting

| Problem | Solution |
|---------|----------|
| MQTT Connection Timeout | Cek firewall VM, pastikan port 8883 terbuka |
| Grafana 404 ke InfluxDB | Gunakan `http://influxdb:8086` (nama container), bukan IP VM |
| No data in Grafana | Pastikan time range "Last 5 minutes" dan refresh interval 5s |
| SSL Certificate Error | Normal untuk demo, gunakan `tls_insecure_set(True)` |

## 📝 Learning Objectives (Sesuai Tugas)

✅ Understanding how energy monitoring devices publish telemetry  
✅ How messaging systems (MQTT/AMQP) handle streaming device data  
✅ How ingestion services process telemetry streams  
✅ How electrical measurements are stored in time-series database  
✅ How dashboards visualize real-time energy data  
✅ Decoupled communication architecture (device tidak langsung ke DB)

## 👤 Author
[Setya aji Pamungkas] - [Batch 3]  
DigitalSkola Cloud Engineering

**Jangan lupa juga buat file `requirements.txt`:**
```txt
paho-mqtt>=1.6.0
influxdb>=5.3.1
pyopenssl>=23.0.0
```


