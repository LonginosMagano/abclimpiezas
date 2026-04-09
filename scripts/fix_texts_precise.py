from pathlib import Path
import re
from bs4 import BeautifulSoup, NavigableString

ROOT = Path('/home/ubuntu/work_abclimpiezas/abclimpiezas')
HTML_FILES = sorted(ROOT.rglob('*.html'))

# Reemplazos seguros para contenido visible y metadatos, evitando alterar href/src o slugs.
PAIRS = [
    ('Menu', 'Menú'),
    ('Descripcion', 'Descripción'),
    ('descripcion', 'descripción'),
    ('Cuanto', 'Cuánto'),
    ('Que', 'Qué'),
    ('Como', 'Cómo'),
    ('anos', 'años'),
    ('ano', 'año'),
    ('Anos', 'Años'),
    ('Ano', 'Año'),
    ('compania', 'compañía'),
    ('Compania', 'Compañía'),
    ('companias', 'compañías'),
    ('Companias', 'Compañías'),
    ('senor', 'señor'),
    ('Senor', 'Señor'),
    ('manana', 'mañana'),
    ('Manana', 'Mañana'),
    ('espana', 'españa'),
    ('Espana', 'España'),
    ('restauracion', 'restauración'),
    ('Restauracion', 'Restauración'),
    ('informacion', 'información'),
    ('Informacion', 'Información'),
    ('atencion', 'atención'),
    ('Atencion', 'Atención'),
    ('gestion', 'gestión'),
    ('Gestion', 'Gestión'),
    ('solucion', 'solución'),
    ('Solucion', 'Solución'),
    ('tecnica', 'técnica'),
    ('Tecnica', 'Técnica'),
    ('tecnicas', 'técnicas'),
    ('Tecnicas', 'Técnicas'),
    ('tecnico', 'técnico'),
    ('Tecnico', 'Técnico'),
    ('tecnicos', 'técnicos'),
    ('Tecnicos', 'Técnicos'),
    ('rapida', 'rápida'),
    ('Rapida', 'Rápida'),
    ('rapido', 'rápido'),
    ('Rapido', 'Rápido'),
    ('gratuita', 'gratuita'),
    ('gratuito', 'gratuito'),
    ('extension', 'extensión'),
    ('Extension', 'Extensión'),
    ('estandar', 'estándar'),
    ('Estandar', 'Estándar'),
    ('varia', 'varía'),
    ('Varia', 'Varía'),
    ('tramitacion', 'tramitación'),
    ('Tramitacion', 'Tramitación'),
    ('ubicacion', 'ubicación'),
    ('Ubicacion', 'Ubicación'),
    ('generacion', 'generación'),
    ('Generacion', 'Generación'),
    ('evaluacion', 'evaluación'),
    ('Evaluacion', 'Evaluación'),
    ('intervencion', 'intervención'),
    ('Intervencion', 'Intervención'),
    ('eliminacion', 'eliminación'),
    ('Eliminacion', 'Eliminación'),
    ('desodorizacion', 'desodorización'),
    ('Desodorizacion', 'Desodorización'),
    ('prevencion', 'prevención'),
    ('Prevencion', 'Prevención'),
    ('documentacion', 'documentación'),
    ('Documentacion', 'Documentación'),
    ('tecnologia', 'tecnología'),
    ('Tecnologia', 'Tecnología'),
    ('certificacion', 'certificación'),
    ('Certificacion', 'Certificación'),
    ('valoracion', 'valoración'),
    ('Valoracion', 'Valoración'),
    ('vanguardía', 'vanguardia'),
    ('Vanguardía', 'Vanguardia'),
    ('laser', 'láser'),
    ('Laser', 'Láser'),
    ('hollin', 'hollín'),
    ('Hollin', 'Hollín'),
    ('actua', 'actúa'),
    ('Actua', 'Actúa'),
    ('adaptandonos', 'adaptándonos'),
    ('Adaptandonos', 'Adaptándonos'),
    ('asegurese', 'asegúrese'),
    ('Asegurese', 'Asegúrese'),
    ('segúndo', 'segundo'),
    ('sistemas', 'sistemas'),
    ('sistemás', 'sistemas'),
    ('ecologico', 'ecológico'),
    ('Ecologico', 'Ecológico'),
    ('maxima', 'máxima'),
    ('Maxima', 'Máxima'),
    ('minima', 'mínima'),
    ('Minima', 'Mínima'),
    ('mas', 'más'),
    ('Mas', 'Más'),
    ('ademas', 'además'),
    ('Ademas', 'Además'),
    ('tambien', 'también'),
    ('Tambien', 'También'),
    ('despues', 'después'),
    ('Despues', 'Después'),
    ('segun', 'según'),
    ('Segun', 'Según'),
    ('politica', 'política'),
    ('Politica', 'Política'),
    ('telefono', 'teléfono'),
    ('Telefono', 'Teléfono'),
    ('numero', 'número'),
    ('Numero', 'Número'),
    ('practicos', 'prácticos'),
    ('Practicos', 'Prácticos'),
    ('guia', 'guía'),
    ('Guia', 'Guía'),
    ('lider', 'líder'),
    ('Lider', 'Líder'),
    ('diagnostico', 'diagnóstico'),
    ('Diagnostico', 'Diagnóstico'),
    ('Aragon', 'Aragón'),
    ('Leon', 'León'),
    ('Cordoba', 'Córdoba'),
    ('Malaga', 'Málaga'),
    ('Cadiz', 'Cádiz'),
    ('Jaen', 'Jaén'),
    ('Almeria', 'Almería'),
    ('Logrono', 'Logroño'),
    ('Avila', 'Ávila'),
    ('Alcala', 'Alcalá'),
    ('Pais Vasco', 'País Vasco'),
    ('A Coruna', 'A Coruña'),
    ('Coruna', 'Coruña'),
]

