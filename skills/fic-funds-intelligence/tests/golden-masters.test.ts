import test from "node:test";
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { createHash } from "node:crypto";

const MASTER_ROOT = new URL("../references/golden-masters/", import.meta.url);
const masters = [
  {
    profile: "analitico_completo",
    file: "frontera_funds_factsheet.html",
    hash: "d969138f6774a0b2b8e2d3c30b9b84de23907720b24d5ffcacb8032d9972330e",
    tables: 11,
    paper: /@page\s*\{\s*size:\s*A4\s*;/,
    sections: ["Indicadores Clave de Rendimiento Comparativos", "Gráficos de Rentabilidades por Período", "Universo Riesgo-Retorno", "Gráficos de Rendimiento Comparativos", "Retorno Acumulado (Base 100)", "Drawdown (%)", "Retornos Mensuales (%)", "Peores Períodos de Drawdown"],
  },
  {
    profile: "tabla_ejecutiva",
    file: "frontera_funds_factsheet (1).html",
    hash: "79fd527d57fd135c90b3a4b4ad3f70bfe117c9b305fc2691bb75b3145aee4d2e",
    tables: 1,
    paper: /@page\s*\{\s*size:\s*A4 landscape\s*;/,
    sections: ["Frontera Score", "Retorno", "Anualizado", "Volatilidad", "Drawdown", "Sharpe", "Nota sobre Frontera Score"],
  },
];
for (const master of masters) {
  test(`golden master ${master.profile} preserves original bytes and sections`, () => {
    const bytes = readFileSync(new URL(master.file, MASTER_ROOT));
    const actual = createHash("sha256").update(bytes).digest("hex");
    assert.equal(actual, master.hash, "Los HTML originales no deben ser editados");
    const html = bytes.toString("utf8");
    assert.equal((html.match(/<table\b/gi) ?? []).length, master.tables);
    assert.match(html, master.paper);
    assert.match(html, /Frontera Funds Factsheet/);
    assert.match(html, /theme-sapphire-executive/);
    for (const label of master.sections) assert.ok(html.includes(label), `Sección ausente: ${label}`);
  });
}

test("reference reports represent the same five fund-class identities", () => {
  const full = readFileSync(new URL(masters[0].file, MASTER_ROOT), "utf8");
  const brief = readFileSync(new URL(masters[1].file, MASTER_ROOT), "utf8");
  const identities = [
    ["FIDUCOLDEX OBJETIVO FONDO DE INVERSIÓN COLECTIVA", "518"],
    ["FONDO DE INVERSION COLECTIVA ABIERTO FIC 600", "408"],
    ["CARTERA COLECTIVA ABIERTA DE ALTA LIQUIDEZ", "523"],
    ["FONDO DE INVERSIÓN COLECTIVA FIDUCOLDEX", "405"],
    ["CARTERA COLECTIVA ABIERTA DE ALTA LIQUIDEZ", "518"],
  ];
  for (const [name, cls] of identities) {
    const identity = `${name} (Clase ${cls})`;
    assert.ok(full.includes(identity), `Ausente del analítico: ${identity}`);
    assert.ok(brief.includes(identity), `Ausente del ejecutivo: ${identity}`);
  }
});
