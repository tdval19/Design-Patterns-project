import uvicorn

from app.runner.asgi import bitcoin_app

uvicorn.run(bitcoin_app, host="0.0.0.0", port=8000, debug=True)
