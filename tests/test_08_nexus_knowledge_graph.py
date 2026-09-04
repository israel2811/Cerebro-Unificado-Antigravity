import os
import unittest
import tempfile
import importlib.util
from unittest.mock import patch
import networkx as nx

class TestNexusKnowledgeGraph(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        script_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", "scripts_leviathan", "08_nexus_knowledge_graph.py")
        )
        spec = importlib.util.spec_from_file_location("nexus_knowledge_graph", script_path)
        cls.kg_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(cls.kg_module)

    def test_build_omni_knowledge_graph(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            test_graph_path = os.path.join(tmpdir, "nexus_vector_db", "tesis_knowledge_graph.graphml")

            with patch.object(self.kg_module, "GRAPH_FILE_PATH", test_graph_path):
                self.kg_module.build_omni_knowledge_graph()

            self.assertTrue(os.path.exists(test_graph_path))

            G = nx.read_graphml(test_graph_path)
            self.assertGreater(len(G.nodes()), 0)
            self.assertGreater(len(G.edges()), 0)

            # Verify specific edge attribute
            has_relation = False
            for u, v, data in G.edges(data=True):
                if "relation" in data:
                    has_relation = True
                    break
            self.assertTrue(has_relation, "Edge relation attribute should be present in GraphML")

if __name__ == "__main__":
    unittest.main()
