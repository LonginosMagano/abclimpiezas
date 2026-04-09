from pathlib import Path

ROOT = Path('/home/ubuntu/work_abclimpiezas/abclimpiezas')
HTML_FILES = sorted(ROOT.rglob('*.html'))

REPLACEMENTS = [
    ('<meta charset="utf-8"/>', '<meta charset="UTF-8">'),
    ('<meta charset="utf-8">', '<meta charset="UTF-8">'),
    ('value="Alcala de Henares"', 'value="Alcalá de Henares"'),
    ('value="Avila"', 'value="Ávila"'),
    ('Hollín vs Ceniza: Diferencias y Metodos de Limpieza Profesional', 'Hollín vs Ceniza: Diferencias y Métodos de Limpieza Profesional'),
    ('Servicio de urgencia 24 horas, 365 días al ano', 'Servicio de urgencia 24 horas, 365 días al año'),
    ('tecnología laser de última generación', 'tecnología láser de última generación'),
    ('Tecnología de vanguardia: hielo seco, laser, ozono', 'Tecnología de vanguardia: hielo seco, láser, ozono'),
]

count = 0
for path in HTML_FILES:
    text = path.read_text(encoding='utf-8')
    original = text
    for old, new in REPLACEMENTS:
        text = text.replace(old, new)
    if text != original:
        path.write_text(text, encoding='utf-8')
        count += 1

print(f'HTML ajustados: {count}')
