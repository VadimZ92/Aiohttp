import json
from db import Advertising, Session, engine, Base
from sqlalchemy.exc import IntegrityError
from aiohttp import web
from typing import Type


app = web.Application()

ERROR_TYPE = Type[web.HTTPUnauthorized] or Type[web.HTTPForbidden] or Type[web.HTTPNotFound]

def raise_http_error(error_class: ERROR_TYPE, message: str or dict):
    raise error_class(
        text=json.dumps({"status": "error", "description": message}),
        content_type="application/json",
    )


async def orm_context(app: web.Application):
    print("Start")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()
    print("Stop")


async def get_advertising(advertising_id: int, session: Session):
    advertising = await session.get(Advertising, advertising_id)
    if advertising is None:
        raise web.HTTPNotFound(text=json.dumps({'status': 'error', 'message': "advertising not found"}),
                               content_type="application/json")
    return advertising

@web.middleware
async def session_middleware(requests: web.Request, handler):
    async with Session() as session:
        requests["session"] = session
        return await handler(requests)

app.cleanup_ctx.append(orm_context)
app.middlewares.append(session_middleware)

class advertisingView(web.View):

    async def get(self):
        session = self.request['session']
        advertising_id = int(self.request.match_info['advertising_id'])
        advertising = await get_advertising(advertising_id, session)
        return web.json_response(
            {
                "id": advertising.id,
                "header": advertising.header,
                "description": advertising.description,
                "creation_time": advertising.creation_time.isoformat(),
                "user": advertising.user
            }
        )

    async def post(self):
        session = self.request['session']
        json_data = await self.request.json()
        if not json_data.get("header") or type(json_data.get("header")) is not str:
            raise_http_error(web.HTTPUnauthorized, "incorrect header")
        else:
            advertising = Advertising(**json_data)
            session.add(advertising)
            try:
                await session.commit()
            except IntegrityError as er:
                raise web.HTTPConflict(
                    text=json.dumps({"status": "error", "message": "user already exists"}),
                    content_type="application/json",
                )
            return web.json_response(
                {
                    "id": int(advertising.id),
                }
            )


    async def patch(self):
        advertising_id = int(self.request.match_info['advertising_id'])
        advertising = await get_advertising(advertising_id, self.request['session'])
        json_data = await self.request.json()
        for field, value in json_data.items():
            setattr(advertising, field, value)
            self.request['session'].add(advertising)
            await self.request['session'].commit()
            return web.json_response({'status': 'ok'})

    async def delete(self):
        advertising_id = int(self.request.match_info["advertising_id"])
        advertising = await get_advertising(advertising_id, self.request["session"])
        await self.request["session"].delete(advertising)
        await self.request["session"].commit()
        return web.json_response({"status": "ok"})



app.add_routes([
    web.get('/advertising/{advertising_id:\d+}/', advertisingView),
    web.post('/advertising/', advertisingView),
    web.patch('/advertising/{advertising_id:\d+}/', advertisingView),
    web.delete('/advertising/{advertising_id:\d+}/', advertisingView)
])

if __name__ == "__main__":
    web.run_app(app, port=5000)
