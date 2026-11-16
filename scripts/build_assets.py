from pathlib import Path
from html import escape
import json, math, re

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / 'assets'
ASSETS.mkdir(parents=True, exist_ok=True)
BG='#0B141B'; PANEL='#101F28'; EDGE='#263D46'; TEAL='#71E5CE'; ORANGE='#FF9B5E'; WHITE='#EBF5F2'; MUTED='#98B2B8'
FONT='DejaVu Sans, sans-serif'; MONO='DejaVu Sans Mono, monospace'

def text(x,y,s,size=20,color=WHITE,weight=400,mono=False,extra=''):
    return f'<text x="{x}" y="{y}" fill="{color}" font-size="{size}" font-weight="{weight}" font-family="{MONO if mono else FONT}" {extra}>{escape(str(s))}</text>'

def rect(x,y,w,h,fill=PANEL,rx=16,stroke=EDGE):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke}"/>'

def svg(w,h,body,label):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{escape(label,quote=True)}"><title>{escape(label)}</title>{body}</svg>'''

def write(name,w,h,body,label):
    (ASSETS/name).write_text(svg(w,h,body,label),encoding='utf-8')

def hero(animated=False, elapsed=6.2):
    """One frame of the Ubuntu workstation scene; elapsed is in seconds."""
    b='<defs><radialGradient id="glow"><stop stop-color="#71E5CE" stop-opacity=".11"/><stop offset="1" stop-color="#71E5CE" stop-opacity="0"/></radialGradient><linearGradient id="desk"><stop stop-color="#172C35"/><stop offset="1" stop-color="#0B141B"/></linearGradient></defs>'
    b+=rect(.5,.5,1279,599,BG,24)
    b+='<ellipse cx="940" cy="315" rx="340" ry="250" fill="url(#glow)"/>'
    b+=text(40,49,'N / 149',20,TEAL,700,True)
    b+=text(172,49,'PERSONAL ENGINEERING STATION',13,MUTED,400,True,extra='letter-spacing="2"')
    b+=text(1218,49,'VIET NAM / UTC+7',13,MUTED,400,True,extra='text-anchor="end"')
    b+='<path d="M40 73 H1240" stroke="#263D46"/>'
    b+=text(42,135,"HELLO, I'M",15,TEAL,400,True,extra='letter-spacing="3"')
    b+=text(36,228,'Nguyen',79,WHITE,700,extra='letter-spacing="-4"')
    b+=text(36,318,'Bao Toan',79,ORANGE,700,extra='letter-spacing="-4"')
    b+=text(42,381,'3RD-YEAR STUDENT',24,TEAL,700)
    b+=text(42,416,'FPT UNIVERSITY',27,WHITE,700)
    b+=text(43,480,'SOFTWARE ENGINEERING / COMPETITIVE PROGRAMMING',15,MUTED,400,True)
    b+=text(648,112,'AFTER HOURS / THE CODING DESK',13,MUTED,400,True,extra='letter-spacing="1.6"')
    # The monitor, stand, keyboard, mouse and coffee make a real illustration.
    b+=rect(644,134,580,290,'#172A33',19,'#36535C')
    b+=rect(653,143,562,272,'#091219',12,'#263D46')
    b+='<path d="M654 178 H1214" stroke="#263D46"/>'
    for x,c in [(674,'#FF9B5E'),(691,'#E5C777'),(708,TEAL)]:
        b+=f'<circle cx="{x}" cy="160" r="4" fill="{c}"/>'
    b+=text(735,165,'toan149@ubuntu: ~/practice/main.cpp',11,MUTED,400,True)
    code=['#include <bits/stdc++.h>','using namespace std;','int main() {','    cout << "Hello, world!";','    return 0;','}']
    char_budget=max(0,int((elapsed-.25)*32))
    cursor_x,cursor_y=713,307
    for i,line in enumerate(code):
        shown=line[:max(0,char_budget)]
        b+=text(677,207+i*20,i+1,12,'#4C6975',400,True)
        color=TEAL if i==0 else '#A8C7F0' if i==1 else '#BDD5E1' if i in (2,5) else ORANGE if i==4 else WHITE
        # SVG collapses leading spaces: position indented code explicitly.
        indent=len(shown)-len(shown.lstrip(' '))
        b+=text(704+indent*8.43,207+i*20,shown.lstrip(' '),14,color,400,True)
        if 0<=char_budget<=len(line):
            cursor_x,cursor_y=704+len(shown)*8.43,207+i*20
        char_budget-=len(line)+1
    if elapsed<3.7 and int(elapsed*3)%2==0:
        b+=f'<rect x="{cursor_x+2}" y="{cursor_y-13}" width="7" height="16" fill="{TEAL}"/>'
    b+='<path d="M674 324 H1194" stroke="#263D46"/>'
    if elapsed>=3.5:
        command='$ g++ main.cpp -std=c++17 && ./a.out'
        shown=command[:max(0,int((elapsed-3.5)*45))]
        b+=text(678,349,shown,13,MUTED,400,True)
    if elapsed>=4.2:
        b+=text(678,380,'Hello, world!' if elapsed>=5.1 else 'Compiling...',15,TEAL,600,True)
        b+=rect(1023,363,170,27,'#132F2E',5,'#2F6059')
        b+=text(1108,382,'BUILD PASSED' if elapsed>=5.1 else 'BUILDING',12,TEAL,700,True,extra='text-anchor="middle"')
    # Progress strip and subtle monitor status light.
    progress=min(1,max(0,(elapsed-4.2)/.9))
    if progress: b+=f'<rect x="674" y="398" width="{520*progress:.1f}" height="2" fill="{TEAL}"/>'
    b+=f'<circle cx="1188" cy="433" r="3" fill="{TEAL}" opacity="{.5+.5*math.sin(elapsed*2)**2:.2f}"/>'
    b+='<path d="M904 424 H966 L978 459 H891 Z" fill="#1C3440" stroke="#34535E"/><rect x="850" y="458" width="174" height="10" rx="5" fill="#263F4A"/>'
    b+='<path d="M708 483 H1055 L1083 514 H686 Z" fill="#142832" stroke="#385662"/>'
    for row in range(3):
        for col in range(16):
            x=718+col*20-row*5; y=488+row*7
            c=TEAL if (col+row*3)==int(elapsed*7)%21 else '#36535E'
            b+=f'<rect x="{x}" y="{y}" width="14" height="3" rx="1" fill="{c}"/>'
    b+='<path d="M638 521 H1235" stroke="#36535E" stroke-width="2"/>'
    # Mouse and cable, placed in the gap between the keyboard and cup.
    b+=rect(1086,482,62,36,'#0D1D26',12,'#233E49')
    b+='<path d="M1117 480 C1117 468 1098 469 1098 456" fill="none" stroke="#4C6D78" stroke-width="1.5"/>'
    b+='<path d="M1116 479 C1100 478 1093 486 1093 499 C1093 509 1101 515 1116 515 C1131 515 1139 509 1139 499 C1139 486 1132 478 1116 479 Z" fill="#1B333E" stroke="#6B9B9F" stroke-width="1.5"/>'
    b+='<path d="M1116 480 V495 M1096 495 H1136" fill="none" stroke="#527780" stroke-width="1"/>'
    b+='<rect x="1113.5" y="483" width="5" height="8" rx="2.5" fill="#71E5CE"/><path d="M1101 508 Q1116 515 1131 508" fill="none" stroke="#71E5CE" stroke-width="1.5" opacity=".65"/>'
    b+='<g transform="translate(35 0)"><ellipse cx="1145" cy="514" rx="53" ry="6" fill="#152B34"/>'
    b+='<path d="M1122 470 H1168 L1162 510 H1128 Z" fill="#FF9B5E"/><path d="M1168 480 C1194 473 1194 499 1164 498" fill="none" stroke="#FF9B5E" stroke-width="6"/>'
    b+=text(1145,496,'</>',12,BG,700,True,extra='text-anchor="middle"')
    for j in range(2):
        dy=math.sin(elapsed*2+j)*4
        b+=f'<path d="M{1135+j*17} {459+dy:.1f} C{1125+j*17} {450+dy:.1f} {1145+j*17} {442+dy:.1f} {1135+j*17} {433+dy:.1f}" fill="none" stroke="#72959B" stroke-width="2" opacity=".6"/>'
    b+='</g>'
    b+='<path d="M40 543 H1240" stroke="#263D46"/>'
    b+=text(42,577,'01 / THINK',12,MUTED,400,True)
    b+=text(247,577,'02 / BUILD',12,MUTED,400,True)
    b+=text(451,577,'03 / REPEAT',12,MUTED,400,True)
    b+=text(1220,577,'A CURIOUS MIND. A TERMINAL OPEN.',12,TEAL,400,True,extra='text-anchor="end"')
    return svg(1280,600,b,'Nguyen Bao Toan · third-year student at FPT University. Ubuntu coding desk: bits/stdc++.h, using namespace std, an animated C++17 program, keyboard, mouse and steaming coffee.')

