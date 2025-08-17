# EasyMocapLite

EasyMocapLite is a lightweight Python toolkit for real-time human motion capture using MediaPipe, with easy export to BVH and live streaming to Blender via UDP.

## Features

- Capture human motion from webcam using [MediaPipe](https://google.github.io/mediapipe/).
- Map MediaPipe 33 landmarks to a basic skeleton (Hips, Spine, Head, Arms, Legs).
- Record joint positions at ~30fps, save to CSV.
- Export CSV motion to BVH (importable in Blender 2.83+).
- Stream motion live, send joint positions over UDP as JSON for Blender to receive.
- Blender add-on creates empties for joints and updates them in real time.

## Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/EasyMocapLite.git
   cd EasyMocapLite
   ```

2. **Install Python requirements**
   ```bash
   python3.10 -m pip install -r requirements.txt
   ```

## Usage

### 1. Record a motion session

- Run the recording example:
  ```bash
  python examples/record_motion.py
  ```
- Move in front of your webcam. Press `q` to finish.
- Output: `output_motion.csv`

### 2. Export to BVH

- Convert your CSV to BVH:
  ```bash
  python examples/export_bvh.py
  ```
- Output: `output_motion.bvh`

### 3. Import BVH into Blender

- Open Blender 2.83+
- `File > Import > Motion Capture (.bvh)` and select `output_motion.bvh`

### 4. Live motion streaming

- Start live streaming from Python:
  ```bash
  python examples/live_stream.py
  ```

- In Blender:
  - Copy `blender_addon/` to your Blender `addons` folder.
  - Enable the add-on: `Edit > Preferences > Add-ons > EasyMocapLite Live Receiver`.
  - Press `F3`, search for "Start EasyMocapLite UDP Listener", run it.
  - Empties named `EasyMocap_<Joint>` will appear and move in real time.

## How it works

- **MediaPipe** detects 33 pose landmarks.
- Landmarks are mapped to a simple skeleton.
- Joint positions are recorded or streamed live.
- BVH export assumes a simple hierarchy and writes Blender-compatible BVH.

## Requirements

- Python 3.10
- mediapipe
- opencv-python
- numpy
- Blender 2.83+ (for add-on/live streaming)

## License

MIT License. See [LICENSE](LICENSE).
