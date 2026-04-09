from pathlib import Path
import re
from PIL import Image

ROOT = Path('/home/ubuntu/work_abclimpiezas/abclimpiezas')
HTML_FILES = sorted(ROOT.rglob('*.html'))
CSS_FILE = ROOT / 'assets' / 'css' / 'global.css'
LOGO_SRC = ROOT / 'assets' / 'img' / 'logo.png'
LOGO_WHITE = ROOT / 'assets' / 'img' / 'logo-white.png'

REPLACEMENTS = [
    ('A Coruna', 'A Coruña'),
    ('Coruna', 'Coruña'),
    ('Espana', 'España'),
    ('anos', 'años'),
    ('Anos', 'Años'),
    ('senor', 'señor'),
    ('Senor', 'Señor'),
    ('compania', 'compañía'),
    ('Compania', 'Compañía'),
    ('companias', 'compañías'),
    ('Companias', 'Compañías'),
    ('manana', 'mañana'),
    ('Manana', 'Mañana'),
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
    ('mas', 'más'),
    ('Mas', 'Más'),
    ('descripcion', 'descripción'),
    ('Descripcion', 'Descripción'),
    ('prevencion', 'prevención'),
    ('Prevencion', 'Prevención'),
    ('evaluacion', 'evaluación'),
    ('Evaluacion', 'Evaluación'),
    ('situacion', 'situación'),
    ('Situacion', 'Situación'),
    ('intervencion', 'intervención'),
    ('Intervencion', 'Intervención'),
    ('eliminacion', 'eliminación'),
    ('Eliminacion', 'Eliminación'),
    ('desodorizacion', 'desodorización'),
    ('Desodorizacion', 'Desodorización'),
    ('proteccion', 'protección'),
    ('Proteccion', 'Protección'),
    ('formacion', 'formación'),
    ('Formacion', 'Formación'),
    ('coordinacion', 'coordinación'),
    ('Coordinacion', 'Coordinación'),
    ('ubicacion', 'ubicación'),
    ('Ubicacion', 'Ubicación'),
    ('actuacion', 'actuación'),
    ('Actuacion', 'Actuación'),
    ('reclamacion', 'reclamación'),
    ('Reclamacion', 'Reclamación'),
    ('documentacion', 'documentación'),
    ('Documentacion', 'Documentación'),
    ('especificas', 'específicas'),
    ('Especificas', 'Específicas'),
    ('especifica', 'específica'),
    ('Especifica', 'Específica'),
    ('continuan', 'continúan'),
    ('Continuan', 'Continúan'),
    ('tecnologia', 'tecnología'),
    ('Tecnologia', 'Tecnología'),
    ('criogenica', 'criogénica'),
    ('Criogenica', 'Criogénica'),
    ('acida', 'ácida'),
    ('Acida', 'Ácida'),
    ('envienos', 'envíenos'),
    ('Envienos', 'Envíenos'),
    ('llamenos', 'llámenos'),
    ('Llamenos', 'Llámenos'),
    ('tambien', 'también'),
    ('Tambien', 'También'),
    ('ultimas', 'últimas'),
    ('Ultimas', 'Últimas'),
    ('ultima', 'última'),
    ('Ultima', 'Última'),
    ('mas alla', 'más allá'),
    ('Pais Vasco', 'País Vasco'),
    ('Aragon', 'Aragón'),
    ('Leon', 'León'),
    ('Cordoba', 'Córdoba'),
    ('Malaga', 'Málaga'),
    ('Cadiz', 'Cádiz'),
    ('Jaen', 'Jaén'),
    ('Almeria', 'Almería'),
    ('Logrono', 'Logroño'),
    ('Coruna', 'Coruña'),
    ('companía', 'compañía'),
]

EXACT_FIXES = [
    ('<meta charset="utf-8">', '<meta charset="UTF-8">'),
    ("<meta charset='utf-8'>", '<meta charset="UTF-8">'),
    ('<meta charset="UTF-8"/>', '<meta charset="UTF-8">'),
    ("<meta charset='UTF-8'>", '<meta charset="UTF-8">'),
    ('assets/img/logo.png', 'assets/img/logo-white.png'),
    ('../assets/img/logo.png', '../assets/img/logo-white.png'),
    ('../../assets/img/logo.png', '../../assets/img/logo-white.png'),
]