(ASSETS/'hero.svg').write_text(hero(True))
(ASSETS/'hero-static.svg').write_text(hero(False))

ICONS={
 'codeforces':'<rect x="2" y="17" width="8" height="17" rx="2"/><rect x="14" y="5" width="8" height="29" rx="2"/><rect x="26" y="12" width="8" height="22" rx="2"/>',
 'email':'<rect x="1" y="6" width="34" height="25" rx="4" fill="none" stroke="currentColor" stroke-width="2.5"/><path d="M2 8 L18 21 L34 8" fill="none" stroke="currentColor" stroke-width="2.5"/>',
 'facebook':'<path d="M24 3 H19 C12 3 10 7 10 13 V18 H5 V25 H10 V36 H18 V25 H24 L25 18 H18 V13 C18 11 19 10 21 10 H25 Z"/>',
 'instagram':'<rect x="2" y="2" width="32" height="32" rx="10" fill="none" stroke="currentColor" stroke-width="2.5"/><circle cx="18" cy="18" r="8" fill="none" stroke="currentColor" stroke-width="2.5"/><circle cx="28" cy="8" r="2"/>'
}
links=[('codeforces','01','CODEFORCES','toan149',TEAL),('email','02','EMAIL','toannb149@gmail.com',ORANGE),('facebook','03','FACEBOOK','ngbaotoan1204',TEAL),('instagram','04','INSTAGRAM','_nberton._',ORANGE)]
for key,no,label,value,color in links:
    b=rect(.5,.5,619,119,BG,14)
    b+=f'<g transform="translate(25 41)" color="{color}" fill="{color}">{ICONS[key]}</g>'
    b+=text(84,41,f'{no} / {label}',13,MUTED,400,True,extra='letter-spacing="1.5"')
    b+=text(84,81,value,25,WHITE,600,True)
    b+=text(584,72,'↗',27,color,400,extra='text-anchor="end"')
    write(key+'.svg',620,120,b,label+': '+value)

