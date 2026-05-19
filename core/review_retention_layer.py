from typing import Dict, List

from core.models import ReviewPlan, StrategyRecommendation


class ReviewRetentionLayer:
    """
    The Oracle does not end with a recommendation.

    Every decision creates a next review point.

    Examples:
    - Wait / No Action → review again in 7 days or when market data improves
    - Current Token Strategy → review in 7 or 14 days
    - PT / Fixed Yield → review near maturity
    - Experimental xStocks → review in 24–72 hours
    - Advanced Looping → frequent review because liquidation and APY conditions can change
    - RWA Market Strategy → review after issuer, redemption, liquidity and exit verification
    - Blocked Strategy → review again only after market data, liquidity or exit clarity improves

    This makes the Oracle a continuous decision layer,
    not a one-time strategy generator.
    """

    def build_review_plan(self, recommendations: List[StrategyRecommendation]) -> ReviewPlan:
        checkpoints: Dict[str, str] = {}

        if not recommendations:
            return ReviewPlan(
                global_checkpoint="Review again after market data improves.",
                review_reason="No recommendation was generated.",
                strategy_checkpoints=checkpoints,
            )

        leading = recommendations[0]

        has_pt = False
        has_xstocks = False
        has_current_token = False
        has_wait = False
        has_needs_review = False

        for rec in recommendations:
            checkpoint = self._checkpoint_for(rec)
            checkpoints[rec.name] = checkpoint

            if "PT" in rec.name or "Fixed" in rec.name:
                has_pt = True

            if "xStocks" in rec.name:
                has_xstocks = True

            if "Current-Token" in rec.name or "Current Token" in rec.name:
                has_current_token = True

            if rec.decision_status == "Valid Option":
                has_wait = True

            if rec.decision_status == "Needs Review":
                has_needs_review = True

        if leading.decision_status in ["Blocked", "Do Not Force Entry"]:
            return ReviewPlan(
                global_checkpoint=(
                    "Leading path is blocked. Review again only after market data, liquidity, exit clarity or missing understanding improves."
                ),
                review_reason=(
                    "The Oracle does not recommend forcing the leading path under current assumptions."
                ),
                strategy_checkpoints=checkpoints,
            )

        if "Advanced" in leading.name or "Looping" in leading.name:
            return ReviewPlan(
                global_checkpoint=(
                    "Advanced route is the leading visible path, but it requires strict review of liquidation, collateral, APY and exit conditions."
                ),
                review_reason=(
                    "Advanced looping strategies can change risk quickly because of borrow rates, liquidation thresholds and exit liquidity."
                ),
                strategy_checkpoints=checkpoints,
            )

        if has_pt:
            return ReviewPlan(
                global_checkpoint="Review PT / fixed-yield paths near maturity and before any early exit.",
                review_reason=(
                    "PT / fixed-yield paths should not be treated like ordinary spot positions. "
                    "Maturity and early-exit conditions matter."
                ),
                strategy_checkpoints=checkpoints,
            )

        if has_xstocks:
            return ReviewPlan(
                global_checkpoint="Review experimental xStocks exposure in 24–72 hours.",
                review_reason=(
                    "Experimental xStocks / tokenized equity paths require closer review because liquidity, price deviation and market access can change quickly."
                ),
                strategy_checkpoints=checkpoints,
            )

        if has_current_token:
            return ReviewPlan(
                global_checkpoint="Review current-token strategy in 7 or 14 days.",
                review_reason=(
                    "Current-token routes may be safer than forcing new RWA exposure, but they still need follow-up."
                ),
                strategy_checkpoints=checkpoints,
            )

        if has_wait:
            return ReviewPlan(
                global_checkpoint="Review again in 7 days or when market data improves.",
                review_reason=(
                    "Wait / No Action is valid when the user lacks market clarity, exit plan or strategy understanding."
                ),
                strategy_checkpoints=checkpoints,
            )

        if has_needs_review:
            return ReviewPlan(
                global_checkpoint="Review in 7 days or after liquidity / route verification.",
                review_reason=(
                    "Some strategies may be usable, but they require verification before execution."
                ),
                strategy_checkpoints=checkpoints,
            )

        return ReviewPlan(
            global_checkpoint="Review in 7–14 days or if liquidity, APY, spread or exit conditions change.",
            review_reason=(
                "Even if a path is ready to explore, RWA strategy conditions can change. "
                "The user should return with a plan, not in panic."
            ),
            strategy_checkpoints=checkpoints,
        )

    def _checkpoint_for(self, rec: StrategyRecommendation) -> str:
        name = rec.name.lower()

        if rec.decision_status in ["Blocked", "Do Not Force Entry"]:
            return "Review only after missing understanding, liquidity or exit clarity improves."

        if rec.decision_status == "Valid Option":
            return "Review again in 7 days or when market data improves."

        if "advanced" in name or "looping" in name:
            return "Review frequently after liquidation, borrow APY, collateral and exit conditions are verified."

        if "pt" in name or "fixed" in name:
            return "Review near maturity and before any early exit."

        if "xstocks" in name:
            return "Review in 24–72 hours."

        if "current-token" in name or "current token" in name:
            return "Review in 7 or 14 days."

        if rec.decision_status == "Needs Review":
            return "Review in 7 days or after verification."

        return "Review in 7–14 days or when conditions change."
