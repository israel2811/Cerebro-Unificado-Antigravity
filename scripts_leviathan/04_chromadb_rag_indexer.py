#!/usr/bin/env python3
# ==============================================================================
# 🧠 PILAR 2: WEAPONIZACIÓN VECTORIAL - RAG LOCAL CON CHROMADB
# ==============================================================================
# Rediseñado para ignorar Supabase/Pinecone. Esto corre 100% gratis en tu PC
# o en la Máquina Virtual de Codespaces, insertando la tesis en SQLite local.
# ==============================================================================

import os

try:
    import chromadb
    from chromadb.utils import embedding_functions
except ImportError:
    print("[!] Dependencias faltantes. Instalando en background...")
    print("Corre: pip install chromadb sentence-transformers")
    exit(1)

# Paths configurados para Codespaces (posix) y Windows local (nt)
BASE_PATH = "/workspaces/Antigravity_Cloud_Project" if os.name == 'posix' \
    else r"C:\Users\Lenovo\Antigravity_Cloud_Project"

CLEAN_CHUNKS_DIR = os.path.join(BASE_PATH, "scripts_leviathan", "clean_chunks")
DB_PATH = os.path.join(BASE_PATH, "nexus_vector_db")


def local_chroma_rag_inject():
    print("🚀 [CHROMADB RAG] Base Vectorial 100% Autónoma Iniciada...")

    # 1. Inicializar Cliente Chroma (Sin API Keys, guardado en disco duro)
    chroma_client = chromadb.PersistentClient(path=DB_PATH)

    # 2. Usar modelo de Embeddings Ligero (MiniLM) para RAM de 2GB
    sentence_transformer_ef = \
        embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name="all-MiniLM-L6-v2"
        )

    # 3. Crear / Cargar Colección
    collection = chroma_client.get_or_create_collection(
        name="tesis_cca",
        embedding_function=sentence_transformer_ef
    )

    if not os.path.exists(CLEAN_CHUNKS_DIR):
        print(f"[!] Directorio {CLEAN_CHUNKS_DIR} vacío. Corre el "
              "02_docs_prep_injector primero.")
        return

    archivos = [f for f in os.listdir(CLEAN_CHUNKS_DIR) if f.endswith(".txt")]

    if not archivos:
        print("[!] No hay chunks de texto para procesar.")
        return

    print(f"[*] Transformando {len(archivos)} chunks de texto...")

    # ⚡ Optimización Bolt: Batching para reducir overhead de API/DB
    BATCH_SIZE = 20
    batch_docs = []
    batch_metadatas = []
    batch_ids = []

    def flush_batch():
        if not batch_docs:
            return
        try:
            print(f"  -> Inyectando lote de {len(batch_docs)} documentos...")
            collection.add(
                documents=batch_docs,
                metadatas=batch_metadatas,
                ids=batch_ids
            )
        except Exception as e:
            print(f"  [X] Error vectorizando lote: {e}")
        finally:
            batch_docs.clear()
            batch_metadatas.clear()
            batch_ids.clear()

    for i, archivo in enumerate(archivos, 1):
        ruta = os.path.join(CLEAN_CHUNKS_DIR, archivo)

        with open(ruta, "r", encoding="utf-8") as f:
            contenido = f.read()

        # ⚡ Optimización Bolt: Truncamiento eficiente usando maxsplit
        # Evita doble split() en documentos grandes (O(N) vs O(2N)).
        words = contenido.split(None, 40001)
        if len(words) > 40000:
            print(f"  [!] Advertencia: {archivo} es enorme. Cortando...")
            contenido = " ".join(words[:40000])

        doc_id = f"chunk_{i}_{archivo}"

        batch_docs.append(contenido)
        batch_metadatas.append({"source": archivo, "type": "nexus_chunk"})
        batch_ids.append(doc_id)

        if len(batch_docs) >= BATCH_SIZE:
            flush_batch()

    # Inyectar el último lote restante
    flush_batch()

    print("\n✅ [CHROMADB RAG] Inyección Completada.")
    print(f"📂 Los archivos matriciales se guardaron en: {DB_PATH}")
    print("🎯 Ahora puedes consultar a Claude o ChatGPT localmente.")


if __name__ == "__main__":
    local_chroma_rag_inject()
