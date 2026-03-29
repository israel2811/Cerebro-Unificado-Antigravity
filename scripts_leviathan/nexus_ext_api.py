from fastapi import FastAPI, Request, HTTPException
import json
import os
import aiofiles
import time
from datetime import datetime
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# RUTAS DEL SISTEMA LEVIATÁN
BRAIN_PATH = r"C:\Users\Lenovo\.gemini\antigravity\brain"

app = FastAPI(title="Antigravity Neo API", description="Simbionte Extensión-Cerebro")

# Permitir a la extensión de Chrome hacer peticiones a este localhost
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_methods=["*"],
    allow_headers=["*"],
)

class NeoPayload(BaseModel):
    prompt: str
    context: str
    url: str

@app.post("/api/nexus/extension")
async def receive_neo_injection(payload: NeoPayload):
    """
    Recibe el contexto directo del navegador capturado por 'Antigravity Neo'.
    Lo formatea y lo inyecta como un archivo .json nativo en el 'brain' local de Codex/Antigravity.
    """
    try:
        timestamp_int = int(time.time())
        date_str = datetime.now().strftime("%Y-%m-%dT%H%M%S")
        
        # Estructura JSON compatible con el formato interno de Antigravity
        nexus_memory = {
            "id": f"neo-inject-{timestamp_int}",
            "title": f"Neo Context: {payload.url[:50]}...",
            "createdAt": date_str,
            "source": "Antigravity Neo Extension",
            "url": payload.url,
            "messages": [
                {
                    "role": "user",
                    "content": payload.prompt
                },
                {
                    "role": "system_context",
                    "content": payload.context
                }
            ]
        }
        
        # Crear un archivo por cada inyección para que el Omni-Parser lo lea después
        filename = f"neo_context_{date_str}.json"
        
        # Fallback si el directorio actual de brain cambia dinámicamente
        os.makedirs(BRAIN_PATH, exist_ok=True)
        file_path = os.path.join(BRAIN_PATH, filename)
        
        # Grabado asíncrono para no trabar el servidor
        async with aiofiles.open(file_path, mode='w', encoding='utf-8') as f:
            await f.write(json.dumps(nexus_memory, indent=4, ensure_ascii=False))
            
        return {"status": "success", "message": f"Inyección Asimilada en {filename}"}
        
    except Exception as e:
        print(f"[!] Falla en inyección Neo: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    # Corre expuesto en el puerto 8080 (separado del 9222 de CDP)
    uvicorn.run(app, host="127.0.0.1", port=8080)
