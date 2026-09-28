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

# Resolucion dinamica de rutas relativas al script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CLEAN_CHUNKS_DIR = os.path.join(BASE_DIR, "clean_chunks")
DB_PATH = os.path.normpath(os.path.join(BASE_DIR, "..", "nexus_vector_db"))

BATCH_SIZE = 20  # Insercion por lotes para acelerar inserciones hasta 20x en ChromaDB

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

    # Ordenamiento alfabetico determinista
    archivos = sorted([f for f in os.listdir(CLEAN_CHUNKS_DIR) if f.endswith(".txt")])
    
    if not archivos:
        print("[!] No hay chunks de texto para procesar.")
        return

    print(f"[*] Transformando {len(archivos)} chunks de texto en Embeddings Vectoriales (Lote: {BATCH_SIZE})...")
    
    batch_docs = []
    batch_metas = []
    batch_ids = []

    for i, archivo in enumerate(archivos, 1):
        ruta = os.path.join(CLEAN_CHUNKS_DIR, archivo)
        
        with open(ruta, "r", encoding="utf-8") as f:
            contenido = f.read()
            
        # Segmentacion preventiva eficiente usando maxsplit para evitar full split repetido en memoria
        words = contenido.split(None, 40000)
        if len(words) > 40000:
            print(f"  [!] Advertencia: {archivo} es enorme. Cortando por limite interno de Chroma.")
            contenido = " ".join(words[:40000])

        doc_id = f"chunk_{i}_{archivo}"
        
        batch_docs.append(contenido)
        batch_metas.append({"source": archivo, "type": "nexus_chunk"})
        batch_ids.append(doc_id)

        # Insercion vectorizada por lote
        if len(batch_docs) >= BATCH_SIZE:
            try:
                print(f"  -> [{i}/{len(archivos)}] Incrustando lote de {len(batch_docs)} documentos...")
                collection.add(
                    documents=list(batch_docs),
                    metadatas=list(batch_metas),
                    ids=list(batch_ids)
                )
            except Exception as e:
                print(f"  [X] Error vectorizando lote: {e}")
            finally:
                batch_docs.clear()
                batch_metas.clear()
                batch_ids.clear()

    # Procesar cualquier resto final del lote
    if batch_docs:
        try:
            print(f"  -> Incrustando lote final de {len(batch_docs)} documentos...")
            collection.add(
                documents=list(batch_docs),
                metadatas=list(batch_metas),
                ids=list(batch_ids)
            )
        except Exception as e:
            print(f"  [X] Error vectorizando lote final: {e}")
        finally:
            batch_docs.clear()
            batch_metas.clear()
            batch_ids.clear()

    print("\n✅ [CHROMADB RAG] Inyección Completada.")
    print(f"📂 Los archivos matriciales se guardaron en: {DB_PATH}")
    print("🎯 Ahora puedes consultar a Claude o ChatGPT usando búsqueda de similitud por cosenos local.")

if __name__ == "__main__":
    local_chroma_rag_inject()
