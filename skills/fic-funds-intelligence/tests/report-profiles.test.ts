import test from "node:test";
import assert from "node:assert/strict";
import { execFileSync } from "node:child_process";
import { mkdtempSync, readFileSync, rmSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { join, resolve } from "node:path";
import { fileURLToPath } from "node:url";
const cwd = resolve(fileURLToPath(new URL("..", import.meta.url)));
const fixture = {
  type: "comparison",
  startDate: "2026-01-01",
  cutoff: "2026-11-12",
  generatedAt: "2026-11-16",
  theme: "sapphire-executive",
  reportProfile: "ambos",
  funds: [
    { id:"A", codigo_negocio:"100", nombre:"Fondo A", administradora:"Admin A", aum:"100 MM", score:1.1, stars:5,
      metrics:{retorno_acumulado_pct:8,cagr_ea_pct:9,volatilidad_anualizada_pct:1,maximum_drawdown_pct:-0.1,sharpe_ratio:2},
      serie:[{fecha:"2026-01-01",nav:100},{fecha:"2026-11-12",nav:108}] },
    { id:"B", codigo_negocio:"200", nombre:"Fondo B", administradora:"Admin B", aum:"90 MM", score:2.4, stars:3,
      metrics:{retorno_acumulado_pct:7,cagr_ea_pct:8,volatilidad_anualizada_pct:2,maximum_drawdown_pct:-0.2,sharpe_ratio:1.5},
      serie:[{fecha:"2026-01-01",nav:100},{fecha:"2026-11-12",nav:107}] },
  ],
};
const run = (data: Record<string, unknown>) => {
 const dir = mkdtempSync(join(tmpdir(), "ff-report-"));
 try {
  const input = join(dir,"input.json"), output = join(dir,"report.html");
  writeFileSync(input,JSON.stringify(data));
  const stdout = execFileSync(process.execPath,["--experimental-strip-types","scripts/render-report.ts",input,output],{cwd,encoding:"utf8"});
  const result = JSON.parse(stdout);
  return { result, html:readFileSync(output,"utf8"), executive:result.executiveTable?readFileSync(result.executiveTable,"utf8"):null };
 } finally { rmSync(dir,{recursive:true,force:true}); }
};
test("comparison produces both deterministic HTML profiles and themed metadata",()=>{
 const {result,html,executive}=run(fixture);
 assert.equal(result.profile,"ambos");
 assert.equal(result.theme,"sapphire-executive");
 assert.match(html,/data-report-profile="analitico_completo"/);
 assert.match(html,/data-theme="sapphire-executive"/);
 assert.ok(html.includes("Fondo A") && html.includes("Fondo B"));
 assert.ok(executive && executive.includes('data-report-profile="tabla_ejecutiva"'));
 assert.ok(executive && executive.includes("Frontera Score"));
});
test("executive-only profile produces only the executive HTML",()=>{
 const {result,html,executive}=run({...fixture,reportProfile:"tabla_ejecutiva"});
 assert.equal(result.executiveTable,null);
 assert.equal(executive,null);
 assert.match(html,/data-report-profile="tabla_ejecutiva"/);
 assert.match(html,/A4 landscape/);
});
test("period is mandatory; no implicit last-year fallback",()=>{
 assert.throws(()=>run({...fixture,startDate:undefined}),/startDate/);
 assert.throws(()=>run({...fixture,cutoff:undefined}),/cutoff/);
 assert.throws(()=>run({...fixture,startDate:"2026-12-01"}),/posterior/);
});
test("unknown report profiles or visual themes fail closed",()=>{
 assert.throws(()=>run({...fixture,reportProfile:"anything"}),/Perfil no soportado/);
 assert.throws(()=>run({...fixture,theme:"disco-neon"}),/Tema inválido/);
});
