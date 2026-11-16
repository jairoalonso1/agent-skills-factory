#!/usr/bin/env python3
"""Deterministic standalone renderer using immutable Frontera SaaS HTML reference DOM.
Input: the JSON accepted by scripts/render-report.ts (type=comparison).
Requires beautifulsoup4>=4.12. Never acquires data itself.
"""
from __future__ import annotations
import argparse, copy, datetime as dt, json, math, statistics
from pathlib import Path
from bs4 import BeautifulSoup, NavigableString

RISK_FREE = .01
PERIODS = [('30 Días',30),('60 Días',60),('90 Días',90),('180 Días',180),('YTD',None),('1 Año',365)]
MONTHS = ['Ene','Feb','Mar','Abr','May','Jun','Jul','Ago','Sep','Oct','Nov','Dic']
COLORS = ['var(--series-1)','var(--series-2)','var(--series-3)','var(--series-4)','var(--series-5)','var(--series-6)','var(--series-7)','var(--series-8)']


def finite(x):
    try:
        v = float(x)
        return v if math.isfinite(v) else None
    except (TypeError, ValueError):
        return None


def pformat(n,dec=2):
    return f'{n:.{dec}f}%' if n is not None else 'N/D'


def nformat(n,dec=2):
    return f'{n:.{dec}f}' if n is not None else 'N/D'


def day(s):
    return dt.date.fromisoformat(s[:10])


def formatted_day(s):
    d=day(s)
    return f'{d.day} de {MONTHS[d.month-1].lower()} de {d.year}'


def validated(payload):
    assert payload.get('type') == 'comparison', 'Only type=comparison supported'
    start=day(payload['startDate']); end=day(payload['cutoff'])
    if start>end: raise ValueError('startDate > cutoff')
    fs=payload['funds']; assert 2<=len(fs)<=8, '2-8 funds/classes required'
    ids=set()
    for f in fs:
        key=(str(f.get('codigo_negocio')),str(f.get('tipo_participacion')))
        if key in ids: raise ValueError('Duplicate fund/class '+str(key))
        ids.add(key)
        raw=f.get('serie') or []
        if len(raw)<2: raise ValueError('Insufficient observations: '+str(key))
        points=[(day(x['fecha']),finite(x.get('nav'))) for x in raw]
        if any(v is None or v<=0 for d,v in points):raise ValueError('NAV must be finite positive')
        if len(set(d for d,v in points))!=len(points):raise ValueError('Duplicate daily date')
        if points!=sorted(points):raise ValueError('Series must be sorted')
        if points[0][0]>start or points[-1][0]<end:raise ValueError('Series does not cover declared period')
    return fs,start,end


def metrics(f,start,end):
    pts=[(day(x['fecha']),float(x['nav'])) for x in f['serie'] if start<=day(x['fecha'])<=end]
    nav=[v for d,v in pts]; dates=[d for d,v in pts]
    rets=[nav[i]/nav[i-1]-1 for i in range(1,len(nav))]
    peak=nav[0]; dd=[]
    for x in nav:
        peak=max(peak,x);dd.append(100*(x/peak-1))
    duration=0; longest=0
    for x in dd:
        duration=0 if x>=-1e-10 else duration+1
        longest=max(longest,duration)
    ordered=sorted(rets)
    def quantile(a,q):
        if not a:return None
        p=(len(a)-1)*q;i=int(p);j=min(len(a)-1,i+1)
        return a[i]+(a[j]-a[i])*(p-i)
    var_index=min(len(ordered)-1,int(math.floor(.05*len(ordered)))) if ordered else None
    threshold=ordered[var_index] if var_index is not None else None
    cvar=statistics.mean(ordered[:var_index+1]) if var_index is not None else None
    m=f.get('metrics') or {}
    result={
        'retorno':finite(m.get('retorno_acumulado_pct')),
        'cagr':finite(m.get('cagr_ea_pct')),
        'vol':finite(m.get('volatilidad_anualizada_pct')),
        'maxdd':finite(m.get('maximum_drawdown_pct')),
        'sharpe':finite(m.get('sharpe_ratio')),
        'sortino':finite(m.get('sortino_ratio')),
        'recovery':finite(m.get('recovery_factor')),
        'max_duration':longest,
        'var':threshold*100 if threshold is not None else None,
        'cvar':cvar*100 if cvar is not None else None,
        'positive':round(sum(x>0 for x in rets)*100/len(nav)) if rets else None,
        'nav':nav,'dates':dates,'drawdowns':dd,
    }
    if result['retorno'] is None:result['retorno']=(nav[-1]/nav[0]-1)*100
    if result['cagr'] is None:result['cagr']=(nav[-1]/nav[0])**(365/max(1,(dates[-1]-dates[0]).days))*100-100
    if result['vol'] is None:result['vol']=statistics.stdev(rets)*math.sqrt(365)*100 if len(rets)>1 else None
    if result['maxdd'] is None:result['maxdd']=min(dd)
    maxdd_precise=abs(min(dd))
    result['calmar']=result['cagr']/maxdd_precise if maxdd_precise>1e-12 else None
    if result['sharpe'] is None and result['vol']:
        result['sharpe']=(result['cagr']-RISK_FREE*100)/result['vol']
    if result['sortino'] is None:
        neg=[x for x in rets if x<0]
        downside=math.sqrt(sum(x*x for x in neg)/len(rets)*365)*100 if rets else 0
        result['sortino']=(result['cagr']-RISK_FREE*100)/downside if downside else None
    return result


