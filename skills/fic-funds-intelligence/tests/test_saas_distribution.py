import copy, json, subprocess, sys, tempfile, unittest
from datetime import date, timedelta
from pathlib import Path
from bs4 import BeautifulSoup

ROOT=Path(__file__).resolve().parents[1]
SCRIPT=ROOT/'scripts'/'render_saas_exact.py'

def fixture(n=5):
    a=[]
    for i in range(n):
        serie=[{'fecha':(date(2026,1,1)+timedelta(days=d)).isoformat(),'nav':100*(1+.0002*(i+1))**d*(.999 if d==11 else 1)} for d in range(45)]
        serie[0]['tasa_diaria']=.0002*(i+1)  # real SaaS first-day rate is never assumed zero
        a.append({'id':f'{i+1}-500','codigo_negocio':str(10000+i),'tipo_participacion':'500','nombre':f'FIC SINTÉTICO {i+1} (Clase 500)','stars':5-i if i<5 else 1,'score':i+1,'serie':serie,'metrics':{'retorno_acumulado_pct':i+1,'cagr_ea_pct':i+2,'volatilidad_anualizada_pct':.2+i*.05,'maximum_drawdown_pct':-.1,'sharpe_ratio':1.5+i,'sortino_ratio':2+i}})
    return {'type':'comparison','startDate':'2026-01-01','cutoff':'2026-02-14','generatedAt':'2026-11-16','funds':a}

def generate(data):
    with tempfile.TemporaryDirectory() as folder:
        root=Path(folder);inp=root/'input.json'
        inp.write_text(json.dumps(data,ensure_ascii=False),encoding='utf-8')
        result=subprocess.run([sys.executable,str(SCRIPT),str(inp),str(root/'out')],text=True,capture_output=True)
        if result.returncode!=0:return result,None,None
        return result,(root/'out'/'comparativo-analitico.html').read_text(),(root/'out'/'tabla-ejecutiva.html').read_text()

class DistributionTests(unittest.TestCase):
    def test_five_classes(self):
        r,f,s=generate(fixture());self.assertEqual(r.returncode,0,r.stderr)
        full=BeautifulSoup(f,'html.parser');brief=BeautifulSoup(s,'html.parser')
        self.assertEqual(len(full.select('table')),11)
        self.assertEqual(len(full.select('section.individual-asset-section')),5)
        self.assertEqual(len(full.select('svg.recharts-surface[viewbox="0 0 615 400"]')),5)
        self.assertEqual(len(brief.select('table')),1)
        self.assertEqual(len(brief.select('table tbody tr')),5)
    def test_varied_class_count(self):
        r,f,s=generate(fixture(2));self.assertEqual(r.returncode,0,r.stderr)
        full=BeautifulSoup(f,'html.parser')
        self.assertEqual(len(full.select('table')),5)
        self.assertEqual(len(full.select('table')[0].select('th')),3)
    def test_live_series_are_not_stale(self):
        original=fixture()
        _,a,_=generate(original)
        changed=copy.deepcopy(original)
        changed['funds'][0]['serie'][10]['nav']*=1.03
        _,b,_=generate(changed)
        self.assertNotEqual([e.get('d') for e in BeautifulSoup(a,'html.parser').select('path.recharts-line-curve')],[e.get('d') for e in BeautifulSoup(b,'html.parser').select('path.recharts-line-curve')])
    def test_requires_period(self):
        payload=fixture();payload.pop('startDate')
        r,_,_=generate(payload);self.assertNotEqual(r.returncode,0)
if __name__=='__main__':unittest.main()