from fastapi import FastAPI, Request


def init_fast_api() -> FastAPI:
    app = FastAPI(title="Translate Mock")

    @app.middleware("http")
    async def add_process_time_header(request: Request, call_next):
        if "content-type" in request.headers and request.headers["content-type"] == "application/x-amz-json-1.1":
            # content-type is "application/x-amz-json-1.1"
            # Interpret as JSON
            headers = dict(request.scope['headers'])
            headers[b"content-type"] = b"application/json"
            request.scope["headers"] = [(k, v) for k, v in headers.items()]
            response = await call_next(request)
            response.headers["content-type"] =  "application/x-amz-json-1.1"
        else:
            response = await call_next(request)
        return response

    return app
