from reportlab.platypus import Image

class HyperlinkedImage(Image, object):
    """Image with a hyperlink, adopted from http://stackoverflow.com/a/26294527/304209."""

    def __init__(self, filename, hyperlink=None, width=None, height=None, kind='direct',
                 mask='auto', lazy=1, hAlign='CENTER'):
        """The only variable added to __init__() is hyperlink.

        It defaults to None for the if statement used later.
        """
        super(HyperlinkedImage, self).__init__(filename, width, height, kind, mask, lazy,
                                               hAlign=hAlign)
        self.hyperlink = hyperlink

    def drawOn(self, canvas, x, y, _sW=0):
        if self.hyperlink:  # If a hyperlink is given, create a canvas.linkURL()
            # This is basically adjusting the x coordinate according to the alignment
            # given to the flowable (RIGHT, LEFT, CENTER)
            x1 = self._hAlignAdjust(x, _sW)
            y1 = y
            x2 = x1 + self._width
            y2 = y1 + self._height
            canvas.linkURL(url=self.hyperlink, rect=(x1, y1, x2, y2), thickness=0, relative=1)
        super(HyperlinkedImage, self).drawOn(canvas, x, y, _sW)
