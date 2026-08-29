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

    # OPTIMIZACIÓN: Batching (Procesamiento por lotes)
    # Reducimos latencia de red/IPC y permitimos que Chroma use operaciones vectorizadas.
    BATCH_SIZE = 50
    batch_docs = []
    batch_metadatas = []
    batch_ids = []

    for i, archivo in enumerate(archivos, 1):
        ruta = os.path.join(CLEAN_CHUNKS_DIR, archivo)

        try:
            with open(ruta, "r", encoding="utf-8") as f:
                contenido = f.read()

            # OPTIMIZACIÓN: Heurística de longitud antes de split()
            # Un split() en un archivo de 16MB toma ~0.3s. len() es instantáneo.
            # 200,000 chars es un aproximado conservador para 40,000 palabras.
            if len(contenido) > 200000:
                words = contenido.split()
                if len(words) > 40000:
                    print(f"  [!] Advertencia: {archivo} es enorme. Cortando por limite interno de Chroma.")
                    contenido = " ".join(words[:40000])

            batch_docs.append(contenido)
            batch_metadatas.append({"source": archivo, "type": "nexus_chunk"})
            batch_ids.append(f"chunk_{i}_{archivo}")

            # Si alcanzamos el tamaño del lote, inyectamos
            if len(batch_docs) >= BATCH_SIZE:
                try:
                    print(f"  -> [{i}/{len(archivos)}] Inyectando lote de {len(batch_docs)} documentos...")
                    collection.add(
                        documents=batch_docs,
                        metadatas=batch_metadatas,
                        ids=batch_ids
                    )
                except Exception as e:
                    print(f"  [X] Error inyectando lote cerca de {archivo}: {e}")
                finally:
                    # Resetear lotes SIEMPRE para evitar 'batch poisoning'
                    batch_docs, batch_metadatas, batch_ids = [], [], []

        except Exception as e:
            print(f"  [X] Error leyendo {archivo}: {e}")

    # Flush final (inyectar lo que quedó en el último lote)
    if batch_docs:
        try:
            print(f"  -> Finalizando inyección: {len(batch_docs)} documentos restantes...")
            collection.add(
                documents=batch_docs,
                metadatas=batch_metadatas,
                ids=batch_ids
            )
        except Exception as e:
            print(f"  [X] Error en inyección final: {e}")

    print("\n✅ [CHROMADB RAG] Inyección Completada.")
    print(f"📂 Los archivos matriciales se guardaron en: {DB_PATH}")
    print("🎯 Ahora puedes consultar a Claude o ChatGPT usando búsqueda de similitud por cosenos local.")

if __name__ == "__main__":
    local_chroma_rag_inject()
