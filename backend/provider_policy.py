"""Provider access policy (fixed providers + tester allowlist)."""

from typing import Optional

from application.container import Container
from application.settings import Settings


def _extract_email(user_payload: Optional[dict]) -> str:
    """Best-effort email extraction from JWT payload."""
    if not user_payload:
        return ""

    email = (
        user_payload.get("email")
        or user_payload.get("email_address")
        or user_payload.get("primary_email_address")
        or ""
    )
    return str(email).strip().lower()


def can_override_providers(user_payload: Optional[dict], settings: Settings) -> bool:
    """Return True if user is in override allowlist."""
    if not user_payload:
        return False

    user_id = str(user_payload.get("sub", "")).strip().lower()
    email = _extract_email(user_payload)

    if user_id and user_id in settings.provider_override_user_ids_set:
        return True
    if email and email in settings.provider_override_emails_set:
        return True
    return False


def allowed_llm_providers(
    container: Container,
    settings: Settings,
    user_payload: Optional[dict],
) -> list[str]:
    """List LLM providers this user can select."""
    available = container.get_available_providers()
    if can_override_providers(user_payload, settings):
        return available

    if settings.fixed_ai_provider in available:
        return [settings.fixed_ai_provider]
    return available[:1]


def allowed_ocr_providers(
    container: Container,
    settings: Settings,
    user_payload: Optional[dict],
) -> list[str]:
    """List OCR providers this user can select."""
    available = container.get_available_ocr_providers()
    if can_override_providers(user_payload, settings):
        return available

    if settings.fixed_ocr_provider in available:
        return [settings.fixed_ocr_provider]
    return available[:1]


def effective_llm_provider(
    requested_provider: str,
    container: Container,
    settings: Settings,
    user_payload: Optional[dict],
) -> str:
    """Resolve the LLM provider actually used for this session."""
    allowed = allowed_llm_providers(container, settings, user_payload)
    if not allowed:
        raise ValueError("Aucun provider LLM configure.")

    if can_override_providers(user_payload, settings) and requested_provider in allowed:
        return requested_provider
    return allowed[0]


def effective_ocr_provider(
    requested_provider: str,
    container: Container,
    settings: Settings,
    user_payload: Optional[dict],
) -> str:
    """Resolve the OCR provider actually used for this session."""
    allowed = allowed_ocr_providers(container, settings, user_payload)
    if not allowed:
        raise ValueError("Aucun provider OCR configure.")

    if can_override_providers(user_payload, settings) and requested_provider in allowed:
        return requested_provider
    return allowed[0]
