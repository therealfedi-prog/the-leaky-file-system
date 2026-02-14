Secure File Upload System
Backend Implementation - I built the Python backend that handles file validation, security, and storage. The frontend was provided separately.
What I did: Created functions for file type validation (images only), size limits (5MB max), SHA-256 hash-based duplicate detection, JSON metadata storage, and auto-cleanup of files older than 24 hours. All the security logic and error handling is mine.
Tech Stack: Python, Flask, hashlib for SHA-256, JSON for metadata storage.
