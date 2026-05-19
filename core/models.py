from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass
class UserInput:
    target_asset: str
    current_token: str
    user_goal: str
    known_market: str
    exit_plan: str
    risk_profile: str
    time_horizon: str
    user_confidence: str
    understands_pt: str
    understands_lp: str
    understands_loop: str
    wants_infinit_first: bool
    demo_mode: str
    show_advanced_route: bool


@dataclass
class MarketScoutReport:
    market_status: str
    summary: str
    red_flags: List[str] = field(default_factory=list)
    positive_signals: List[str] = field(default_factory=list)
    should_force_rwa_exposure: bool = False
    use_current_token_fallback: bool = False
    confidence_level: str = "Medium"


@dataclass
class CurrentTokenRoute:
    id: str
    name: str
    ecosystem: str
    simple_description: str
    possible_protocols: List[str] = field(default_factory=list)
    risk_level: str = "Medium"
    complexity_level: str = "Medium"
    verification_required: List[str] = field(default_factory=list)


@dataclass
class StrategyOption:
    id: str
    name: str
    category: str
    simple_description: str
    mechanism_explanation: str
    why_it_may_make_sense: List[str] = field(default_factory=list)
    main_risks: List[str] = field(default_factory=list)
    required_understanding: List[str] = field(default_factory=list)
    preferred_execution_layer: str = "INFINIT if route exists"
    fallback_execution_layer: Optional[str] = None
    base_risk: str = "Medium"
    base_complexity: str = "Medium"
    is_demo_case: bool = False
    is_current_token_route: bool = False
    is_advanced_route: bool = False


@dataclass
class PulseReport:
    pulse_status: str
    summary: str
    watch_items: List[str] = field(default_factory=list)
    review_signals: List[str] = field(default_factory=list)


@dataclass
class RiskReport:
    strategy_id: str
    decision_status: str
    risk_level: str
    complexity_level: str
    risk_points: int
    blockers: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    missing_understanding: List[str] = field(default_factory=list)


@dataclass
class RouteDecision:
    strategy_id: str
    execution_status: str
    preferred_execution_layer: str
    fallback_execution_layer: str
    route_message: str
    user_confirmation_required: bool = True


@dataclass
class StrategyRecommendation:
    strategy_id: str
    name: str
    rank: int
    decision_status: str
    risk_level: str
    complexity_level: str
    simple_description: str
    route_message: str
    why_this_path: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    verification_steps: List[str] = field(default_factory=list)
    next_checkpoint: str = "Review in 7 days"


@dataclass
class ReviewPlan:
    global_checkpoint: str
    review_reason: str
    strategy_checkpoints: Dict[str, str] = field(default_factory=dict)


@dataclass
class OracleResult:
    title: str
    context_summary: str
    market_report: MarketScoutReport
    current_token_routes: List[CurrentTokenRoute]
    pulse_report: PulseReport
    recommendations: List[StrategyRecommendation]
    review_plan: ReviewPlan
    final_message: str
    disclaimer: str
    metadata: Dict[str, str] = field(default_factory=dict)
