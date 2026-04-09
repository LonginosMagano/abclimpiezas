from pathlib import Path
import re
from bs4 import BeautifulSoup, NavigableString

ROOT = Path('/home/ubuntu/work_abclimpiezas/abclimpiezas')
HTML_FILES = sorted(ROOT.rglob('*.html'))

WORD_FIXES = [
    ('Articulo', 'Artículo'),
    ('articulo', 'artículo'),
    ('Metodos', 'Métodos'),
    ('metodos', 'métodos'),
    ('revolucion', 'revolución'),
    ('Revolucion', 'Revolución'),
    ('criogenica', 'criogénica'),
    ('Criogenica', 'Criogénica'),
    ('danos', 'daños'),
    ('Danos', 'Daños'),
    ('lider', 'líder'),
    ('Lider', 'Líder'),
    ('mas', 'más'),
    ('Mas', 'Más'),
    ('alla', 'allá'),
    ('Alla', 'Allá'),
    ('acompanamos', 'acompañamos'),
    ('Acompanamos', 'Acompañamos'),
    ('acompanarle', 'acompañarle'),
    ('Acompanarle', 'Acompañarle'),
    ('acompanamiento', 'acompañamiento'),
    ('Acompanamiento', 'Acompañamiento'),
    ('inspeccion', 'inspección'),
    ('Inspeccion', 'Inspección'),
    ('estara', 'estará'),
    ('Estara', 'Estará'),
    ('escribanos', 'escríbanos'),
    ('Escribanos', 'Escríbanos'),
    ('llamenos', 'llámenos'),
    ('Llamenos', 'Llámenos'),
    ('proteccion', 'protección'),
    ('Proteccion', 'Protección'),
    ('tecnologia', 'tecnología'),
    ('Tecnologia', 'Tecnología'),
    ('evaluacion', 'evaluación'),
    ('Evaluacion', 'Evaluación'),
    ('inspeccion', 'inspección'),
    ('intervencion', 'intervención'),
    ('Intervencion', 'Intervención'),
    ('ademas', 'además'),
    ('Ademas', 'Además'),
    ('practicos', 'prácticos'),
    ('Practicos', 'Prácticos'),
    ('companía', 'compañía'),
    ('Companía', 'Compañía'),
    ('companias', 'compañías'),
    ('Companias', 'Compañías'),
]

PHRASE_FIXES = [
    ('Necesita ayuda tras un incendio?', '¿Necesita ayuda tras un incendio?'),
    ('Trabajan con compañías de seguros en ', '¿Trabajan con compañías de seguros en '),
    ('Cuánto cuesta la limpieza de un incendio en ', '¿Cuánto cuesta la limpieza de un incendio en '),
    ('Cuánto tiempo tarda la limpieza tras un incendio en ', '¿Cuánto tiempo tarda la limpieza tras un incendio en '),
    ('Ofrecen servicio de urgencia en ', '¿Ofrecen servicio de urgencia en '),
    ('Qué técnicas de limpieza utilizan en ', '¿Qué técnicas de limpieza utilizan en '),
    ('Limpian también el olor a humo en ', '¿Limpian también el olor a humo en '),
    ('Necesita limpieza con láser?', '¿Necesita limpieza con láser?'),
]

WORD_PATTERNS = {old: re.compile(rf'(?<![\w/-]){re.escape(old)}(?![\w/-])') for old, _ in WORD_FIXES}
CHARSET_RE = re.compile(r'<meta\s+charset\s*=\s*["\']?[^"\'>\s]+["\']?\s*/?>', re.I)


def normalize_text(text: str) -> str:
    out = text
    for old, new in PHRASE_FIXES:
        out = out.replace(old, new)
    for old, new in WORD_FIXES:
        out = WORD_PATTERNS[old].sub(new, out)
    # Cierra correctamente las interrogaciones abiertas añadidas por patrón.
    out = re.sub(r'¿([^?\n]+?)\?', r'¿\1?', out)
    return out


def process(path: Path) -> bool:
    original = path.read_text(encoding='utf-8')
    html = CHARSET_RE.sub('<meta charset="UTF-8">', original, count=1)
    soup = BeautifulSoup(html, 'html.parser')

    for node in list(soup.find_all(string=True)):
        if node.parent and node.parent.name == 'style':
            continue
        new = normalize_text(str(node))
        if new != str(node):
            node.replace_with(NavigableString(new))

    for tag in soup.find_all(True):
        for attr in ['alt', 'title', 'aria-label', 'placeholder', 'content', 'value']:
            if attr in tag.attrs:
                tag[attr] = normalize_text(str(tag[attr]))

    final = str(soup)
    final = final.replace('<meta charset="utf-8"/>', '<meta charset="UTF-8">').replace('<meta charset="utf-8">', '<meta charset="UTF-8">')
    if final != original:
        path.write_text(final, encoding='utf-8')
        return True
    return False

changed = 0
for file in HTML_FILES:
    if process(file):
        changed += 1
print(f'HTML corregidos en la pasada final: {changed}')
