## 1 环境安装
### 1.1 安装TensorRT、PyCUDA
```bash
git clone https://github.com/jkjung-avt/tensorrt_demos
```

```bash
cd  tensorrt_demos/ssd
```

```bash
./install.sh
```

```bash
./build_engines.sh
```

将`tensorrt_demos`中的utils\plugins的libyolo_layer复制到GIMS文件夹中的相同位置，
替换掉这个文件。

### 1.2 安装GStreamer
```bash
sudo apt-get install python3-opencv
sudo apt-get install python3-gi
sudo apt install python3 python3-gst-1.0 \
    gstreamer1.0-plugins-base \
    gir1.2-gst-rtsp-server-1.0
```
### 1.3 其他环境
PyQt5