WORD_PATTERN_CACHE = {}

def replace_word_boundaries(text: str, old: str, new: str) -> str:
    if old not in WORD_PATTERN_CACHE:
        WORD_PATTERN_CACHE[old] = re.compile(rf'(?<![\w\-]){re.escape(old)}(?![\w\-])')
    return WORD_PATTERN_CACHE[old].sub(new, text)


def ensure_charset(text: str) -> str:
    charset_pattern = re.compile(r'<meta\s+charset\s*=\s*["\']?[^"\'>\s]+["\']?\s*/?>', re.I)
    if charset_pattern.search(text):
        text = charset_pattern.sub('<meta charset="UTF-8">', text, count=1)
    else:
        text = text.replace('<head>', '<head>\n<meta charset="UTF-8">', 1)
    return text


def fix_html_file(path: Path) -> bool:
    original = path.read_text(encoding='utf-8')
    text = original
    text = ensure_charset(text)
    for old, new in EXACT_FIXES:
        text = text.replace(old, new)
    for old, new in REPLACEMENTS:
        text = replace_word_boundaries(text, old, new)

    # Limpieza adicional de preguntas y expresiones frecuentes.
    text = text.replace('Cuanto ', 'Cuánto ')
    text = text.replace('Cuanto?', 'Cuánto?')
    text = text.replace('Que ', 'Qué ')
    text = text.replace('Que?', 'Qué?')
    text = text.replace('Como ', 'Cómo ')
    text = text.replace('Como?', 'Cómo?')
    text = text.replace('Si, ', 'Sí, ')
    text = text.replace('si es necesario', 'si es necesario')
    text = text.replace('dia', 'día')
    text = text.replace('dias', 'días')
    text = text.replace('dia.', 'día.')
    text = text.replace('diagnostico', 'diagnóstico')
    text = text.replace('maxima', 'máxima')
    text = text.replace('minima', 'mínima')
    text = text.replace('Practicos', 'Prácticos')
    text = text.replace('practicos', 'prácticos')
    text = text.replace('Guia', 'Guía')
    text = text.replace('guia', 'guía')
    text = text.replace('lider', 'líder')
    text = text.replace('Lider', 'Líder')
    text = text.replace('despues', 'después')
    text = text.replace('Despues', 'Después')
    text = text.replace('dejo', 'dejó')
    text = text.replace('fabrica', 'fábrica')
    text = text.replace('también el olor', 'también el olor')
    text = text.replace('politica', 'política')
    text = text.replace('Politica', 'Política')
    text = text.replace('telefono', 'teléfono')
    text = text.replace('Telefono', 'Teléfono')
    text = text.replace('numero', 'número')
    text = text.replace('Numero', 'Número')
    text = text.replace('poblacion', 'población')
    text = text.replace('Poblacion', 'Población')
    text = text.replace('solida', 'sólida')
    text = text.replace('criticos', 'críticos')
    text = text.replace('critico', 'crítico')
    text = text.replace('criticas', 'críticas')
    text = text.replace('critica', 'crítica')
    text = text.replace('exito', 'éxito')
    text = text.replace('economico', 'económico')
    text = text.replace('economica', 'económica')
    text = text.replace('caracteristicas', 'características')
    text = text.replace('segun', 'según')
    text = text.replace('segun', 'según')
    text = text.replace('metodos', 'métodos')
    text = text.replace('metodo', 'método')
    text = text.replace('Tambien', 'También')
    text = text.replace('ubicación en menos', 'ubicación en menos')
    text = text.replace('introduccion', 'introducción')
    text = text.replace('proteccion', 'protección')
    text = text.replace('resolucion', 'resolución')
    text = text.replace('cooperacion', 'cooperación')
    text = text.replace('restauración post-incendio. Mas', 'restauración post-incendio. Más')
    text = text.replace('Mas de', 'Más de')
    text = text.replace('mas de', 'más de')
    text = text.replace('mas avanzada', 'más avanzada')
    text = text.replace('mas avanzadas', 'más avanzadas')
    text = text.replace('mas alta', 'más alta')
    text = text.replace('mas siniestros', 'más siniestros')
    text = text.replace('mas alla', 'más allá')
    text = text.replace('esta disenado', 'está diseñado')
    text = text.replace('disenado', 'diseñado')
    text = text.replace('Disenado', 'Diseñado')
    text = text.replace('disenamos', 'diseñamos')
    text = text.replace('Disenamos', 'Diseñamos')
    text = text.replace('danos', 'daños')
    text = text.replace('Danos', 'Daños')

    if text != original:
        path.write_text(text, encoding='utf-8')
        return True
    return False


