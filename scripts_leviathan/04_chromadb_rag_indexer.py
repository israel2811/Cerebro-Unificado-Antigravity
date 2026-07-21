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

# Dynamic path calculations relative to this script's directory for environment compatibility
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CLEAN_CHUNKS_DIR = os.path.join(SCRIPT_DIR, "clean_chunks")
DB_PATH = os.path.join(os.path.dirname(SCRIPT_DIR), "nexus_vector_db")

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

    # Deterministic alphabetical ordering of text chunks
    archivos = sorted([f for f in os.listdir(CLEAN_CHUNKS_DIR) if f.endswith(".txt")])
    
    if not archivos:
        print("[!] No hay chunks de texto para procesar.")
        return

    print(f"[*] Transformando {len(archivos)} chunks de texto en Embeddings Vectoriales...")
    
    # Batch processing initialization
    batch_docs = []
    batch_metadatas = []
    batch_ids = []
    BATCH_SIZE = 20

    for i, archivo in enumerate(archivos, 1):
        ruta = os.path.join(CLEAN_CHUNKS_DIR, archivo)
        
        with open(ruta, "r", encoding="utf-8") as f:
            contenido = f.read()
            
        # ⚡ OPTIMIZACIÓN BOLT: split(None, 40001) para truncar recuentos de palabras sin doble split() de cadena completa
        words = contenido.split(None, 40001)
        if len(words) > 40000:
            print(f"  [!] Advertencia: {archivo} es enorme. Cortando por limite interno de Chroma.")
            contenido = " ".join(words[:40000])

        doc_id = f"chunk_{i}_{archivo}"
        
        # Buffer the items
        batch_docs.append(contenido)
        batch_metadatas.append({"source": archivo, "type": "nexus_chunk"})
        batch_ids.append(doc_id)

        # ⚡ OPTIMIZACIÓN BOLT: Batch inserts to reduce indexing API call overhead
        if len(batch_docs) >= BATCH_SIZE:
            try:
                print(f"  -> [{i}/{len(archivos)}] Incrustando lote de {len(batch_docs)} chunks...")
                collection.add(
                    documents=batch_docs,
                    metadatas=batch_metadatas,
                    ids=batch_ids
                )
            except Exception as e:
                print(f"  [X] Error vectorizando lote: {e}")
            finally:
                # Robust cleanup to prevent "batch poisoning" (leaking failed items or multiplying items)
                batch_docs.clear()
                batch_metadatas.clear()
                batch_ids.clear()

    # Flush remaining documents in the final batch
    if batch_docs:
        try:
            print(f"  -> [Flush] Incrustando lote final de {len(batch_docs)} chunks...")
            collection.add(
                documents=batch_docs,
                metadatas=batch_metadatas,
                ids=batch_ids
            )
        except Exception as e:
            print(f"  [X] Error vectorizando lote final: {e}")
        finally:
            batch_docs.clear()
            batch_metadatas.clear()
            batch_ids.clear()

    print("\n✅ [CHROMADB RAG] Inyección Completada.")
    print(f"📂 Los archivos matriciales se guardaron en: {DB_PATH}")
    print("🎯 Ahora puedes consultar a Claude o ChatGPT usando búsqueda de similitud por cosenos local.")

if __name__ == "__main__":
    local_chroma_rag_inject()
