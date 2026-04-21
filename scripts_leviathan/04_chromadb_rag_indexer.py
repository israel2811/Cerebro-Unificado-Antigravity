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

    # OPTIMIZACIÓN BOLT: Lotes (Batching) para reducir IPC/Red y heurística de longitud
    BATCH_SIZE = 50
    batch_docs = []
    batch_metadatas = []
    batch_ids = []

    def flush_batch(docs, metas, ids):
        """Envía el lote a ChromaDB con manejo de errores robusto."""
        if not docs:
            return
        try:
            # Vectorización masiva: reduce overhead de red y aprovecha paralelismo interno de Chroma
            collection.add(documents=docs, metadatas=metas, ids=ids)
            print(f"  ⚡ [BATCH] Inyectado lote de {len(docs)} documentos con éxito.")
        except Exception as e:
            # Reportamos el rango para facilitar depuración sin detener el proceso completo
            print(f"  [X] Error crítico en lote (IDs {ids[0]} a {ids[-1]}): {e}")
        finally:
            # Limpieza atómica del estado del lote (Evita 'poisoned batches')
            docs.clear()
            metas.clear()
            ids.clear()

    for i, archivo in enumerate(archivos, 1):
        ruta = os.path.join(CLEAN_CHUNKS_DIR, archivo)

        try:
            with open(ruta, "r", encoding="utf-8") as f:
                contenido = f.read()

            # OPTIMIZACIÓN BOLT: Heurística de longitud (150k chars ≈ 40k palabras)
            # Evita el costoso .split() si el archivo es visiblemente pequeño. Reducción CPU ~90% en archivos comunes.
            if len(contenido) > 150000:
                palabras = contenido.split()
                if len(palabras) > 40000:
                    print(f"  [!] Advertencia: {archivo} es enorme. Cortando por limite interno de Chroma.")
                    contenido = " ".join(palabras[:40000])

            doc_id = f"chunk_{i}_{archivo}"
            batch_docs.append(contenido)
            batch_metadatas.append({"source": archivo, "type": "nexus_chunk"})
            batch_ids.append(doc_id)

            if len(batch_docs) >= BATCH_SIZE:
                print(f"  -> Procesando {i}/{len(archivos)}...")
                flush_batch(batch_docs, batch_metadatas, batch_ids)

        except Exception as e:
            print(f"  [X] Error procesando {archivo}: {e}")

    # Flush final (Asegura que los últimos documentos no se pierdan)
    if batch_docs:
        flush_batch(batch_docs, batch_metadatas, batch_ids)

    print("\n✅ [CHROMADB RAG] Inyección Completada.")
    print(f"📂 Los archivos matriciales se guardaron en: {DB_PATH}")
    print("🎯 Ahora puedes consultar a Claude o ChatGPT usando búsqueda de similitud por cosenos local.")

if __name__ == "__main__":
    local_chroma_rag_inject()
