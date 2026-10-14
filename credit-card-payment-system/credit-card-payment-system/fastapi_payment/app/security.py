import jwt
from jwt import InvalidTokenError
from fastapi import Depends, Header, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from .config import SECRET_KEY

bearer_scheme = HTTPBearer(auto_error=False)


def current_user_id(
 authorization: str | None = Header(default=None, include_in_schema=False),
 _credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
) -> int:
 if not authorization or not authorization.startswith("Bearer "): raise HTTPException(401,"Bearer access token required")
 try:
  payload=jwt.decode(authorization.split(" ",1)[1],SECRET_KEY,algorithms=["HS256"],options={"require":["exp","user_id","token_type"]})
  if payload.get("token_type")!="access": raise HTTPException(401,"Access token required")
  return int(payload["user_id"])
 except (InvalidTokenError,ValueError,KeyError): raise HTTPException(401,"Invalid or expired access token")
