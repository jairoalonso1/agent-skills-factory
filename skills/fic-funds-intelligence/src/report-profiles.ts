/** Two published comparison profiles use ONE financial payload and ONE versioned renderer. */
export type ReportProfile = "analitico_completo" | "tabla_ejecutiva";
export type ReportTheme = "frontera" | "sapphire-executive" | "urban-graphite" | "emerald-silver" | "neutral-terracotta";
const themes: Record<ReportTheme, { background: string; surface: string; heading: string; text: string; accent: string; border: string }> = {
  frontera: { background:"#FFFFFF", surface:"#F9FAFB", heading:"#111827", text:"#1F2937", accent:"#0bda46", border:"#E5E7EB" },
  "sapphire-executive": { background:"#FFFFFF", surface:"#F8F9FA", heading:"#001D3D", text:"#212529", accent:"#FFC300", border:"#DEE2E6" },
  "urban-graphite": { background:"#121212", surface:"#1E1E1E", heading:"#FFFFFF", text:"#E0E0E0", accent:"#00BFFF", border:"#333333" },
  "emerald-silver": { background:"#FFFFFF", surface:"#F7F9F9", heading:"#2C3E50", text:"#34495E", accent:"#1ABC9C", border:"#D5DBDB" },
  "neutral-terracotta": { background:"#FDFCFB", surface:"#FFFFFF", heading:"#2E2E2E", text:"#4A4A4A", accent:"#E07A5F", border:"#EAEAEA" },
};
export function applyReportTheme(
  html: string, theme: ReportTheme, profile: ReportProfile | "fund" | "market", generatedAt?: string,
): string {
  if (!Object.hasOwn(themes, theme)) throw new Error(`Tema inválido: ${String(theme)}`);
  const t = themes[theme];
  const style = [
    `body,.page{background:${t.background};color:${t.text}}`,
    `.page h1,.page h2,.page h3,.brand{color:${t.heading}}`,
    `.kpi,.chart,.chart-card,thead,th{background:${t.surface};border-color:${t.border}}`,
    `td,th,.section,.header,.footer{border-color:${t.border}}`,
    `.stars{color:${t.accent}}`,
  ].join("");
  let result = html.replace("</style>", style + "</style>");
  result = result.replace("<html lang=\"es\">", `<html lang="es" data-report-profile="${profile}" data-theme="${theme}">`);
  if (generatedAt != null) {
    if (!/^\d{4}-\d{2}-\d{2}$/.test(generatedAt)) throw new Error("generatedAt debe ser AAAA-MM-DD");
    const formatted = new Intl.DateTimeFormat("es-CO", { timeZone:"UTC", day:"2-digit", month:"short", year:"numeric" }).format(new Date(generatedAt + "T00:00:00Z"));
    result = result.replace(/(Generado\s+)(\d{1,2}\s+\w+\.?\s+\d{4})/, (_,label) => label + formatted);
  }
  return result;
}
