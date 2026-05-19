from core.models import MarketScoutReport, UserInput


class RWAMarketScoutAgent:
    """
    Checks whether a usable RWA / xStocks market exists before the user buys.

    Current MVP:
    - uses user-provided answers
    - uses static demo assumptions
    - does not verify live markets yet

    Future version:
    - live RWA / xStocks market discovery
    - wallet analysis
    - liquidity checks
    - spread checks
    - issuer / redemption checks
    - INFINIT route availability
    - Pendle market availability
    """

    def analyze(self, user_input: UserInput) -> MarketScoutReport:
        red_flags = []
        positive_signals = []

        target_asset = user_input.target_asset.strip()
        current_token = user_input.current_token.strip()

        if target_asset:
            positive_signals.append(f"Target RWA / tokenized asset selected: {target_asset}.")
        else:
            red_flags.append("No target RWA / tokenized asset selected.")

        if current_token:
            positive_signals.append(f"Current token detected: {current_token}.")
        else:
            red_flags.append("Current token is missing. Current-token fallback is harder to evaluate.")

        if user_input.known_market == "I know several markets":
            positive_signals.append("User claims awareness of several possible markets.")
        elif user_input.known_market == "I only saw one market":
            red_flags.append("Market awareness is limited to one visible market.")
        else:
            red_flags.append("Market availability is unclear.")

        if user_input.exit_plan == "Clear exit plan":
            positive_signals.append("User has a defined exit plan.")
        elif user_input.exit_plan == "Partial exit plan":
            red_flags.append("Exit plan is only partial.")
        else:
            red_flags.append("Exit plan is missing.")

        if user_input.user_confidence == "High":
            positive_signals.append("User confidence is high.")
        elif user_input.user_confidence == "Medium":
            red_flags.append("User confidence is moderate. This may require review.")
        else:
            red_flags.append("User confidence is low.")

        if user_input.user_goal == "Highest APY":
            red_flags.append("Goal may be APY-driven instead of strategy-driven.")

        if user_input.risk_profile == "Aggressive":
            red_flags.append("Aggressive profile requires stronger risk controls.")

        if user_input.understands_pt == "No":
            red_flags.append("User does not understand PT / maturity mechanics.")

        if user_input.understands_lp == "No":
            red_flags.append("User does not understand LP / impermanent loss mechanics.")

        if user_input.understands_loop == "No":
            red_flags.append("User does not understand loops / liquidation mechanics.")

        if len(red_flags) >= 5:
            return MarketScoutReport(
                market_status="weak_or_unclear",
                summary=(
                    "The RWA market path is not clear enough to force exposure. "
                    "The Oracle should consider Wait / No Action or current-token strategy routes."
                ),
                red_flags=red_flags,
                positive_signals=positive_signals,
                should_force_rwa_exposure=False,
                use_current_token_fallback=True,
                confidence_level="Low",
            )

        if len(red_flags) >= 2:
            return MarketScoutReport(
                market_status="needs_review",
                summary=(
                    "The RWA path may be usable, but market awareness, exit clarity or user understanding needs review."
                ),
                red_flags=red_flags,
                positive_signals=positive_signals,
                should_force_rwa_exposure=False,
                use_current_token_fallback=True,
                confidence_level="Medium",
            )

        return MarketScoutReport(
            market_status="usable",
            summary=(
                "The RWA path appears usable based on the user's answers, but live verification is still required."
            ),
            red_flags=red_flags,
            positive_signals=positive_signals,
            should_force_rwa_exposure=False,
            use_current_token_fallback=False,
            confidence_level="High",
        )
