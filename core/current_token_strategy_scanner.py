from typing import List

from core.models import CurrentTokenRoute, MarketScoutReport, UserInput


class CurrentTokenStrategyScanner:
    """
    If no usable RWA market exists, the Oracle does not force RWA exposure.

    Instead, it analyzes the token the user already holds and checks whether safer
    current-token strategy routes may exist.

    Current MVP:
    - static route logic
    - no live protocol checks

    Planned protocol layers:
    - Ethereum / Multi-chain: Morpho, Aave, Pendle, INFINIT
    - Solana: Kamino
    - BNB Chain: Venus, Lista, PancakeSwap, Beefy, Thena
    - Mantle: Mantle ecosystem routes, INFINIT-style orchestration, future RWA / xStocks routes
    """

    def scan(
        self,
        user_input: UserInput,
        market_report: MarketScoutReport,
    ) -> List[CurrentTokenRoute]:
        routes = []

        if not market_report.use_current_token_fallback:
            return routes

        token = user_input.current_token.upper().strip()

        if token in ["USDC", "USDT", "DAI"]:
            routes.extend(self._stablecoin_routes(token))

        elif token in ["BNB", "WBNB"]:
            routes.extend(self._bnb_routes(token))

        elif token in ["MNT", "WMNT"]:
            routes.extend(self._mantle_routes(token))

        elif token in ["ETH", "WETH"]:
            routes.extend(self._ethereum_routes(token))

        else:
            routes.append(
                CurrentTokenRoute(
                    id="generic_current_token_review",
                    name="Generic Current-Token Review",
                    ecosystem="Multi-chain",
                    simple_description=(
                        "The Oracle cannot classify this token in the MVP, but it can still recommend "
                        "reviewing safer current-token routes before forcing new RWA exposure."
                    ),
                    possible_protocols=[
                        "INFINIT",
                        "Aave",
                        "Morpho",
                        "Pendle",
                        "chain-specific protocols",
                    ],
                    risk_level="Medium",
                    complexity_level="Medium",
                    verification_required=[
                        "Verify token liquidity.",
                        "Verify protocol support.",
                        "Check whether a simple hold, lending, or fixed-yield route exists.",
                        "Avoid leverage if the user does not understand liquidation.",
                    ],
                )
            )

        return routes

    def _stablecoin_routes(self, token: str) -> List[CurrentTokenRoute]:
        return [
            CurrentTokenRoute(
                id="stablecoin_lending_review",
                name=f"{token} Lending / Vault Review",
                ecosystem="Ethereum / Multi-chain",
                simple_description=(
                    f"Review whether {token} can be used in a simpler lending or vault route before entering a new RWA market."
                ),
                possible_protocols=["Morpho", "Aave", "INFINIT"],
                risk_level="Low-Medium",
                complexity_level="Medium",
                verification_required=[
                    "Check vault curator / manager risk.",
                    "Check withdrawal conditions.",
                    "Check APY source.",
                    "Check liquidity and protocol risk.",
                ],
            ),
            CurrentTokenRoute(
                id="stablecoin_pt_review",
                name=f"{token} PT / Fixed-Yield Review",
                ecosystem="Pendle / INFINIT",
                simple_description=(
                    f"Review whether a fixed-yield style route exists for {token}, instead of forcing uncertain RWA exposure."
                ),
                possible_protocols=["Pendle", "INFINIT"],
                risk_level="Medium",
                complexity_level="Medium",
                verification_required=[
                    "Check PT maturity date.",
                    "Check liquidity before maturity.",
                    "Check implied APY.",
                    "Check whether user understands maturity risk.",
                ],
            ),
        ]

    def _bnb_routes(self, token: str) -> List[CurrentTokenRoute]:
        return [
            CurrentTokenRoute(
                id="bnb_liquid_staking_review",
                name=f"{token} Liquid Staking / Yield Review",
                ecosystem="BNB Chain",
                simple_description=(
                    f"Review whether {token} can be used in a simpler BNB Chain strategy before forcing RWA exposure."
                ),
                possible_protocols=["Lista", "Venus", "INFINIT"],
                risk_level="Medium",
                complexity_level="Medium",
                verification_required=[
                    "Check staking derivative risk.",
                    "Check borrowing / liquidation risk if leverage is involved.",
                    "Check LTV and liquidation thresholds.",
                    "Avoid loops if the user does not understand liquidation.",
                ],
            )
        ]

    def _mantle_routes(self, token: str) -> List[CurrentTokenRoute]:
        return [
            CurrentTokenRoute(
                id="mantle_current_token_review",
                name=f"{token} Mantle Ecosystem Review",
                ecosystem="Mantle",
                simple_description=(
                    f"Review whether {token} can be used in Mantle ecosystem routes before entering a new RWA / xStocks market."
                ),
                possible_protocols=[
                    "INFINIT",
                    "Mantle ecosystem routes",
                    "future RWA / xStocks routes",
                ],
                risk_level="Medium",
                complexity_level="Medium",
                verification_required=[
                    "Check available Mantle routes.",
                    "Check liquidity.",
                    "Check xStocks / RWA market availability.",
                    "Check whether INFINIT has a route.",
                ],
            )
        ]

    def _ethereum_routes(self, token: str) -> List[CurrentTokenRoute]:
        return [
            CurrentTokenRoute(
                id="eth_current_token_review",
                name=f"{token} Current-Token Review",
                ecosystem="Ethereum / Multi-chain",
                simple_description=(
                    f"Review whether {token} can be used in existing lending, vault, or fixed-yield routes before forcing RWA exposure."
                ),
                possible_protocols=["Aave", "Morpho", "Pendle", "INFINIT"],
                risk_level="Medium",
                complexity_level="Medium",
                verification_required=[
                    "Check lending risk.",
                    "Check vault curator risk.",
                    "Check fixed-yield maturity risk.",
                    "Check liquidity and exit conditions.",
                ],
            )
        ]
