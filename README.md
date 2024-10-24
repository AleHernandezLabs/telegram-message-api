# Telegram Message API

### Overview

The Telegram Message API is a RESTful API built with FastAPI to send messages via Telegram bots. The API allows users to securely send messages to specified Telegram chat IDs using a bot token, and it stores all message details in a PostgreSQL database. The API is secured by an API key for authentication and supports easy configuration and deployment.

### Features

- FastAPI-based: High-performance, modern web framework for building APIs.
- Telegram Integration: Send messages to specific Telegram chat IDs using bot tokens.
- Secure Access: API key authentication for secure message sending.
- Database Storage: Logs all sent messages and details in a PostgreSQL database.
- Asynchronous: Supports non-blocking I/O for high performance.
- Easy Deployment: Fully documented and easily deployable to platforms like Render.com.
- Customizable: Configuration through .env files for easy setup and environment management.
- Prerequisites
- Python 3.8 or higher
- PostgreSQL (or any compatible SQLAlchemy-supported database)
- Telegram Bot API Token (create a bot via BotFather)
