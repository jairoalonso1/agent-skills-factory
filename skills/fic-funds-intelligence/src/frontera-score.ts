/**
 * Frontera Score — reference-compatible port of Frontera SaaS
 * components/FundAnalysisPage.tsx (main), lines 1685–1743.
 *
 * Do not alter weights, ranking, missing-value penalties or quintile
 * boundaries here without an explicitly versioned methodology change.
 */

export type FronteraScoreMetrics = {
  cagr?: number | null;
  sharpeRatio?: number | null;
  sortinoRatio?: number | null;
  maxDrawdown?: number | null;
  recoveryFactor?: number | null;
  volatility?: number | null;
};

export type FronteraScoreInput = {
  id: string;
  metrics?: FronteraScoreMetrics | null;
  itemError?: boolean;
};

export type FronteraScoreResult = {
  id: string;
  score: number;
  stars: 1 | 2 | 3 | 4 | 5;
};

const RATING_METRICS: ReadonlyArray<{
  key: keyof FronteraScoreMetrics;
  weight: number;
  higherIsBetter: boolean;
}> = [
  { key: "cagr", weight: 0.35, higherIsBetter: true },
  { key: "sharpeRatio", weight: 0.25, higherIsBetter: true },
  { key: "sortinoRatio", weight: 0.10, higherIsBetter: true },
  // SaaS comment says higher (less negative) drawdown is better.
  { key: "maxDrawdown", weight: 0.15, higherIsBetter: true },
  { key: "recoveryFactor", weight: 0.10, higherIsBetter: true },
  { key: "volatility", weight: 0.05, higherIsBetter: false },
];

function isFiniteMetric(value: unknown): value is number {
  return typeof value === "number" && Number.isFinite(value);
}

/**
 * Preserves SaaS behavior exactly:
 * - failed items / empty metrics are excluded from scoring;
 * - each metric uses distinct sorted values (ties share a rank);
 * - missing/non-finite metric penalty = eligible item count * weight;
 * - total score ascending; JS stable sort preserves input order on equal scores;
 * - star buckets use fractional quintile boundaries without tie correction;
 * - one eligible item receives score 0 and 3 stars.
 *
 * Returns results only for eligible items, in score order (same as SaaS).
 */
export function calculateFronteraScore(
  items: FronteraScoreInput[],
): FronteraScoreResult[] {
  const eligible = items.filter(
    (item) =>
      item.metrics &&
      Object.keys(item.metrics).length > 0 &&
      !item.itemError,
  );

  if (eligible.length === 0) return [];

  if (eligible.length === 1) {
    return [{ id: eligible[0].id, score: 0, stars: 3 }];
  }

  const scored = eligible.map((item) => {
    let score = 0;

    for (const metric of RATING_METRICS) {
      const itemValue = item.metrics?.[metric.key];

      if (!isFiniteMetric(itemValue)) {
        score += eligible.length * metric.weight;
        continue;
      }

      const values = eligible
        .map((candidate) => candidate.metrics?.[metric.key])
        .filter(isFiniteMetric);

      const sortedValues = [...new Set(values)].sort((a, b) =>
        metric.higherIsBetter ? b - a : a - b,
      );
      const rank = sortedValues.indexOf(itemValue);

      score += (rank !== -1 ? rank + 1 : eligible.length) * metric.weight;
    }

    return { id: item.id, score };
  });

  // Stable sort is intentional: equal composite scores retain source order,
  // matching the original SaaS implementation in modern JavaScript.
  scored.sort((a, b) => a.score - b.score);

  const quintileSize = scored.length / 5;
  return scored.map((item, index) => {
    let stars: 1 | 2 | 3 | 4 | 5 = 5;
    if (index >= quintileSize) stars = 4;
    if (index >= quintileSize * 2) stars = 3;
    if (index >= quintileSize * 3) stars = 2;
    if (index >= quintileSize * 4) stars = 1;
    return { ...item, stars };
  });
}

export const FRONTERA_SCORE_METHODOLOGY = {
  version: "1.0.0",
  weights: {
    cagr: 0.35,
    sharpeRatio: 0.25,
    sortinoRatio: 0.10,
    maxDrawdown: 0.15,
    recoveryFactor: 0.10,
    volatility: 0.05,
  },
} as const;
