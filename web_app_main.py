"""
Enhanced Homepage with Live Trading App Interface
Replaces the simple docs page with a professional trading dashboard
"""

from fastapi import APIRouter
from fastapi.responses import HTMLResponse

web_app_router = APIRouter()



@web_app_router.get("/web/client", response_class=HTMLResponse)
async def api_client():
    """Serve API testing client for advanced users"""
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>API Test Client</title>
    </head>
    <body>
        <h1>API Testing Interface</h1>
        <p><a href="/">← Back to Live Dashboard</a></p>
        <p>This is the advanced API testing interface.</p>
    </body>
    </html>
    """