# Algunos textos específicos aparecen repetidos en el sitio.
PHRASE_FIXES = [
    ('Servicio de urgencia 24 horas, 365 días al ano', 'Servicio de urgencia 24 horas, 365 días al año'),
    ('Tecnología de vanguardia: hielo seco, laser, ozono', 'Tecnología de vanguardia: hielo seco, láser, ozono'),
    ('tecnología laser de última generación', 'tecnología láser de última generación'),
    ('limpieza con laser', 'limpieza con láser'),
    ('Limpieza con Laser', 'Limpieza con Láser'),
    ('Servicio profesional de limpieza con laser', 'Servicio profesional de limpieza con láser'),
    ('hielo seco, laser y tratamientos de ozono', 'hielo seco, láser y tratamientos de ozono'),
    ('hielo seco, laser, ozono', 'hielo seco, láser, ozono'),
    ('hielo seco, laser y ozono', 'hielo seco, láser y ozono'),
]

WORD_PATTERNS = {old: re.compile(rf'(?<![\w/-]){re.escape(old)}(?![\w/-])') for old, _ in PAIRS}
CHARSET_RE = re.compile(r'<meta\s+charset\s*=\s*["\']?[^"\'>\s]+["\']?\s*/?>', re.I)


def normalize_text(text: str) -> str:
    out = text
    for old, new in PHRASE_FIXES:
        out = out.replace(old, new)
    for old, new in PAIRS:
        out = WORD_PATTERNS[old].sub(new, out)
    # Correcciones finas de signos de apertura interrogativa muy frecuentes.
    out = out.replace('Cuánto cuesta la limpieza de un incendio?', '¿Cuánto cuesta la limpieza de un incendio?')
    out = out.replace('Cuánto tiempo tarda la limpieza post-incendio?', '¿Cuánto tiempo tarda la limpieza post-incendio?')
    out = out.replace('Trabajan con compañías de seguros?', '¿Trabajan con compañías de seguros?')
    out = out.replace('Qué zonas cubren?', '¿Qué zonas cubren?')
    out = out.replace('Necesita limpieza con láser?', '¿Necesita limpieza con láser?')
    return out


def ensure_charset(raw_html: str) -> str:
    if CHARSET_RE.search(raw_html):
        return CHARSET_RE.sub('<meta charset="UTF-8">', raw_html, count=1)
    return raw_html.replace('<head>', '<head>\n<meta charset="UTF-8">', 1)


def process_file(path: Path) -> bool:
    original = path.read_text(encoding='utf-8')
    html = ensure_charset(original)
    soup = BeautifulSoup(html, 'html.parser')

    # Texto visible y scripts JSON-LD.
    for node in list(soup.find_all(string=True)):
        parent = node.parent.name if node.parent else ''
        if parent in {'style'}:
            continue
        new_text = normalize_text(str(node))
        if new_text != str(node):
            node.replace_with(NavigableString(new_text))

    # Metadatos y atributos textuales seguros.
    for tag in soup.find_all(True):
        for attr in ['alt', 'title', 'aria-label', 'placeholder', 'content']:
            if attr in tag.attrs:
                tag[attr] = normalize_text(str(tag[attr]))

    # Mantener el logo blanco para el encabezado/hero en todos los HTML.
    for img in soup.find_all('img'):
        src = img.get('src', '')
        if src.endswith('assets/img/logo.png'):
            img['src'] = src.replace('assets/img/logo.png', 'assets/img/logo-white.png')

    final = str(soup)
    if final != original:
        path.write_text(final, encoding='utf-8')
        return True
    return False


def main() -> None:
    modified = 0
    for path in HTML_FILES:
        if process_file(path):
            modified += 1
    print(f'HTML revisados: {len(HTML_FILES)}')
    print(f'HTML modificados: {modified}')


if __name__ == '__main__':
    main()
