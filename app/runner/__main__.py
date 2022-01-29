import uvicorn

from app.runner.asgi import test_app

uvicorn.run(test_app, host="0.0.0.0", port=8000, debug=True)
