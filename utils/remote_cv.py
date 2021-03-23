import gi

gi.require_version('Gst', '1.0')
gi.require_version('GstRtspServer', '1.0')
from gi.repository import Gst, GstRtspServer

from utils.DetectTensorRT import global_image

_width = '1280'
_height = '720'


class SensorFactory(GstRtspServer.RTSPMediaFactory):
    def __init__(self, **properties):
        super(SensorFactory, self).__init__(**properties)
        self._number_frames = 0
        self._fps = 30
        self._duration = 1 / self._fps * Gst.SECOND  # duration of a frame in nanoseconds
        self._launch_string = 'appsrc name=source is-live=true block=true format=GST_FORMAT_TIME ' \
                              'caps=video/x-raw,format=BGR,width=' + _width + ',height=' + _height + \
                              ',framerate={}/1 ! videoconvert ! video/x-raw,format=I420 ' \
                              '! x264enc speed-preset=ultrafast tune=zerolatency ' \
                              '! rtph264pay config-interval=1 name=pay0 pt=96'.format(self._fps)

    def on_need_data(self, src, length):
        """
        If any image request.
        :param src: source
        :param length: length
        :return: None
        """
        data = global_image.tostring()
        buf = Gst.Buffer.new_allocate(None, len(data), None)
        buf.fill(0, data)
        buf._duration = self._duration
        timestamp = self._number_frames * self._duration
        buf.pts = buf.dts = int(timestamp)
        buf.offset = timestamp
        self._number_frames += 1
        retval = src.emit('push-buffer', buf)

        if retval != Gst.FlowReturn.OK:
            print(retval)

    def do_create_element(self, url):
        """
        Create GStreamer element.
        :param url: url
        :return: None
        """
        return Gst.parse_launch(self._launch_string)

    def do_configure(self, rtsp_media):
        """
        ?
        :param rtsp_media: ?
        :return: None
        """
        self._number_frames = 0
        appsrc = rtsp_media.get_element().get_child_by_name('source')
        appsrc.connect('need-data', self.on_need_data)


class GstServer(GstRtspServer.RTSPServer):
    def __init__(self, **properties):
        super(GstServer, self).__init__(**properties)
        self._set_address = '0.0.0.0'
        self._set_service = '8554'
        self._factory = SensorFactory()
        self._factory.set_shared(True)
        self.get_mount_points().add_factory("/test", self._factory)
        self.attach(None)
