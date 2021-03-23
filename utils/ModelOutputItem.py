# -*- coding: utf-8 -*-
# /usr/bin/python3


class ModelOutputItem:
    __slots__ = '_box', '_confidence', '_cls', '_label', '_cls_dict'

    def __init__(self, *args, **kwargs):
        for k, v in kwargs.items():
            self.__setattr__(k, v)
        self._label = self._cls_dict[self._cls]

    def __str__(self):
        return 'box={%s}\tconfidence={%s}\tcls={%s}\tlabel={%s}\t' % \
               (self._box, self._confidence, self._cls, self._label)

    def get_box(self):
        return self._box

    def get_label(self):
        return self._label

    def get_confidence(self):
        return self._confidence

    def get_cls(self):
        return self._cls
