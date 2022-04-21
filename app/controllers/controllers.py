from blacksheep import Request, Response
from blacksheep.server.controllers import get, post, Controller
from blacksheep.server.responses import json, redirect

from app.helpers.basecontroller import BaseController


class TourController(BaseController):
    @get('/tour')
    @post('/tour')
    async def tour_list(self, request: Request):
        print(request)
        return json({"message": "tour list"})