def fix_css() -> bool:
    original = CSS_FILE.read_text(encoding='utf-8')
    text = original
    replacements = {
        '.hero { padding: 60px 0 50px; background: #fff; }': '.hero { padding: 60px 0 50px; background: #1A2B5F; }',
        '.hero h1 { margin-bottom: 20px; color: #1A2B5F; }': '.hero h1 { margin-bottom: 20px; color: #FFFFFF; }',
        '.hero-desc { font-size: 1.15rem; color: #555; margin-bottom: 30px; line-height: 1.8; }': '.hero-desc { font-size: 1.15rem; color: rgba(255,255,255,0.92); margin-bottom: 30px; line-height: 1.8; }',
        '.btn-secondary { display: inline-flex; align-items: center; gap: 8px; background: transparent; color: #1A2B5F; padding: 14px 32px; border-radius: 8px; font-family: \'Montserrat\', sans-serif; font-weight: 700; font-size: 1rem; border: 2px solid #1A2B5F; transition: all .3s; cursor: pointer; }': '.btn-secondary { display: inline-flex; align-items: center; gap: 8px; background: transparent; color: #FFFFFF; padding: 14px 32px; border-radius: 8px; font-family: \'Montserrat\', sans-serif; font-weight: 700; font-size: 1rem; border: 2px solid rgba(255,255,255,0.9); transition: all .3s; cursor: pointer; }',
        '.btn-secondary:hover { background: #1A2B5F; color: #fff; transform: translateY(-2px); }': '.btn-secondary:hover { background: #FFFFFF; color: #1A2B5F; transform: translateY(-2px); }',
        '.trust-item { display: flex; align-items: center; gap: 8px; font-size: 0.85rem; color: #666; }': '.trust-item { display: flex; align-items: center; gap: 8px; font-size: 0.85rem; color: rgba(255,255,255,0.82); }',
    }
    for old, new in replacements.items():
        text = text.replace(old, new)

    additions = '\n.hero .section-label, .hero .section-subtitle { color: rgba(255,255,255,0.82); }\n.hero .hero-badge { background: rgba(255,255,255,0.12); color: #FFFFFF; }\n.hero .hero-badge svg { fill: #00A878; }\n.hero .hero-content a { color: inherit; }\n.hero .hero-image-badge { border-color: rgba(255,255,255,0.85); }\n'
    if '.hero .hero-badge { background: rgba(255,255,255,0.12); color: #FFFFFF; }' not in text:
        text += additions

    if text != original:
        CSS_FILE.write_text(text, encoding='utf-8')
        return True
    return False


def build_white_logo() -> None:
    img = Image.open(LOGO_SRC).convert('RGBA')
    pixels = img.load()
    for y in range(img.height):
        for x in range(img.width):
            r, g, b, a = pixels[x, y]
            if a == 0:
                continue
            if r < 70 and g < 70 and b < 70:
                pixels[x, y] = (255, 255, 255, a)
    img.save(LOGO_WHITE)


def main() -> None:
    changed = 0
    for html in HTML_FILES:
        if fix_html_file(html):
            changed += 1
    css_changed = fix_css()
    build_white_logo()
    print(f'HTML modificados: {changed}')
    print(f'CSS modificado: {css_changed}')
    print(f'Logo blanco generado: {LOGO_WHITE}')


if __name__ == '__main__':
    main()
