"""
Hybrid Indexing System: Centralized Metadata + Distributed Index Layer
CS63016 Project - Shahbaz Shaikh, Piyusha Kadam, Mohammed Rameez Usman
"""

import hashlib
import time
import random
import math
from collections import defaultdict
from dataclasses import dataclass, field
from typing import Any, Optional
import json


# ─── Data Structures ──────────────────────────────────────────────────────────

@dataclass
class Document:
    doc_id: str
    content: str
    metadata: dict = field(default_factory=dict)

@dataclass
class NodeSummary:
    node_id: str
    doc_count: int
    term_count: int
    load: float  # 0.0 to 1.0

@dataclass
class QueryResult:
    doc_id: str
    node_id: str
    score: float
    latency_ms: float


# ─── Distributed Index Node ───────────────────────────────────────────────────

class IndexNode:
    """Simulates one node in the distributed index layer."""

    def __init__(self, node_id: str):
        self.node_id = node_id
        self.inverted_index: dict[str, list[str]] = defaultdict(list)  # term -> [doc_ids]
        self.documents: dict[str, Document] = {}
        self.query_count = 0

    def add_document(self, doc: Document):
        self.documents[doc.doc_id] = doc
        for term in self._tokenize(doc.content):
            if doc.doc_id not in self.inverted_index[term]:
                self.inverted_index[term].append(doc.doc_id)

    def search(self, terms: list[str]) -> list[QueryResult]:
        start = time.perf_counter()
        # Simulate network/IO delay (10-50ms per node)
        time.sleep(random.uniform(0.010, 0.050))
        matched = set()
        for term in terms:
            for doc_id in self.inverted_index.get(term, []):
                matched.add(doc_id)
        elapsed = (time.perf_counter() - start) * 1000
        self.query_count += 1
        return [QueryResult(doc_id=d, node_id=self.node_id,
                            score=random.uniform(0.5, 1.0), latency_ms=elapsed)
                for d in matched]

    def get_summary(self) -> NodeSummary:
        return NodeSummary(
            node_id=self.node_id,
            doc_count=len(self.documents),
            term_count=len(self.inverted_index),
            load=min(self.query_count / 100.0, 1.0)
        )

    @staticmethod
    def _tokenize(text: str) -> list[str]:
        stopwords = {"a","an","the","is","in","of","and","or","to","for","with","on","at"}
        return [w.lower() for w in text.split() if w.isalpha() and w.lower() not in stopwords]


# ─── Central Metadata Index ───────────────────────────────────────────────────

class CentralMetadataIndex:
    """
    Lightweight central layer: stores node summaries + doc-to-node mappings.
    Used for query routing — avoids broadcasting to all nodes.
    """

    def __init__(self):
        self.doc_to_node: dict[str, str] = {}          # doc_id -> node_id
        self.term_to_nodes: dict[str, set[str]] = defaultdict(set)  # term -> {node_ids}
        self.node_summaries: dict[str, NodeSummary] = {}
        self.lookups = 0

    def register_document(self, doc: Document, node_id: str):
        self.doc_to_node[doc.doc_id] = node_id
        for term in IndexNode._tokenize(doc.content):
            self.term_to_nodes[term].add(node_id)

    def update_summary(self, summary: NodeSummary):
        self.node_summaries[summary.node_id] = summary

    def route_query(self, terms: list[str]) -> set[str]:
        """Returns the minimal set of nodes that might have results."""
        self.lookups += 1
        candidates: set[str] = set()
        for term in terms:
            candidates |= self.term_to_nodes.get(term, set())
        return candidates  # empty means no relevant nodes known


# ─── Hybrid Indexing System ───────────────────────────────────────────────────

