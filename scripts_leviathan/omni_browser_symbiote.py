import asyncio
import os
import json
import time
import subprocess
import gc
from playwright.async_api import async_playwright, Error as PlaywrightError

# CONFIGURACIÓN LEVIATÁN
PORT = 9222
CDP_URL = f"http://localhost:{PORT}"
CHECKPOINT_FILE = "symbiote_state.lock"
MAX_RETRIES = 5

def save_checkpoint(line_read, doc_id):
    """Guarda atómicamente el estado para evitar pérdidas post-crasheo."""
    state_temp = f"{CHECKPOINT_FILE}.tmp"
    with open(state_temp, "w") as f:
        json.dump({"line": line_read, "doc_id": doc_id, "timestamp": time.time()}, f)
    # Reemplazo atómico
    os.replace(state_temp, CHECKPOINT_FILE)

def load_checkpoint():
    if os.path.exists(CHECKPOINT_FILE):
        with open(CHECKPOINT_FILE, "r") as f:
            return json.load(f)
    return {"line": 0, "doc_id": 1, "timestamp": 0}

async def launch_chrome_failsafe():
    """Si Chrome muere (Fuga de RAM), esto lo resucita."""
    print("[Failsafe] Lanzando Chrome en puerto 9222. Restaurando sesión CDP...")
    subprocess.Popen([
        "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
        f"--remote-debugging-port={PORT}",
        "--restore-last-session",
        "--remote-allow-origins=*"
    ])
    await asyncio.sleep(8)  # Tiempo para arranque

async def run_symbiote():
    state = load_checkpoint()
    print(f"[*] Simbionte Iniciando. Resumiendo Doc {state['doc_id']}, Línea {state['line']}")
    
    async with async_playwright() as p:
        browser = None
        for attempt in range(MAX_RETRIES):
            try:
                print(f"[*] Enlazando núcleo CDP (Intento {attempt+1}/{MAX_RETRIES})...")
                browser = await p.chromium.connect_over_cdp(CDP_URL)
                break
            except Exception as e:
                print(f"[!] TargetClosed. Ejecutando Failsafe de reinicio de Navegador: {e}")
                await launch_chrome_failsafe()
        
        if not browser:
             print("[X] Abortando. No se puede enganchar el navegador tras múltiples intentos.")
             return

        context = browser.contexts[0]
        pages = context.pages
        page = pages[0] if pages else await context.new_page()

        try:
            print("[*] Accediendo a la Interfaz Cognitiva de Claude...")
            await page.goto("https://claude.ai/chats")
            
            while True:
                # Simulación de carga desde el Data Lake (Google Docs P2P chunk)
                chunk_payload = f"[Chunk {state['line']}] Input automatizado desde Protocolo Leviatán."
                
                try:
                    # Encontrar campo de input
                    input_box = page.locator("div[contenteditable='true']").first
                    await input_box.wait_for(state="visible", timeout=15000)
                    await input_box.fill("Analiza el siguiente extracto académico y adapta a formato APA 7: " + chunk_payload)
                    await page.keyboard.press("Enter")
                    
                    # Chequeo dinámico para Rate Limits y Baneos
                    alertas = await page.get_by_text("limit reached", ignore_case=True).count()
                    if alertas > 0:
                        print("[!] Límite de Tasa (Rate Limit). Ejecutando Exponential Backoff (300s)...")
                        # Aquí se puede añadir lógica para cambiar a ChatGPT / Gemini
                        await asyncio.sleep(300)
                        continue
                        
                except PlaywrightError as pe:
                    if "Target closed" in str(pe):
                        print("[!] NAVEGADOR REVENTADO (OOM). Reiniciando Simbionte...")
                        await launch_chrome_failsafe()
                        break 
                
                # Checkpoint Atómico
                state['line'] += 100
                save_checkpoint(state['line'], state['doc_id'])
                
                print(f"[*] Iteración completada. Guardando estado en disco duro y forzando liberación de RAM.")
                gc.collect() # Garbage Collection Forzado (Armadura Fuga de Memoria)
                
                await asyncio.sleep(15) # Retardo para emular humano
                
        except Exception as e:
             print(f"[X] Excepción Crítica: {e}")
        finally:
             if browser:
                 await browser.close()

if __name__ == "__main__":
    while True:
        try:
            asyncio.run(run_symbiote())
        except KeyboardInterrupt:
            print("Detenido manualmente.")
            break
        except Exception as e:
            print(f"Fallo del Event Loop. Resucitando el hilo en 10s... {e}")
            time.sleep(10)
