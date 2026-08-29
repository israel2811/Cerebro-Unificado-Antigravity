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
BATCH_SIZE = 50 # Optimización: Reducir latencia de IPC y red mediante procesamiento por lotes

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

    print(f"[*] Transformando {len(archivos)} chunks de texto en Embeddings Vectoriales (Batch Size: {BATCH_SIZE})...")
    
    batch_docs = []
    batch_metas = []
    batch_ids = []

    for i, archivo in enumerate(archivos, 1):
        ruta = os.path.join(CLEAN_CHUNKS_DIR, archivo)
        
        try:
            with open(ruta, "r", encoding="utf-8") as f:
                contenido = f.read()

            # Heurística Bolt: Solo realizar split() costoso si el string es lo suficientemente largo
            # Un string de < 200,000 chars raramente supera las 40,000 palabras (promedio 5 chars/word).
            if len(contenido) > 200000:
                words = contenido.split()
                if len(words) > 40000:
                    print(f"  [!] Advertencia: {archivo} es enorme. Cortando por limite interno de Chroma.")
                    contenido = " ".join(words[:40000])

            doc_id = f"chunk_{i}_{archivo}"
            batch_docs.append(contenido)
            batch_metas.append({"source": archivo, "type": "nexus_chunk"})
            batch_ids.append(doc_id)

            if len(batch_docs) >= BATCH_SIZE:
                try:
                    print(f"  -> Inyectando lote de {len(batch_docs)} documentos...")
                    collection.add(documents=batch_docs, metadatas=batch_metas, ids=batch_ids)
                except Exception as e:
                    print(f"  [X] Error inyectando lote (archivos {i-len(batch_docs)+1} a {i}): {e}")
                finally:
                    # Siempre resetear el lote para evitar envenenamiento de lotes subsiguientes
                    batch_docs, batch_metas, batch_ids = [], [], []

        except Exception as e:
            print(f"  [X] Error procesando archivo {archivo}: {e}")

    # Flush final para el último lote
    if batch_docs:
        try:
            print(f"  -> Finalizando inyección: lote de {len(batch_docs)} documentos...")
            collection.add(documents=batch_docs, metadatas=batch_metas, ids=batch_ids)
        except Exception as e:
            print(f"  [X] Error en lote final: {e}")

    print("\n✅ [CHROMADB RAG] Inyección Completada.")
    print(f"📂 Los archivos matriciales se guardaron en: {DB_PATH}")
    print("🎯 Ahora puedes consultar a Claude o ChatGPT usando búsqueda de similitud por cosenos local.")

if __name__ == "__main__":
    local_chroma_rag_inject()
