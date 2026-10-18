# Batch 2: Terms 36-70

TERMS_BATCH_2 = {
    "hsts": {
        "category": "http-networking",
        "difficulty": "beginner",
        "nature": "defense tooling",
        "definition": "HTTP Strict Transport Security (HSTS, RFC 6797) is an HTTP response header that forces compliant user agents to establish encrypted HTTPS connections exclusively. It prevents SSL-stripping attacks and prohibits users from clicking through SSL certificate warnings. Domains can also submit to the browser HSTS Preload list to guarantee TLS enforcement on the very first connection.",
        "why_matters": "Without HSTS, the initial unencrypted HTTP handshake or redirect can be intercepted via active Man-in-the-Middle (MitM) tools (e.g. sslstrip), allowing attackers to hijack session cookies and plaintext data before HTTPS negotiation occurs.",
        "example": "Strict-Transport-Security: max-age=63072000; includeSubDomains; preload",
        "related": ["tls-certificate-expiry", "security-headers", "dns"],
        "links": [
            {"title": "RFC 6797: HTTP Strict Transport Security (HSTS)", "url": "https://datatracker.ietf.org/doc/html/rfc6797"},
            {"title": "MDN Web Docs: Strict-Transport-Security", "url": "https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Strict-Transport-Security"}
        ]
    },
    "encryption-at-rest": {
        "category": "crypto-identity",
        "difficulty": "intermediate",
        "nature": "defense technique",
        "definition": "Encryption at Rest protects non-volatile persistent data stored in databases, block volumes, object stores, and backup archives against physical theft or unauthorized offline access. Implementations utilize symmetric encryption ciphers like AES-256 with envelope encryption, where data encryption keys (DEKs) are protected by key encryption keys (KEKs) managed within Hardware Security Modules (HSMs) or cloud Key Management Services (KMS).",
        "why_matters": "Meets regulatory compliance mandates (PCI-DSS, HIPAA, GDPR) and prevents exposure if raw disk drives are decommissioned, lost, or compromised via unmounted snapshot theft.",
        "example": "# AWS S3 bucket default encryption via CLI\naws s3api put-bucket-encryption --bucket my-secure-bucket \\\n  --server-side-encryption-configuration '{\"Rules\": [{\"ApplyServerSideEncryptionByDefault\": {\"SSEAlgorithm\": \"aws:kms\", \"KMSMasterKeyId\": \"arn:aws:kms:us-east-1:123456789012:key/sample\"}}]}'",
        "related": ["hashing-vs-encryption", "secrets-management", "backups"],
        "links": [
            {"title": "NIST SP 800-111: Storage Encryption Technologies", "url": "https://csrc.nist.gov/publications/detail/sp/800-111/final"},
            {"title": "AWS KMS Cryptographic Details", "url": "https://docs.aws.amazon.com/kms/latest/developerguide/concepts.html"}
        ]
    },
    "dependency-vulnerabilities": {
        "category": "secure-sdlc",
        "difficulty": "beginner",
        "nature": "attack defense",
        "definition": "Dependency Vulnerabilities refer to security flaws, unpatched bugs, and known exploits residing inside third-party open-source libraries, packages, and frameworks incorporated into software projects. Software Composition Analysis (SCA) tools inspect lockfiles and manifest files to identify known Common Vulnerabilities and Exposures (CVEs) published in databases such as the National Vulnerability Database (NVD).",
        "why_matters": "Modern applications are composed of over 80% open-source dependencies; a single critical CVE in an indirect dependency (like Log4j CVE-2021-44228) can allow unauthenticated remote code execution across thousands of internal services simultaneously.",
        "example": "# Check npm project for known dependency vulnerabilities\nnpm audit\n# Scan Python dependencies with pip-audit\npip-audit -r requirements.txt",
        "related": ["supply-chain-attacks", "image-scanning", "lockfiles"],
        "links": [
            {"title": "OWASP Top 10: Vulnerable and Outdated Components", "url": "https://owasp.org/Top10/A06_2021-Vulnerable_and_Outdated_Components/"},
            {"title": "NIST National Vulnerability Database", "url": "https://nvd.nist.gov/"}
        ]
    },
    "supply-chain-attacks": {
        "category": "secure-sdlc",
        "difficulty": "advanced",
        "nature": "attack technique",
        "definition": "Supply Chain Attacks target third-party vendors, build infrastructure, package registries, and developer toolchains rather than attacking the target organization's primary production network directly. Adversaries compromise maintainer accounts, publish typosquatted package names, inject malicious commits into upstream repositories (e.g. xz-utils backdoor), or poison CI/CD pipeline dependencies to distribute trojanized binaries.",
        "why_matters": "Bypasses perimeter defenses and traditional firewalls by piggybacking on trusted build processes and cryptographic release channels (e.g., SolarWinds breach), affecting millions of downstream consumer installations through authentic updates.",
        "example": "# Typosquatting attack example:\n# Legitimate package: 'requests'\n# Malicious payload package: 'requsts' or 'python-requests'\npip install requsts  # Inadvertently executes post-install malicious script",
        "related": ["dependency-vulnerabilities", "reproducible-builds", "lockfiles"],
        "links": [
            {"title": "CISA: Defending Against Software Supply Chain Attacks", "url": "https://www.cisa.gov/resources-tools/resources/defending-against-software-supply-chain-attacks"},
            {"title": "NIST SP 800-161: Cybersecurity Supply Chain Risk Management", "url": "https://csrc.nist.gov/publications/detail/sp/800-161/rev-1/final"}
        ]
    },
    "threat-modeling": {
        "category": "secure-sdlc",
        "difficulty": "intermediate",
        "nature": "defense concept",
        "definition": "Threat Modeling is a structured engineering process for identifying, analyzing, and prioritizing potential architectural security threats and attack vectors before and during system development. Popular frameworks include STRIDE (Spoofing, Tampering, Repudiation, Information Disclosure, Denial of Service, Elevation of Privilege) and PASTA. It maps trust boundaries, data flows, and assets to design proportional defensive mitigations.",
        "why_matters": "Remediating an architectural flaw during design is orders of magnitude cheaper than fixing an exploitable vulnerability in production. It ensures engineering teams systematically address attack surfaces rather than applying reactive patches.",
        "example": "# STRIDE Threat Matrix Example\n# Component: Password Reset Endpoint\n# Threat: Spoofing (Attacker requests reset for victim)\n# Mitigation: Send cryptographically random single-use token to verified email\n# Threat: Tampering (Modifying reset token in transit)\n# Mitigation: Enforce HTTPS and sign token with HMAC",
        "related": ["input-validation", "least-privilege", "server-side-authorization"],
        "links": [
            {"title": "OWASP Threat Modeling Project", "url": "https://owasp.org/www-community/Threat_Modeling"},
            {"title": "Microsoft Threat Modeling Tool & Guide", "url": "https://learn.microsoft.com/en-us/azure/security/develop/threat-modeling-tool"}
        ]
    },
    "indexes": {
        "category": "data-databases",
        "difficulty": "beginner",
        "nature": "technique concept",
        "definition": "Database Indexes are specialized data structures (predominantly B-Trees, Hash tables, GiST, or GIN) that maintain ordered pointers to table rows to accelerate search, range, and filter queries. Without indexes, database engines must perform sequential scans over every table page on disk. Indexes introduce a small write-amplification trade-off during INSERT, UPDATE, and DELETE operations.",
        "why_matters": "Missing indexes on frequently filtered columns cause high CPU consumption and disk I/O bottlenecks as tables grow into millions of rows, turning sub-millisecond queries into multi-second table scans that exhaust connection pools.",
        "example": "-- Create B-Tree index on foreign key and lookup column\nCREATE INDEX idx_orders_user_id ON orders (user_id);\nCREATE INDEX idx_users_email ON users (email);",
        "related": ["explain-analyze", "full-table-scans", "n-plus-1-queries"],
        "links": [
            {"title": "PostgreSQL Documentation: Indexes", "url": "https://www.postgresql.org/docs/current/indexes.html"},
            {"title": "Use The Index, Luke! SQL Indexing Guide", "url": "https://use-the-index-luke.com/"}
        ]
    },
    "explain-analyze": {
        "category": "data-databases",
        "difficulty": "intermediate",
        "nature": "tooling technique",
        "definition": "EXPLAIN ANALYZE is an essential SQL profiling command that instructs the query optimizer to execute a statement, measure actual execution time, page accesses, memory buffers, and compare the estimated cost against actual row counts for every node in the execution plan tree. It reveals whether queries use Index Scans, Bitmap Scans, or costly Sequential Scans.",
        "why_matters": "Provides undeniable ground truth for diagnosing slow database queries. It exposes optimizer misestimations caused by stale table statistics, unintended nested loops, and memory spills to temporary disk buffers during sorting.",
        "example": "EXPLAIN (ANALYZE, BUFFERS) \nSELECT o.id, o.total, u.email \nFROM orders o \nJOIN users u ON o.user_id = u.id \nWHERE o.created_at >= NOW() - INTERVAL '7 days';",
        "related": ["indexes", "full-table-scans", "n-plus-1-queries"],
        "links": [
            {"title": "PostgreSQL Documentation: Using EXPLAIN", "url": "https://www.postgresql.org/docs/current/using-explain.html"},
            {"title": "PostgreSQL Documentation: EXPLAIN Command", "url": "https://www.postgresql.org/docs/current/sql-explain.html"}
        ]
    },
    "n-plus-1-queries": {
        "category": "data-databases",
        "difficulty": "intermediate",
        "nature": "concept",
        "definition": "The N+1 Query problem occurs when an Object-Relational Mapping (ORM) framework or data layer executes one initial query to fetch N parent records, and subsequently executes N separate queries inside a loop to retrieve related child records for each parent. Instead of retrieving all associated data in a single coordinated JOIN or IN query, the database is flooded with individual round-trips.",
        "why_matters": "Severely degrades backend throughput and amplifies network latency. A single HTTP request displaying 100 items can accidentally issue 101 database queries, causing severe database connection pool exhaustion and spiking p99 latency.",
        "example": "# VULNERABLE (N+1 queries issued):\nusers = User.objects.all()  # 1 query\nfor user in users:\n    print(user.profile.bio)  # N additional queries!\n\n# OPTIMIZED (Eager loading):\nusers = User.objects.select_related('profile').all()  # 1 single JOIN query",
        "related": ["orm-lazy-loading", "indexes", "full-table-scans"],
        "links": [
            {"title": "Django Documentation: select_related and prefetch_related", "url": "https://docs.djangoproject.com/en/stable/ref/models/querysets/#select-related"},
            {"title": "Martin Fowler: Lazy Load", "url": "https://martinfowler.com/eaaCatalog/lazyLoad.html"}
        ]
    },
    "full-table-scans": {
        "category": "data-databases",
        "difficulty": "beginner",
        "nature": "concept",
        "definition": "A Full Table Scan (sequential scan / Seq Scan) occurs when the database storage engine reads every single page and row of a table from disk into memory to evaluate a query filter condition. While sequential scans can be efficient for tiny tables or when selecting a large percentage of rows, they are disastrous when retrieving small subsets of massive tables. Creating appropriate indexes avoids unnecessary table scans.",
        "why_matters": "Causes severe disk I/O saturation, thrashing the database buffer cache and ejecting frequently read hot data pages. During peak traffic, simultaneous full table scans lead to cascade latency spikes and database lockups.",
        "example": "-- Full table scan if 'status' has no index and low cardinality:\nSELECT * FROM payments WHERE status = 'pending_verification';\n-- EXPLAIN shows: 'Seq Scan on payments  (cost=0.00..45281.00 rows=320 width=98)'",
        "related": ["indexes", "explain-analyze", "n-plus-1-queries"],
        "links": [
            {"title": "PostgreSQL Documentation: Optimizer Performance", "url": "https://www.postgresql.org/docs/current/performance-tips.html"},
            {"title": "PostgreSQL Documentation: Indexes Overview", "url": "https://www.postgresql.org/docs/current/indexes-intro.html"}
        ]
    },
    "connection-pooling": {
        "category": "data-databases",
        "difficulty": "intermediate",
        "nature": "technique tooling",
        "definition": "Connection Pooling maintains a cache of pre-established, reusable database connections that application worker threads share instead of repeatedly establishing new TCP and TLS handshakes. Database servers assign dedicated memory, processes, or threads to each connection; tools like PgBouncer or HikariCP pool and multiplex thousands of client requests over a fixed pool of backend connections.",
        "why_matters": "Forking new database processes and negotiating SSL handshakes on every HTTP request consumes massive CPU and RAM, quickly triggering connection limits (max_connections). Connection pools prevent backend crashes during sudden traffic spikes.",
        "example": "# PgBouncer configuration (pgbouncer.ini)\n[databases]\nproduction_db = host=127.0.0.1 port=5432 dbname=prod\n\n[pgbouncer]\npool_mode = transaction\nmax_client_conn = 5000\ndefault_pool_size = 50",
        "related": ["database-migrations", "transactions", "stateless-services"],
        "links": [
            {"title": "PgBouncer Documentation", "url": "https://www.pgbouncer.org/usage.html"},
            {"title": "HikariCP GitHub Documentation", "url": "https://github.com/brettwooldridge/HikariCP"}
        ]
    },
    "database-migrations": {
        "category": "data-databases",
        "difficulty": "intermediate",
        "nature": "tooling technique",
        "definition": "Database Migrations are version-controlled, repeatable scripts that incrementally evolve relational database schemas (tables, columns, indexes, constraints) across development, staging, and production environments. Migration tools (Liquibase, Flyway, Alembic, Prisma) record applied versions in a metadata tracking table, enabling continuous delivery and schema synchronization.",
        "why_matters": "Manual ad-hoc schema modifications in production lead to drift, broken application releases, and catastrophic data loss. Automated migrations ensure deterministic and auditable database changes across deployment fleets.",
        "example": "-- Example Alembic / Flyway migration: V2__add_phone_to_users.sql\nALTER TABLE users ADD COLUMN phone_number VARCHAR(32);\nCREATE INDEX idx_users_phone ON users (phone_number);",
        "related": ["down-migrations", "transactions", "blue-green-deployments"],
        "links": [
            {"title": "Flyway Documentation", "url": "https://documentation.red-gate.com/fd"},
            {"title": "Prisma Documentation: Database Migrations", "url": "https://www.prisma.io/docs/concepts/components/prisma-migrate"}
        ]
    },
    "down-migrations": {
        "category": "data-databases",
        "difficulty": "intermediate",
        "nature": "technique defense",
        "definition": "Down Migrations (rollback scripts) are inverse schema migration scripts designed to cleanly reverse the structural changes introduced by a corresponding 'up' migration. While easy for additive changes (e.g. dropping a newly added column), destructive schema changes like deleting columns or altering types require careful staging to avoid irrecoverable data loss.",
        "why_matters": "When a production software deployment fails mid-flight, reliable down migrations allow operations teams to roll back the database schema to the prior stable version without having to restore from cold backups.",
        "example": "-- Up migration: add column\n-- ALTER TABLE accounts ADD COLUMN tier VARCHAR(16) DEFAULT 'standard';\n-- Down migration (reversal):\nALTER TABLE accounts DROP COLUMN tier;",
        "related": ["database-migrations", "rollbacks", "blue-green-deployments"],
        "links": [
            {"title": "Alembic Documentation: Downgrades", "url": "https://alembic.sqlalchemy.org/en/latest/tutorial.html#downgrading"},
            {"title": "PostgreSQL Documentation: ALTER TABLE", "url": "https://www.postgresql.org/docs/current/sql-altertable.html"}
        ]
    },
    "transactions": {
        "category": "data-databases",
        "difficulty": "beginner",
        "nature": "concept",
        "definition": "A Database Transaction represents a single logical unit of work consisting of one or more database read and write operations that are executed atomically. Marked by BEGIN, COMMIT, and ROLLBACK boundaries, transactions ensure that either all enclosed operations successfully persist to disk, or all modifications are completely reverted if an error occurs.",
        "why_matters": "Without transactions, partial failures during multi-step business logic (such as deducting money from one bank account before crediting another) leave the database in a corrupted, inconsistent state.",
        "example": "BEGIN;\nUPDATE accounts SET balance = balance - 100 WHERE id = 'acc_alice';\nUPDATE accounts SET balance = balance + 100 WHERE id = 'acc_bob';\nCOMMIT;",
        "related": ["acid", "isolation-levels", "deadlocks"],
        "links": [
            {"title": "PostgreSQL Documentation: Transactions", "url": "https://www.postgresql.org/docs/current/tutorial-transactions.html"},
            {"title": "SQL Standard Transactions (Wikipedia)", "url": "https://en.wikipedia.org/wiki/Database_transaction"}
        ]
    },
    "acid": {
        "category": "data-databases",
        "difficulty": "intermediate",
        "nature": "concept",
        "definition": "ACID is the foundational acronym for Atomicity, Consistency, Isolation, and Durability—the four core guarantees that ensure reliable transaction processing in database management systems. Atomicity guarantees all-or-nothing execution; Consistency enforces schema constraints and invariants; Isolation prevents concurrent transactions from interfering; Durability guarantees committed data survives power failures via write-ahead logging (WAL).",
        "why_matters": "ACID compliance is indispensable for financial ledgers, inventory systems, and transactional commerce where data corruption or lost writes can cause catastrophic monetary and legal liability.",
        "example": "-- ACID relies heavily on Write-Ahead Logging (WAL)\n-- Every committed mutation is flushed to disk in the WAL before returning success:\nCOMMIT; -- Durability achieved through synchronous WAL flush",
        "related": ["transactions", "isolation-levels", "cap-theorem"],
        "links": [
            {"title": "PostgreSQL Documentation: Reliability and the Write-Ahead Log", "url": "https://www.postgresql.org/docs/current/wal-intro.html"},
            {"title": "Martin Kleppmann: Designing Data-Intensive Applications", "url": "https://dataintensive.net/"}
        ]
    },
    "isolation-levels": {
        "category": "data-databases",
        "difficulty": "advanced",
        "nature": "concept",
        "definition": "Isolation Levels define the degree to which concurrently executing transactions are shielded from each other's uncommitted or modifying data. The ANSI SQL standard defines four levels: Read Uncommitted, Read Committed, Repeatable Read, and Serializable. Higher isolation levels prevent concurrency anomalies like Dirty Reads, Non-Repeatable Reads, and Phantom Reads at the cost of concurrency and throughput.",
        "why_matters": "Running under weak isolation (such as Read Committed) exposes systems to race conditions and phantom updates, allowing users to double-spend funds or bypass inventory checks during concurrent requests.",
        "example": "-- Set transaction isolation level in PostgreSQL\nBEGIN TRANSACTION ISOLATION LEVEL SERIALIZABLE;\nSELECT balance FROM accounts WHERE user_id = 42;\n-- Serializable Snapshot Isolation (SSI) detects and aborts conflicting concurrent writes",
        "related": ["transactions", "acid", "deadlocks"],
        "links": [
            {"title": "PostgreSQL Documentation: Transaction Isolation", "url": "https://www.postgresql.org/docs/current/transaction-iso.html"},
            {"title": "ANSI SQL Isolation Levels (Wikipedia)", "url": "https://en.wikipedia.org/wiki/Isolation_(database_systems)"}
        ]
    },
    "deadlocks": {
        "category": "data-databases",
        "difficulty": "intermediate",
        "nature": "concept",
        "definition": "A Deadlock is an impasse where two or more concurrent transactions hold locks on resources that the other transactions need, creating a circular dependency where no participant can proceed. Database engines run internal deadlock detection algorithms that periodically scan lock dependency graphs, detect cycles, and terminate one transaction (the deadlock victim) with a serialization error to break the lock.",
        "why_matters": "Frequent deadlocks cause sudden transaction aborts, user-facing 500 errors, and application retry storms. Enforcing consistent global lock acquisition order across queries eliminates circular lock dependencies.",
        "example": "-- Transaction 1: Locks row A, attempts to lock row B\n-- Transaction 2: Locks row B, attempts to lock row A\n-- Engine triggers:\n-- ERROR: deadlock detected\n-- DETAIL: Process 14002 waits for ShareLock on transaction; blocked by 14003.",
        "related": ["pessimistic-locking", "optimistic-locking", "transactions"],
        "links": [
            {"title": "PostgreSQL Documentation: Explicit Locking & Deadlocks", "url": "https://www.postgresql.org/docs/current/explicit-locking.html#LOCKING-DEADLOCKS"},
            {"title": "MySQL Documentation: Deadlocks in InnoDB", "url": "https://dev.mysql.com/doc/refman/en/innodb-deadlocks.html"}
        ]
    },
    "optimistic-locking": {
        "category": "data-databases",
        "difficulty": "intermediate",
        "nature": "defense technique",
        "definition": "Optimistic Locking is a concurrency control pattern where transactions read data without acquiring exclusive locks, assuming conflict is infrequent. Before committing updates, the transaction verifies that no other process has modified the record by checking a version number or timestamp column in the WHERE clause. If the version changed, the update affects zero rows and the application retries.",
        "why_matters": "Eliminates database lock contention and deadlocks in read-heavy applications with high concurrency, providing substantial throughput gains over blocking pessimistic locks.",
        "example": "-- Optimistic concurrency update via version token\nUPDATE products \nSET quantity = quantity - 1, version = version + 1 \nWHERE id = 101 AND version = 5;\n-- If affected rows == 0, conflict detected -> reload and retry!",
        "related": ["pessimistic-locking", "deadlocks", "race-conditions"],
        "links": [
            {"title": "Martin Fowler: Optimistic Offline Lock", "url": "https://martinfowler.com/eaaCatalog/optimisticOfflineLock.html"},
            {"title": "PostgreSQL Documentation: Concurrency Control", "url": "https://www.postgresql.org/docs/current/mvcc.html"}
        ]
    },
    "pessimistic-locking": {
        "category": "data-databases",
        "difficulty": "intermediate",
        "nature": "defense technique",
        "definition": "Pessimistic Locking is a concurrency control mechanism that assumes data conflicts will happen and eagerly acquires exclusive row-level locks (e.g. SELECT ... FOR UPDATE) upon reading data. Other transactions attempting to access or modify the locked rows are blocked until the holding transaction issues a COMMIT or ROLLBACK.",
        "why_matters": "Essential for high-contention financial transactions where retries are unacceptable and strict serialization must be guaranteed. However, excessive pessimistic locking increases queue latency and risk of deadlocks.",
        "example": "BEGIN;\n-- Acquire exclusive row lock preventing concurrent modification\nSELECT balance FROM accounts WHERE account_id = 'acc_99' FOR UPDATE;\nUPDATE accounts SET balance = balance - 50 WHERE account_id = 'acc_99';\nCOMMIT;",
        "related": ["optimistic-locking", "deadlocks", "transactions"],
        "links": [
            {"title": "PostgreSQL Documentation: SELECT FOR UPDATE", "url": "https://www.postgresql.org/docs/current/sql-select.html#SQL-FOR-UPDATE-SHARE"},
            {"title": "Martin Fowler: Pessimistic Offline Lock", "url": "https://martinfowler.com/eaaCatalog/pessimisticOfflineLock.html"}
        ]
    },
    "normalization": {
        "category": "data-databases",
        "difficulty": "beginner",
        "nature": "concept",
        "definition": "Database Normalization is the formal process of structuring a relational database schema according to standard Normal Forms (1NF, 2NF, 3NF, BCNF) to reduce data redundancy and eliminate insert, update, and delete anomalies. It decomposes large, unorganized tables into smaller, logically coherent entities linked by foreign keys.",
        "why_matters": "Reduces storage footprint and ensures that an entity's data lives in exactly one canonical place, preventing synchronization bugs where an updated address in one row fails to reflect across duplicate records.",
        "example": "-- Unnormalized: user_name and user_email repeated per order\n-- Normalized into 3NF:\nCREATE TABLE users (id SERIAL PRIMARY KEY, name TEXT, email TEXT UNIQUE);\nCREATE TABLE orders (id SERIAL PRIMARY KEY, user_id INT REFERENCES users(id), amount NUMERIC);",
        "related": ["denormalization", "foreign-keys", "unique-constraints"],
        "links": [
            {"title": "Database Normalization (Wikipedia)", "url": "https://en.wikipedia.org/wiki/Database_normalization"},
            {"title": "PostgreSQL Documentation: Database Design Basics", "url": "https://www.postgresql.org/docs/current/ddl.html"}
        ]
    },
    "denormalization": {
        "category": "data-databases",
        "difficulty": "intermediate",
        "nature": "technique concept",
        "definition": "Denormalization is the intentional optimization strategy of adding redundant data or precomputed aggregated values into a normalized database schema to reduce costly JOIN operations and accelerate read queries. It trades write performance and storage space for dramatic read throughput improvements in high-traffic read-heavy environments.",
        "why_matters": "In high-throughput systems, multi-table JOINs across millions of rows can overwhelm CPU caches and disk I/O. Denormalizing frequently accessed fields reduces query response times from hundreds of milliseconds to single digits.",
        "example": "-- Adding denormalized order_count directly to users table\nALTER TABLE users ADD COLUMN total_orders INT DEFAULT 0;\n-- Updated via application logic or database trigger on new orders",
        "related": ["normalization", "materialized-views", "read-replicas"],
        "links": [
            {"title": "Denormalization (Wikipedia)", "url": "https://en.wikipedia.org/wiki/Denormalization"},
            {"title": "PostgreSQL Documentation: Performance Tips", "url": "https://www.postgresql.org/docs/current/performance-tips.html"}
        ]
    },
    "foreign-keys": {
        "category": "data-databases",
        "difficulty": "beginner",
        "nature": "defense concept",
        "definition": "A Foreign Key is a relational database constraint that links a column (or set of columns) in one table to the primary key or unique column of another table. The database engine enforces referential integrity by guaranteeing that foreign key values must always match a valid referenced record, rejecting invalid inserts or orphaned child records.",
        "why_matters": "Enforces referential integrity at the database layer rather than trusting application code. Without foreign keys, bugs and partial deletes leave orphaned records that corrupt accounting and reporting pipelines.",
        "example": "CREATE TABLE orders (\n    id SERIAL PRIMARY KEY,\n    customer_id INTEGER NOT NULL REFERENCES customers(id) ON DELETE RESTRICT,\n    order_total NUMERIC(10, 2)\n);",
        "related": ["unique-constraints", "cascading-deletes", "normalization"],
        "links": [
            {"title": "PostgreSQL Documentation: Foreign Keys", "url": "https://www.postgresql.org/docs/current/ddl-constraints.html#DDL-CONSTRAINTS-FK"},
            {"title": "SQL Foreign Key Constraint (Wikipedia)", "url": "https://en.wikipedia.org/wiki/Foreign_key"}
        ]
    },
    "unique-constraints": {
        "category": "data-databases",
        "difficulty": "beginner",
        "nature": "defense concept",
        "definition": "A Unique Constraint is a database integrity rule that ensures all values in a column or set of columns are distinct across all rows in a table. Implemented internally via unique B-tree indexes, the engine automatically checks for existing matches on every INSERT and UPDATE, immediately rejecting duplicates with a unique violation error.",
        "why_matters": "Prevents data duplication races (such as two concurrent requests registering the same email or claiming the same username). Application-level checks like 'SELECT WHERE email=...' are prone to race conditions without a database constraint.",
        "example": "ALTER TABLE users ADD CONSTRAINT unique_user_email UNIQUE (email);",
        "related": ["foreign-keys", "race-conditions", "indexes"],
        "links": [
            {"title": "PostgreSQL Documentation: Unique Constraints", "url": "https://www.postgresql.org/docs/current/ddl-constraints.html#DDL-CONSTRAINTS-UNIQUE-CONSTRAINTS"},
            {"title": "PostgreSQL Documentation: Unique Indexes", "url": "https://www.postgresql.org/docs/current/indexes-unique.html"}
        ]
    },
    "cascading-deletes": {
        "category": "data-databases",
        "difficulty": "intermediate",
        "nature": "technique concept",
        "definition": "Cascading Deletes (ON DELETE CASCADE) is a foreign key action in relational databases specifying that when a referenced parent row is deleted, all matching child rows in associated tables are automatically deleted by the database engine. This prevents orphaned child records without requiring manual multi-table deletion queries.",
        "why_matters": "Simplifies cleanup of tightly coupled dependent records, but represents a serious operational risk: accidentally deleting a single parent customer record can invisibly purge thousands of historical orders, invoices, and audit logs.",
        "example": "CREATE TABLE order_items (\n    id SERIAL PRIMARY KEY,\n    order_id INT REFERENCES orders(id) ON DELETE CASCADE,\n    product_id INT,\n    quantity INT\n);",
        "related": ["foreign-keys", "soft-deletes", "database-migrations"],
        "links": [
            {"title": "PostgreSQL Documentation: Foreign Key Actions", "url": "https://www.postgresql.org/docs/current/ddl-constraints.html#DDL-CONSTRAINTS-FK"},
            {"title": "PostgreSQL Documentation: DDL Constraints", "url": "https://www.postgresql.org/docs/current/ddl-constraints.html"}
        ]
    },
    "soft-deletes": {
        "category": "data-databases",
        "difficulty": "beginner",
        "nature": "technique defense",
        "definition": "Soft Deletes is an application design pattern where records are marked as deleted using a status flag or timestamp column (e.g. deleted_at IS NOT NULL) rather than being physically removed from storage via an SQL DELETE statement. Application queries filter out soft-deleted records, preserving data for audit trails, compliance, and instant undelete operations.",
        "why_matters": "Prevents catastrophic data loss from accidental user operations or malicious deletion attacks. However, soft deletes complicate unique constraints and can degrade query performance if unindexed deleted records clutter tables.",
        "example": "-- Soft deletion implementation\nUPDATE users SET deleted_at = NOW() WHERE id = 42;\n\n-- Application query wrapper\nSELECT * FROM users WHERE id = 42 AND deleted_at IS NULL;",
        "related": ["cascading-deletes", "postgres-vacuum", "unique-constraints"],
        "links": [
            {"title": "PostgreSQL Documentation: Partial Indexes for Soft Deletes", "url": "https://www.postgresql.org/docs/current/indexes-partial.html"},
            {"title": "Prisma Documentation: Soft Delete Middleware", "url": "https://www.prisma.io/docs/concepts/components/prisma-client/middleware/soft-delete-middleware"}
        ]
    },
    "uuids-vs-auto-increment": {
        "category": "data-databases",
        "difficulty": "intermediate",
        "nature": "concept defense",
        "definition": "The trade-off between UUIDs (Universally Unique Identifiers) and Auto-Increment integers is a central architectural decision in database schema design. Sequential integers offer compact 4-to-8-byte storage and optimal B-tree page locality, but expose internal volume metrics and enable sequential IDOR enumeration attacks. Random UUIDs (UUIDv4) prevent enumeration and allow distributed generation without coordination, but cause B-tree index fragmentation. Modern UUIDv7 combines millisecond timestamps with randomness.",
        "why_matters": "Using auto-increment IDs in public URLs allows competitors and attackers to easily scrape data and estimate business metrics (e.g., number of customers). UUIDv7 provides IDOR defense while preserving B-tree write performance.",
        "example": "-- PostgreSQL UUID generation\nCREATE EXTENSION IF NOT EXISTS \"pgcrypto\";\nCREATE TABLE accounts (\n    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),\n    name TEXT\n);",
        "related": ["idor", "indexes", "sharding"],
        "links": [
            {"title": "RFC 9562: UUID Formats and Version 7", "url": "https://datatracker.ietf.org/doc/html/rfc9562"},
            {"title": "PostgreSQL Documentation: UUID Data Type", "url": "https://www.postgresql.org/docs/current/datatype-uuid.html"}
        ]
    },
    "cursor-based-pagination": {
        "category": "data-databases",
        "difficulty": "intermediate",
        "nature": "technique concept",
        "definition": "Cursor-Based Pagination (keyset pagination) retrieves sequential pages of dataset results by filtering on a unique, sequentially ordered column (such as an ID or timestamp) using a WHERE clause (e.g., WHERE id > last_seen_id LIMIT 20), rather than using OFFSET. Because OFFSET forces the database to scan and discard all preceding rows, cursor pagination provides constant O(1) performance regardless of how deep a client paginates.",
        "why_matters": "Deep pagination using OFFSET 100000 causes severe CPU and disk thrashing because the database scans 100,000 rows only to return 20. Cursor pagination delivers predictable sub-millisecond API response times across massive datasets.",
        "example": "-- Inefficient Offset Pagination:\nSELECT * FROM events ORDER BY id ASC LIMIT 20 OFFSET 50000;\n\n-- High-Performance Keyset Cursor Pagination:\nSELECT * FROM events WHERE id > 50000 ORDER BY id ASC LIMIT 20;",
        "related": ["indexes", "full-table-scans", "explain-analyze"],
        "links": [
            {"title": "Use The Index, Luke: Keyset Pagination", "url": "https://use-the-index-luke.com/no-offset"},
            {"title": "Slack Engineering: Evolving API Pagination", "url": "https://slack.engineering/evolving-api-pagination-at-slack/"}
        ]
    },
    "full-text-search": {
        "category": "data-databases",
        "difficulty": "intermediate",
        "nature": "technique tooling",
        "definition": "Full-Text Search (FTS) is a database search capability that parses natural language text into tokens, strips linguistic stop words, applies stemming algorithms (reducing words to their root forms), and indexes documents using inverted indexes (GIN in PostgreSQL, Lucene in Elasticsearch). FTS enables fast fuzzy matching, relevance ranking, and boolean search queries across millions of text documents.",
        "why_matters": "Executing wildcard SQL queries like LIKE '%search_term%' forces disastrous full table scans across text columns. Inverted index full-text search returns ranked results in milliseconds without dedicated search clusters.",
        "example": "-- PostgreSQL Full Text Search\nSELECT title, ts_rank(to_tsvector('english', content), query) AS rank\nFROM articles, to_tsquery('english', 'security & vulnerability') query\nWHERE to_tsvector('english', content) @@ query\nORDER BY rank DESC LIMIT 10;",
        "related": ["indexes", "explain-analyze", "full-table-scans"],
        "links": [
            {"title": "PostgreSQL Documentation: Full Text Search", "url": "https://www.postgresql.org/docs/current/textsearch.html"},
            {"title": "Elasticsearch Documentation: Text analysis", "url": "https://www.elastic.co/guide/en/elasticsearch/reference/current/analysis-overview.html"}
        ]
    },
    "read-replicas": {
        "category": "data-databases",
        "difficulty": "intermediate",
        "nature": "technique concept",
        "definition": "Read Replicas are read-only database nodes that continuously replicate data from a primary write database node via physical streaming replication or logical replication logs. By directing read-heavy traffic (analytics, dashboards, public feeds) to replicas, systems horizontally scale read throughput while isolating the primary node to process write transactions.",
        "why_matters": "Prevents heavy reporting queries from consuming CPU and locking tables on the master write node. However, asynchronous replication exposes applications to replication lag and stale reads.",
        "example": "# Application routing reads to replica pool and writes to primary\nDATABASES = {\n    'default': {'HOST': 'primary.db.internal', 'PORT': 5432},\n    'replica': {'HOST': 'read-pool.db.internal', 'PORT': 5432}\n}",
        "related": ["replication-lag", "connection-pooling", "sharding"],
        "links": [
            {"title": "PostgreSQL Documentation: High Availability and Replication", "url": "https://www.postgresql.org/docs/current/high-availability.html"},
            {"title": "AWS Aurora Replicas Overview", "url": "https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/Aurora.Replication.html"}
        ]
    },
    "replication-lag": {
        "category": "data-databases",
        "difficulty": "intermediate",
        "nature": "concept",
        "definition": "Replication Lag is the delay in time or transaction log byte offset between when a write is committed on the primary database node and when that write is replayed and visible on read replicas. Under asynchronous replication, high write throughput, long-running queries on replicas, or network latency increase lag, causing read replicas to return stale data.",
        "why_matters": "Leads to read-your-own-writes anomalies where a user updates their profile or creates a post, refreshes the page, and sees their changes missing because the read request hit a lagging replica.",
        "example": "-- Check PostgreSQL replication lag on primary\nSELECT client_addr, state,\n       write_lag, flush_lag, replay_lag\nFROM pg_stat_replication;",
        "related": ["read-replicas", "eventual-consistency", "strong-consistency"],
        "links": [
            {"title": "PostgreSQL Documentation: Monitoring Replication", "url": "https://www.postgresql.org/docs/current/monitoring-stats.html#MONITORING-PG-STAT-REPLICATION-VIEW"},
            {"title": "Martin Kleppmann: Designing Data-Intensive Applications", "url": "https://dataintensive.net/"}
        ]
    },
    "sharding": {
        "category": "data-databases",
        "difficulty": "advanced",
        "nature": "technique concept",
        "definition": "Sharding is an architectural horizontal database partitioning technique where a massive dataset is split across multiple independent database instances (shards), each holding a distinct subset of the data based on a shard key (e.g. hash of tenant_id). Unlike vertical scaling, sharding allows relational databases to scale storage and throughput linearly beyond the hardware limits of any single physical server.",
        "why_matters": "Enables hyper-scale platforms to process millions of transactions per second. However, sharding introduces immense architectural complexity: cross-shard transactions, distributed joins, and shard rebalancing require sophisticated orchestration.",
        "example": "-- Consistent Hash Sharding routing in application code:\nshard_id = hash(tenant_id) % num_shards\ndb_connection = connection_pool.get_connection(shard_id)",
        "related": ["partitioning", "consistent-hashing", "read-replicas"],
        "links": [
            {"title": "PostgreSQL Documentation: Distributed Sharding with Citus", "url": "https://docs.citusdata.com/"},
            {"title": "Martin Fowler: Sharding", "url": "https://martinfowler.com/articles/patterns-of-distributed-systems/"}
        ]
    },
    "partitioning": {
        "category": "data-databases",
        "difficulty": "intermediate",
        "nature": "technique concept",
        "definition": "Database Table Partitioning is the division of a single logical table into distinct physical underlying sub-tables (partitions) based on specified partition keys, such as ranges (date ranges), lists (status values), or hashes. The query planner automatically performs partition pruning, scanning only relevant physical partitions and ignoring unrelated segments of table data.",
        "why_matters": "Accelerates time-series and large-scale analytical queries. In addition, dropping an expired month of data via DROP TABLE partition_2023_01 is instantaneous and incurs zero VACUUM overhead compared to running a catastrophic multi-million row DELETE.",
        "example": "-- PostgreSQL Declarative Range Partitioning\nCREATE TABLE audit_logs (\n    id BIGSERIAL,\n    event_time TIMESTAMPTZ NOT NULL,\n    message TEXT\n) PARTITION BY RANGE (event_time);\n\nCREATE TABLE audit_logs_2024_01 PARTITION OF audit_logs\n    FOR VALUES FROM ('2024-01-01') TO ('2024-02-01');",
        "related": ["sharding", "hot-partitions", "postgres-vacuum"],
        "links": [
            {"title": "PostgreSQL Documentation: Table Partitioning", "url": "https://www.postgresql.org/docs/current/ddl-partitioning.html"},
            {"title": "MySQL Documentation: Partitioning Overview", "url": "https://dev.mysql.com/doc/refman/en/partitioning.html"}
        ]
    },
    "hot-partitions": {
        "category": "data-databases",
        "difficulty": "advanced",
        "nature": "concept",
        "definition": "A Hot Partition (or hot-spotting) occurs in partitioned or sharded systems when traffic, read requests, or write operations concentrate disproportionately onto a single partition or shard due to skewed key distribution (e.g. celebrity accounts or sequential timestamp keys). While neighboring shards sit idle, the hot partition exhausts CPU, disk IOPS, and memory buffers.",
        "why_matters": "Degrades the performance of the entire distributed storage cluster to the speed of the overloaded bottleneck node. Mitigations include compound shard keys, salted hash keys, and secondary caching tiers.",
        "example": "# Key salting to prevent hot-spotting on write timestamps\nshard_key = f\"{tenant_id}_{random.randint(0, 15)}\"",
        "related": ["partitioning", "sharding", "consistent-hashing"],
        "links": [
            {"title": "AWS DynamoDB Documentation: Partition Keys and Hot Spotting", "url": "https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/bp-partition-key-design.html"},
            {"title": "Google Cloud Spanner: Designing for performance", "url": "https://cloud.google.com/spanner/docs/schema-design"}
        ]
    },
    "postgres-vacuum": {
        "category": "data-databases",
        "difficulty": "intermediate",
        "nature": "tooling technique",
        "definition": "PostgreSQL VACUUM is a vital background maintenance process that reclaims storage occupied by dead row versions (tuples). Because PostgreSQL implements Multi-Version Concurrency Control (MVCC) by writing new tuple copies on UPDATE and marking old tuples dead on DELETE, uncleaned dead tuples cause table bloat. VACUUM also freezes transaction IDs to prevent 32-bit transaction ID wraparound failure.",
        "why_matters": "If the PostgreSQL autovacuum daemon falls behind, disk usage balloons, sequential scans slow to a crawl, and the database engine will eventually enter read-only emergency shutdown mode to prevent transaction ID wraparound data loss.",
        "example": "-- Manual vacuum with verbose table statistics\nVACUUM (VERBOSE, ANALYZE) customer_orders;\n-- Or reclaim space to OS (requires exclusive lock):\n-- VACUUM FULL customer_orders;",
        "related": ["soft-deletes", "database-migrations", "explain-analyze"],
        "links": [
            {"title": "PostgreSQL Documentation: Routine Vacuuming", "url": "https://www.postgresql.org/docs/current/routine-vacuuming.html"},
            {"title": "PostgreSQL Documentation: VACUUM Command", "url": "https://www.postgresql.org/docs/current/sql-vacuum.html"}
        ]
    },
    "materialized-views": {
        "category": "data-databases",
        "difficulty": "intermediate",
        "nature": "technique tooling",
        "definition": "A Materialized View is a database object that stores the physical persisted result of a complex query on disk, unlike standard SQL views which re-execute the underlying query dynamically every time they are referenced. Relational engines allow periodic or concurrent refreshes (REFRESH MATERIALIZED VIEW CONCURRENTLY) to update cached aggregations without blocking concurrent SELECT queries.",
        "why_matters": "Provides sub-millisecond response times for expensive multi-table analytical joins and aggregations without needing external cache systems. Indexes can be placed directly on materialized view columns to accelerate search filters.",
        "example": "CREATE MATERIALIZED VIEW monthly_sales_summary AS\nSELECT date_trunc('month', sale_date) AS month,\n       product_category,\n       sum(amount) AS total_revenue\nFROM sales\nGROUP BY 1, 2;\n\n-- Fast non-blocking refresh\nREFRESH MATERIALIZED VIEW CONCURRENTLY monthly_sales_summary;",
        "related": ["denormalization", "indexes", "explain-analyze"],
        "links": [
            {"title": "PostgreSQL Documentation: Materialized Views", "url": "https://www.postgresql.org/docs/current/rules-materializedviews.html"},
            {"title": "PostgreSQL Documentation: REFRESH MATERIALIZED VIEW", "url": "https://www.postgresql.org/docs/current/sql-refreshmaterializedview.html"}
        ]
    },
    "backups": {
        "category": "reliability-observability",
        "difficulty": "beginner",
        "nature": "defense tooling",
        "definition": "Backups are regular, automated copies of application databases, persistent filesystems, and configuration state preserved in secure secondary storage locations (such as cross-region object storage). Backup regimes combine periodic complete physical snapshots with continuous Write-Ahead Log (WAL) archiving to ensure comprehensive disaster recoverability against hardware failures, ransomware, and human error.",
        "why_matters": "Backups are the ultimate last line of defense against ransomware attacks, infrastructure destruction, or catastrophic operator error. Without reliable, isolated backups, data loss events can destroy businesses permanently.",
        "example": "# Physical PostgreSQL database backup via pg_dump\npg_dump -Fc -h localhost -U db_admin -d production > prod_backup_$(date +%F).dump\n# Or stream WAL for continuous backup with pgBackRest\npgbackrest --stanza=prod archive-push /var/lib/postgresql/data/pg_wal/000000010000000000000001",
        "related": ["testing-your-restores", "point-in-time-recovery", "disaster-recovery"],
        "links": [
            {"title": "PostgreSQL Documentation: Backup and Restore", "url": "https://www.postgresql.org/docs/current/backup.html"},
            {"title": "AWS Well-Architected Reliability Pillar: Backups", "url": "https://docs.aws.amazon.com/wellarchitected/latest/reliability-pillar/rel_backing_up_data.html"}
        ]
    }
}
