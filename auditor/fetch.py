"""Téléchargement et archivage des exports publics du site audité.

Seuls des fichiers de données sont téléchargés ; aucun script du site n'est exécuté (le recalcul.py publié par le site est
archivé comme document, jamais lancé). Chaque fichier est vérifié (taille, encodage, en-têtes), puis archivé avec son
empreinte SHA-256, son URL et l'heure UTC du téléchargement.
"""
from __future__ import annotations

import datetime as dt
import gzip
import hashlib
import json
import shutil
import urllib.request
from pathlib import Path

BASE = 'https://meilleure-agence-nice.fr'
FILES = {
    'parametres.json': '/methode/reproduction/parametres.json',
    'agences.csv': '/methode/reproduction/agences.csv',
    'avis-elementaires.csv': '/methode/reproduction/avis-elementaires.csv',
    'agregats-plateformes.csv': '/methode/reproduction/agregats-plateformes.csv',
    'criteres-sites.csv': '/methode/reproduction/criteres-sites.csv',
    'sources-agences.csv': '/methode/reproduction/sources-agences.csv',
    'lectures.csv': '/methode/reproduction/lectures.csv',                              # journal des lectures (v5.7 du site)
    'relectures-exceptionnelles.csv': '/methode/reproduction/relectures-exceptionnelles.csv',
    'classement-notes.txt': '/classement-notes.txt',
    'methode-details.html': '/methode/details/',
    'calcul.zip': '/methode/code/meilleure-agence-nice-calcul.zip',   # données anonymisées (dédoublonnage, V-14)
}
OPTIONAL = {'sources-agences.csv', 'calcul.zip', 'lectures.csv', 'relectures-exceptionnelles.csv'}          # export ajouté le 15/11/2026 : absent des relevés antérieurs
MAX_BYTES = 50 * 1024 * 1024                # limite de taille par fichier
TIMEOUT = 60
UA = 'nice-agencies-open-audit (+https://github.com/thomasgestioncassini/nice-agencies-open-audit)'


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(1 << 20), b''):
            h.update(chunk)
    return h.hexdigest()


BINARY = {'calcul.zip'}                     # archive ZIP : vérifiée comme ZIP, pas comme texte


def download(url: str, dest: Path) -> dict:
    req = urllib.request.Request(url, headers={'User-Agent': UA, 'Cache-Control': 'no-cache'})
    with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
        status = r.status
        data = r.read(MAX_BYTES + 1)
    if len(data) > MAX_BYTES:
        raise ValueError(f'{url} : fichier plus grand que la limite ({MAX_BYTES} octets)')
    if dest.name in BINARY:
        if not data.startswith(b'PK'):
            raise ValueError(f'{url} : ce n’est pas une archive ZIP')
    else:
        data.decode('utf-8')                 # rejette un fichier qui n'est pas du texte UTF-8
    dest.write_bytes(data)
    return {'url': url, 'http_status': status, 'bytes': len(data)}


def fetch(out_dir: Path, base: str = BASE) -> dict:
    """Télécharge les exports dans out_dir/inputs et renvoie le manifeste des entrées."""
    inp = out_dir / 'inputs'
    inp.mkdir(parents=True, exist_ok=True)
    started = dt.datetime.now(dt.timezone.utc)
    files, errors = {}, []
    for name, path in FILES.items():
        url = f'{base}{path}?audit={int(started.timestamp())}'   # contourne un cache intermédiaire ; URL exacte archivée
        try:
            info = download(url, inp / name)
            info['sha256'] = sha256(inp / name)
            info['fetched_utc'] = dt.datetime.now(dt.timezone.utc).isoformat(timespec='seconds')
            files[name] = info
        except Exception as e:                # noqa: BLE001 — toute erreur est archivée, jamais ignorée
            (errors if name not in OPTIONAL else errors).append({'file': name, 'url': url, 'error': f'{type(e).__name__}: {e}'})
    return {'started_utc': started.isoformat(timespec='seconds'), 'base': base, 'files': files, 'errors': errors}


def archive(src_dir: Path, snap_dir: Path) -> dict:
    """Copie compressée (gzip, déterministe) des entrées dans snapshots/<date>/ ; renvoie les empreintes."""
    snap_dir.mkdir(parents=True, exist_ok=True)
    out = {}
    for p in sorted(src_dir.iterdir()):
        dest = snap_dir / (p.name + '.gz')
        with open(p, 'rb') as f, open(dest, 'wb') as raw:
            with gzip.GzipFile(filename='', mode='wb', fileobj=raw, mtime=0) as g:
                shutil.copyfileobj(f, g)
        out[p.name] = {'sha256': sha256(p), 'archive': dest.name, 'archive_sha256': sha256(dest)}
    return out


def restore(snap_dir: Path, dest: Path) -> dict:
    """Décompresse un relevé archivé et vérifie chaque empreinte contre le manifeste du relevé."""
    manifest = json.loads((snap_dir / 'manifest.json').read_text(encoding='utf-8'))
    dest.mkdir(parents=True, exist_ok=True)
    bad = []
    for name, info in manifest['inputs'].items():
        with gzip.open(snap_dir / info['archive'], 'rb') as g:
            (dest / name).write_bytes(g.read())
        if sha256(dest / name) != info['sha256']:
            bad.append(name)
    if bad:
        raise ValueError(f'empreinte SHA-256 différente du manifeste pour : {", ".join(bad)}')
    return manifest
