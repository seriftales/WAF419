import aiohttp
import aiohttp.web
import asyncio 
from app.config import TARGET_SERVER, PROXY_PORT , HOST
from app.utils.logger import logger
from app.filters.filters import Rules  

async def handle (request) : 

    path = request.rel_url
    method = request.method
    headers = request.headers
    body = await request.read() 
    rule = Rules()

    logger.info(f"Received {method} request for {path} with headers {headers} and body {body}")

    if rule.is_blocked(str(path), body.decode('utf-8')):
        logger.info(f"Request blocked for path: {path}")
        return aiohttp.web.Response(status=403, text="Forbidden")
    
    
    async with aiohttp.ClientSession() as session:
        async with session.request(method, f"{TARGET_SERVER}{path}", headers=headers, data=body) as response:
            response_body = await response.read()
            logger.info(f"Forwarded {method} request to {TARGET_SERVER}{path} with response status {response.status}")
            print(f"[Response] Status: {response.status}")
            return aiohttp.web.Response(body=response_body, status=response.status, headers=response.headers)
        

async def init_app():
    app = aiohttp.web.Application()
    app.router.add_route('*', '/{tail:.*}', handle)
    runner = aiohttp.web.AppRunner(app)
    await runner.setup()
    site = aiohttp.web.TCPSite(runner, HOST, PROXY_PORT) 
    logger.info(f"Starting proxy server on port {PROXY_PORT}")
    await site.start()

    while True:
        await asyncio.sleep(3600)

if __name__ == '__main__':
    try: 
        asyncio.run(init_app()) 
    except KeyboardInterrupt:
       
        print("Proxy server stopped by user") 