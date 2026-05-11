from fastapi import FastAPI
from app.presentation.routes import router
from app.core.database import db_manager, Base

app = FastAPI(title="Adocão Prototype")

# Include API routes
app.include_router(router)

@app.on_event("startup")
def on_startup():
    # Build tables dynamically for the prototype
    Base.metadata.create_all(bind=db_manager.engine)