def data_asof(m,days,annual=False):
    dates=m['dates'];nav=m['nav']
    end=dates[-1]
    if days is None:
        start=0
    else:
        target=end-dt.timedelta(days=days)
        start=next((i for i,d in enumerate(dates) if d>=target),None)
    if start is None or start==len(dates)-1:return None
    span=(end-dates[start]).days
    if days is not None and span<days-2:return None
    relative=nav[-1]/nav[start]
    return (relative**(365/span)-1)*100 if annual and span else (relative-1)*100


def period_series(m):
    return [data_asof(m,d) for label,d in PERIODS]


def monthly(m):
    grouped={}
    for d,v in zip(m['dates'],m['nav']):
        key=(d.year,d.month)
        if key not in grouped:grouped[key]=[v,v]
        else:grouped[key][1]=v
    ordered=sorted(grouped.items())
    prior=m['nav'][0]
    results={}
    for key,(first,last) in ordered:
        results[key]=(last/prior-1)*100
        prior=last
    return results


def drawdown_periods(m):
    dates=m['dates'];nav=m['nav'];peak=nav[0];peak_ix=0;active=None;out=[]
    for i,v in enumerate(nav):
        if v>=peak:
            if active:
                active['end']=i;out.append(active);active=None
            peak=v;peak_ix=i
        else:
            dd=(v/peak-1)*100
            if active is None:active={'start':peak_ix,'valley':i,'lowest':dd,'end':None}
            elif dd<active['lowest']:
                active['valley']=i;active['lowest']=dd
    if active:out.append(active)
    return sorted(out,key=lambda x:x['lowest'])[:5]


def write_text(el,text):
    if el is None: return
    el.clear();el.append(str(text))


def render_table(template,fs,mets):
    table=template.select_one('table')
    rows=table.select('tr');hdr=rows[0].select('th');body=rows[1:]
    for j,f in enumerate(fs):
        if j+1>=len(hdr):
            new=copy.deepcopy(hdr[-1]);rows[0].append(new);hdr.append(new)
        name=f['nombre'];write_text(hdr[j+1],name)
    for cell in hdr[len(fs)+1:]:cell.decompose()
    rowspec={
      'Retorno (YTD)':lambda m:pformat(m['retorno'],1),
      'CAGR':lambda m:pformat(m['cagr'],1),
      'Volatilidad (Anual.)':lambda m:pformat(m['vol'],1),
      'Max Drawdown':lambda m:pformat(m['maxdd'],1),
      'Duración Max DD (días)':lambda m:f"{m['max_duration']} días",
      'VaR Diario (95%)':lambda m:pformat(m['var']),
      'CVaR Diario (95%)':lambda m:pformat(m['cvar']),
      'Sharpe Ratio':lambda m:nformat(m['sharpe']),
      'Sortino Ratio':lambda m:nformat(m['sortino']),
      'Calmar Ratio':lambda m:nformat(m['calmar']),
      '% Días Positivos':lambda m:pformat(m['positive'],0),
    }
    for row in body:
        cells=row.select('td');key=cells[0].get_text(' ',strip=True) if cells else ''
        if key in rowspec:
            for j,m in enumerate(mets):
                if j+1>=len(cells):
                    new=copy.deepcopy(cells[-1]);row.append(new);cells.append(new)
                write_text(cells[j+1],rowspec[key](m))
            for cell in cells[len(mets)+1:]:cell.decompose()


