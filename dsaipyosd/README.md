Trying to get OpenSeadragon and the DSA and ipyleaflet working together

Useful links:
https://gist.github.com/manthey/a66f69ae84dc59bbd54c2fbbb1c8844f

_repr_html_ is a fantastic way to add an interactive representation style for objects in Jupyuter and we could easily expose a slippy-maps style viewer that fetches tiles from a large-image source.

For example, I implemented this in localtileserver: https://localtileserver.banesullivan.com/user-guide/index.html#user-guide

I'd like to wrap up the rasterio source and consolidate a new "GeoBaseTileSource", then think about implementing this as:

_repr_html_ on the base TileSource class that shows an slippy maps style image viewer (non-geospatially referenced)
_repr_html_ on the base "GeoBaseTileSource" that has a geospatial reference
Implementation
We need to launch a webserver to host the endpoints for our JS-based viewer to fetch tiles from. Launching the server isn't too bad and as I've shared in plenty of places, we can do this easily with server-thread and a simple wsgi/asgi app.

https://localtileserver.banesullivan.com/user-guide/compare.html

Here is a minimal, yet fairly robust example:

import io

from fastapi import FastAPI
from server_thread import ServerThread
from starlette.responses import StreamingResponse

def get_server(src):

    app = FastAPI()

    @app.get("/metadata")
    async def get_metadata():
        return src.getMetadata()

    @app.get("/tile/{z}/{x}/{y}.png")
    async def get_tile(z: int, x: int, y: int):
        tile_binary = src.getTile(x, y, z)
        return StreamingResponse(io.BytesIO(tile_binary), media_type="image/png")

    # Launch app in a background thread
    server = ServerThread(app)

    return server

With usage looking like:

import large_image
from tileserver import get_server
from ipyleaflet import Map, TileLayer

source = large_image.open('path/to/raster.tif')

server = get_server(source)

t = TileLayer(
url=f"http://{server.host}:{server.port}/tile/{{z}}/{{x}}/{{y}}.png",
attribution="Served with large-image",
)

m = Map()
m.add_layer(t)
m
Complications
An issue arises from gaining access to that webserver when running on managed, deployed environments (think MyBinder, university JupyterLab deployments, Sagemaker, etc.), we'll likely need to rely on jupyter-server-proxy to proxy the port so that the user's web browser can access this. Thing is, it has to be configured slightly differently in just about every managed environment -- a maintenance and support burden we're facing on PyVista with its webserver-based Jupyter viewer.

Though, a good chunk of the implementation to support most platforms in a standard way can be taken from localtileserver: https://github.com/banesullivan/localtileserver/blob/main/localtileserver/configure.py

Which viewer do we use?
We could custom bundle a viewer based on GeoJS, CesiumJS, LeafletJS, etc and this wouldn't require any additional dependencies. However, this would be somewhat of "oh neat,... but I can't do anything with that" situation. I think it would behoove us to add an extra_requires section for Jupyter that would leverage ipyleaflet for creating these viewers in Jupyter. This would enable users to add annotations, add additional tile sources, and customize to their heart's desire.

Using ipyleaflet will require nailing down the non-geospatial case as it's still a bit weird: https://localtileserver.banesullivan.com/user-guide/non-geo.html
