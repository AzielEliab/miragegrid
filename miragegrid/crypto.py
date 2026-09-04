"""Stdlib mesh-VPN primitives: HKDF-SHA256, X25519, ChaCha20-Poly1305.

These are the same families WireGuard uses (RFC 7748, RFC 8439). Implemented
in-tree so the core stays dependency-free. Tested against the public RFC
vectors in ``tests/test_crypto.py``.

Author: Aziel Eliab
"""

from __future__ import annotations

import hashlib
import hmac
import secrets
from typing import Final

P: Final[int] = 2**255 - 19
_MASK255: Final[int] = (1 << 255) - 1
_MASK32: Final[int] = 0xFFFFFFFF
CHACHA20_CONSTANTS: Final[tuple[int, int, int, int]] = (
    0x61707865,
    0x3320646E,
    0x79622D32,
    0x6B206574,
)


def hkdf_sha256(ikm: bytes, *, salt: bytes = b"", info: bytes = b"", length: int = 32) -> bytes:
    """HKDF-SHA256 (RFC 5869)."""
    if not salt:
        salt = b"\x00" * 32
    prk = hmac.new(salt, ikm, hashlib.sha256).digest()
    okm = b""
    block = b""
    counter = 1
    while len(okm) < length:
        block = hmac.new(prk, block + info + bytes([counter]), hashlib.sha256).digest()
        okm += block
        counter += 1
    return okm[:length]


def _rotl32(v: int, n: int) -> int:
    return ((v << n) | (v >> (32 - n))) & _MASK32


def _quarter(s: list[int], a: int, b: int, c: int, d: int) -> None:
    s[a] = (s[a] + s[b]) & _MASK32
    s[d] = _rotl32(s[d] ^ s[a], 16)
    s[c] = (s[c] + s[d]) & _MASK32
    s[b] = _rotl32(s[b] ^ s[c], 12)
    s[a] = (s[a] + s[b]) & _MASK32
    s[d] = _rotl32(s[d] ^ s[a], 8)
    s[c] = (s[c] + s[d]) & _MASK32
    s[b] = _rotl32(s[b] ^ s[c], 7)


def _chacha20_block(key: bytes, counter: int, nonce: bytes) -> bytes:
    if len(key) != 32 or len(nonce) != 12:
        raise ValueError("ChaCha20 requires a 32-byte key and 12-byte nonce")
    state = list(CHACHA20_CONSTANTS)
    state += [int.from_bytes(key[i : i + 4], "little") for i in range(0, 32, 4)]
    state.append(counter & _MASK32)
    state += [int.from_bytes(nonce[i : i + 4], "little") for i in range(0, 12, 4)]
    working = state[:]
    for _ in range(10):
        _quarter(working, 0, 4, 8, 12)
        _quarter(working, 1, 5, 9, 13)
        _quarter(working, 2, 6, 10, 14)
        _quarter(working, 3, 7, 11, 15)
        _quarter(working, 0, 5, 10, 15)
        _quarter(working, 1, 6, 11, 12)
        _quarter(working, 2, 7, 8, 13)
        _quarter(working, 3, 4, 9, 14)
    out = bytearray()
    for i in range(16):
        out.extend(((working[i] + state[i]) & _MASK32).to_bytes(4, "little"))
    return bytes(out)


def chacha20_xor(key: bytes, nonce: bytes, data: bytes, *, counter: int = 1) -> bytes:
    """ChaCha20 (RFC 8439) with a 32-bit counter starting at ``counter``."""
    out = bytearray()
    offset = 0
    block_counter = counter
    while offset < len(data):
        block = _chacha20_block(key, block_counter, nonce)
        take = min(64, len(data) - offset)
        out.extend(a ^ b for a, b in zip(data[offset : offset + take], block[:take]))
        offset += take
        block_counter = (block_counter + 1) & _MASK32
    return bytes(out)


def _poly1305_clamp(r: int) -> int:
    return r & 0x0FFFFFFC0FFFFFFC0FFFFFFC0FFFFFFF


def poly1305_tag(key: bytes, message: bytes) -> bytes:
    """Poly1305 one-time authenticator (RFC 8439). ``key`` is 32 bytes."""
    if len(key) != 32:
        raise ValueError("Poly1305 key must be 32 bytes")
    r = _poly1305_clamp(int.from_bytes(key[:16], "little"))
    s = int.from_bytes(key[16:], "little")
    acc = 0
    p = 2**130 - 5
    for i in range(0, len(message), 16):
        block = message[i : i + 16]
        n = int.from_bytes(block + b"\x01", "little")
        acc = (acc + n) * r % p
    acc = (acc + s) % (1 << 128)
    return acc.to_bytes(16, "little")


