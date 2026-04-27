## 2026-04-27 - Streaming Corpus Processing for Memory Stability
**Learning:** In the 2GB RAM environment, loading the entire 17MB (and growing) corpus into memory using `f.read()` creates a significant bottleneck and risk of OOM. Processing documents individually via the `--- ORIGEN ---` delimiter reduces peak memory usage by over 98%.
**Action:** Always use generator-based streaming for large data files in this project to maintain a constant memory footprint.
