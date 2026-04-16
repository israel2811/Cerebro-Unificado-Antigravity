## 2024-04-16 - Memory-Efficient Document Processing in 02_docs_prep_injector.py
**Learning:** Reading a large input corpus (17MB+) entirely into memory and running BeautifulSoup on the whole string causes a significant RAM spike (~250MB), which is risky in a 2GB RAM environment.
**Action:** Implemented a streaming generator to process the corpus document-by-document. This reduced peak RAM usage by ~88% (from ~247MB to ~28MB) while maintaining functional output. Use streaming/buffered processing for any file-based data pipeline in this repository.