def _pad16(data: bytes) -> bytes:
    rem = len(data) % 16
    return data if rem == 0 else data + b"\x00" * (16 - rem)


def aead_encrypt(key: bytes, nonce: bytes, plaintext: bytes, aad: bytes = b"") -> bytes:
    """ChaCha20-Poly1305 encrypt; returns ciphertext || 16-byte tag."""
    otk = _chacha20_block(key, 0, nonce)[:32]
    ciphertext = chacha20_xor(key, nonce, plaintext, counter=1)
    mac_data = _pad16(aad) + _pad16(ciphertext)
    mac_data += len(aad).to_bytes(8, "little") + len(ciphertext).to_bytes(8, "little")
    tag = poly1305_tag(otk, mac_data)
    return ciphertext + tag


def aead_decrypt(key: bytes, nonce: bytes, blob: bytes, aad: bytes = b"") -> bytes:
    """ChaCha20-Poly1305 decrypt. Raises ValueError on tag mismatch."""
    if len(blob) < 16:
        raise ValueError("ciphertext too short")
    ciphertext, tag = blob[:-16], blob[-16:]
    otk = _chacha20_block(key, 0, nonce)[:32]
    mac_data = _pad16(aad) + _pad16(ciphertext)
    mac_data += len(aad).to_bytes(8, "little") + len(ciphertext).to_bytes(8, "little")
    expected = poly1305_tag(otk, mac_data)
    if not hmac.compare_digest(expected, tag):
        raise ValueError("AEAD authentication failed")
    return chacha20_xor(key, nonce, ciphertext, counter=1)


def _inv25519(x: int) -> int:
    return pow(x, P - 2, P)


def x25519(scalar: bytes, u_in: bytes) -> bytes:
    """X25519 DH (RFC 7748). ``scalar`` and ``u_in`` are 32-byte little-endian."""
    if len(scalar) != 32 or len(u_in) != 32:
        raise ValueError("X25519 inputs must be 32 bytes")
    k = int.from_bytes(scalar, "little")
    k &= ~7
    k &= ~(128 << 248)
    k |= 64 << 248
    u = int.from_bytes(u_in, "little") & _MASK255
    x_2, z_2 = 1, 0
    x_3, z_3 = u, 1
    swap = 0
    for t in range(254, -1, -1):
        kt = (k >> t) & 1
        swap ^= kt
        if swap:
            x_2, x_3 = x_3, x_2
            z_2, z_3 = z_3, z_2
        swap = kt
        a = (x_2 + z_2) % P
        aa = (a * a) % P
        b = (x_2 - z_2) % P
        bb = (b * b) % P
        e = (aa - bb) % P
        c = (x_3 + z_3) % P
        d = (x_3 - z_3) % P
        da = (d * a) % P
        cb = (c * b) % P
        x_3 = ((da + cb) % P) ** 2 % P
        z_3 = (u * ((da - cb) % P) ** 2) % P
        x_2 = (aa * bb) % P
        z_2 = (e * (aa + 121665 * e)) % P
    if swap:
        x_2, x_3 = x_3, x_2
        z_2, z_3 = z_3, z_2
    out = (x_2 * _inv25519(z_2)) % P
    return out.to_bytes(32, "little")


X25519_BASEPOINT = b"\x09" + b"\x00" * 31


def x25519_keypair(secret: bytes | None = None) -> tuple[bytes, bytes]:
    """Return ``(secret, public)`` 32-byte X25519 keys."""
    if secret is None:
        secret = secrets.token_bytes(32)
    if len(secret) != 32:
        raise ValueError("X25519 secret must be 32 bytes")
    return secret, x25519(secret, X25519_BASEPOINT)


def node_identity_secret(mesh_seed: bytes, node_id: str) -> bytes:
    """Derive a persistent X25519 secret for a named mesh node."""
    return hkdf_sha256(mesh_seed, salt=b"miragegrid-node-id-v2", info=node_id.encode("utf-8"), length=32)


def fingerprint(public_key: bytes) -> str:
    """Short hex fingerprint of a public key."""
    return hashlib.sha256(public_key).hexdigest()[:16]
