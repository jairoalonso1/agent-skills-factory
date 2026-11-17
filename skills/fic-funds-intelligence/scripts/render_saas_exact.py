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
    return f'{n:.{dec}f}%' if n is not None else 'N/A'


def nformat(n,dec=2):
    return f'{n:.{dec}f}' if n is not None else 'N/A'


def day(s):
    return dt.date.fromisoformat(s[:10])


def formatted_day(s):
    d=day(s)
    return f'{d.day} de '+('sept' if d.month==9 else MONTHS[d.month-1].lower())+f' de {d.year}'


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
    """Direct port of SaaS FundAnalysisPage.calculatePerformanceMetrics.

    First observation retains its effectiveDailyRate from complete history.
    YTD price may be normalized to 100, but the first daily return is not
    zero. Connector must supply tasa_diaria at the first dated observation.
    Incoming metrics are diagnostics, not calculation overrides.
    """
    obs=[x for x in f['serie'] if start <= day(x['fecha']) <= end]
    dates=[day(x['fecha']) for x in obs]
    nav=[float(x['nav']) for x in obs]
    first_rate=finite(obs[0].get('tasa_diaria'))
    if first_rate is None:
        raise ValueError('SaaS calculation requires first-day tasa_diaria for '+str(f['id']))
    if first_rate <= -1:
        raise ValueError('Invalid first-day tasa_diaria')
    rets=[first_rate]+[nav[i]/nav[i-1]-1 for i in range(1,len(nav))]
    logs=[math.log1p(first_rate)]+[math.log(nav[i]/nav[i-1]) for i in range(1,len(nav))]
    n=len(nav)
    period_return=nav[-1]/nav[0]-1
    cagr=(1+period_return)**(365/(n-1))-1
    vol=statistics.stdev(logs)*math.sqrt(365)
    peak=-math.inf
    dd=[]
    for price in nav:
        peak=max(price,peak)
        dd.append(price/peak-1)
    maxdd=min(dd)
    current_peak=-math.inf
    start_ix=-1
    longest=0
    for i,price in enumerate(nav):
        if price >= current_peak:
            if start_ix!=-1:
                longest=max(longest,(dates[i-1]-dates[start_ix]).days+1)
                start_ix=-1
            current_peak=price
        elif start_ix==-1:
            start_ix=i-1 if i>0 and nav[i-1]>price else i
    if start_ix!=-1:longest=max(longest,(dates[-1]-dates[start_ix]).days+1)
    ordered=sorted(rets)
    var_ix=math.floor(.05*n)
    var=ordered[var_ix]
    cvar=statistics.mean(ordered[:var_ix+1])
    positive=sum(r>0 for r in rets)/n
    downside=math.sqrt(sum(r*r for r in rets if r<0)/n)*math.sqrt(365)
    result={
        'retorno':period_return*100,
        'cagr':cagr*100,
        'vol':vol*100,
        'maxdd':maxdd*100,
        'sharpe':(cagr-RISK_FREE)/vol if vol else 0,
        'sortino':(cagr-RISK_FREE)/downside if downside else None,
        'recovery':period_return/abs(maxdd) if maxdd else None,
        'calmar':cagr/abs(maxdd) if maxdd else None,
        'max_duration':longest,
        'var':var*100,
        'cvar':cvar*100,
        'positive':positive*100,
        'nav':nav,'dates':dates,'drawdowns':[d*100 for d in dd],
        'history_dates':[day(x['fecha']) for x in (f.get('chart_history') or f['serie'])],
        'history_nav':[float(x['nav']) for x in (f.get('chart_history') or f['serie'])],
        'returns':rets,
    }
    result['upstream_comparison']={}
    mapping={'retorno':'retorno_acumulado_pct','cagr':'cagr_ea_pct',
             'vol':'volatilidad_anualizada_pct','maxdd':'maximum_drawdown_pct',
             'sharpe':'sharpe_ratio','sortino':'sortino_ratio'}
    for key,field in mapping.items():
        reported=finite((f.get('metrics') or {}).get(field))
        if reported is not None and result[key] is not None:
            result['upstream_comparison'][key]=round(result[key]-reported,8)
    return result

