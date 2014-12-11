#!/usr/bin/python
# -*- coding: utf-8 -*-

import appier
import appier_extras

class DigitalriverApp(appier.WebApp):

    def __init__(self):
        appier.WebApp.__init__(
            self,
            name = "digitalriver",
            parts = (
                appier_extras.AdminPart,
            )
        )

    def start(self):
        appier.WebApp.start(self)
        self.scheduler.start()

if __name__ == "__main__":
    app = DigitalriverApp()
    app.serve()
