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

# Dynamic relative path fallback if hardcoded path does not exist
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CLEAN_CHUNKS_DIR = r"/workspaces/Antigravity_Cloud_Project/scripts_leviathan/clean_chunks" if os.name == 'posix' else r"C:\Users\Lenovo\Antigravity_Cloud_Project\scripts_leviathan\clean_chunks"
DB_PATH = r"/workspaces/Antigravity_Cloud_Project/nexus_vector_db" if os.name == 'posix' else r"C:\Users\Lenovo\Antigravity_Cloud_Project\nexus_vector_db"

def local_chroma_rag_inject(batch_size: int = 20):
    print("🚀 [CHROMADB RAG] Base Vectorial 100% Autónoma y Gratuita Iniciada...")
    
    chunks_dir = CLEAN_CHUNKS_DIR if os.path.exists(CLEAN_CHUNKS_DIR) else os.path.join(SCRIPT_DIR, "clean_chunks")
    db_path = DB_PATH if os.path.exists(os.path.dirname(DB_PATH)) else os.path.join(os.path.dirname(SCRIPT_DIR), "nexus_vector_db")

    # 1. Inicializar Cliente Chroma (Sin API Keys, guardado en disco duro)
    chroma_client = chromadb.PersistentClient(path=db_path)
    
    # 2. Usar modelo de Embeddings Ligero (MiniLM) para no ahogar la RAM de 2GB
    sentence_transformer_ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
    
    # 3. Crear / Cargar Colección
    collection = chroma_client.get_or_create_collection(name="tesis_cca", embedding_function=sentence_transformer_ef)
    
    if not os.path.exists(chunks_dir):
        print(f"[!] Directorio {chunks_dir} vacío. Corre el 02_docs_prep_injector primero.")
        return

    # Sort files alphabetically for deterministic processing
    archivos = sorted([f for f in os.listdir(chunks_dir) if f.endswith(".txt")])
    
    if not archivos:
        print("[!] No hay chunks de texto para procesar.")
        return

    print(f"[*] Transformando {len(archivos)} chunks de texto en Embeddings Vectoriales (Batch size: {batch_size})...")
    
    # Batch lists to group database insertions and reduce SQLite write transactions & embedding model calls
    batch_docs = []
    batch_metadatas = []
    batch_ids = []

    for i, archivo in enumerate(archivos, 1):
        ruta = os.path.join(chunks_dir, archivo)
        
        with open(ruta, "r", encoding="utf-8") as f:
            contenido = f.read()
            
        # Fast single-pass truncation using maxsplit=40001 to avoid splitting entire large strings twice
        words = contenido.split(None, 40001)
        if len(words) > 40000:
            print(f"  [!] Advertencia: {archivo} es enorme. Cortando por limite interno de Chroma.")
            contenido = " ".join(words[:40000])

        doc_id = f"chunk_{i}_{archivo}"
        
        batch_docs.append(contenido)
        batch_metadatas.append({"source": archivo, "type": "nexus_chunk"})
        batch_ids.append(doc_id)

        if len(batch_docs) >= batch_size:
            try:
                print(f"  -> Inyectando lote de {len(batch_docs)} documentos...")
                collection.add(
                    documents=list(batch_docs),
                    metadatas=list(batch_metadatas),
                    ids=list(batch_ids)
                )
            except Exception as e:
                print(f"  [X] Error vectorizando lote: {e}")
            finally:
                batch_docs.clear()
                batch_metadatas.clear()
                batch_ids.clear()

    # Flush remaining documents in final batch
    if batch_docs:
        try:
            print(f"  -> Inyectando lote final de {len(batch_docs)} documentos...")
            collection.add(
                documents=list(batch_docs),
                metadatas=list(batch_metadatas),
                ids=list(batch_ids)
            )
        except Exception as e:
            print(f"  [X] Error vectorizando lote final: {e}")
        finally:
            batch_docs.clear()
            batch_metadatas.clear()
            batch_ids.clear()

    print("\n✅ [CHROMADB RAG] Inyección Completada.")
    print(f"📂 Los archivos matriciales se guardaron en: {db_path}")
    print("🎯 Ahora puedes consultar a Claude o ChatGPT usando búsqueda de similitud por cosenos local.")

if __name__ == "__main__":
    local_chroma_rag_inject()