def data_asof(m,days,annual=False):
    """Exact SaaS calculateReturnForDays and bar-chart annualization.

    30/60/90/180/365-day returns come from the full available history,
    even when the selected reporting window is YTD. YTD alone uses its
    January-first NAV series and annualizes over inclusive elapsed days.
    """
    if days is None:
        dates=m['dates'];nav=m['nav']
        start=0
        annual_days=(dates[-1]-dates[0]).days+1
    else:
        dates=m['history_dates'];nav=m['history_nav']
        end=dates[-1]
        target=end-dt.timedelta(days=days)
        start=next((i for i,d in enumerate(dates) if d>=target),None)
        annual_days=days
    if start is None or start==len(dates)-1:return None
    relative=nav[-1]/nav[start]
    return (relative**(365/annual_days)-1)*100 if annual and annual_days else (relative-1)*100

def period_series(m):
    return [data_asof(m,d) for label,d in PERIODS]


def monthly(m):
    """FundAnalysisPage.calculateMonthlyReturnsTableData: month first/last."""
    grouped={}
    for d,v in zip(m['dates'],m['nav']):
        key=(d.year,d.month)
        if key not in grouped:grouped[key]=[v,v]
        else:grouped[key][1]=v
    return {key:(last/first-1)*100 for key,(first,last) in grouped.items()}

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
                    max_abs=max((abs(v) for v in grouped.values() if v is not None),default=.1)
                    alpha=min(.85,math.sqrt(abs(n)/max_abs)*.85)
                    bg=f'rgba(11, 218, 70, {alpha:.3f})' if n>=0 else f'rgba(250, 85, 56, {alpha:.3f})'
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
            values=[formatted_day(dates[st].isoformat()),formatted_day(dates[val].isoformat()),formatted_day(dates[end].isoformat()) if end is not None else formatted_day(dates[-1].isoformat()),pformat(period['lowest']),f'{(dates[end]-dates[st]).days} días' if end is not None else f'{(dates[-1]-dates[st]).days} días',f'{(dates[end]-dates[val]).days} días' if end is not None else 'N/A']
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


def _bs_path_tag(soup, template, series_index, kind):
    tag=copy.deepcopy(template)
    tag['stroke']=COLORS[series_index % len(COLORS)]
    tag['data-series-index']=str(series_index)
    tag['aria-label']=kind
    return tag


def _recharts_smooth_line(values,xmin,xmax,ymin,ymax,left=60,top=5,right=585,bottom=270):
    """Port the monotoneX cubic interpolation used by Recharts (d3-shape).

    The validated data array drives all paths; nothing is copied from sample
    chart data. Formatting to 3 decimals is visual, not metric rounding.
    """
    n=len(values)
    if n<2:return ''
    x=[left+(right-left)*i/(n-1) for i in range(n)]
    y=[bottom-(float(v)-ymin)/(ymax-ymin or 1)*(bottom-top) for v in values]
    slopes=[(y[i+1]-y[i])/(x[i+1]-x[i]) for i in range(n-1)]
    def signed(z):return -1 if z<0 else 1
    def interior(a,b):
        p=(a+b)/2
        return (signed(a)+signed(b))*min(abs(a),abs(b),.5*abs(p)) if a*b>0 else 0.
    deriv=[0.]*n
    for i in range(1,n-1):
        deriv[i]=interior(slopes[i-1],slopes[i])
    if n==2:deriv=[slopes[0],slopes[0]]
    else:
        deriv[0]=(3*slopes[0]-deriv[1])/2
        deriv[-1]=(3*slopes[-1]-deriv[-2])/2
    out=[f'M{x[0]:.3f},{y[0]:.3f}']
    for i in range(1,n):
        dx=(x[i]-x[i-1])/3
        out.append(f'C{x[i-1]+dx:.3f},{y[i-1]+dx*deriv[i-1]:.3f},'
                   f'{x[i]-dx:.3f},{y[i]-dx*deriv[i]:.3f},'
                   f'{x[i]:.3f},{y[i]:.3f}')
    return ''.join(out)

