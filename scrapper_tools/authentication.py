from fastapi import Depends, HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

TOKEN = "g4k8j9a2l1m6n7b3d5"

security = HTTPBearer()

def get_token(credentials: HTTPAuthorizationCredentials = Security(security)):
    if credentials.credentials != TOKEN:
        raise HTTPException(status_code=403, detail="Invalid token")
    return credentials
