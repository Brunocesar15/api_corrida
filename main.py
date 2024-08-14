from fastapi import FastAPI
from ulid import ULID
from fastapi import FastAPI, HTTPException, Response
from pydantic import BaseModel
from fastapi.encoders import jsonable_encoder


app = FastAPI()

class Corrida(BaseModel):
    id: str | None
    origem: str
    destino: str
    distancia: float
    valor: float
    estado: str

corridas: list[Corrida] = [
    Corrida(id=str(ULID()), origem='mangue', destino='cupuaçu', distancia=255, valor=129, estado="Requisitada"),
    Corrida(id=str(ULID()), origem='timbre', destino='morro', distancia=450, valor=209, estado="Requisitada"),
    Corrida(id=str(ULID()), origem='osasco', destino='macau', distancia=300, valor=190, estado="Em Andamento"),
    Corrida(id=str(ULID()), origem='zona rural', destino='ministro', distancia=30, valor=210, estado="Finalizado"),
]

@app.get('/corrida')
async def listar_corridas() -> list[Corrida]:
    return corridas


@app.get('/corrida/{estado}')
async def corrida_filtrar_estado(estado: str) -> list[Corrida]:
    corridas_filtradas = [corrida for corrida in corridas if corrida.estado.upper().split() == estado.upper().split()]
    
    return jsonable_encoder(corridas_filtradas) 
    raise HTTPException(status_code=404, detail='Corrida não localizada!')


@app.post('/corrida')
async def criar_corrida(corre: Corrida) -> Corrida:
    u_corrida = Corrida(id=str(ULID()), origem=corre.origem, destino=corre.destino, distancia=corre.distancia, valor=2 * corre.distancia + 6.65, estado='requisitada')
    corridas.append(u_corrida)
    return u_corrida


@app.post('/corrida')
async def criar_corrida(corre: Corrida) -> Corrida:
    return "corrida iniciada"


@app.put('/corrida/{id}')
async def corrida_alterar(id: str, corrida: Corrida):
    for corre in corridas:
        if id == corre.id and ('requisitada'.upper().split() == corre.estado.upper().split() or 'em andamento'.upper().split() == corre.estado.upper().split()):
            corre.origem = corrida.origem
            corre.destino = corrida.destino
            corre.distancia = corrida.distancia
            corre.valor = corrida.valor
            corre.estado = corrida.estado
            return corre
        else:
            return HTTPException(status_code=400, detail="A corrida deve ter sido requisitada ou estar em andamento")
    raise HTTPException(status_code=404, detail='Corrida não localizada!')


@app.delete('/corrida/{id}')
async def corrida_remover(id: str):
    for corrida in corridas:
        if corrida.id == id and 'requisitada'.upper().split() == corrida.estado.upper().split():
            corridas.remove(corrida)
            return Response(status_code=204)

    return HTTPException(status_code=404, detail="A corrida deve ter sido requisitada")

@app.post('/corrida/iniciar/{id}')
async def iniciar_corrida(id: str):
    for corrida in corridas:
        if corrida.id == id:
            if corrida.estado.upper().split() != "Requisitada".upper().split():
                return HTTPException(status_code=400, detail='A corrida deve ter sido finalizada')
            corrida.estado = "Em Andamento"
            return jsonable_encoder(corrida)
        raise HTTPException(status_code=404, detail='Corrida não encontrada')
    

@app.post('/corrida/finalizar/{id}')
async def finalizar_corrida(id: str):
    for corrida in corridas:
        if corrida.id == id:
            if corrida.estado.upper().replace(" ","_") != "Em Andamento".upper().replace(" ","_"):
                print("Em Andamento".upper().replace(" ","_"))
                return HTTPException(status_code=400, detail='A corrida deve ter sido finalizada ou deletada')
            corrida.estado = "Finalizado"
            return corrida
    raise HTTPException(status_code=404, detail='Corrida não encontrada')
    


        