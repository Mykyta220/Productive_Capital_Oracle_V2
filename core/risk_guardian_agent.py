from typing import Dict

from core.models import MarketScoutReport, PulseReport, RiskReport, StrategyOption, UserInput


class RiskGuardianAgent:
    """
    Validates safety.

    It checks:
    - weak market conditions
    - unclear exit
    - high volatility assumptions
    - low confidence
    - hidden leverage
    - experimental xStocks risk
    - too many red flags
    - vault / curator risk for Morpho-style routes
    - lending / liquidity / leverage risk for Kamino-style routes
    - advanced looping / liquidation risk

    The Risk Guardian can downgrade confidence or block a strategy.
    """

    def validate(
        self,
        user_input: UserInput,
        market_report: MarketScoutReport,
        pulse_report: PulseReport,
        strategy: StrategyOption,
    ) -> RiskReport:
        risk_points = self._base_points(strategy.base_risk)
        blockers = []
        warnings = []
        missing_understanding = []

        fallback_layer = (strategy.fallback_execution_layer or "").lower()
        required = [item.lower() for item in strategy.required_understanding]

        if market_report.market_status == "weak_or_unclear":
            risk_points += 20
            warnings.append("RWA market path is weak or unclear.")

        if user_input.exit_plan == "No exit plan":
            risk_points += 20
            blockers.append("Exit plan is missing.")

        if user_input.exit_plan == "Partial exit plan":
            risk_points += 10
            warnings.append("Exit plan is only partial.")

        if user_input.user_confidence == "Low":
            risk_points += 15
            warnings.append("User confidence is low.")

        if user_input.user_confidence == "High" and market_report.red_flags:
            risk_points += 10
            warnings.append("Possible fake confidence: user confidence is high but red flags exist.")

        if user_input.known_market in ["I only saw one market", "Not sure"]:
            risk_points += 10
            warnings.append("Market awareness is incomplete.")

        if user_input.user_goal == "Highest APY":
            risk_points += 10
            warnings.append("APY-driven goal detected.")

        if "pt" in required and user_input.understands_pt == "No":
            risk_points += 20
            missing_understanding.append("PT / maturity")
            warnings.append("User does not understand PT / maturity mechanics.")

        if "pt" in required and user_input.understands_pt == "Partially":
            risk_points += 10
            warnings.append("User only partially understands PT / maturity mechanics.")

        if "lp" in required and user_input.understands_lp == "No":
            risk_points += 25
            missing_understanding.append("LP / impermanent loss")
            warnings.append("User does not understand LP / impermanent loss mechanics.")

        if "lp" in required and user_input.understands_lp == "Partially":
            risk_points += 12
            warnings.append("User only partially understands LP / impermanent loss mechanics.")

        if "impermanent loss" in required and user_input.understands_lp == "No":
            risk_points += 15
            missing_understanding.append("impermanent loss")

        if "loop" in required and user_input.understands_loop == "No":
            risk_points += 35
            missing_understanding.append("loop mechanics")
            blockers.append("User does not understand loop mechanics.")

        if "liquidation" in required and user_input.understands_loop == "No":
            risk_points += 35
            missing_understanding.append("liquidation / leverage")
            blockers.append("User does not understand liquidation risk.")

        if strategy.is_advanced_route:
            risk_points += 25
            warnings.append("Advanced pro route detected: leverage looping / PT strategy.")

            if user_input.risk_profile != "Aggressive":
                blockers.append("Advanced looping route requires an aggressive or professional risk profile.")

            if user_input.understands_loop != "Yes":
                blockers.append("Advanced looping route requires full loop / liquidation understanding.")

            if user_input.exit_plan != "Clear exit plan":
                blockers.append("Advanced looping route requires a clear exit plan.")

            if user_input.understands_pt != "Yes":
                warnings.append("Advanced looping route requires full PT / maturity understanding.")

        if "loop" in strategy.name.lower() or "recursive" in strategy.name.lower():
            risk_points += 25
            warnings.append("Loop / recursive strategy risk detected.")

        if "xstocks" in strategy.category.lower() or "xstocks" in strategy.name.lower():
            risk_points += 20
            warnings.append("Experimental xStocks risk detected.")

        if "vault" in strategy.category.lower() or "vault" in strategy.name.lower():
            warnings.append("Vault route requires curator / manager risk review.")

        if "kamino" in fallback_layer:
            warnings.append("Kamino-style route requires lending, liquidity and leverage review.")

        if pulse_report.pulse_status == "unstable":
            risk_points += 15
            warnings.append("Market Pulse status is unstable.")

        if user_input.risk_profile == "Conservative" and strategy.base_risk in ["High", "Medium-High", "Extreme"]:
            risk_points += 20
            blockers.append("Strategy risk is too high for conservative profile.")

        risk_points = min(risk_points, 100)

        risk_level = self._risk_level(risk_points)
        complexity_level = self._complexity_level(strategy, missing_understanding)
        decision_status = self._decision_status(risk_points, blockers, missing_understanding, strategy)

        return RiskReport(
            strategy_id=strategy.id,
            decision_status=decision_status,
            risk_level=risk_level,
            complexity_level=complexity_level,
            risk_points=risk_points,
            blockers=self._deduplicate(blockers),
            warnings=self._deduplicate(warnings),
            missing_understanding=self._deduplicate(missing_understanding),
        )

    def _base_points(self, base_risk: str) -> int:
        mapping: Dict[str, int] = {
            "Low": 15,
            "Low-Medium": 25,
            "Medium": 40,
            "Medium-High": 55,
            "High": 70,
            "Extreme": 90,
            "Depends": 45,
        }
        return mapping.get(base_risk, 45)

    def _risk_level(self, points: int) -> str:
        if points < 25:
            return "Low"
        if points < 45:
            return "Low-Medium"
        if points < 60:
            return "Medium"
        if points < 75:
            return "High"
        return "Extreme"

    def _complexity_level(self, strategy: StrategyOption, missing_understanding: list) -> str:
        if strategy.base_complexity in ["High", "Very High"]:
            return strategy.base_complexity

        if missing_understanding:
            return "High"

        return strategy.base_complexity

    def _decision_status(
        self,
        risk_points: int,
        blockers: list,
        missing_understanding: list,
        strategy: StrategyOption,
    ) -> str:
        if strategy.id == "wait_no_action":
            return "Valid Option"

        if blockers:
            return "Blocked"

        if strategy.is_advanced_route and risk_points >= 55:
            return "Needs Review"

        if risk_points >= 80:
            return "Do Not Force Entry"

        if risk_points >= 55:
            return "Needs Review"

        if missing_understanding:
            return "Needs Review"

        return "Ready to Explore"

    def _deduplicate(self, items: list) -> list:
        result = []
        seen = set()

        for item in items:
            if item and item not in seen:
                result.append(item)
                seen.add(item)

        return result
