# Flood Watcher

This project is an experiment using the `tago.io`, `openstreetmap` and `open-elevation` APIs to generate iso-elevation polygons around sensors placed in the Madison, WI area. Currently this code focuses on the He_003 (E. Mifflin & Blount St.) sensor.

* `tago.io` is used to query the device's location
* `open-elevation` is used to query points in a grid surrounding the device for elevation data. Elevation data is at 1m resolution, over 30m^2 regions.

The code is currently slow, and bare-bones. Faster querying of the `open-elevation` API is possible using bundled POST commands. This is TBD

Thanks to Bill Selbig who came up with the idea.