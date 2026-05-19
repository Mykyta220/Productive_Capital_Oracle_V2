from typing import List

from core.models import CurrentTokenRoute, MarketScoutReport, StrategyOption, UserInput


class StrategyAgent:
    """
    Proposes strategy paths.

    The Strategy Agent proposes.
    It does not validate safety.
    Safety validation is handled by RiskGuardianAgent.

    Possible paths:
    - RWA market discovery
    - current-token strategy
    - PT / fixed-yield review
    - experimental xStocks path
    - STRCx / Pendle demo case: PT / LP / 50/50
    - advanced pro route: Leverage Looping - PT apyUSD via INFINIT
    - Wait / No Action
    """

    def propose(
        self,
        user_input: UserInput,
        market_report: MarketScoutReport,
        current_token_routes: List[CurrentTokenRoute],
    ) -> List[StrategyOption]:
        strategies = []

        strategies.append(self._wait_no_action())

        if current_token_routes:
            strategies.extend(self._current_token_options(current_token_routes))

        if market_report.market_status in ["usable", "needs_review"]:
            strategies.extend(self._general_rwa_options(user_input))

        if self._is_strcx_demo(user_input):
            strategies.extend(self._strcx_pendle_demo_options())

        if self._should_show_advanced_route(user_input):
            strategies.append(self._advanced_leverage_looping_pt())

        if user_input.user_goal == "Tokenized equity exposure" or "xstock" in user_input.target_asset.lower():
            strategies.append(self._experimental_xstocks_path())

        strategies.append(self._infinit_orchestration_path())

        return self._deduplicate(strategies)

    def _is_strcx_demo(self, user_input: UserInput) -> bool:
        target = user_input.target_asset.lower()
        return (
            user_input.demo_mode == "STRCx / Pendle demo"
            or "strcx" in target
            or "strc" in target
        )

    def _should_show_advanced_route(self, user_input: UserInput) -> bool:
        """
        Advanced route belongs to the committee demo ladder:

        STRCx / Pendle
        → PT
        → LP
        → 50/50 PT-LP
        → Advanced Pro Route: Leverage Looping - PT apyUSD via INFINIT

        It should not appear as a random route in unrelated RWA scenarios.
        """

        is_committee_demo = self._is_strcx_demo(user_input)

        if not is_committee_demo:
            return False

        if user_input.show_advanced_route:
            return True

        if user_input.risk_profile == "Aggressive":
            return True

        if user_input.user_goal == "Highest APY":
            return True

        return False

    def _wait_no_action(self) -> StrategyOption:
        return StrategyOption(
            id="wait_no_action",
            name="Wait / No Action",
            category="Wait",
            simple_description=(
                "Do not enter a new RWA strategy until market clarity, exit route and user understanding improve."
            ),
            mechanism_explanation=(
                "No Action is a valid decision. The user avoids forcing exposure when the market or strategy is unclear."
            ),
            why_it_may_make_sense=[
                "Protects the user from fake confidence.",
                "Gives time to verify liquidity, exit path and strategy mechanics.",
                "Avoids entering only because of APY.",
            ],
            main_risks=[
                "The user may miss an opportunity.",
                "Waiting still requires discipline and follow-up.",
            ],
            required_understanding=[],
            preferred_execution_layer="None",
            fallback_execution_layer=None,
            base_risk="Low",
            base_complexity="Low",
        )

    def _current_token_options(self, routes: List[CurrentTokenRoute]) -> List[StrategyOption]:
        options = []

        for route in routes:
            options.append(
                StrategyOption(
                    id=f"current_token_{route.id}",
                    name=route.name,
                    category="Current Token Strategy",
                    simple_description=route.simple_description,
                    mechanism_explanation=(
                        "Instead of forcing new RWA exposure, the Oracle reviews whether the user's current token "
                        "can be used through a safer or clearer strategy route."
                    ),
                    why_it_may_make_sense=[
                        "Avoids unnecessary new exposure.",
                        "Uses the asset the user already holds.",
                        "Can be safer when RWA market discovery is weak.",
                    ],
                    main_risks=route.verification_required,
                    required_understanding=[
                        "protocol risk",
                        "liquidity",
                        "withdrawal conditions",
                    ],
                    preferred_execution_layer="INFINIT if route exists",
                    fallback_execution_layer=", ".join(route.possible_protocols),
                    base_risk=route.risk_level,
                    base_complexity=route.complexity_level,
                    is_current_token_route=True,
                )
            )

        return options

    def _general_rwa_options(self, user_input: UserInput) -> List[StrategyOption]:
        return [
            StrategyOption(
                id="rwa_market_discovery",
                name="RWA Market Discovery",
                category="RWA Discovery",
                simple_description=(
                    "Map where the selected RWA / tokenized asset can actually be used before entering."
                ),
                mechanism_explanation=(
                    "The user should verify market availability, liquidity, spread, exit route, issuer, redemption and protocol support."
                ),
                why_it_may_make_sense=[
                    "Prevents single-market tunnel vision.",
                    "Helps avoid weak liquidity or unclear exit paths.",
                    "Creates a stronger basis for any strategy decision.",
                ],
                main_risks=[
                    "Market data may be incomplete.",
                    "Some routes may be visible but not safe.",
                    "Live verification is required.",
                ],
                required_understanding=[
                    "market availability",
                    "liquidity",
                    "exit route",
                    "issuer / redemption assumptions",
                ],
                preferred_execution_layer="INFINIT if route exists",
                fallback_execution_layer="Manual market review",
                base_risk="Medium",
                base_complexity="Medium",
            ),
            StrategyOption(
                id="pt_fixed_yield_review",
                name="PT / Fixed-Yield Review",
                category="PT",
                simple_description=(
                    "Review whether a fixed-yield style route exists for the selected RWA asset."
                ),
                mechanism_explanation=(
                    "PT means Principal Token. The user buys a discounted token that matures into the underlying asset later."
                ),
                why_it_may_make_sense=[
                    "Often simpler than LP or loops.",
                    "No borrowing is required.",
                    "Can fit users who can hold until maturity.",
                ],
                main_risks=[
                    "Maturity risk.",
                    "Early-exit risk.",
                    "Liquidity risk.",
                    "Underlying asset risk.",
                ],
                required_understanding=[
                    "PT",
                    "maturity",
                    "early exit",
                ],
                preferred_execution_layer="INFINIT if route exists",
                fallback_execution_layer="Pendle if relevant market exists",
                base_risk="Medium",
                base_complexity="Medium",
            ),
        ]

    def _strcx_pendle_demo_options(self) -> List[StrategyOption]:
        return [
            StrategyOption(
                id="demo_strcx_pendle_pt",
                name="Demo: STRCx Pendle PT Route",
                category="Demo PT",
                simple_description=(
                    "Demo case: user considers PT STRCx on Pendle as a fixed-yield style route."
                ),
                mechanism_explanation=(
                    "PT STRCx is a Principal Token route. If held until maturity, it is designed to redeem into the underlying STRCx. "
                    "This is a demo case for showing how the Oracle explains PT risk."
                ),
                why_it_may_make_sense=[
                    "Simpler than LP or 50/50.",
                    "No borrowing or loop is required.",
                    "Can fit users who can hold until maturity.",
                    "Works as a fixed-yield core route in the committee demo.",
                ],
                main_risks=[
                    "Maturity risk.",
                    "Early-exit risk.",
                    "Liquidity risk.",
                    "Underlying STRCx risk.",
                    "Live market verification required.",
                ],
                required_understanding=[
                    "PT",
                    "maturity",
                    "early exit",
                ],
                preferred_execution_layer="INFINIT if route exists",
                fallback_execution_layer="Pendle",
                base_risk="Medium",
                base_complexity="Medium",
                is_demo_case=True,
            ),
            StrategyOption(
                id="demo_strcx_pendle_lp",
                name="Demo: STRCx Pendle LP Route",
                category="Demo LP",
                simple_description=(
                    "Demo case: user considers providing liquidity to a STRCx-related Pendle market."
                ),
                mechanism_explanation=(
                    "LP means Liquidity Provider. The user supplies liquidity and may earn fees or incentives, "
                    "but accepts liquidity, price movement and impermanent loss risk."
                ),
                why_it_may_make_sense=[
                    "May offer higher yield potential.",
                    "Can support market liquidity.",
                    "May fit advanced users who understand LP mechanics.",
                    "Works as a growth / liquidity layer in the committee demo.",
                ],
                main_risks=[
                    "Impermanent loss.",
                    "Liquidity risk.",
                    "APY variability.",
                    "Exit risk.",
                    "Not suitable for users who do not understand LP.",
                ],
                required_understanding=[
                    "LP",
                    "impermanent loss",
                    "liquidity",
                ],
                preferred_execution_layer="INFINIT if route exists",
                fallback_execution_layer="Pendle",
                base_risk="High",
                base_complexity="High",
                is_demo_case=True,
            ),
            StrategyOption(
                id="demo_strcx_pendle_50_50",
                name="Demo: STRCx 50/50 PT-LP Route",
                category="Demo Hybrid",
                simple_description=(
                    "Demo case: user splits capital between PT and LP exposure."
                ),
                mechanism_explanation=(
                    "50/50 means half the capital goes into PT and half into LP. "
                    "It is balanced by allocation, but not simple by risk."
                ),
                why_it_may_make_sense=[
                    "Combines fixed-yield style exposure with LP exposure.",
                    "May diversify compared with using only PT or only LP.",
                    "Can fit users who understand both PT and LP.",
                ],
                main_risks=[
                    "Combines PT maturity risk and LP risk.",
                    "Requires understanding both mechanisms.",
                    "Liquidity and exit conditions must be checked.",
                ],
                required_understanding=[
                    "PT",
                    "LP",
                    "maturity",
                    "impermanent loss",
                ],
                preferred_execution_layer="INFINIT if route exists",
                fallback_execution_layer="Pendle",
                base_risk="Medium-High",
                base_complexity="High",
                is_demo_case=True,
            ),
        ]

    def _advanced_leverage_looping_pt(self) -> StrategyOption:
        return StrategyOption(
            id="advanced_leverage_looping_pt_apyusd",
            name="Advanced: Leverage Looping - PT apyUSD",
            category="Advanced Pro Route",
            simple_description=(
                "Professional demo route: an INFINIT-style leveraged looping strategy using PT apyUSD."
            ),
            mechanism_explanation=(
                "This route belongs to the fixed-yield / PT strategy family, but adds lending and borrowing loops. "
                "It can amplify APY, but also adds liquidation risk, collateral risk, borrow-rate risk, loop complexity and exit complexity."
            ),
            why_it_may_make_sense=[
                "Shows the professional route after simple PT / LP / 50/50 comparison.",
                "May fit advanced users who understand PT, lending, borrowing and liquidation risk.",
                "Demonstrates that the Oracle can surface advanced INFINIT routes without forcing them.",
                "Useful as a committee demo of Risk Guardian blocking high-APY complexity.",
            ],
            main_risks=[
                "Leverage risk.",
                "Liquidation risk.",
                "Borrow APY instability.",
                "Deposit APY instability.",
                "Lending protocol risk.",
                "Collateral risk.",
                "Loop complexity.",
                "Exit complexity.",
                "Not suitable for users who do not understand liquidation.",
            ],
            required_understanding=[
                "PT",
                "maturity",
                "loop",
                "liquidation",
                "lending",
                "borrowing",
                "collateral",
                "exit route",
            ],
            preferred_execution_layer="INFINIT",
            fallback_execution_layer="No fallback for beginners",
            base_risk="Extreme",
            base_complexity="Very High",
            is_demo_case=True,
            is_advanced_route=True,
        )

    def _experimental_xstocks_path(self) -> StrategyOption:
        return StrategyOption(
            id="experimental_xstocks_path",
            name="Experimental xStocks Path",
            category="xStocks",
            simple_description=(
                "Experimental path for tokenized equity exposure."
            ),
            mechanism_explanation=(
                "xStocks / tokenized equities can provide onchain exposure to traditional equity-like assets, "
                "but the user must understand issuer, redemption, liquidity, price deviation and market access risks."
            ),
            why_it_may_make_sense=[
                "Can provide tokenized equity exposure.",
                "May become useful as RWA infrastructure matures.",
                "Fits users who understand experimental market risk.",
            ],
            main_risks=[
                "Experimental market risk.",
                "Price deviation risk.",
                "Issuer / redemption uncertainty.",
                "Liquidity and exit risk.",
                "Regulatory and access uncertainty.",
            ],
            required_understanding=[
                "issuer",
                "redemption",
                "liquidity",
                "price deviation",
            ],
            preferred_execution_layer="INFINIT if route exists",
            fallback_execution_layer="xStocks market / supported venue",
            base_risk="High",
            base_complexity="High",
        )

    def _infinit_orchestration_path(self) -> StrategyOption:
        return StrategyOption(
            id="infinit_orchestration_path",
            name="INFINIT Strategy Orchestration Path",
            category="Orchestration",
            simple_description=(
                "Use INFINIT as the preferred orchestration layer if a valid strategy route exists."
            ),
            mechanism_explanation=(
                "The Oracle does not execute. It decides whether a path is reasonable. "
                "INFINIT can orchestrate the strategy if a route exists and the user confirms execution."
            ),
            why_it_may_make_sense=[
                "Can reduce manual transaction complexity.",
                "Can assemble multi-step DeFi strategies.",
                "Keeps the user in control of execution confirmation.",
            ],
            main_risks=[
                "Route may not exist yet.",
                "User must still review every step.",
                "Protocol and transaction risks remain.",
            ],
            required_understanding=[
                "strategy route",
                "execution steps",
                "protocol risk",
            ],
            preferred_execution_layer="INFINIT",
            fallback_execution_layer="Manual protocol route",
            base_risk="Depends",
            base_complexity="Medium",
        )

    def _deduplicate(self, strategies: List[StrategyOption]) -> List[StrategyOption]:
        seen = set()
        result = []

        for strategy in strategies:
            if strategy.id not in seen:
                result.append(strategy)
                seen.add(strategy.id)

        return result
