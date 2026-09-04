"""RFC vectors for X25519 and ChaCha20-Poly1305."""

from __future__ import annotations

from miragegrid.crypto import (
    aead_decrypt,
    aead_encrypt,
    fingerprint,
    hkdf_sha256,
    x25519,
    x25519_keypair,
)


def test_x25519_rfc7748() -> None:
    alice_sk = bytes.fromhex(
        "77076d0a7318a57d3c16c17251b26645df4c2f87ebc0992ab177fba51db92c2a"
    )
    bob_sk = bytes.fromhex(
        "5dab087e624a8a4b79e17f8b83800ee66f3bb1292618b6fd1c2f8b27ff88e0eb"
    )
    alice_pk = x25519_keypair(alice_sk)[1]
    bob_pk = x25519_keypair(bob_sk)[1]
    assert alice_pk.hex() == (
        "8520f0098930a754748b7ddcb43ef75a0dbf3a0d26381af4eba4a98eaa9b4e6a"
    )
    assert bob_pk.hex() == (
        "de9edb7d7b7dc1b4d35b61c2ece435373f8343c85b78674dadfc7e146f882b4f"
    )
    shared_a = x25519(alice_sk, bob_pk)
    shared_b = x25519(bob_sk, alice_pk)
    assert shared_a == shared_b
    assert shared_a.hex() == (
        "4a5d9d5ba4ce2de1728e3bf480350f25e07e21c947d19e3376f09b3c1e161742"
    )


def test_chacha20_poly1305_rfc8439() -> None:
    key = bytes.fromhex(
        "808182838485868788898a8b8c8d8e8f909192939495969798999a9b9c9d9e9f"
    )
    nonce = bytes.fromhex("070000004041424344454647")
    aad = bytes.fromhex("50515253c0c1c2c3c4c5c6c7")
    plaintext = (
        b"Ladies and Gentlemen of the class of '99: If I could offer you only one "
        b"tip for the future, sunscreen would be it."
    )
    blob = aead_encrypt(key, nonce, plaintext, aad)
    expected = bytes.fromhex(
        "d31a8d34648e60db7b86afbc53ef7ec2a4aded51296e08fea9e2b5a736ee62d6"
        "3dbea45e8ca9671282fafb69da92728b1a71de0a9e060b2905d6a5b67ecd3b36"
        "92ddbd7f2d778b8c9803aee328091b58fab324e4fad675945585808b4831d7bc"
        "3ff4def08e4b7a9de576d26586cec64b6116"
        "1ae10b594f09e26a7e902ecbd0600691"
    )
    assert blob == expected
    assert aead_decrypt(key, nonce, blob, aad) == plaintext


def test_aead_rejects_tamper() -> None:
    blob = bytearray(aead_encrypt(b"k" * 32, b"n" * 12, b"hello"))
    blob[-1] ^= 1
    try:
        aead_decrypt(b"k" * 32, b"n" * 12, bytes(blob))
    except ValueError:
        return
    raise AssertionError("tamper should fail")


def test_hkdf_and_fingerprint_lengths() -> None:
    out = hkdf_sha256(b"ikm", salt=b"salt", info=b"info", length=42)
    assert len(out) == 42
    assert len(fingerprint(b"\x01" * 32)) == 16
