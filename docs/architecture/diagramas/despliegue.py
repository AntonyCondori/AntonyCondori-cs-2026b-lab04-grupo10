"""E6. python3 despliegue.py [--sin-graphviz]

Normal: pip install diagrams y Graphviz instalado (comando dot).
Alternativa local: pip install Pillow; python3 despliegue.py --sin-graphviz.
La alternativa dibuja la misma topología; no usa el motor de Python Diagrams.
La salida se guarda junto al script, independientemente del directorio actual.
"""
from pathlib import Path
import argparse

OUTPUT = Path(__file__).resolve().parent / 'img' / 'despliegue.png'


def diagrams_render():
    from diagrams import Diagram, Cluster, Edge
    from diagrams.onprem.client import Users
    from diagrams.onprem.network import Nginx, Internet
    from diagrams.onprem.compute import Server
    from diagrams.onprem.database import PostgreSQL
    from diagrams.onprem.monitoring import Grafana
    from diagrams.generic.device import Mobile

    with Diagram('EcoRecicla AQP - Vista de despliegue',
                 filename=str(OUTPUT.with_suffix('')), show=False,
                 direction='LR', outformat='png',
                 graph_attr={'pad': '0.5', 'bgcolor': 'white'}):
        usuarios = Users('Vecinos, recicladores\ny municipalidad')
        movil = Mobile('PWA / navegador\ncola local de pendientes')
        with Cluster('Un servidor en la nube - sin alta disponibilidad'):
            proxy = Nginx('HTTPS / Nginx')
            app = Server('Node.js - monolito modular\nIdentidad, Solicitudes, Rutas,\nPuntos y Reportes')
            db = PostgreSQL('PostgreSQL\nun esquema por módulo')
            mon = Grafana('Monitoreo\nfuente de métricas por definir')
        mapas = Internet('Servicio de mapas\nproveedor por definir (S-03)')
        respaldo = Server('Respaldo externo\nacceso restringido')
        usuarios >> Edge(label='interacción') >> movil
        movil >> Edge(label='HTTPS / API REST') >> proxy
        proxy >> Edge(label='HTTP local') >> app
        app >> Edge(label='SQL / transacciones') >> db
        app >> Edge(label='HTTPS / geocodificación', style='dashed') >> mapas
        app >> Edge(label='salud y métricas', style='dotted') >> mon
        db >> Edge(label='copia diaria cifrada', style='dashed') >> respaldo


def local_render():
    """Renderizado alternativo reproducible, sin conexión ni Graphviz."""
    from PIL import Image, ImageDraw, ImageFont
    import math
    img = Image.new('RGB', (1800, 1140), '#f4f7fa')
    draw = ImageDraw.Draw(img)
    font_dir = Path('/usr/share/fonts/truetype/dejavu')
    def font(size, bold=False):
        name = 'DejaVuSans-Bold.ttf' if bold else 'DejaVuSans.ttf'
        try:
            return ImageFont.truetype(str(font_dir / name), size)
        except OSError:
            return ImageFont.truetype(name, size)
    def text(x, y, value, size=23, fill='#203348', bold=False):
        draw.multiline_text((x, y), value, font=font(size, bold), fill=fill, spacing=9)
    def box(rect, title, body, color='#ffffff'):
        x,y,xx,yy = rect
        draw.rounded_rectangle(rect, radius=16, fill=color, outline='#9cb3c5', width=2)
        text(x+20,y+17,title,24,bold=True)
        text(x+20,y+61,body,21)
    def arrow(points, label, pos, dashed=False):
        color='#466981'
        for a,b in zip(points,points[1:]):
            if dashed:
                length=math.dist(a,b)
                for i in range(0,int(length),18):
                    t=i/length; u=min(i+10,length)/length
                    draw.line((a[0]+(b[0]-a[0])*t,a[1]+(b[1]-a[1])*t,
                               a[0]+(b[0]-a[0])*u,a[1]+(b[1]-a[1])*u),fill=color,width=3)
            else:
                draw.line((a,b),fill=color,width=3)
        a,b=points[-2:]; ang=math.atan2(b[1]-a[1],b[0]-a[0])
        draw.polygon([b,(b[0]-15*math.cos(ang-.45),b[1]-15*math.sin(ang-.45)),
                      (b[0]-15*math.cos(ang+.45),b[1]-15*math.sin(ang+.45))],fill=color)
        text(*pos,label,19)
    text(60,35,'EcoRecicla AQP',40,bold=True)
    text(60,94,'Vista de despliegue · MVP · Node.js + PostgreSQL',25)
    draw.rounded_rectangle((430,175,1325,1000),radius=22,fill='#e8f3ed',outline='#72a38a',width=3)
    text(460,200,'UN SERVIDOR EN LA NUBE',25,bold=True)
    text(460,240,'Un despliegue · sin alta disponibilidad',20)
    box((55,325,350,470),'Usuarios','Vecinos\nRecicladores\nMunicipalidad')
    box((55,590,350,770),'PWA / navegador','Celular o equipo web\nCola local de recojos\nReintentos con UUID')
    box((475,585,750,750),'Nginx','Entrada HTTPS\nProxy inverso')
    box((870,565,1270,780),'API Node.js','Monolito modular\nIdentidad · Solicitudes\nRutas · Puntos · Reportes')
    box((875,325,1270,475),'PostgreSQL','Un esquema por módulo\nTransacciones y unicidad')
    box((875,855,1270,975),'Monitoreo','Salud y métricas / Grafana')
    box((1435,575,1750,745),'Mapas externos','Geocodificación\nProveedor pendiente\nSupuesto S-03')
    box((1435,325,1750,475),'Respaldo externo','Copia diaria cifrada\nAcceso restringido')
    arrow([(200,470),(200,590)],'Interacción',(215,513))
    arrow([(350,665),(475,665)],'HTTPS\nAPI REST',(358,595))
    arrow([(750,665),(870,665)],'HTTP\nlocal',(777,602))
    arrow([(1065,565),(1065,475)],'SQL / transacciones',(1080,511))
    arrow([(1065,780),(1065,855)],'Salud / métricas',(1080,803),True)
    arrow([(1270,665),(1435,665)],'HTTPS',(1302,630),True)
    arrow([(1270,395),(1435,395)],'Copia diaria',(1283,358),True)
    text(60,1030,'Decisiones: ADR-001 monolito modular · ADR-002 persistencia · ADR-003 PWA',22,bold=True)
    text(60,1072,'Diseño propuesto. Fuente de métricas y proveedor de mapas por definir. Render local con Pillow.',19)
    img.save(OUTPUT)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--sin-graphviz', action='store_true')
    args = parser.parse_args()
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    if args.sin_graphviz:
        local_render()
    else:
        diagrams_render()
    print(OUTPUT)