def apply_saas_chart_geometry(soup,svg,series,kind,labels,mets):
    """Modify ONLY the data shapes inside the original Recharts DOM.

    This preserves the SaaS clipping paths, classes, axis grids, dimensions,
    legends, chart cards, typography, and inline theme CSS. Unlike the old
    create_svg function, it never substitutes a simplified diagram.
    """
    if kind.startswith('Rentabilidades'):
        allvals=[v for row in series for v in row if v is not None]
        if not allvals:raise ValueError('No return observations: '+kind)
        lo,hi=min(allvals),max(allvals)
        pad=max((hi-lo)*.10,2.0)  # SaaS uses fractional values & >=2pp padding
        ymin,ymax=lo-pad,hi+pad
        groups=svg.select('g.recharts-bar')
        if not groups:raise ValueError('Missing native SaaS Recharts bar geometry')
        initial=[copy.deepcopy(g) for g in groups]
        host=groups[0].parent
        for g in groups:g.decompose()
        for j,values in enumerate(series):
            group=copy.deepcopy(initial[j%len(initial)])
            group['data-series-index']=str(j)
            color=COLORS[j%len(COLORS)]
            bars=group.select('path.recharts-rectangle')
            if not bars:raise ValueError('No Recharts native bar shape')
            for k,bar in enumerate(bars):
                value=values[k] if k<len(values) else None
                if value is None:
                    bar['style']='display:none'
                    bar['data-missing']='true'
                    continue
                x=float(bar.get('x','0')); width=float(bar.get('width','11'))
                y0=270-(0-ymin)/(ymax-ymin)*250
                yy=270-(value-ymin)/(ymax-ymin)*250
                y0=max(20,min(270,y0))  # Recharts clips zero baseline outside the Y domain
                top=min(y0,yy);bottom=max(y0,yy);height=max(.2,bottom-top)
                r=min(4.,height/2,width/2)
                bar['d']=(f'M{x:.3f},{bottom:.3f}L{x:.3f},{top+r:.3f}'
                          f'Q{x:.3f},{top:.3f},{x+r:.3f},{top:.3f}'
                          f'L{x+width-r:.3f},{top:.3f}'
                          f'Q{x+width:.3f},{top:.3f},{x+width:.3f},{top+r:.3f}'
                          f'L{x+width:.3f},{bottom:.3f}Z')
                bar['x']=f'{x:.3f}';bar['y']=f'{top:.3f}'
                bar['height']=f'{height:.3f}';bar['width']=f'{width:.3f}'
                bar['fill']=color
                bar.attrs.pop('style',None)
            host.append(group)
        return
    if kind=='Comparación Riesgo vs. Retorno':
        # Shapes are native Recharts markers, not hand-written <circle> symbols.
        shapes=svg.select('path.recharts-symbols')
        if not shapes:raise ValueError('Missing original SaaS risk-return markers')
        if len(shapes)>len(series):
            for extra in shapes[len(series):]:extra.decompose()
            shapes=shapes[:len(series)]
        elif len(shapes)<len(series):
            prototype=copy.deepcopy(shapes[-1]);host=shapes[-1].parent
            for _ in range(len(series)-len(shapes)):
                clone=copy.deepcopy(prototype);host.append(clone);shapes.append(clone)
        risks=[row[0] for row in series if row[0] is not None]
        returns=[row[1] for row in series if row[1] is not None]
        xmin,xmax=min(risks),max(risks);ymin,ymax=min(returns),max(returns)
        range_x=xmax-xmin;range_y=ymax-ymin
        pad_x=range_x*.2 if range_x else (abs(xmax*.2) or .02)
        pad_y=range_y*.2 if range_y else (abs(ymax*.2) or 2.)
        xmin=max(0,xmin-pad_x);xmax+=pad_x;ymin-=pad_y;ymax+=pad_y
        zvals=[max(0,m['sharpe'] or 0) for m in mets]
        zmin,zmax=min(zvals),max(zvals)
        for j,(shape,row) in enumerate(zip(shapes,series)):
            if row[0] is None or row[1] is None:
                shape['style']='display:none';continue
            x=90+(row[0]-xmin)/(xmax-xmin)*495
            y=300-(row[1]-ymin)/(ymax-ymin)*280
            shape['cx']=f'{x:.3f}';shape['cy']=f'{y:.3f}'
            shape['transform']=f'translate({x:.3f},{y:.3f})'
            shape['name']=labels[j];shape['fill']=COLORS[j%len(COLORS)]
            # ZAxis range [100,800] from FactsheetRiskReturnChart.tsx
            area=100+(zvals[j]-zmin)/(zmax-zmin)*700 if zmax>zmin else 450
            radius=math.sqrt(area/math.pi)
            r=f'{radius:.3f}'
            shape['d']=f'M{r},0A{r},{r},0,1,1,-{r},0A{r},{r},0,1,1,{r},0'
            shape['height']=f'{radius*2:.6f}';shape['width']=f'{radius*2:.6f}'
        return
    paths=svg.select('path.recharts-line-curve')
    if not paths:raise ValueError('Missing original SaaS line chart paths: '+kind)
    if kind=='Drawdown (%)':
        lo=min(min(row) for row in series)
        ymin=min(lo-max(abs(lo*.05),.1),-.01)
        ymax=0
    else:
        allvals=[v for row in series for v in row]
        lo,hi=min(allvals),max(allvals)
        padding=max((hi-lo)*.05,abs(lo*.01),.5)
        ymin,ymax=lo-padding,hi+padding
    if ymax==ymin:ymax=ymin+1
    old=[copy.deepcopy(p) for p in paths]
    host=paths[0].parent
    for p in paths:p.decompose()
    for j,row in enumerate(series):
        tag=_bs_path_tag(soup,old[j%len(old)],j,kind)
        tag['d']=_recharts_smooth_line(row,0,len(row)-1,ymin,ymax)
        tag['name']=labels[j]
        host.append(tag)


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
        apply_saas_chart_geometry(soup,canvas,chart_data[kind],kind,labels,mets)
        for j,legend in enumerate(card.select('.recharts-legend-item')):
            if j>=len(fs):legend.decompose();continue
            text=legend.select_one('.recharts-legend-item-text')
            if text:write_text(text,labels[j])
        if kind.startswith('Rentabilidades'):
            ticks=card.select('.recharts-cartesian-axis-tick-value')
            for j,(label,num) in enumerate(PERIODS):
                if j<len(ticks):write_text(ticks[j],label)


