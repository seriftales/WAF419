import aiohttp
import aiohttp.web
import asyncio
from app.config import TARGET_SERVER, PROXY_PORT, HOST
from app.utils.logger import logger
from app.filters.filters import Rules
import gzip
from io import BytesIO
from multidict import CIMultiDict  # Alternatif import

async def handle(request):
    path = request.rel_url
    query = request.query_string
    method = request.method
    headers = request.headers
    body = await request.read()
    rule = Rules()

    # Log: Gelen isteğin başlıkları ve body
    logger.info(f"Received {method} request for {path} {query} with headers {headers} and body {body}")

    if rule.is_blocked(str(path), body.decode('utf-8'), query):
        logger.warning(f"Request blocked for path: {path}, body: {body.decode('utf-8')}, query: {query}")
        return aiohttp.web.Response(status=403, text="Forbidden")

    async with aiohttp.ClientSession() as session:
        async with session.request(method, f"{TARGET_SERVER}{path}", headers=headers, data=body) as response:
            # Log: Yanıtın durum kodu
            logger.info(f"Response Status: {response.status}")
            # Log: Yanıt başlıkları
            logger.info(f"Response Headers: {response.headers}")
            
            # Log: Yanıtın içeriği
            response_body = await response.read()
            logger.info(f"Response Body (first 500 bytes): {response_body[:500]}...")  # İlk 500 byte'ı logla

            # Content-Encoding başlığını kontrol et
            content_encoding = response.headers.get('Content-Encoding', '').lower()
            logger.info(f"Content-Encoding: {content_encoding}")  # Content-Encoding logla

            if 'gzip' in content_encoding:
                try:
                    buf = BytesIO(response_body)
                    with gzip.GzipFile(fileobj=buf) as f:
                        response_body = f.read()  # Gzip sıkıştırmasını çöz
                    logger.info(f"Gzip decompressed successfully.")  # Gzip çözümlemesi başarılıysa logla
                except gzip.BadGzipFile:
                    logger.error(f"Bad gzip file encountered for {path}. Returning original content.")
                    # Eğer gzip çözümlemesi başarısız olursa, orijinal içeriği geri döndür
                    pass

            # Başlıkları yeni bir CIMultiDict ile oluştur ve Content-Encoding'i kaldır
            new_headers = CIMultiDict(response.headers)

            if 'Content-Encoding' in new_headers:
                del new_headers['Content-Encoding']  # Gzip başlığını kaldır

            # Content-Type başlığını kontrol et ve form verilerini ilet
            content_type = new_headers.get('Content-Type', '')
            logger.info(f"Content-Type: {content_type}")  # Content-Type logla

            if 'application/x-www-form-urlencoded' in content_type or 'multipart/form-data' in content_type:
                logger.info(f"Handling form data for {path} with content-type: {content_type}")
            
            # Cookie başlıklarının doğru iletildiğinden emin olalım
            if 'Cookie' in headers:
                new_headers['Cookie'] = headers['Cookie']
                logger.info(f"Cookie: {headers['Cookie']}")  # Cookie başlığını logla

            # Log: Yönlendirilen istek ve yanıt bilgileri
            logger.info(f"Forwarded {method} request to {TARGET_SERVER}{path} with response status {response.status}")
            return aiohttp.web.Response(body=response_body, status=response.status, headers=new_headers)

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
