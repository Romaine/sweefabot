from urllib.parse import urlencode
import hashlib
import os
import requests
import sys
import tempfile


def build_hash(text, engine, voice, language, fx=None, fx_level=None):
    fragments = [
        "<engineID>%s</engineID>" % engine,
        "<voiceID>%s</voiceID>" % voice,
        "<langID>%s</langID>" % language,
        ("<FX>%s%s</FX>" % (fx, fx_level)) if fx else '',
        "<ext>mp3</ext>",
        text,
    ]

    return hashlib.md5(''.join(fragments).encode('utf-8')).hexdigest()


def get_tts_url(text, engine, voice, language, fx=None, fx_level=None):
    hash = build_hash(**locals())
    params = [
        ('engine', engine),
        ('language', language),
        ('voice', voice),
        ('text', text),
        ('useUTF8', 1),
        ('fx_type', fx),
        ('fx_level', fx_level),
    ]
    params = [(key, value) for (key, value) in params if (key and value)]

    return 'http://cache-a.oddcast.com/c_fs/%s.mp3?%s' % (
        hash,
        urlencode(params),
    )


def download(text, engine, language, voice, fx=None, fx_level=None):
    url = get_tts_url(**locals())
    temp_name = os.path.join(tempfile.gettempdir(), 'tts-%s.mp3' % hashlib.md5(url.encode('utf-8')).hexdigest())
    if not os.path.exists(temp_name):
        with open(temp_name, 'wb') as outf:
            resp = requests.get(url)
            resp.raise_for_status()
            outf.write(resp.content)
    return temp_name


def test_hash():
    assert build_hash('nnep', engine=4, language=23, voice=1) == '8663a3e4e10637477864d8252704a38d'


if __name__ == '__main__':
    tmp = download(
        text=(' '.join(sys.argv[1:]) or 'nnep'),
        engine=6,
        language=9,
        voice=4,
    )
    print("The File", tmp)
    player = ('afplay' if sys.platform == 'darwin' else 'ffplay')
    os.system('%s %s' % (player, tmp))
