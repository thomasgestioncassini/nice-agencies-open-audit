"""Test des clés d'API (phase C) : présence, modèles disponibles, un appel minuscule par fournisseur.
N'affiche JAMAIS les clés. Coût attendu : moins d'un centime par fournisseur."""
import json
import os
import urllib.request


def call(url, data=None, headers=None):
    req = urllib.request.Request(url, data=json.dumps(data).encode() if data else None,
                                 headers={'Content-Type': 'application/json', **(headers or {})})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.loads(r.read())


def openai():
    k = os.environ.get('OPENAI_API_KEY')
    if not k:
        return print('OPENAI_API_KEY : ABSENTE')
    h = {'Authorization': f'Bearer {k}'}
    try:
        models = sorted(m['id'] for m in call('https://api.openai.com/v1/models', headers=h)['data'])
        print('OpenAI : clé acceptée ·', len(models), 'modèles ·', ', '.join(m for m in models if m.startswith(('gpt', 'o')))[:1500])
        cand = [m for m in models if m.startswith('gpt') and 'mini' in m and not any(x in m for x in ('audio', 'realtime', 'tts', 'transcribe', 'search', 'image'))]
        model = sorted(cand)[-1] if cand else None
        if model:
            r = call('https://api.openai.com/v1/responses', {'model': model, 'input': 'Réponds uniquement : OK', 'max_output_tokens': 16}, h)
            print('OpenAI : appel test', model, '· statut', r.get('status'), '· jetons', r.get('usage'))
    except urllib.error.HTTPError as e:
        print('OpenAI : ERREUR', e.code, e.read()[:300])


def gemini():
    k = os.environ.get('GEMINI_API_KEY')
    if not k:
        return print('GEMINI_API_KEY : ABSENTE')
    h = {'x-goog-api-key': k}
    try:
        models = [m['name'].split('/')[-1] for m in call('https://generativelanguage.googleapis.com/v1beta/models?pageSize=200', headers=h)['models']
                  if 'generateContent' in m.get('supportedGenerationMethods', [])]
        print('Gemini : clé acceptée ·', len(models), 'modèles ·', ', '.join(models)[:1500])
        cand = [m for m in models if 'flash' in m and 'lite' not in m and 'image' not in m and 'tts' not in m and 'live' not in m and 'exp' not in m]
        model = sorted(cand)[-1] if cand else (models[0] if models else None)
        if model:
            r = call(f'https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent',
                     {'contents': [{'parts': [{'text': 'Réponds uniquement : OK'}]}], 'generationConfig': {'maxOutputTokens': 16}}, h)
            print('Gemini : appel test', model, '· jetons', r.get('usageMetadata'))
    except urllib.error.HTTPError as e:
        print('Gemini : ERREUR', e.code, e.read()[:300])


openai()
gemini()
