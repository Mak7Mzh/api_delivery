from fastapi import FastAPI

from cfg import default_port
from bd_folder.db__ import database
from models import ReqCreate

app = FastAPI(title="Test API", docs_url=None, redoc_url=None, openapi_url=None)

@app.get("/api/cancel_req/")
async def cancel_requestss(req_id: int):
    """ Отмена заявки на доставку """
    try:
        response = await database.cancel_req(req_id)
        if response == "good": return {"message": "ok"}
        elif response == "tovar_v_govne": return {"message": "Невозможно отменить! Товар уже передан в доставку!"}
        elif response == "tovar_alredy_v_govne": return {"message": "Товар уже отменён!"}
        else: return {"message": "error"}
    except Exception as e:
        print(f"ОШИБКА(cancel_requestss): {e}")
        return {"message": "error"}

@app.get("/api/get_req/")
async def get_request_po_id(req_id: int):
    """ Получение заявки по ID заказа """
    try:
        niger_page = await database.get_req(req_id)
        if niger_page: return {"message": niger_page}
        else: return {"message": "error"}
    except Exception as e:
        print(f"ОШИБКА(get_request_po_id): {e}")
        return {"message": "error"}

@app.post("/api/create_req")
async def create_requestss(req_data: ReqCreate):
    try:
        response = await database.create_new_req(req_data)
        if response: return {"id": response}
        else: return {"message": "error"}
    except Exception as e:
        print(f"ОШИБКА(create_requestss): {e}")
        return {"message": "error"}


@app.post("/api/update_next_status/")
async def update_request_status(req_id: int):
    """Изменение статуса заявки с проверкой порядка статусов"""
    try:
        response = await database.update_req_status(req_id)
        if response[0] == "updated":
            return {"message": f"Статус успешно обновлен на >{response[1]}<"}
        elif response == "max_status": return {"message": "Не удалось обновить статус! Эта заявка уже имеет максимальный статус из возможных"}
        elif response == "req_cancelled": return {"message": "Не удалось обновить статус! Эта заявка имеет статус >Отменён<"}
        elif response == "already_delivered": return {"message": "Не удалось обновить статус! Эта заявка имеет статус >Товар доставлен<"}
        elif response == "req_not_found": return {"message": "Не удалось обновить статус! Заявка не найдена"}
        else: return {"message": "error"}
    except Exception as e:
        print(f"ОШИБКА(update_request_status): {e}")
        return {"message": "error"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, port=default_port)