def apply_report_branding(soup):
    """Frontera Eficiente rights notice for both Frontera Funds outputs."""
    header=soup.select_one('header.page-header')
    if header is not None and not header.select_one('.frontera-eficiente-byline'):
        byline=soup.new_tag('p')
        byline['class']=['frontera-eficiente-byline','text-center','text-xs','text-secondary']
        byline.string='Frontera Funds · Un producto de Frontera Eficiente'
        header.append(byline)
    footer=soup.select_one('footer')
    if footer is None:raise ValueError('Missing original SaaS footer')
    for p in list(footer.select('p')):
        if 'info@example.com' in p.get_text(' ',strip=True):
            p.decompose()  # The demo SaaS contact is a placeholder, not an official address.
        elif 'Reporte generado con Frontera Funds' in p.get_text(' ',strip=True):
            write_text(p,'Frontera Funds · Un producto de Frontera Eficiente')
    rights=soup.new_tag('p')
    rights['class']=['text-center','text-xs','text-secondary','frontera-rights']
    rights.string='© Frontera Eficiente. Todos los derechos reservados.'
    footer.append(rights)


def compact_report_chart_labels(soup,fs):
    """Keep native Recharts SVG but fit legends/ticks within 615px chart cards."""
    names={
       (str(x.get('codigo_negocio')),str(x.get('tipo_participacion'))):x
       for x in fs
    }
    def short_name(f):
        code=str(f.get('codigo_negocio',''))
        classe=str(f.get('tipo_participacion',''))
        aliases={
            '69537':'FIC 600',
            '11149':'FIC Fiducoldex',
            '11407':'Alta Liquidez',
            '124209':'Fiducoldex Objetivo',
        }
        source=f.get('nombre','')
        base=aliases.get(code) or source.split(' (Clase')[0].strip()
        if len(base)>28:base=base[:27].rstrip()+'…'
        return base+' · '+classe
    by_full={f['nombre']:short_name(f) for f in fs}
    for card in soup.select('.chart-card'):
        card['data-compact-legends']='true'
        content=card.select_one('div[class*="h-"]')
        if content:
            existing=content.get('style','')
            content['style']=existing.rstrip(';')+'; height: 432px; min-height: 432px;'
        wrap=card.select_one('.recharts-legend-wrapper')
        if wrap:
            wrap['style']='position: absolute; width: calc(100% - 30px); height: auto; left: 15px; bottom: 0; padding-top: 5px;'
        ul=card.select_one('.recharts-default-legend')
        if ul:
            ul['style']='display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 4px 10px; margin: 0; padding: 0; list-style: none; text-align: left;'
        for li in card.select('.recharts-legend-item'):
            li['style']='display: flex; align-items: center; gap: 5px; margin: 0; min-width: 0; white-space: nowrap;'
            text=li.select_one('.recharts-legend-item-text')
            if text:
                full=text.get_text(' ',strip=True)
                short=by_full.get(full,full if len(full)<=31 else full[:30]+'…')
                text['title']=full
                write_text(text,short)
                col=None
                if li.select_one('svg path[fill]'):col=li.select_one('svg path[fill]').get('fill')
                text['style']='font-size: 9px; line-height: 1.25; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; min-width: 0; '+(f'color: {col};' if col else '')
            icon=li.select_one('svg.recharts-surface')
            if icon:
                icon['style']='flex: 0 0 9px; display: inline-block; vertical-align: middle;'
                icon['width']='9';icon['height']='9'
    css="""
    /* Frontera Eficiente: readable, contained SaaS Recharts charts */
    .chart-card { min-width: 0; overflow: hidden; }
    .chart-card svg.recharts-surface text { font-size: 9px !important; }
    .chart-card .recharts-legend-wrapper { z-index: 2; max-width: calc(100% - 20px); }
    .chart-card .recharts-legend-item-text { font-size: 9px !important; line-height: 1.25; }
    .chart-card .recharts-legend-item svg { max-width: 9px; max-height: 9px; }
    .frontera-eficiente-byline, .frontera-rights { font-size: 10px; letter-spacing: 0.01em; }
    @media print {
      .chart-card { break-inside: avoid; page-break-inside: avoid; }
      .chart-card > div[class*="h-"] { height: 432px !important; min-height: 432px !important; }
      .chart-card .recharts-legend-item-text { font-size: 8px !important; }
    }
    """
    style=soup.new_tag('style')
    style.string=css
    if soup.head:soup.head.append(style)
    else:soup.append(style)


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
    compact_report_chart_labels(full,fs)
    for report in (full,short):
        apply_report_branding(report)
    # Original SaaS calculation, DOM and data geometry remain unchanged.
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