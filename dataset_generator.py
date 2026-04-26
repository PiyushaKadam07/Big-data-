import random
import json

# Rich vocabulary for synthetic document generation
TOPICS = {
    "search": {
        "terms": ["inverted index", "keyword retrieval", "full text search", "query ranking", "BM25", "TF-IDF", "tokenization", "stemming", "relevance scoring", "search engine", "index shard", "document frequency", "term frequency", "postings list", "vocabulary", "crawler", "web indexing", "snippet generation", "query expansion", "boolean search"],
        "verbs": ["indexes", "retrieves", "ranks", "scores", "tokenizes", "crawls", "processes", "optimizes", "caches", "shards"]
    },
    "database": {
        "terms": ["B-Tree", "hash index", "primary key", "foreign key", "SQL query", "NoSQL", "ACID transaction", "replication", "sharding", "partitioning", "schema", "relational model", "document store", "column family", "key-value store", "MongoDB", "Cassandra", "PostgreSQL", "Redis", "HBase"],
        "verbs": ["stores", "retrieves", "indexes", "replicates", "partitions", "queries", "joins", "aggregates", "commits", "rolls back"]
    },
    "distributed": {
        "terms": ["consistent hashing", "distributed hash table", "node", "cluster", "replication factor", "CAP theorem", "eventual consistency", "partition tolerance", "load balancer", "fault tolerance", "leader election", "consensus protocol", "Raft", "Paxos", "gossip protocol", "heartbeat", "quorum", "shard", "replica", "coordinator"],
        "verbs": ["distributes", "replicates", "coordinates", "balances", "synchronizes", "routes", "partitions", "scales", "tolerates", "elects"]
    },
    "bigdata": {
        "terms": ["Apache Spark", "Hadoop", "MapReduce", "HDFS", "data pipeline", "batch processing", "stream processing", "Kafka", "Flink", "data lake", "ETL", "data warehouse", "columnar storage", "Parquet", "Avro", "throughput", "latency", "scalability", "data ingestion", "real-time analytics"],
        "verbs": ["processes", "ingests", "transforms", "aggregates", "streams", "batches", "pipelines", "parallelizes", "compresses", "serializes"]
    },
    "systems": {
        "terms": ["memory management", "cache", "CPU", "I/O", "network bandwidth", "latency", "throughput", "concurrency", "thread pool", "connection pool", "buffer", "queue", "scheduler", "load balancing", "rate limiting", "circuit breaker", "monitoring", "logging", "metrics", "alerting"],
        "verbs": ["manages", "allocates", "schedules", "monitors", "limits", "buffers", "queues", "optimizes", "profiles", "benchmarks"]
    },
    "ml": {
        "terms": ["feature vector", "embedding", "neural network", "gradient descent", "loss function", "training data", "inference", "model serving", "recommendation engine", "collaborative filtering", "content-based filtering", "matrix factorization", "cosine similarity", "k-nearest neighbors", "clustering", "classification", "regression", "deep learning", "transformer", "attention mechanism"],
        "verbs": ["predicts", "classifies", "recommends", "trains", "infers", "embeds", "clusters", "optimizes", "evaluates", "fine-tunes"]
    },
    "iot": {
        "terms": ["sensor data", "time series", "device telemetry", "edge computing", "MQTT", "IoT gateway", "stream ingestion", "data aggregation", "real-time monitoring", "anomaly detection", "device registry", "firmware", "protocol", "bandwidth", "power consumption", "latency constraint", "event driven", "pub sub", "message broker", "smart device"],
        "verbs": ["collects", "streams", "monitors", "detects", "aggregates", "publishes", "subscribes", "processes", "transmits", "alerts"]
    },
    "adtech": {
        "terms": ["contextual targeting", "click-through rate", "impression", "bid request", "real-time bidding", "ad exchange", "demand side platform", "supply side platform", "cookie", "user profile", "behavioral targeting", "retargeting", "conversion tracking", "CPM", "CPC", "audience segment", "frequency capping", "viewability", "brand safety", "ad inventory"],
        "verbs": ["targets", "bids", "serves", "tracks", "segments", "retargets", "optimizes", "measures", "attributes", "monetizes"]
    }
}

TEMPLATES = [
    "{topic_term} {verb} large scale datasets efficiently in distributed environments",
    "efficient {topic_term} improves query performance across multiple cluster nodes",
    "the {topic_term} system {verb} data using parallel execution strategies",
    "distributed {topic_term} reduces query latency by routing to relevant nodes only",
    "{topic_term} and {topic_term2} work together to achieve fault tolerant data retrieval",
    "benchmarking {topic_term} reveals significant performance gains over centralized approaches",
    "hybrid architecture combines {topic_term} with metadata-driven query routing",
    "{topic_term} {verb} index partitions across nodes to balance load evenly",
    "scalable {topic_term} handles millions of queries per second with low overhead",
    "metadata layer tracks {topic_term} mappings for efficient node selection",
    "consistent hashing assigns {topic_term} to nodes minimizing rebalancing overhead",
    "{topic_term} reduces communication cost compared to broadcast-based {topic_term2}",
    "real-time {topic_term} enables sub-millisecond lookups in distributed index systems",
    "partitioned {topic_term} achieves linear scalability as cluster size grows",
    "{topic_term} {verb} query results from multiple shards and merges them efficiently",
    "the central metadata index stores {topic_term} summaries for fast routing decisions",
    "node-level {topic_term} metrics guide load balancing and query scheduling",
    "{topic_term} replication ensures data availability during node failures",
    "inverted index built on {topic_term} enables fast document retrieval at scale",
    "query optimizer leverages {topic_term} statistics to choose optimal execution plan",
]

def generate_doc(doc_id, idx):
    topic = random.choice(list(TOPICS.keys()))
    topic_data = TOPICS[topic]
    term1 = random.choice(topic_data["terms"])
    verb = random.choice(topic_data["verbs"])
    
    # Sometimes mix two topics
    topic2 = random.choice(list(TOPICS.keys()))
    term2 = random.choice(TOPICS[topic2]["terms"])
    
    template = random.choice(TEMPLATES)
    content = template.format(
        topic_term=term1,
        topic_term2=term2,
        verb=verb
    )
    
    return {
        "id": doc_id,
        "content": content,
        "category": topic,
        "doc_num": idx
    }

def generate_dataset(n=1000):
    docs = []
    for i in range(n):
        doc_id = f"doc_{i:04d}"
        docs.append(generate_doc(doc_id, i))
    return docs

if __name__ == "__main__":
    docs = generate_dataset(1000)
    with open("/home/claude/hybrid_indexing/dataset_1000.json", "w") as f:
        json.dump(docs, f, indent=2)
    print(f"Generated {len(docs)} documents")
    print("Sample:", docs[0])
    print("Sample:", docs[42])
    print("Sample:", docs[999])
