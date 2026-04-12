#!/usr/bin/env python3
# ==============================================================================
# 🧠 PILAR 2: WEAPONIZACIÓN VECTORIAL - RAG LOCAL CON CHROMADB
# ==============================================================================
# Rediseñado para ignorar Supabase/Pinecone. Esto corre 100% gratis en tu PC
# o en la Máquina Virtual de Codespaces, insertando la tesis en SQLite local.
# ==============================================================================

import os
import time

try:
    import chromadb
    from chromadb.utils import embedding_functions
except ImportError:
    print("[!] Dependencias faltantes. Instalando en background...")
    print("Corre: pip install chromadb sentence-transformers")
    exit(1)

CLEAN_CHUNKS_DIR = r"/workspaces/Antigravity_Cloud_Project/scripts_leviathan/clean_chunks" if os.name == 'posix' else r"C:\Users\Lenovo\Antigravity_Cloud_Project\scripts_leviathan\clean_chunks"
DB_PATH = r"/workspaces/Antigravity_Cloud_Project/nexus_vector_db" if os.name == 'posix' else r"C:\Users\Lenovo\Antigravity_Cloud_Project\nexus_vector_db"

def local_chroma_rag_inject():
    print("🚀 [CHROMADB RAG] Base Vectorial 100% Autónoma y Gratuita Iniciada...")
    
    # 1. Inicializar Cliente Chroma (Sin API Keys, guardado en disco duro)
    chroma_client = chromadb.PersistentClient(path=DB_PATH)
    
    # 2. Usar modelo de Embeddings Ligero (MiniLM) para no ahogar la RAM de 2GB
    sentence_transformer_ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
    
    # 3. Crear / Cargar Colección
    collection = chroma_client.get_or_create_collection(name="tesis_cca", embedding_function=sentence_transformer_ef)
    
    if not os.path.exists(CLEAN_CHUNKS_DIR):
        print(f"[!] Directorio {CLEAN_CHUNKS_DIR} vacío. Corre el 02_docs_prep_injector primero.")
        return

    archivos = [f for f in os.listdir(CLEAN_CHUNKS_DIR) if f.endswith(".txt")]
    
    if not archivos:
        print("[!] No hay chunks de texto para procesar.")
        return

    print(f"[*] Transformando {len(archivos)} chunks de texto en Embeddings Vectoriales...")
    
    # Optimizaciones BOLT: Procesamiento por lotes y heurística de longitud
    BATCH_SIZE = 50
    current_batch = {"documents": [], "metadatas": [], "ids": []}

    for i, archivo in enumerate(archivos, 1):
        ruta = os.path.join(CLEAN_CHUNKS_DIR, archivo)
        
        with open(ruta, "r", encoding="utf-8") as f:
            contenido = f.read()
            
        # BOLT OPTIMIZATION: Heurística de conteo de caracteres para evitar split() costoso
        # Se asume que 150k caracteres es el umbral de seguridad para ~40k palabras.
        if len(contenido) > 150000:
            words = contenido.split()
            if len(words) > 40000:
                print(f"  [!] Advertencia: {archivo} es enorme. Cortando por limite interno de Chroma.")
                contenido = " ".join(words[:40000])

        doc_id = f"chunk_{i}_{archivo}"
        current_batch["documents"].append(contenido)
        current_batch["metadatas"].append({"source": archivo, "type": "nexus_chunk"})
        current_batch["ids"].append(doc_id)

        # Inyección por lotes (Reduce latencia de red e IPC)
        if len(current_batch["ids"]) >= BATCH_SIZE:
            try:
                print(f"  -> [{i}/{len(archivos)}] Incrustando lote de {len(current_batch['ids'])}...")
                collection.add(**current_batch)
            except Exception as e:
                # El manejo de errores en lotes evita que un solo error detenga el pipeline
                print(f"  [X] Error vectorizando lote cerca de {archivo}: {e}")
            finally:
                # Reset atómico del lote para evitar 'poisoned batches'
                current_batch = {"documents": [], "metadatas": [], "ids": []}

    # Flush final (Procesar remanentes)
    if current_batch["ids"]:
        try:
            print(f"  -> Finalizando inyección de {len(current_batch['ids'])} restantes...")
            collection.add(**current_batch)
        except Exception as e:
            print(f"  [X] Error vectorizando lote final: {e}")

    print("\n✅ [CHROMADB RAG] Inyección Completada con Optimizaciones Bolt.")
    print(f"📂 Los archivos matriciales se guardaron en: {DB_PATH}")
    print("🎯 Ahora puedes consultar a Claude o ChatGPT usando búsqueda de similitud por cosenos local.")

if __name__ == "__main__":
    local_chroma_rag_inject()
