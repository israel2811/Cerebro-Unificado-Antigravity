# Bolt Performance Journal

## 2025-04-20 - Memory-Efficient Corpus Processing
**Learning:** In environments with strict RAM limits (like the 2GB limit in this project), loading large text files (17MB+) into memory and then processing them with BeautifulSoup creates massive memory spikes due to internal object overhead. Processing the corpus in a streaming fashion, delimited by document origins, reduces peak RAM usage from ~257MB to ~30MB (an ~88% reduction).
**Action:** Always prefer streaming generators and granular processing for data pipeline scripts handling concatenated corpora.