def update_dates(soup,payload):
    head=soup.select_one('header')
    if head:
        for p in head.select('p'):
            t=p.get_text(' ',strip=True)
            if t.startswith('Rango de Análisis:'):
                write_text(p,f"Rango de Análisis: {payload['startDate']} - {payload['cutoff']} (Período: YTD)" if payload['startDate'].endswith('-01-01') else f"Rango de Análisis: {payload['startDate']} - {payload['cutoff']}")
            if 'de 2026' in t or 'de 2027' in t:
                if p.find_previous('p') and 'Generado el:' in p.find_previous('p').get_text(' ',strip=True):write_text(p,formatted_day(payload.get('generatedAt') or payload['cutoff']))


def render_monthly(soup,fs,mets):
    sections=soup.select('section.individual-asset-section')
    if len(fs)>len(sections):
        for _ in range(len(fs)-len(sections)):
            clone=copy.deepcopy(sections[-1]);sections[-1].insert_after(clone);sections.append(clone)
    for sec in sections[len(fs):]:sec.decompose()
    sections=sections[:len(fs)]
    for sec,f,m in zip(sections,fs,mets):
        write_text(sec.select_one('h2'),f['nombre'])
        if sec.select_one('h2'):sec.select_one('h2')['data-fund-key']=f['id']
        tables=sec.select('table')
        if len(tables)!=2:raise ValueError('Invalid golden master individual section structure')
        mtable,dtable=tables
        grouped=monthly(m)
        tbody=mtable.select_one('tbody');rowprototype=copy.deepcopy(tbody.select_one('tr'))
        tbody.clear()
        for year in sorted({y for y,month in grouped}):
            tr=copy.deepcopy(rowprototype);tds=tr.select('td');write_text(tds[0],year)
            for month in range(1,13):
                n=grouped.get((year,month))
                write_text(tds[month],pformat(n))
                if n is not None:
                    alpha=max(.12,min(.85,abs(n)/3.5))
                    bg=f'rgba(11, 218, 70, {alpha:.3f})' if n>=0 else f'rgba(220, 38, 38, {alpha:.3f})'
                    tds[month]['style']=f'background-color: {bg}; color: rgb(255,255,255);'
                else:tds[month].attrs.pop('style',None)
            ret=data_asof(m,None)
            write_text(tds[13],pformat(ret))
            tbody.append(tr)
        dbody=dtable.select_one('tbody'); dproto=copy.deepcopy(dbody.select_one('tr')) if dbody.select_one('tr') else soup.new_tag('tr')
        dbody.clear()
        for period in drawdown_periods(m):
            tr=copy.deepcopy(dproto);cells=tr.select('td')
            if len(cells)!=6:raise ValueError('Invalid golden master drawdown row template')
            st=period['start'];val=period['valley'];end=period['end'];dates=m['dates']
            values=[formatted_day(dates[st].isoformat()),formatted_day(dates[val].isoformat()),formatted_day(dates[end].isoformat()) if end is not None else 'Sin recuperar',pformat(period['lowest']),f'{(dates[end]-dates[st]).days} días' if end is not None else 'En curso',f'{(dates[end]-dates[val]).days} días' if end is not None else 'En curso']
            for c,v in zip(cells,values):write_text(c,v)
            dbody.append(tr)
        if not dbody.contents:
            tr=soup.new_tag('tr');td=soup.new_tag('td',colspan='6');td.string='Sin episodios de drawdown';tr.append(td);dbody.append(tr)


