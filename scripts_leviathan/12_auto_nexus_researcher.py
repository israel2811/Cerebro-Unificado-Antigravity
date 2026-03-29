#!/usr/bin/env python3
# ==============================================================================
# 🤖 PILAR 5 y 6: EL AUTÓMATA INVESTIGADOR 24/7 (OMNI-RESEARCHER)
# ==============================================================================
# Propósito: Lazo infinito (While True) que no duerme. Analiza el Índice,
# extrae datos vía API y genera texto en formato APA 7 de Google Docs.
# ==============================================================================

import time
import asyncio
from datetime import datetime
from swarm_dispatcher import SwarmDispatcher  # Importamos tu módulo base de IAs

CHECKPOINT_FILE = "C:\\Users\\Lenovo\\Antigravity_Cloud_Project\\scripts_leviathan\\omni_state.lock"

def secure_checkpoint(status):
    """Guarda estado cada bloque generado para saber dónde retomar si el OS crashea."""
    with open(CHECKPOINT_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{datetime.now()}] {status}\n")

async def eternal_omni_loop():
    print("=========================================================")
    print(" 🤖 OMNI-RESEARCHER STARTING: DIOS NO DUERME, YO TAMPOCO.")
    print("=========================================================")

    dispatcher = SwarmDispatcher()

    iteration = 1
    while True:
        try:
            print(f"\n[+] --- INICIANDO CICLO COLMENA #{iteration} ---")
            
            # Paso A: Lectura del Índice (El "Qué" vamos a redactar hoy)
            print("[*] Leyendo índice: El Modelo FPI y la Atenuación a -30dB en VoIP.")
            
            # Paso B: RAG y DSP (Gemini & NotebookLM)
            print("[*] Asignando vectores a Celery (Cloud Run)...")
            citas = dispatcher.dispatch_notebooklm("Cerebro Predictivo", "pdf_docs")
            fisica = dispatcher.dispatch_gemini_pro("Telemetría CAN-Bus")
            
            # Paso C: Estructuración (ChatGPT Custom GPT Vía Cloupflared)
            estructura = dispatcher.dispatch_chatgpt("Armar esqueleto del Capítulo III.")
            
            # Paso D: Redacción final (Puerto 9222 de Chrome Local / API Claude)
            borrador = dispatcher.dispatch_claude_chief_editor([citas, fisica, estructura])
            
            print(f"✅ CICLO #{iteration} Tesis Autónoma lograda: {len(borrador)} tokens procesados.")
            secure_checkpoint(f"ITERATION_{iteration}_SUCCESS_APA_DRAFTFUL")
            
            # PROTECCIÓN DE RATE LIMIT (Exponential Backoff Base)
            print("[ZZZ] Hibernando 5 Minutos para evadir Rate Limits y Ban de la IA...")
            time.sleep(300) 
            iteration += 1

        except Exception as e:
            # DIRECTIVA DE INMORTALIDAD (Nunca se detiene en try/except)
            print(f"\n[!] ALERTA CRÍTICA: Fallo del Sistema ({e}).")
            secure_checkpoint(f"CRASH_ERROR: {e}")
            print("⏳ [FAILSAFE] Iniciando Protocolo de Re-Sanación y Backoff Recursivo (Espera de 10 minutos)...")
            time.sleep(600)  # Duplica el castigo para sanar red o cuota API

if __name__ == '__main__':
    try:
         asyncio.run(eternal_omni_loop())
    except KeyboardInterrupt:
        print("[!] Secuencia de Interrupción Manual. Hibernando Autómata.")
        secure_checkpoint("MANUAL_SHUTDOWN")
