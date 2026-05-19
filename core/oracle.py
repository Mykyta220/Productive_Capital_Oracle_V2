from typing import Dict, List

from core.current_token_strategy_scanner import CurrentTokenStrategyScanner
from core.market_pulse_agent import MarketPulseAgent
from core.models import (
    OracleResult,
    RiskReport,
    RouteDecision,
    StrategyOption,
    StrategyRecommendation,
    UserInput,
)
from core.review_retention_layer import ReviewRetentionLayer
from core.risk_guardian_agent import RiskGuardianAgent
from core.route_orchestrator_agent import RouteOrchestratorAgent
from core.rwa_market_scout_agent import RWAMarketScoutAgent
from core.strategy_agent import StrategyAgent


class ProductiveCapitalOracleV2:
    """
    Productive Capital Oracle V2.

    V1:
    "So, you bought RWA. What next?"

    V2:
    A broader RWA decision layer.

    It checks:
    - readiness
    - fake confidence
    - market awareness
    - exit plan
    - current-token fallback
    - strategy paths
    - pulse / review signals
    - risk blocks
    - INFINIT-first routing
    - fallback execution logic

    STRCx / Pendle / PT / LP / 50/50 is only a demo case.
    Advanced: Leverage Looping - PT apyUSD is the professional route in the same committee demo ladder.
    """

    def __init__(self) -> None:
        self.market_scout = RWAMarketScoutAgent()
        self.current_token_scanner = CurrentTokenStrategyScanner()
        self.strategy_agent = StrategyAgent()
        self.market_pulse = MarketPulseAgent()
        self.risk_guardian = RiskGuardianAgent()
        self.route_orchestrator = RouteOrchestratorAgent()
        self.review_layer = ReviewRetentionLayer()

    def analyze(self, user_input: UserInput) -> OracleResult:
        market_report = self.market_scout.analyze(user_input)

        current_token_routes = self.current_token_scanner.scan(
            user_input=user_input,
            market_report=market_report,
        )

        strategies = self.strategy_agent.propose(
            user_input=user_input,
            market_report=market_report,
            current_token_routes=current_token_routes,
        )

        pulse_report = self.market_pulse.analyze(
            user_input=user_input,
            market_report=market_report,
            strategies=strategies,
        )

        risk_reports: Dict[str, RiskReport] = {}
        route_decisions: Dict[str, RouteDecision] = {}

        for strategy in strategies:
            risk_reports[strategy.id] = self.risk_guardian.validate(
                user_input=user_input,
                market_report=market_report,
                pulse_report=pulse_report,
                strategy=strategy,
            )

            route_decisions[strategy.id] = self.route_orchestrator.decide_route(
                user_input=user_input,
                strategy=strategy,
            )

        recommendations = self._build_recommendations(
            strategies=strategies,
            risk_reports=risk_reports,
            route_decisions=route_decisions,
        )

        review_plan = self.review_layer.build_review_plan(recommendations)

        return OracleResult(
            title="Productive Capital Oracle V2",
            context_summary=self._context_summary(user_input),
            market_report=market_report,
            current_token_routes=current_token_routes,
            pulse_report=pulse_report,
            recommendations=recommendations,
            review_plan=review_plan,
            final_message=self._final_message(recommendations, market_report),
            disclaimer=(
                "This is an MVP decision-support prototype. It does not provide financial advice, "
                "does not execute transactions, does not connect to a wallet, and does not verify live market data yet. "
                "The user remains the final decision maker."
            ),
            metadata={
                "version": "V2 MVP",
                "mode": "static_decision_logic",
                "live_market_discovery": "disabled",
                "wallet_analysis": "disabled",
                "execution": "disabled",
                "preferred_orchestration_layer": "INFINIT",
                "demo_case": "STRCx / Pendle / PT / LP / 50/50",
                "advanced_demo_route": "Leverage Looping - PT apyUSD via INFINIT",
                "product_scope": "general RWA decision layer",
            },
        )

    def _build_recommendations(
        self,
        strategies: List[StrategyOption],
        risk_reports: Dict[str, RiskReport],
        route_decisions: Dict[str, RouteDecision],
    ) -> List[StrategyRecommendation]:
        recommendations = []

        for strategy in strategies:
            risk = risk_reports[strategy.id]
            route = route_decisions[strategy.id]

            rec = StrategyRecommendation(
                strategy_id=strategy.id,
                name=strategy.name,
                rank=self._rank(strategy, risk),
                decision_status=risk.decision_status,
                risk_level=risk.risk_level,
                complexity_level=risk.complexity_level,
                simple_description=strategy.simple_description,
                route_message=route.route_message,
                why_this_path=self._why_this_path(strategy, risk),
                warnings=self._warnings(strategy, risk),
                verification_steps=self._verification_steps(strategy, route),
                next_checkpoint=self._checkpoint(strategy, risk),
            )

            recommendations.append(rec)

        recommendations.sort(key=lambda item: item.rank)
        return recommendations

    def _rank(self, strategy: StrategyOption, risk: RiskReport) -> int:
        """
        Ranking is designed for the committee demo flow.

        The Oracle should show the decision ladder clearly:

        1. Current-token fallback if RWA path is weak
        2. STRCx PT
        3. STRCx LP
        4. STRCx 50/50 PT-LP
        5. Advanced Pro Route
        6. INFINIT orchestration path
        7. Wait / No Action
        8. Blocked / unsafe routes lower

        Important:
        Wait / No Action remains valid, but it should not hide
        the PT / LP / 50/50 / Advanced demo ladder.
        """

        if risk.decision_status in ["Blocked", "Do Not Force Entry"]:
            if strategy.id == "wait_no_action":
                return 7
            return 50

        if strategy.id.startswith("current_token"):
            return 1

        if strategy.id == "demo_strcx_pendle_pt":
            return 2

        if strategy.id == "demo_strcx_pendle_lp":
            return 3

        if strategy.id == "demo_strcx_pendle_50_50":
            return 4

        if strategy.is_advanced_route:
            return 5

        if strategy.id == "infinit_orchestration_path":
            return 6

        if strategy.id == "wait_no_action":
            return 7

        if risk.decision_status == "Ready to Explore":
            return 8

        if risk.decision_status == "Needs Review":
            return 9

        return 10

    def _why_this_path(self, strategy: StrategyOption, risk: RiskReport) -> List[str]:
        reasons = list(strategy.why_it_may_make_sense)

        if risk.decision_status == "Ready to Explore":
            reasons.append("Risk Guardian did not block this path, but live verification is still required.")

        if risk.decision_status == "Needs Review":
            reasons.append("This path may be relevant, but it requires review before any execution.")

        if risk.decision_status in ["Do Not Force Entry", "Blocked"]:
            reasons.append("Risk Guardian warns that this path should not be forced.")

        if strategy.is_demo_case:
            reasons.append("This is part of the committee demo flow.")

        if strategy.is_advanced_route:
            reasons.append(
                "This is the professional branch of the committee demo: shown after PT / LP / 50/50, but not forced."
            )

        if strategy.is_current_token_route:
            reasons.append("This path avoids forcing new RWA exposure and starts from the token the user already holds.")

        return reasons

    def _warnings(self, strategy: StrategyOption, risk: RiskReport) -> List[str]:
        warnings = []
        warnings.extend(strategy.main_risks)
        warnings.extend(risk.warnings)
        warnings.extend(risk.blockers)

        if risk.missing_understanding:
            warnings.append("Missing understanding: " + ", ".join(risk.missing_understanding))

        return self._deduplicate(warnings)

    def _verification_steps(self, strategy: StrategyOption, route: RouteDecision) -> List[str]:
        steps = [
            "Verify live market availability.",
            "Check liquidity, spread and exit route.",
            "Confirm the user understands the mechanism before execution.",
        ]

        if "PT" in strategy.category or "PT" in strategy.name:
            steps.append("Check maturity date and early-exit conditions.")

        if "LP" in strategy.category or "LP" in strategy.name:
            steps.append("Check LP mechanics, impermanent loss risk and liquidity conditions.")

        if strategy.is_advanced_route:
            steps.extend([
                "Check collateral ratio.",
                "Check liquidation threshold.",
                "Check borrow APY and deposit APY.",
                "Check loop health.",
                "Check exit liquidity.",
                "Confirm the user understands liquidation risk.",
            ])

        if "xStocks" in strategy.category or "xStocks" in strategy.name:
            steps.append("Check issuer, redemption, price deviation and market access.")

        if "Vault" in strategy.category or "vault" in strategy.name.lower():
            steps.append("Check vault curator / manager risk and withdrawal conditions.")

        if route.preferred_execution_layer == "INFINIT":
            steps.append("Check whether INFINIT has a ready strategy route.")

        excluded_fallbacks = [
            "None",
            "No transaction",
            "No beginner fallback",
            "No fallback for beginners",
        ]

        if route.fallback_execution_layer not in excluded_fallbacks:
            steps.append(f"If no INFINIT route exists, review fallback route: {route.fallback_execution_layer}.")

        return self._deduplicate(steps)

    def _checkpoint(self, strategy: StrategyOption, risk: RiskReport) -> str:
        if risk.decision_status in ["Blocked", "Do Not Force Entry"]:
            return "Review only after market data, liquidity, exit clarity or missing understanding improves."

        if strategy.id == "wait_no_action":
            return "Review again in 7 days or when market data improves."

        if strategy.is_advanced_route:
            return "Review frequently after liquidation, borrow APY, collateral and exit conditions are verified."

        if strategy.is_current_token_route:
            return "Review current-token route in 7 or 14 days."

        if "PT" in strategy.category or "PT" in strategy.name:
            return "Review near maturity and before any early exit."

        if "xStocks" in strategy.category or "xStocks" in strategy.name:
            return "Review in 24–72 hours."

        if risk.decision_status == "Needs Review":
            return "Review in 7 days or after verification."

        return "Review in 7–14 days or if liquidity, APY, spread or exit conditions change."

    def _context_summary(self, user_input: UserInput) -> str:
        return (
            f"The user is evaluating RWA-related decisions around {user_input.target_asset}. "
            f"Current token: {user_input.current_token}. "
            f"Known market: {user_input.known_market}. "
            f"Goal: {user_input.user_goal}. "
            f"Risk profile: {user_input.risk_profile}. "
            f"Confidence: {user_input.user_confidence}. "
            f"Preferred orchestration: {'INFINIT first' if user_input.wants_infinit_first else 'manual review'}. "
            f"Advanced route visible: {'Yes' if user_input.show_advanced_route else 'No'}."
        )

    def _final_message(self, recommendations: List[StrategyRecommendation], market_report) -> str:
        if not recommendations:
            return (
                "No strategy path was found. The safest decision is to wait and perform market discovery first."
            )

        top = recommendations[0]

        if market_report.market_status == "weak_or_unclear":
            return (
                "The Oracle does not recommend forcing RWA exposure now. "
                f"Leading path: {top.name}. "
                "The user should review market clarity, exit route, liquidity and current-token alternatives first."
            )

        if top.decision_status == "Ready to Explore":
            return (
                f"The leading path to explore is: {top.name}. "
                "Execution should happen only after live verification and user confirmation."
            )

        if top.decision_status == "Needs Review":
            return (
                f"The leading path is: {top.name}, but it needs review before execution. "
                "The user should verify liquidity, exit conditions, strategy mechanics and route availability."
            )

        if top.decision_status in ["Blocked", "Do Not Force Entry"]:
            return (
                "The Oracle does not recommend forcing entry. "
                "The user should first resolve missing understanding, weak market data or unclear exit conditions."
            )

        if top.decision_status == "Valid Option":
            return (
                "Wait / No Action is a valid decision. "
                "The user should return after market discovery, route verification or improved understanding."
            )

        return "The Oracle found possible paths, but further review is needed before any action."

    def _deduplicate(self, items: List[str]) -> List[str]:
        result = []
        seen = set()

        for item in items:
            if item and item not in seen:
                result.append(item)
                seen.add(item)

        return result