def render_executive(soup,fs,mets):
    body=soup.select_one('table tbody'); prototype=copy.deepcopy(body.select_one('tr'))
    body.clear()
    filled=prototype.select('td')[1].select_one('svg.star-filled')
    unfilled=prototype.select('td')[1].select_one('svg.star-unfilled')
    if unfilled is None:
        unfilled=copy.deepcopy(filled);unfilled['class']=['w-4','h-4','star-unfilled']
    for j,(f,m) in enumerate(zip(fs,mets)):
        row=copy.deepcopy(prototype);cells=row.select('td')
        namecell=cells[0].select_one('span[title]')
        if not namecell:raise ValueError('Invalid executive template')
        namecell['title']=f['nombre'];write_text(namecell,f['nombre'])
        dot=cells[0].select_one('span[style]')
        if dot:dot['style']=f'background-color: var(--series-{j+1});'
        starroot=cells[1].select_one('div');starroot.clear()
        stars=int(f.get('stars') or 0)
        for k in range(5):starroot.append(copy.deepcopy(filled if k<stars else unfilled))
        vals=[pformat(m['retorno']),pformat(m['cagr']),pformat(m['vol']),pformat(m['maxdd']),nformat(m['sharpe'])]
        for cell,val in zip(cells[2:],vals):write_text(cell,val)
        body.append(row)


def create_svg(soup,series,kind,labels,colors,width=615,height=400):
    """Generate SVG paths from current series, never preserve static reference chart paths."""
    svg=soup.new_tag('svg',attrs={'xmlns':'http://www.w3.org/2000/svg','class':'recharts-surface','viewBox':f'0 0 {width} {height}','width':str(width),'height':str(height),'role':'img','aria-label':kind})
    left,top,right,bottom=60.,15.,width-30.,height-80.
    values=[v for a in series for v in a if v is not None]
    if not values:raise ValueError('Empty chart series')
    vmin,vmax=min(values),max(values)
    if vmin==vmax:vmin-=1;vmax+=1
    pad=(vmax-vmin)*.08;vmin-=pad;vmax+=pad
    if kind=='Drawdown (%)':vmax=max(0,vmax)
    def y(v):return bottom-(v-vmin)/(vmax-vmin)*(bottom-top)
    grid=soup.new_tag('g',attrs={'class':'recharts-cartesian-grid'})
    for tick in range(5):
        value=vmin+(vmax-vmin)*tick/4
        yy=y(value)
        line=soup.new_tag('line',attrs={'x1':str(left),'y1':f'{yy:.2f}','x2':str(right),'y2':f'{yy:.2f}','stroke':'var(--border-color)','stroke-dasharray':'3 3'})
        grid.append(line)
        txt=soup.new_tag('text',attrs={'x':str(left-5),'y':f'{yy+4:.2f}','text-anchor':'end','font-size':'10','fill':'var(--text-secondary)'})
        txt.string=(f'{value:.1f}%' if kind!='Retorno Acumulado (Base 100)' else f'{value:.1f}')
        grid.append(txt)
    if kind != 'Comparación Riesgo vs. Retorno':
        nticks=6 if kind.startswith('Rentabilidades') else 5
        for tick in range(nticks):
            xx=left+(tick+.5)*(right-left)/nticks if kind.startswith('Rentabilidades') else left+tick*(right-left)/(nticks-1)
            label=PERIODS[tick][0] if kind.startswith('Rentabilidades') else ('Inicio' if tick==0 else 'Corte' if tick==nticks-1 else '')
            tag=soup.new_tag('text',attrs={'x':f'{xx:.2f}','y':f'{bottom+20:.2f}','text-anchor':'middle','font-size':'10','fill':'var(--text-secondary)'})
            tag.string=label;grid.append(tag)
    svg.append(grid)
    n=max(len(a) for a in series)
    for idx,values in enumerate(series):
        if kind.startswith('Rentabilidades'):
            stride=(right-left)/len(PERIODS)
            w=stride/(len(series)+1)
            for k,val in enumerate(values):
                if val is None:continue
                baseline=y(0) if vmin<=0<=vmax else bottom
                x=left+k*stride+(idx+.5)*w
                r=soup.new_tag('rect',attrs={'x':f'{x:.2f}','y':f'{min(y(val),baseline):.2f}','width':f'{w*.85:.2f}','height':f'{max(0.3,abs(y(val)-baseline)):.2f}','rx':'3','fill':colors[idx%len(colors)]})
                svg.append(r)
        elif kind=='Comparación Riesgo vs. Retorno':
            xvals=[v[0] for v in series if v[0] is not None]
            xmax=max(xvals) or 1
            if values[0] is None or values[1] is None:continue
            x=left+(values[0]/(xmax*1.15))*(right-left)
            c=soup.new_tag('circle',attrs={'cx':f'{x:.2f}','cy':f'{y(values[1]):.2f}','r':'8','fill':colors[idx%len(colors)],'stroke':'white','stroke-width':'1.5'})
            title=soup.new_tag('title');title.string=labels[idx];c.append(title);svg.append(c)
        else:
            pts=[(left+k*(right-left)/(n-1),y(v)) for k,v in enumerate(values) if v is not None]
            path=soup.new_tag('path',attrs={'d':' '.join(('M' if k==0 else 'L')+f'{x:.2f},{yy:.2f}' for k,(x,yy) in enumerate(pts)),'fill':'none','stroke':colors[idx%len(colors)],'stroke-width':'2','class':'recharts-curve recharts-line-curve'})
            svg.append(path)
    return svg


