from core.models import RouteDecision, StrategyOption, UserInput


class RouteOrchestratorAgent:
    """
    Decides where execution should happen.

    Core principle:
    Productive Capital Oracle does not execute trades.

    Preferred execution / orchestration layer:
    INFINIT

    Fallback execution:
    - Pendle for PT / LP / 50/50 demo case
    - INFINIT Pro Route for advanced leverage looping demo
    - protocol-specific route for current-token strategies
    - manual review for unsupported routes

    Current MVP:
    - route availability is simulated / static
    - no live INFINIT API
    - no live Pendle API
    """

    def decide_route(self, user_input: UserInput, strategy: StrategyOption) -> RouteDecision:
        if strategy.id == "wait_no_action":
            return RouteDecision(
                strategy_id=strategy.id,
                execution_status="not_required",
                preferred_execution_layer="None",
                fallback_execution_layer="None",
                route_message=(
                    "No Action does not require execution. The user should review again after market data or understanding improves."
                ),
                user_confirmation_required=False,
            )

        if strategy.is_advanced_route:
            return RouteDecision(
                strategy_id=strategy.id,
                execution_status="advanced_infinit_review_required",
                preferred_execution_layer="INFINIT",
                fallback_execution_layer="No beginner fallback",
                route_message=(
                    "Advanced route detected. INFINIT is the preferred orchestration layer for this professional strategy. "
                    "The user should not proceed unless Risk Guardian checks pass and live route conditions are verified."
                ),
                user_confirmation_required=True,
            )

        infinit_status = self._mock_infinit_status(user_input, strategy)

        if infinit_status == "available":
            return RouteDecision(
                strategy_id=strategy.id,
                execution_status="infinit_available",
                preferred_execution_layer="INFINIT",
                fallback_execution_layer=strategy.fallback_execution_layer or "Manual protocol route",
                route_message=(
                    "INFINIT is the preferred orchestration layer. "
                    "The user should review the route inside INFINIT and confirm execution there."
                ),
                user_confirmation_required=True,
            )

        if strategy.fallback_execution_layer:
            return RouteDecision(
                strategy_id=strategy.id,
                execution_status="fallback_required",
                preferred_execution_layer="INFINIT",
                fallback_execution_layer=strategy.fallback_execution_layer,
                route_message=(
                    "No ready INFINIT route is available in this MVP scenario. "
                    f"Fallback route: {strategy.fallback_execution_layer}. "
                    "The user should proceed only after verifying liquidity, exit conditions and strategy risk."
                ),
                user_confirmation_required=True,
            )

        return RouteDecision(
            strategy_id=strategy.id,
            execution_status="manual_review_required",
            preferred_execution_layer="INFINIT",
            fallback_execution_layer="Manual review",
            route_message=(
                "No ready INFINIT route or clear fallback route is available in this MVP scenario. "
                "Manual market and risk review is required before any action."
            ),
            user_confirmation_required=True,
        )

    def _mock_infinit_status(self, user_input: UserInput, strategy: StrategyOption) -> str:
        """
        Static MVP logic.

        Future version should query:
        - INFINIT strategy catalog
        - supported assets
        - route availability
        - chain compatibility
        - route complexity
        """

        if not user_input.wants_infinit_first:
            return "not_available"

        if strategy.id == "infinit_orchestration_path":
            return "available"

        if strategy.is_demo_case:
            return "not_available"

        return "not_available"
