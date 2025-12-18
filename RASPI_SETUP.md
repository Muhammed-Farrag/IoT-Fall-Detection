# Raspberry Pi Camera Setup Guide

Complete guide to set up your Raspberry Pi as a camera server for the NovaCare Fall Detection System.

---

## Prerequisites

- Raspberry Pi (3B+, 4, or 5 recommended)
- Raspberry Pi Camera Module (v1, v2, or v3)
- MicroSD card with Raspberry Pi OS
- Network connection (Wi-Fi or Ethernet)
- Your Windows laptop on the same network

---

## Step 1: Enable Camera on Raspberry Pi

1. **Connect the camera module** to the CSI port on your Pi (the ribbon cable connector near the HDMI port)

2. **Open terminal** and run:

   ```bash
   sudo raspi-config
   ```

3. Navigate to: **Interface Options** → **Camera** → **Enable**

4. **Reboot** the Pi:
   ```bash
   sudo reboot
   ```

---

## Step 2: Install Dependencies on Pi

SSH into your Pi or open terminal and run:

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python packages
sudo apt install python3-pip python3-opencv -y

# Install picamera2 (for Raspberry Pi OS Bullseye/Bookworm)
sudo apt install python3-picamera2 -y

# Alternative: If using legacy camera stack
# sudo apt install python3-picamera -y
```

---

## Step 3: Copy Camera Server to Pi

**Option A: Using SCP (from your Windows laptop)**

Open PowerShell and run:

```powershell
scp c:\Users\Pc\IoT-Fall-Detection\raspi_camera_server.py pi@raspberrypi.local:~/
```

**Option B: Create file directly on Pi**

SSH into Pi and create the file:

```bash
nano ~/raspi_camera_server.py
```

Then paste the contents of `raspi_camera_server.py`.

---

## Step 4: Find Your Pi's IP Address

On the Raspberry Pi, run:

```bash
hostname -I
```

Note the IP address (e.g., `192.168.1.100`)

---

## Step 5: Start the Camera Server

On the Raspberry Pi:

```bash
cd ~
python3 raspi_camera_server.py
```

You should see:

```
╔═══════════════════════════════════════════════════════════╗
║     📹 Raspberry Pi Camera Server                         ║
║     ──────────────────────────────────────────────────    ║
║     Starting camera stream on port 8000...                ║
╚═══════════════════════════════════════════════════════════╝

📷 Camera started (PiCamera2 mode)
🌐 Stream available at: http://0.0.0.0:8000/video_feed
```

---

## Step 6: Configure Windows App

On your Windows laptop, create the `.env` file:

1. **Copy the example file**:

   ```powershell
   cd c:\Users\Pc\IoT-Fall-Detection
   copy .env.example .env
   ```

2. **Edit `.env`** with your Pi's IP address:

   ```env
   # Set to your Pi's IP address
   RASPI_STREAM_URL=http://192.168.1.100:8000/video_feed

   # Enable Pi camera mode
   USE_PI_CAMERA=true

   # Optional: Email settings for alerts
   SMTP_SERVER=smtp.gmail.com
   SMTP_PORT=587
   SMTP_USERNAME=your-email@gmail.com
   SMTP_PASSWORD=your-app-password
   ALERT_EMAIL_TO=emergency@example.com
   ```

---

## Step 7: Install Python Dependencies on Windows

Open PowerShell:

```powershell
cd c:\Users\Pc\IoT-Fall-Detection

# Activate virtual environment (if using venv)
.\venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

---

## Step 8: Run the System

1. **On Raspberry Pi** (keep this running):

   ```bash
   python3 raspi_camera_server.py
   ```

2. **On Windows laptop**:

   ```powershell
   cd c:\Users\Pc\IoT-Fall-Detection
   python run.py
   ```

3. **Open browser**: http://localhost:5000/dashboard

---

## Step 9: Test the System

1. Click **"Live Stream"** in the dashboard sidebar
2. You should see the camera feed from your Pi
3. **Test fall detection**:

   - Stand in front of the camera
   - Simulate a fall (quickly lower yourself)
   - Check if alert appears on dashboard

4. **Test bending** (should NOT trigger alert):
   - Slowly bend down as if picking something up
   - System should ignore this movement

---

## Troubleshooting

### Camera not detected on Pi

```bash
# Check if camera is enabled
vcgencmd get_camera

# Should show: supported=1 detected=1
```

### Can't connect from Windows

```bash
# On Pi, check if server is running
curl http://localhost:8000/health

# Check firewall
sudo ufw allow 8000
```

### Video lag

- Reduce resolution in `raspi_camera_server.py`
- Use Ethernet instead of Wi-Fi
- Move Pi closer to router

### OpenCV fallback warning

If you see "picamera2 not available", the legacy OpenCV fallback is being used. Install picamera2:

```bash
sudo apt install python3-picamera2 libcamera-apps -y
```

---

## Auto-Start on Boot (Optional)

Create a systemd service:

```bash
sudo nano /etc/systemd/system/camera-server.service
```

Add:

```ini
[Unit]
Description=NovaCare Camera Server
After=network.target

[Service]
ExecStart=/usr/bin/python3 /home/pi/raspi_camera_server.py
WorkingDirectory=/home/pi
User=pi
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable and start:

```bash
sudo systemctl enable camera-server
sudo systemctl start camera-server
```

---

## Architecture

```
┌─────────────────┐         ┌──────────────────────┐
│  Raspberry Pi   │         │   Windows Laptop     │
│                 │         │                      │
│  ┌───────────┐  │  HTTP   │  ┌────────────────┐  │
│  │  Camera   │──┼─────────┼──│  Flask App     │  │
│  │  Server   │  │  :8000  │  │  (AI + Dashboard)│ │
│  └───────────┘  │         │  └────────────────┘  │
│                 │         │          │           │
│                 │         │          ▼           │
│                 │         │  ┌────────────────┐  │
│                 │         │  │  Browser UI    │  │
│                 │         │  │  :5000         │  │
│                 │         │  └────────────────┘  │
└─────────────────┘         └──────────────────────┘
```

The camera server runs on the Pi, streaming video over HTTP. The Windows app fetches frames, processes them with AI, and serves the dashboard.
