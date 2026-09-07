from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config import BackendSettings
from database import make_engine, make_session_factory
from routers import news, sources, admin, collector, media, scraper
def create_app(settings: BackendSettings | None = None):
    settings=settings or BackendSettings(); engine=make_engine(settings.database_url)
    @asynccontextmanager
    async def lifespan(app): yield
    app=FastAPI(title="UniNews API",version="2.0.0",lifespan=lifespan); app.state.settings=settings; app.state.engine=engine; app.state.session_factory=make_session_factory(engine)
    app.add_middleware(CORSMiddleware,allow_origins=settings.allowed_origins,allow_credentials=False,allow_methods=["GET","POST","PATCH","PUT","DELETE"],allow_headers=["Authorization","Content-Type","X-Lease-Token"])
    for r in (news.router,sources.router,admin.router,collector.router,media.router,scraper.router): app.include_router(r)
    @app.get("/api/info")
    def info(): return {"status":"running","rag_enabled":settings.rag_enabled}
    @app.get("/health")
    def health(): return {"status":"healthy","rag_enabled":settings.rag_enabled}
    return app
app=create_app()
