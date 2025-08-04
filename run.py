#!/usr/bin/env python3

#Bu dosya WAF419 uygulamasının ana çalıştırma dosyasıdır.
from app.core.proxy import init_app
import asyncio

if __name__ == '__main__':
    try:
        asyncio.run(init_app())
    except KeyboardInterrupt:
        print("Proxy server stopped by user")