class HybridIndexingSystem:
    """
    Combines CentralMetadataIndex (routing) + distributed IndexNodes (storage).
    Partitioning strategy: consistent hashing by doc_id.
    """

    def __init__(self, num_nodes: int = 4, strategy: str = "hash"):
        self.strategy = strategy  # "hash" or "range"
        self.nodes: dict[str, IndexNode] = {
            f"node_{i}": IndexNode(f"node_{i}") for i in range(num_nodes)
        }
        self.node_ids = list(self.nodes.keys())
        self.metadata = CentralMetadataIndex()
        self.total_docs = 0
        self.stats = {
            "hybrid_queries": 0,
            "centralized_queries": 0,
            "distributed_queries": 0,
            "hybrid_latency_ms": [],
            "centralized_latency_ms": [],
            "distributed_latency_ms": [],
        }

    def _assign_node(self, doc_id: str) -> str:
        if self.strategy == "hash":
            h = int(hashlib.md5(doc_id.encode()).hexdigest(), 16)
            return self.node_ids[h % len(self.node_ids)]
        else:  # range
            idx = int(doc_id.split("_")[-1]) % len(self.node_ids)
            return self.node_ids[idx]

    def add_document(self, doc: Document):
        node_id = self._assign_node(doc.doc_id)
        self.nodes[node_id].add_document(doc)
        self.metadata.register_document(doc, node_id)
        self.total_docs += 1
        # Refresh summary
        self.metadata.update_summary(self.nodes[node_id].get_summary())

    def hybrid_search(self, query: str) -> dict:
        """Smart query: routes only to relevant nodes via metadata."""
        terms = IndexNode._tokenize(query)
        t0 = time.perf_counter()
        target_nodes = self.metadata.route_query(terms)
        results = []
        nodes_queried = 0
        for nid in target_nodes:
            results.extend(self.nodes[nid].search(terms))
            nodes_queried += 1
        elapsed = (time.perf_counter() - t0) * 1000
        self.stats["hybrid_queries"] += 1
        self.stats["hybrid_latency_ms"].append(elapsed)
        return {"results": results, "nodes_queried": nodes_queried,
                "total_nodes": len(self.nodes), "latency_ms": elapsed,
                "mode": "hybrid"}

    def distributed_search(self, query: str) -> dict:
        """Naive distributed: broadcast to ALL nodes (no routing)."""
        terms = IndexNode._tokenize(query)
        t0 = time.perf_counter()
        results = []
        for node in self.nodes.values():
            results.extend(node.search(terms))
        elapsed = (time.perf_counter() - t0) * 1000
        self.stats["distributed_queries"] += 1
        self.stats["distributed_latency_ms"].append(elapsed)
        return {"results": results, "nodes_queried": len(self.nodes),
                "total_nodes": len(self.nodes), "latency_ms": elapsed,
                "mode": "distributed"}

    def centralized_search(self, query: str) -> dict:
        """Simulate centralized: single node holds everything (bottleneck)."""
        terms = IndexNode._tokenize(query)
        t0 = time.perf_counter()
        # Only query node_0 (simulates single-node bottleneck + extra delay)
        time.sleep(random.uniform(0.04, 0.12))  # simulate index scan overhead
        results = self.nodes["node_0"].search(terms)
        elapsed = (time.perf_counter() - t0) * 1000
        self.stats["centralized_queries"] += 1
        self.stats["centralized_latency_ms"].append(elapsed)
        return {"results": results, "nodes_queried": 1,
                "total_nodes": len(self.nodes), "latency_ms": elapsed,
                "mode": "centralized"}

    def get_node_stats(self) -> list[dict]:
        return [
            {
                "node_id": nid,
                "doc_count": node.get_summary().doc_count,
                "term_count": node.get_summary().term_count,
                "query_count": node.query_count,
                "load": round(node.get_summary().load * 100, 1)
            }
            for nid, node in self.nodes.items()
        ]

    def avg_latency(self, mode: str) -> float:
        key = f"{mode}_latency_ms"
        vals = self.stats.get(key, [])
        return round(sum(vals) / len(vals), 2) if vals else 0.0


# ─── Sample Dataset Generator ─────────────────────────────────────────────────

SAMPLE_DOCS = [
    ("search engines use distributed inverted indexes for efficient keyword retrieval", {"category": "search"}),
    ("NoSQL databases handle large scale data with partitioned storage", {"category": "database"}),
    ("Apache Spark enables distributed processing of big data workloads", {"category": "processing"}),
    ("consistent hashing distributes load evenly across cluster nodes", {"category": "systems"}),
    ("inverted index maps terms to document identifiers for fast search", {"category": "search"}),
    ("Elasticsearch provides distributed full text search with sharding", {"category": "search"}),
    ("B-Tree indexes are common in centralized relational databases", {"category": "database"}),
    ("query routing reduces network overhead in distributed index systems", {"category": "systems"}),
    ("metadata layer stores node summaries and partition mappings", {"category": "systems"}),
    ("IoT devices generate high velocity data streams requiring real time indexing", {"category": "iot"}),
    ("recommendation systems need fast lookup of user and item features", {"category": "ml"}),
    ("AdTech platforms use real time indexing for contextual targeting", {"category": "adtech"}),
    ("distributed hash tables provide scalable key value lookups", {"category": "systems"}),
    ("Apache Cassandra uses consistent hashing for partitioned indexing", {"category": "database"}),
    ("Google Bigtable offers distributed storage with row key indexing", {"category": "database"}),
    ("range partitioning splits data by key range across nodes", {"category": "systems"}),
    ("load balancing ensures even distribution across index nodes", {"category": "systems"}),
    ("parallel query execution improves throughput in distributed systems", {"category": "processing"}),
    ("fault tolerance requires replication of index partitions", {"category": "systems"}),
    ("social media platforms index billions of posts for fast retrieval", {"category": "search"}),
]


def build_demo_system(num_nodes: int = 4) -> HybridIndexingSystem:
    sys = HybridIndexingSystem(num_nodes=num_nodes)
    for i, (content, meta) in enumerate(SAMPLE_DOCS):
        doc = Document(doc_id=f"doc_{i:03d}", content=content, metadata=meta)
        sys.add_document(doc)
    return sys


if __name__ == "__main__":
    print("=== Hybrid Indexing System Demo ===\n")
    system = build_demo_system(num_nodes=4)

    queries = ["distributed indexing nodes", "search engines inverted index", "NoSQL databases"]
    for q in queries:
        print(f"\nQuery: '{q}'")
        h = system.hybrid_search(q)
        d = system.distributed_search(q)
        c = system.centralized_search(q)
        print(f"  Hybrid:       {h['nodes_queried']}/{h['total_nodes']} nodes, {h['latency_ms']:.1f}ms, {len(h['results'])} results")
        print(f"  Distributed:  {d['nodes_queried']}/{d['total_nodes']} nodes, {d['latency_ms']:.1f}ms, {len(d['results'])} results")
        print(f"  Centralized:  {c['nodes_queried']}/{c['total_nodes']} nodes, {c['latency_ms']:.1f}ms, {len(c['results'])} results")

    print("\n=== Node Stats ===")
    for s in system.get_node_stats():
        print(f"  {s['node_id']}: docs={s['doc_count']}, terms={s['term_count']}, queries={s['query_count']}")
