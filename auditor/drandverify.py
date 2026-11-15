"""Vérification cryptographique d'une balise drand « quicknet » (schéma bls-unchained-g1-rfc9380).

Signature BLS sur G1 du message SHA-256(numéro de tour sur 8 octets), clé publique du réseau sur G2, épinglée ici.
La clé a été contrôlée sur une balise réelle (tour 33979778, enregistrée le 15/11/2026). Nécessite py_ecc
(requirements-tirage.txt) ; sans cette bibliothèque, le résultat est « non vérifiée », jamais « valide ».
"""
from __future__ import annotations

import hashlib

QUICKNET_PUBKEY = ('83cf0f2896adee7eb8b5f01fcad3912212c437e0073e911fb90022d3e760183c8c4b450b6a0a6c3ac6a5776a2d1064510d'
                   '1fec758c921cc22b0e17e63aaf4bcb5ed66304de9cf809bd274ca73bab4af5a6e9c76a4bc09e76eae8991ef5ece45a')
DST = b'BLS_SIG_BLS12381G1_XMD:SHA-256_SSWU_RO_NUL_'


def verify(round_: int, signature_hex: str) -> bool | None:
    """True : signature authentique ; False : signature fausse ; None : vérification impossible (bibliothèque absente)."""
    try:
        from py_ecc.bls.hash_to_curve import hash_to_G1
        from py_ecc.bls.point_compression import decompress_G1, decompress_G2
        from py_ecc.optimized_bls12_381 import FQ12, G2, final_exponentiate, neg, pairing
    except ImportError:
        return None
    try:
        pk = bytes.fromhex(QUICKNET_PUBKEY)
        pub = decompress_G2((int.from_bytes(pk[:48], 'big'), int.from_bytes(pk[48:], 'big')))
        sig = decompress_G1(int.from_bytes(bytes.fromhex(signature_hex), 'big'))
        h = hash_to_G1(hashlib.sha256(int(round_).to_bytes(8, 'big')).digest(), DST, hashlib.sha256)
        acc = pairing(G2, sig, final_exponentiate=False) * pairing(neg(pub), h, final_exponentiate=False)
        return final_exponentiate(acc) == FQ12.one()
    except Exception:                         # noqa: BLE001 — point invalide, longueur fausse : signature fausse
        return False
