from __future__ import annotations

import re
from dataclasses import dataclass

import boto3
from botocore.config import Config

from app.core.config import settings


@dataclass(frozen=True)
class PresignedUrl:
    url: str
    key: str
    bucket: str
    expiresIn: int


_SAFE_KEY_PART = re.compile(r"^[0-9A-Za-z._=-]+$")


def _clean_env(value: str | None) -> str | None:
    if value is None:
        return None
    v = value.strip()
    if not v:
        return None
    if len(v) >= 2 and v[0] == v[-1] and v[0] in ("'", '"'):
        v = v[1:-1].strip()
    return v or None


def _key_part(value: str) -> str:
    v = value.strip()
    if not v or not _SAFE_KEY_PART.match(v):
        raise ValueError("Invalid key component")
    return v


def build_s3_key_from_xy(x: str, y: str) -> str:
    x_part = _key_part(x)
    y_part = _key_part(y)

    prefix = settings.s3_prefix.strip("/")
    base = f"grid_x{x_part}_y{y_part}.png"
    return f"{prefix}/{base}" if prefix else base


def _client():
    access_key_id = _clean_env(settings.aws_access_key_id)
    secret_access_key = _clean_env(settings.aws_secret_access_key)
    region = _clean_env(settings.aws_region) or "eu-north-1"

    # IMPORTANT: Use the regional endpoint to avoid 301/307 redirects from the
    # global endpoint (s3.amazonaws.com). Redirects change the Host header and
    # break SigV4 presigned URLs.
    endpoint_url = f"https://s3.{region}.amazonaws.com"

    return boto3.client(
        "s3",
        region_name=region,
        endpoint_url=endpoint_url,
        aws_access_key_id=access_key_id,
        aws_secret_access_key=secret_access_key,
        config=Config(signature_version="s3v4", s3={"addressing_style": "virtual"}),
    )


def presign_get_object(key: str) -> PresignedUrl:
    bucket = _clean_env(settings.s3_bucket)
    if not bucket:
        raise RuntimeError("S3 bucket is not configured")

    url = _client().generate_presigned_url(
        ClientMethod="get_object",
        Params={"Bucket": bucket, "Key": key},
        ExpiresIn=settings.presign_expires_seconds,
    )

    return PresignedUrl(
        url=url,
        key=key,
        bucket=bucket,
        expiresIn=settings.presign_expires_seconds,
    )
