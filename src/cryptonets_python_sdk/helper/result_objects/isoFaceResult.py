class ISOFaceResult:
    def __init__(
        self,
        iso_image_width=None,
        iso_image_height=None,
        iso_image_channels=None,
        confidence=None,
        image=None,
        status=-1,
        message="",
    ):
        self._iso_image_width = iso_image_width
        self._iso_image_height = iso_image_height
        self._iso_image_channels = iso_image_channels
        self._confidence = confidence
        self._image = image
        self._status = status
        self._message = message

    @property
    def iso_image_width(self) -> int:
        """
        Returns the width of the Image object
        """
        return self._iso_image_width

    @property
    def iso_image_height(self) -> str:
        """
        Returns the height of the Image object
        """
        return self._iso_image_height

    @property
    def iso_image_channels(self) -> str:
        """
        Returns the number of channels present in the image
        """
        return self._iso_image_channels

    @property
    def confidence(self) -> str:
        """
        Returns the confidence score for the converted ISO image
        """
        return self._confidence

    @property
    def image(self) -> str:
        """
        Returns the PIL Image object face ISO Specification converted
        """
        return self._image

    @property
    def status(self) -> int:
        """
        Returns the status of the operation
        """
        return self._status

    @property
    def message(self) -> str:
        """
        Returns the message of the operation
        """
        return self._message

    @iso_image_width.setter
    def iso_image_width(self, value):
        self._iso_image_width = value

    @iso_image_width.setter
    def iso_image_width(self, value):
        self._iso_image_width = value

    @iso_image_height.setter
    def iso_image_height(self, value):
        self._iso_image_height = value

    @iso_image_channels.setter
    def iso_image_channels(self, value):
        self._iso_image_channels = value

    @status.setter
    def status(self, value):
        self._status = value

    @message.setter
    def message(self, value):
        self._message = value
