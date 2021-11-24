from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.config import Config
from src.routes import dict_route, ping_route

app = FastAPI(**Config().dict(), debug=True)
app.include_router(dict_route.router, prefix="/dict")
app.include_router(ping_route.router, prefix="/ping")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://typeddict-ui.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def redirect_to_docs():
    return {"message": "live"}