for num,label,suffix in [('01','ABOUT ME','SOFTWARE + PROBLEM SOLVING'),('02','SOFTWARE ENGINEERING','APPLICATIONS / DATA / TOOLING'),('03','COMPETITIVE PROGRAMMING','ALGORITHMS / CODEFORCES')]:
    b=text(1,39,num,15,ORANGE,700,True)+text(49,39,label,22,WHITE,700)
    b+=text(1279,39,suffix,12,MUTED,400,True,extra='text-anchor="end" letter-spacing="1.5"')
    b+='<path d="M0 60 H1280" stroke="#2C414B"/>'
    write('section-'+num+'.svg',1280,65,b,label)

b=rect(.5,.5,1279,141,BG,15)
b+=text(28,35,'MY TOOLBOX',12,ORANGE,400,True,extra='letter-spacing="1.5"')
tools=[('JAVA','APPLICATIONS'),('JAVASCRIPT','WEB UI'),('SQL SERVER','DATA'),('C++17','ALGORITHMS'),('PYTHON','TOOLING'),('GIT','VERSIONING'),('DOCKER','ENVIRONMENTS'),('UBUNTU','WORKSPACE')]
for i,(name,sub) in enumerate(tools):
    x=25+i*156
    if i:b+=f'<path d="M{x-13} 57 V116" stroke="#263D46"/>'
    b+=text(x,81,name,19,TEAL if i in (0,3) else WHITE,700,True)
    b+=text(x,111,sub,11,MUTED,400,True)
write('toolchain.svg',1280,142,b,'Java, JavaScript, SQL Server, C++17, Python, Git, Docker and Ubuntu')

# Equal visual weight for the two sides of the profile.
b=''
for x,label,title,subtitle,detail,color in [
    (0,'01 / SOFTWARE ENGINEERING','Build useful software.','Applications, databases and developer tools.','Java · SQL · Web · Git · Docker',ORANGE),
    (652,'02 / COMPETITIVE PROGRAMMING','Solve with clarity.','Algorithms, data structures and contest practice.','C++17 · Codeforces · CSES · VNOJ',TEAL)
]:
    b+=rect(x+.5,.5,627,199,BG,15)
    b+=f'<rect x="{x+23}" y="25" width="4" height="28" rx="2" fill="{color}"/>'
    b+=text(x+42,43,label,12,color,700,True,extra='letter-spacing="1"')
    b+=text(x+25,96,title,30,WHITE,700)
    b+=text(x+25,135,subtitle,17,MUTED)
    b+=text(x+25,174,detail,15,color,400,True)
write('disciplines.svg',1280,200,b,'Software engineering: build useful software. Competitive programming: solve with clarity.')

b=rect(.5,.5,1279,111,BG,14)
b+=text(28,40,'build(); solve(); improve();',17,ORANGE,700,True)
b+=text(28,78,'Build with purpose. Solve with clarity.',20,WHITE,400)
b+=text(1251,41,'NGBAOTOAN / TOAN149',12,MUTED,400,True,extra='text-anchor="end"')
b+=text(1251,78,'SOFTWARE ENGINEERING + ALGORITHMS',12,TEAL,400,True,extra='text-anchor="end"')
write('footer.svg',1280,112,b,'Build with purpose. Solve with clarity. Software engineering and algorithms. Nguyen Bao Toan, toan149.')

