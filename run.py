#!/usr/bin/env python3

from app.core.proxy import init_app
import asyncio

if __name__ == '__main__':
    try:
        asyncio.run(init_app())
    except KeyboardInterrupt:
        print("Proxy server stopped by user")