def refresh_charts(soup,fs,mets):
    labels=[f['nombre'] for f in fs]
    chart_data={
      'Rentabilidades por Período (Simple)':[[data_asof(m,n) for label,n in PERIODS] for m in mets],
      'Rentabilidades por Período (Anualizada)':[[data_asof(m,n,True) for label,n in PERIODS] for m in mets],
      'Comparación Riesgo vs. Retorno':[[m['vol'],m['cagr']] for m in mets],
      'Retorno Acumulado (Base 100)':[m['nav'] for m in mets],
      'Drawdown (%)':[m['drawdowns'] for m in mets],
    }
    for card in soup.select('.chart-card'):
        h=card.select_one('h3')
        if not h:continue
        kind=h.get_text(' ',strip=True)
        if kind not in chart_data:continue
        canvas=card.select_one('svg.recharts-surface[viewbox="0 0 615 400"]')
        if canvas is None:raise ValueError('Original chart SVG is absent: '+kind)
        new=create_svg(soup,chart_data[kind],kind,labels,COLORS)
        canvas.replace_with(new)
        for j,legend in enumerate(card.select('.recharts-legend-item')):
            if j>=len(fs):legend.decompose();continue
            text=legend.select_one('.recharts-legend-item-text')
            if text:write_text(text,labels[j])
        if kind.startswith('Rentabilidades'):
            ticks=card.select('.recharts-cartesian-axis-tick-value')
            for j,(label,num) in enumerate(PERIODS):
                if j<len(ticks):write_text(ticks[j],label)


def render(payload,reference_full,reference_short):
    fs,start,end=validated(payload)
    if all(finite(f.get('score')) is not None for f in fs):
        fs=sorted(fs,key=lambda f:(finite(f['score']),str(f.get('id',''))))
    mets=[metrics(f,start,end) for f in fs]
    full=BeautifulSoup(Path(reference_full).read_text(encoding='utf-8'),'html.parser')
    short=BeautifulSoup(Path(reference_short).read_text(encoding='utf-8'),'html.parser')
    update_dates(full,payload);update_dates(short,payload)
    render_table(full.select('section')[0],fs,mets)
    render_monthly(full,fs,mets)
    render_executive(short,fs,mets)
    refresh_charts(full,fs,mets)
    # Do not alter CSS and institutional footer; provenance records exact source and methodology.
    for soup in (full,short):
        root=soup.select_one('.a4-page-container, .a4-landscape-page-container')
        if root:root['data-report-period']=f"{payload['startDate']}/{payload['cutoff']}"
    return str(full),str(short),mets


def main():
    p=argparse.ArgumentParser();p.add_argument('input');p.add_argument('output_dir');p.add_argument('--templates',default=str(Path(__file__).resolve().parents[1]/'references'/'golden-masters'))
    a=p.parse_args();payload=json.loads(Path(a.input).read_text(encoding='utf-8'))
    full,short,mets=render(payload,Path(a.templates)/'frontera_funds_factsheet.html',Path(a.templates)/'frontera_funds_factsheet (1).html')
    target=Path(a.output_dir);target.mkdir(parents=True,exist_ok=True)
    (target/'comparativo-analitico.html').write_text(full,encoding='utf-8')
    (target/'tabla-ejecutiva.html').write_text(short,encoding='utf-8')
    print(json.dumps({'ok':True,'reports':['comparativo-analitico.html','tabla-ejecutiva.html'],'funds':len(mets),'date_end':payload['cutoff']},ensure_ascii=False))

if __name__=='__main__':main()