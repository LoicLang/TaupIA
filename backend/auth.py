"""
Verification JWT Clerk pour FastAPI.

Verifie le token Bearer envoye par le frontend via les cles publiques Clerk (JWKS).
Si CLERK_PUBLISHABLE_KEY n'est pas defini, l'auth est desactivee (dev local).
"""

import os
import base64
from functools import lru_cache
from typing import Optional

import jwt
from jwt import PyJWKClient
from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer(auto_error=True)


@lru_cache(maxsize=1)
def _get_jwk_client() -> Optional[PyJWKClient]:
    """Cree un client JWKS a partir de la cle publique Clerk (cache)."""
    publishable_key = os.getenv("CLERK_PUBLISHABLE_KEY", "")
    if not publishable_key:
        return None

    # La publishable key Clerk a le format: pk_test_<base64(frontend-api)>
    # ou pk_live_<base64(frontend-api)>
    try:
        parts = publishable_key.split("_", 2)
        if len(parts) < 3:
            return None
        # Decode le frontend API domain depuis la cle
        padded = parts[2] + "=="  # padding base64
        frontend_api = base64.b64decode(padded).decode("utf-8").rstrip("$")
        jwks_url = f"https://{frontend_api}/.well-known/jwks.json"
        return PyJWKClient(jwks_url)
    except Exception:
        return None


def verify_clerk_token(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> dict:
    """
    Dependency FastAPI : verifie le JWT Clerk.

    Retourne le payload decode (contient sub, email, etc.)
    Leve 401 si le token est invalide ou absent.
    """
    token = credentials.credentials

    jwk_client = _get_jwk_client()
    if jwk_client is None:
        raise HTTPException(
            status_code=500,
            detail="Clerk n'est pas configure (CLERK_PUBLISHABLE_KEY manquant)",
        )

    try:
        signing_key = jwk_client.get_signing_key_from_jwt(token)
        payload = jwt.decode(
            token,
            signing_key.key,
            algorithms=["RS256"],
            options={"verify_aud": False},
        )
        return payload

    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expire")
    except jwt.InvalidTokenError as e:
        raise HTTPException(status_code=401, detail=f"Token invalide: {e}")
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Erreur d'authentification: {e}")


def get_auth_dependencies() -> list:
    """Retourne les dependencies d'auth si Clerk est configure, sinon liste vide."""
    if os.getenv("CLERK_PUBLISHABLE_KEY"):
        return [Depends(verify_clerk_token)]
    return []
