import math
import weakref
from fontTools.misc import transform
from fontParts.base.errors import FontPartsError
from fontParts.base.base import (
    BaseObject, TransformationMixin, dynamicProperty)
from fontParts.base import validators


class BaseGuideline(BaseObject, TransformationMixin):

    """
    A guideline object. This object is almost always
    created with :meth:`BaseGlyph.appendGuideline`.
    An orphan anchor can be created like this::

        >>> guideline = RGuideline
    """

    copyAttributes = (
        "x",
        "y",
        "angle",
        "name",
        "color"
    )

    # -------
    # Parents
    # -------

    def getParent(self):
        """
        Return the guideline's parent :class:`fontParts.base.BaseGlyph`.
        This is a backwards compatibility method.
        """
        glyph = self.glyph
        if glyph is not None:
            return glyph
        return self.font

    # Glyph

    _glyph = None

    glyph = dynamicProperty("glyph", "The guideline's parent :class:`BaseGlyph`.")

    def _get_glyph(self):
        if self._glyph is None:
            return None
        return self._glyph()

    def _set_glyph(self, glyph):
        assert self._font is None
        assert self._glyph is None
        if glyph is not None:
            glyph = weakref.ref(glyph)
        self._glyph = glyph

    # Layer

    layer = dynamicProperty("layer", "The guideline's parent :class:`BaseLayer`.")

    def _get_layer(self):
        if self._glyph is None:
            return None
        return self.glyph.layer

    # Font

    _font = None

    font = dynamicProperty("font", "The guideline's parent :class:`BaseFont`.")

    def _get_font(self):
        if self._font is not None:
            return self._font()
        elif self._glyph is not None:
            return self.glyph.font
        return None

    def _set_font(self, font):
        assert self._font is None
        assert self._glyph is None
        if font is not None:
            font = weakref.ref(font)
        self._font = font

    # --------
    # Position
    # --------

    # x

    x = dynamicProperty(
        "base_x", 
        """
        The x coordinate of the guideline.
        It must be an :ref:`type-int-float`. ::

            >>> guideline.x
            100
            >>> guideline.x = 101
        """
    )

    def _get_base_x(self):
        value = self._get_x()
        value = validators.validateX(value)
        return value

    def _set_base_x(self, value):
        value = validators.validateX(value)
        self._set_x(value)

    def _get_x(self):
        """
        This is the environment implementation of
        :attr:`BaseGuideline.x`. This must return an
        :ref:`type-int-float`.

        Subclasses must override this method.
        """
        self.raiseNotImplementedError()

    def _set_x(self, value):
        """
        This is the environment implementation of
        :attr:`BaseGuideline.x`. **value** will be
        an :ref:`type-int-float`.

        Subclasses must override this method.
        """
        self.raiseNotImplementedError()

    # y

    y = dynamicProperty(
        "base_y", 
        """
        The y coordinate of the guideline.
        It must be an :ref:`type-int-float`. ::

            >>> guideline.y
            100
            >>> guideline.y = 101
        """
    )

    def _get_base_y(self):
        value = self._get_y()
        value = validators.validateY(value)
        return value

    def _set_base_y(self, value):
        value = validators.validateY(value)
        self._set_y(value)

    def _get_y(self):
        """
        This is the environment implementation of
        :attr:`BaseGuideline.y`. This must return an
        :ref:`type-int-float`.

        Subclasses must override this method.
        """
        self.raiseNotImplementedError()

    def _set_y(self, value):
        """
        This is the environment implementation of
        :attr:`BaseGuideline.y`. **value** will be
        an :ref:`type-int-float`.

        Subclasses must override this method.
        """
        self.raiseNotImplementedError()

    # angle

    angle = dynamicProperty(
        "base_angle", 
        """
        The angle of the guideline.
        It must be an :ref:`type-angle`.
        Please check how :meth:`fontParts.base.validators.validateGuidelineAngle`
        handles the angle. ::

            >>> guideline.angle
            45.0
            >>> guideline.angle = 90
        """
    )

    def _get_base_angle(self):
        value = self._get_angle()
        value = validators.validateGuidelineAngle(value)
        return value

    def _set_base_angle(self, value):
        value = validators.validateGuidelineAngle(value)
        self._set_angle(value)

    def _get_angle(self):
        """
        This is the environment implementation of
        :attr:`BaseGuideline.angle`. This must return an
        :ref:`type-angle`.

        Subclasses must override this method.
        """
        self.raiseNotImplementedError()

    def _set_angle(self, value):
        """
        This is the environment implementation of
        :attr:`BaseGuideline.angle`. **value** will be
        an :ref:`type-angle`. 

        Subclasses must override this method.
        """
        self.raiseNotImplementedError()

    # --------------
    # Identification
    # --------------

    # index

    index = dynamicProperty(
        "base_index", 
        """
        The index of the guideline within the ordered
        list of the parent glyph's guidelines. This
        attribute is read only. ::

            >>> guideline.index
            0
        """
    )

    def _get_base_index(self):
        value = self._get_index()
        value = validators.validateIndex(value)
        return value

    def _get_index(self):
        """
        Get the guideline's index.
        This must return an ``int``.

        Subclasses may override this method.
        """
        glyph = self.glyph
        if glyph is not None:
            parent = glyph
        else:
            parent = self.font
        if parent is None:
            return None
        return parent.guidelines.index(self)

    # name

    name = dynamicProperty(
        "base_name", 
        """
        The name of the guideline. This will be a
        :ref:`type-string` or ``None``.

            >>> guideline.name
            'my guideline'
            >>> guideline.name = None
        """
    )

    def _get_base_name(self):
        value = self._get_name()
        if value is not None:
            value = validators.validateGuidelineName(value)
        return value

    def _set_base_name(self, value):
        if value is not None:
            value = validators.validateGuidelineName(value)
        self._set_value(value)

    def _get_name(self):
        """
        Subclasses must override this method.
        """
        self.raiseNotImplementedError()

    def _set_name(self, value):
        """
        Subclasses must override this method.
        """
        self.raiseNotImplementedError()

    # identifier

    identifier = dynamicProperty("base_identifier", "The unique identifier for the guideline.")

    def _get_base_identifier(self):
        value = self._get_identifier()
        value = validators.validateIdentifier(value)
        return value

    def _get_identifier(self):
        """
        Subclasses must override this method.
        """
        self.raiseNotImplementedError()

    # color

    color = dynamicProperty("base_color", "The guideline's color.")

    def _get_base_color(self):
        value = self._get_color()
        if value is not None:
            value = validators.validateColor(value)
            value = Color(value)
        return value

    def _set_base_color(self, value):
        if value is not None:
            value = validators.validateColor(value)
        self._set_color(value)

    def _get_color(self):
        """
        Get the color of the guideline.
        This must return a color tuple or None.

        Subclasses must override this method.
        """
        self.raiseNotImplementedError()

    def _set_color(self, value):
        """
        Set the color of the guideline.
        This will be a color tuple or None.

        Subclasses must override this method.
        """
        self.raiseNotImplementedError()

    # --------------
    # Transformation
    # --------------

    def _transformBy(self, matrix, origin=None, originOffset=None, **kwargs):
        """
        Subclasses may override this method.
        """
        t = transform.Transform(*matrix)
        # coordinates
        x, y = t.transformPoint((self.x, self.y))
        self.x = x
        self.y = y
        if originOffset != (0, 0):
            self.moveBy(originOffset)
        # angle
        angle = math.radians(self.angle)
        dx = math.cos(angle)
        dy = math.sin(angle)
        tdx, tdy = t.transformPoint((dx, dy))
        ta = math.atan2(tdy, tdx)
        self.angle = math.degrees(ta)

    # -------------
    # Normalization
    # -------------

    def round(self):
        """
        Round coordinates.
        """
        self._round()

    def _round(self, **kwargs):
        """
        Subclasses may override this method.
        """
        self.x = int(round(self.x))
        self.y = int(round(self.y))
