# Contratos de datos para informes

Los renderizadores reciben datos estructurados y no consultan fuentes externas. La Skill/agent obtiene los datos mediante las herramientas disponibles y entrega un JSON con uno de estos contratos.

## Ficha individual (`type: fund`)

```json
{
  "type": "fund",
  "fund": { "nombre_patrimonio": "Fondo", "nombre_entidad": "Administradora", "codigo_negocio": "123", "numero_inversionistas": 100, "valor_fondo_cierre_dia_t": 1000000 },
  "points": [{ "fecha": "2026-01-02", "nav": 100.0 }],
  "metrics": { "fecha_inicio": "2026-01-01", "fecha_fin": "2026-11-11", "periodo_dias": 314, "retorno_acumulado_pct": 8.2, "cagr_ea_pct": 9.1, "volatilidad_anualizada_pct": 0.8, "maximum_drawdown_pct": -0.1, "sharpe_ratio": 2.1, "sortino_ratio": 2.8, "recovery_factor": 4.5 },
  "cutoff": "2026-11-11"
}
```

`points` usa `fecha` y `nav`; `nav` debe ser la serie ya reconstruida/normalizada conforme a la fuente y metodología que se declara en el informe. No volver a reconstruir NAV dentro del renderizador.

## Peer Group (`type: comparison`)\n\nAdemás de los campos obligatorios del JSON, admite `reportProfile: "ambos" | "analitico_completo" | "tabla_ejecutiva"`, `theme: "frontera" | "sapphire-executive" | "urban-graphite" | "emerald-silver" | "neutral-terracotta"`, y `generatedAt: "AAAA-MM-DD"` para pruebas repetibles. `startDate` y `cutoff` son **obligatorios** y no se completan con supuestos. Los dos perfiles usan **exactamente las mismas métricas y series**.

```json
{
  "type": "comparison",
  "startDate": "2026-01-01",
  "cutoff": "2026-11-11",
  "funds": [{
    "id": "123", "codigo_negocio": "123", "nombre": "Fondo A", "administradora": "Administradora", "aum": "$100 MM",
    "score": 1.2, "stars": 5,
    "metrics": { "retorno_acumulado_pct": 8.2, "cagr_ea_pct": 9.1, "volatilidad_anualizada_pct": 0.8, "maximum_drawdown_pct": -0.1, "sharpe_ratio": 2.1, "sortino_ratio": 2.8, "recovery_factor": 4.5 },
    "serie": [{ "fecha": "2026-01-02", "nav": 100 }, { "fecha": "2026-01-03", "nav": 100.01 }]
  }]
}
```

Cada fondo debe representar una única clase de participación. No mezclar clases de un mismo fondo. Las series pueden comenzar en fechas diferentes; el informe las normaliza individualmente a base 100 y advierte sobre diferencias de inicio.

El `score` y `stars` deben calcularse antes de renderizar con `src/frontera-score.ts`, usando las métricas y las unidades esperadas por ese módulo.

## Inteligencia de mercado (`type: market`)

```json
{
  "type": "market",
  "input": {
    "fechaCorte": "2026-11-11", "fechaInicio": "2026-10-12",
    "ranking": { "ranking": [], "criterio_ordenamiento": "rentabilidad_anual", "aum_minimo_filtro_cop": 0 },
    "marketShare": { "tabla_market_share": [], "aum_total_universo_cop": 0, "inversionistas_totales_universo": 0 },
    "flows": { "resultados": [] },
    "alerts": { "alertas_liquidez": [] }
  }
}
```

## Procedencia obligatoria

La Skill debe conservar junto al JSON o en el contexto del informe: proveedor, dataset/endpoint, fecha de recuperación, fecha de corte del dato, filtros, clase de participación y advertencias de cobertura. No completar vacíos con estimaciones silenciosas.
