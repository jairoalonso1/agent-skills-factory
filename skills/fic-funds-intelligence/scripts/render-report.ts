import { readFileSync, writeFileSync } from "node:fs";
import { resolve } from "node:path";
import { buildFundReportHtml, buildComparisonHtml, buildExecutiveTableHtml } from "../src/report-html.ts";
import { buildMarketReportHtml } from "../src/market-report-html.ts";
import { applyReportTheme, type ReportProfile, type ReportTheme } from "../src/report-profiles.ts";

const inputPath = process.argv[2];
if (!inputPath) throw new Error("Uso: npm run render -- <input.json> [output.html]");
const input = JSON.parse(readFileSync(resolve(inputPath), "utf8"));
const outputPath = resolve(process.argv[3] || input.output || inputPath.replace(/\.json$/i, ".html"));
const theme: ReportTheme = input.theme ?? "frontera";
const generatedAt = input.generatedAt;
let html: string;
let extraOutput: string | undefined;
let primaryProfile: ReportProfile | "fund" | "market";

function requireDate(value: unknown, name: string): string {
  if (typeof value !== "string" || !/^\d{4}-\d{2}-\d{2}$/.test(value) || Number.isNaN(Date.parse(value + "T00:00:00Z"))) {
    throw new Error(`El campo ${name} (AAAA-MM-DD) es obligatorio; si falta período, el agente debe preguntarlo antes de ejecutar.`);
  }
  return value;
}

switch (input.type) {
  case "fund": {
    requireDate(input.metrics?.fecha_inicio, "metrics.fecha_inicio");
    requireDate(input.cutoff, "cutoff");
    primaryProfile = "fund";
    html = buildFundReportHtml(input.fund, input.points || [], input.metrics || {}, input.cutoff);
    break;
  }
  case "comparison": {
    const startDate = requireDate(input.startDate, "startDate");
    const cutoff = requireDate(input.cutoff, "cutoff");
    if (startDate > cutoff) throw new Error("startDate no puede ser posterior al cutoff.");
    if (!Array.isArray(input.funds) || input.funds.length < 2) throw new Error("Se necesitan al menos dos fondos/clases para comparar.");
    const profile: string = input.reportProfile || (input.executiveTable === false ? "analitico_completo" : "ambos");
    if (!["ambos", "analitico_completo", "tabla_ejecutiva"].includes(profile)) {
      throw new Error(`Perfil no soportado: ${profile}. Usa ambos, analitico_completo o tabla_ejecutiva.`);
    }
    if (profile === "tabla_ejecutiva") {
      primaryProfile = "tabla_ejecutiva";
      html = buildExecutiveTableHtml(input.funds, cutoff, startDate);
    } else {
      primaryProfile = "analitico_completo";
      html = buildComparisonHtml(input.funds, cutoff, startDate);
      if (profile === "ambos") extraOutput = buildExecutiveTableHtml(input.funds, cutoff, startDate);
    }
    break;
  }
  case "market":
    primaryProfile = "market";
    html = buildMarketReportHtml(input.input || input);
    break;
  default:
    throw new Error(`Tipo de informe no soportado: ${String(input.type)}. Usa fund, comparison o market.`);
}
html = applyReportTheme(html, theme, primaryProfile, generatedAt);
writeFileSync(outputPath, html, "utf8");
let executivePath: string | undefined;
if (extraOutput) {
  executivePath = outputPath.replace(/\.html$/i, "-tabla-ejecutiva.html");
  writeFileSync(executivePath, applyReportTheme(extraOutput, theme, "tabla_ejecutiva", generatedAt), "utf8");
}
process.stdout.write(JSON.stringify({ ok: true, type: input.type, profile: input.reportProfile || "ambos", theme, output: outputPath, executiveTable: executivePath || null }) + "\n");
