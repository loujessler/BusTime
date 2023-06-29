import os

from aiohttp import web


async def handle(request):
    name = request.match_info.get('name', "data/routes")
    print(os.path.join('data', 'routes', name))
    with open(os.path.join('data', 'routes', name), 'rb') as file:
        return web.Response(body=file, content_type='text/html')


async def home(request):
    return web.Response(text="Server is running")
