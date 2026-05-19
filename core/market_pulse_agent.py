from typing import List

from core.models import MarketScoutReport, PulseReport, StrategyOption, UserInput


class MarketPulseAgent:
    """
    Observes market conditions.

    Current V2:
    - static demo assumptions
    - no live data

    Future versions may connect:
    - live price
    - EMA7 / EMA25 / EMA50
    - volatility
    - liquidity
    - price deviation
    - APY changes
    - maturity dates
    - exit conditions
    - Morpho vault data
    - Kamino lending / liquidity data

    The Market Pulse Agent does not trade.
    It only produces review signals.
    """

    def analyze(
        self,
        user_input: UserInput,
        market_report: MarketScoutReport,
        strategies: List[StrategyOption],
    ) -> PulseReport:
        watch_items = []
        review_signals = []

        if market_report.market_status == "weak_or_unclear":
            pulse_status = "unstable"
            summary = (
                "Market conditions or user understanding are too unclear for confident RWA exposure."
            )
            watch_items.extend([
                "market availability",
                "liquidity clarity",
                "exit route clarity",
                "issuer / redemption assumptions",
            ])
            review_signals.append("Review only after market clarity improves.")

        elif market_report.market_status == "needs_review":
            pulse_status = "cautious"
            summary = (
                "The market path may be usable, but it needs monitoring and verification."
            )
            watch_items.extend([
                "liquidity",
                "spread",
                "APY changes",
                "maturity date",
                "exit conditions",
            ])
            review_signals.append("Review in 7 days or after route verification.")

        else:
            pulse_status = "active_but_requires_review"
            summary = (
                "The market path appears usable in the MVP logic, but live review is still required."
            )
            watch_items.extend([
                "liquidity depth",
                "APY sustainability",
                "price deviation",
                "protocol conditions",
                "exit route",
            ])
            review_signals.append("Review in 7–14 days or when market conditions change.")

        for strategy in strategies:
            if "PT" in strategy.category or "PT" in strategy.name:
                watch_items.append("PT maturity date")
                review_signals.append("PT / fixed-yield paths should be reviewed near maturity.")

            if "LP" in strategy.category or "LP" in strategy.name:
                watch_items.append("LP liquidity and impermanent loss risk")
                review_signals.append("LP paths should be reviewed if liquidity or price conditions change.")

            if strategy.is_advanced_route:
                watch_items.extend([
                    "collateral ratio",
                    "liquidation threshold",
                    "borrow APY",
                    "deposit APY",
                    "loop health",
                    "exit liquidity",
                ])
                review_signals.append(
                    "Advanced looping routes require frequent review because liquidation and APY conditions can change."
                )

            if "xStocks" in strategy.category or "xStocks" in strategy.name:
                watch_items.append("xStocks price deviation and market access")
                review_signals.append("Experimental xStocks paths should be reviewed in 24–72 hours.")

            if "Vault" in strategy.category or "vault" in strategy.name.lower():
                watch_items.append("vault curator / manager risk")
                review_signals.append("Vault routes require curator, withdrawal and risk review.")

        return PulseReport(
            pulse_status=pulse_status,
            summary=summary,
            watch_items=self._deduplicate(watch_items),
            review_signals=self._deduplicate(review_signals),
        )

    def _deduplicate(self, items: List[str]) -> List[str]:
        result = []
        seen = set()

        for item in items:
            if item not in seen:
                result.append(item)
                seen.add(item)

        return result
