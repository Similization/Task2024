from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from config import Config
from database.postgres import Database

config = Config.from_file("config.yaml")
database = Database(config.database)
app = FastAPI()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Действие при запуске приложения (подключение к базе данных)
    await database.connect_to_db()
    yield
    # Действие при завершении приложения (отключение от базы данных)
    await database.disconnect()

# Создание приложения FastAPI с использованием lifespan событий
app = FastAPI(lifespan=lifespan)

@app.get("/{text}")
async def find_by_text(text: str):
    query = """
    SELECT id, text, create_date, rubrics
    FROM task.document
    WHERE to_tsvector('russian', text) @@ to_tsquery('russian', $1)
    ORDER BY create_date DESC
    LIMIT 20;
    """
    try:
        # Выполняем запрос и передаем параметр text
        result = await database.execute_query(query, f"%{text}%")
        
        if not result:
            raise HTTPException(status_code=404, detail="Document not found")
        
        # Возвращаем id всех найденных записей
        ids = [record['id'] for record in result]
        return {"ids": ids}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/{id}")
async def find_by_text(id: int):
    query = """
    DELETE FROM task.document WHERE id = $1
    """
    try:
        # Выполняем запрос и передаем параметр text
        result = await database.execute_query(query, f"%{id}%")
        
        if not result:
            raise HTTPException(status_code=404, detail="Document not found")
        
        # Возвращаем id всех найденных записей
        ids = [record['id'] for record in result]
        return {"ids": ids}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app,
        host=config.server.host,
        port=config.server.port,
    )