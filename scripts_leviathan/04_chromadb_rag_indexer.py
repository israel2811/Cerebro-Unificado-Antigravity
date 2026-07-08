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

# Usar rutas relativas al script para mayor portabilidad
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(BASE_DIR)
CLEAN_CHUNKS_DIR = os.path.join(BASE_DIR, "clean_chunks")
DB_PATH = os.path.join(ROOT_DIR, "nexus_vector_db")

def local_chroma_rag_inject():
    print("🚀 [CHROMADB RAG] Base Vectorial 100% Autónoma y Gratuita Iniciada...")
    
    # 1. Inicializar Cliente Chroma (Sin API Keys, guardado en disco duro)
    chroma_client = chromadb.PersistentClient(path=DB_PATH)
    
    # 2. Usar modelo de Embeddings Ligero (MiniLM) para no ahogar la RAM de 2GB
    sentence_transformer_ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
    
    # 3. Crear / Cargar Colección
    collection = chroma_client.get_or_create_collection(name="tesis_cca", embedding_function=sentence_transformer_ef)
    
    if not os.path.exists(CLEAN_CHUNKS_DIR):
        print(f"[!] Directorio {CLEAN_CHUNKS_DIR} no encontrado. Corre el 02_docs_prep_injector primero.")
        return

    # Sorteo alfabético para procesamiento determinístico
    archivos = sorted([f for f in os.listdir(CLEAN_CHUNKS_DIR) if f.endswith(".txt")])
    
    if not archivos:
        print("[!] No hay chunks de texto para procesar.")
        return

    print(f"[*] Transformando {len(archivos)} chunks de texto en Embeddings Vectoriales...")
    
    BATCH_SIZE = 20
    batch_state = {
        'docs': [],
        'metas': [],
        'ids': []
    }

    def flush_batch():
        if not batch_state['docs']:
            return
        try:
            print(f"  -> Inyectando lote de {len(batch_state['docs'])} documentos...")
            collection.add(
                documents=batch_state['docs'],
                metadatas=batch_state['metas'],
                ids=batch_state['ids']
            )
        except Exception as e:
            print(f"  [X] Error vectorizando lote: {e}")
        finally:
            batch_state['docs'] = []
            batch_state['metas'] = []
            batch_state['ids'] = []

    for i, archivo in enumerate(archivos, 1):
        ruta = os.path.join(CLEAN_CHUNKS_DIR, archivo)
        
        try:
            with open(ruta, "r", encoding="utf-8") as f:
                contenido = f.read()
            
            # OPTIMIZACIÓN: Truncado eficiente usando maxsplit
            # Evita duplicar el split() de todo el archivo en memoria
            words = contenido.split(None, 40001)
            if len(words) > 40000:
                print(f"  [!] Advertencia: {archivo} es enorme (>40k palabras). Truncando para Chroma.")
                contenido = " ".join(words[:40000])

            batch_state['docs'].append(contenido)
            batch_state['metas'].append({"source": archivo, "type": "nexus_chunk"})
            batch_state['ids'].append(f"chunk_{i}_{archivo}")

            if len(batch_state['docs']) >= BATCH_SIZE:
                flush_batch()

        except Exception as e:
            print(f"  [X] Error procesando {archivo}: {e}")

    # Vaciar el último lote restante
    flush_batch()

    print("\n✅ [CHROMADB RAG] Inyección Completada.")
    print(f"📂 Los archivos matriciales se guardaron en: {DB_PATH}")
    print("🎯 Ahora puedes consultar a Claude o ChatGPT usando búsqueda de similitud por cosenos local.")

if __name__ == "__main__":
    local_chroma_rag_inject()
