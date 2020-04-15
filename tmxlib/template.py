"""Tiled template"""

from __future__ import division

import itertools

from tmxlib import helpers, fileio, tileset, mapobject


class TemplateList(helpers.NamedElementList):
    """A list of templates.

    Allows indexing by source.
    """

    def __init__(self, map, lst=None):
        self.map = map
        super(TemplateList, self).__init__(lst)


class Template(fileio.ReadWriteBase):
    """A template definition

    Templates are always externally defined, and may be shared between maps.

    init arguments, which become attributes:

        .. attribute:: source

            The filename of the template file.
    """
    _rw_obj_type = 'template'

    # XXX: Fully implement, test, and document base_path:
    #   This should be used for saving, so that relative paths work as
    #   correctly as they can.
    #   And it's not just here...
    def __init__(self):
        self.object = None
        self.tileset = None

    def generate_draw_commands(self):
        for cmd in self.object.generate_draw_commands():
            yield cmd

    def to_dict(self):
        """Export to a dict compatible with Tiled's JSON plugin

        You can use e.g. a JSON or YAML library to write such a dict to a file.
        """
        d = dict(
            object=self.object.to_dict(),
        )

        if self.tileset:
            d['tileset'] = self.tileset.to_dict()

        return d

    @helpers.from_dict_method
    def from_dict(cls, dct, map, base_path=None):
        """Import from a dict compatible with Tiled's JSON plugin

        Use e.g. a JSON or YAML library to read such a dict from a file.

        :param dct: Dictionary with data
        :param base_path: Base path of the file, for loading linked resources
        """
        if dct.pop('version', 1) != 1:
            raise ValueError('tmxlib only supports Tiled JSON version 1')
        self = cls()
        if base_path:
            self.base_path = base_path

        self.tileset = tileset.Tileset.from_dict(dct.pop('tileset'), base_path)
        self.object = mapobject.MapObject.from_dict(dct.pop('object'), map)
        return self
