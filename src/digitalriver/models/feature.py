#!/usr/bin/python
# -*- coding: utf-8 -*-

import appier

from . import base

class Feature(base.DRBase):

    url = appier.field(
        index = True,
        default = True
    )

    name = appier.field(
        index = True
    )

    data = appier.field(
        type = dict
    )

    config = appier.field(
        type = list
    )

    @classmethod
    def validate(cls):
        return super(Feature, cls).validate() + [
            appier.not_null("url"),
            appier.not_empty("url"),
            appier.is_url("url"),

            appier.not_null("name"),
            appier.not_empty("name")
        ]
