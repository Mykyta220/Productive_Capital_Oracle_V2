import streamlit as st

from core.models import UserInput
from core.oracle import ProductiveCapitalOracleV2


st.set_page_config(
    page_title="Productive Capital Oracle V2",
    page_icon="🧭",
    layout="wide",
)


def build_user_input() -> UserInput:
    st.sidebar.header("Oracle Input")

    preset = st.sidebar.selectbox(
        "Demo preset",
        [
            "STRCx / Pendle demo",
            "STRCx + Pro INFINIT route",
            "STRCx with doubts",
            "USDC current-token fallback",
            "xStocks beginner",
            "Aggressive APY seeker",
            "Manual input",
        ],
    )

    presets = {
        "STRCx / Pendle demo": {
            "target_asset": "STRCx",
            "current_token": "USDC",
            "user_goal": "RWA yield",
            "known_market": "I only saw one market",
            "exit_plan": "Partial exit plan",
            "risk_profile": "Balanced",
            "time_horizon": "Medium-term",
            "user_confidence": "Medium",
            "understands_pt": "Partially",
            "understands_lp": "No",
            "understands_loop": "No",
            "wants_infinit_first": True,
            "demo_mode": "STRCx / Pendle demo",
            "show_advanced_route": False,
        },
        "STRCx + Pro INFINIT route": {
            "target_asset": "STRCx",
            "current_token": "USDC",
            "user_goal": "Highest APY",
            "known_market": "I know several markets",
            "exit_plan": "Clear exit plan",
            "risk_profile": "Aggressive",
            "time_horizon": "Medium-term",
            "user_confidence": "High",
            "understands_pt": "Yes",
            "understands_lp": "Partially",
            "understands_loop": "Yes",
            "wants_infinit_first": True,
            "demo_mode": "STRCx / Pendle demo",
            "show_advanced_route": True,
        },
        "STRCx with doubts": {
            "target_asset": "STRCx",
            "current_token": "USDC",
            "user_goal": "RWA yield",
            "known_market": "I only saw one market",
            "exit_plan": "No exit plan",
            "risk_profile": "Conservative",
            "time_horizon": "Medium-term",
            "user_confidence": "Low",
            "understands_pt": "Partially",
            "understands_lp": "No",
            "understands_loop": "No",
            "wants_infinit_first": True,
            "demo_mode": "STRCx / Pendle demo",
            "show_advanced_route": True,
        },
        "USDC current-token fallback": {
            "target_asset": "RWA market",
            "current_token": "USDC",
            "user_goal": "Safer structure",
            "known_market": "Not sure",
            "exit_plan": "No exit plan",
            "risk_profile": "Conservative",
            "time_horizon": "Medium-term",
            "user_confidence": "Low",
            "understands_pt": "Partially",
            "understands_lp": "No",
            "understands_loop": "No",
            "wants_infinit_first": True,
            "demo_mode": "General RWA decision",
            "show_advanced_route": False,
        },
        "xStocks beginner": {
            "target_asset": "xStocks",
            "current_token": "USDC",
            "user_goal": "Tokenized equity exposure",
            "known_market": "Not sure",
            "exit_plan": "No exit plan",
            "risk_profile": "Conservative",
            "time_horizon": "Short-term",
            "user_confidence": "Low",
            "understands_pt": "No",
            "understands_lp": "No",
            "understands_loop": "No",
            "wants_infinit_first": True,
            "demo_mode": "General RWA decision",
            "show_advanced_route": False,
        },
        "Aggressive APY seeker": {
            "target_asset": "RWA stablecoin",
            "current_token": "USDT",
            "user_goal": "Highest APY",
            "known_market": "I only saw one market",
            "exit_plan": "Partial exit plan",
            "risk_profile": "Aggressive",
            "time_horizon": "Short-term",
            "user_confidence": "High",
            "understands_pt": "No",
            "understands_lp": "No",
            "understands_loop": "No",
            "wants_infinit_first": True,
            "demo_mode": "General RWA decision",
            "show_advanced_route": True,
        },
        "Manual input": {
            "target_asset": "STRCx",
            "current_token": "USDC",
            "user_goal": "RWA yield",
            "known_market": "I only saw one market",
            "exit_plan": "Partial exit plan",
            "risk_profile": "Balanced",
            "time_horizon": "Medium-term",
            "user_confidence": "Medium",
            "understands_pt": "Partially",
            "understands_lp": "No",
            "understands_loop": "No",
            "wants_infinit_first": True,
            "demo_mode": "STRCx / Pendle demo",
            "show_advanced_route": False,
        },
    }

    selected = presets[preset]

    target_asset = st.sidebar.text_input("Target RWA / tokenized asset", selected["target_asset"])
    current_token = st.sidebar.text_input("Current token", selected["current_token"])

    user_goal_options = [
        "RWA yield",
        "Safer structure",
        "Stable RWA yield",
        "Tokenized equity exposure",
        "Fixed yield",
        "Liquidity provision",
        "Highest APY",
        "Not sure",
    ]

    user_goal = st.sidebar.selectbox(
        "User goal",
        user_goal_options,
        index=user_goal_options.index(selected["user_goal"]),
    )

    known_market_options = [
        "I know several markets",
        "I only saw one market",
        "Not sure",
    ]

    known_market = st.sidebar.selectbox(
        "Known market status",
        known_market_options,
        index=known_market_options.index(selected["known_market"]),
    )

    exit_plan_options = [
        "Clear exit plan",
        "Partial exit plan",
        "No exit plan",
    ]

    exit_plan = st.sidebar.selectbox(
        "Exit plan",
        exit_plan_options,
        index=exit_plan_options.index(selected["exit_plan"]),
    )

    risk_profile_options = [
        "Conservative",
        "Balanced",
        "Aggressive",
    ]

    risk_profile = st.sidebar.selectbox(
        "Risk profile",
        risk_profile_options,
        index=risk_profile_options.index(selected["risk_profile"]),
    )

    time_horizon_options = [
        "Short-term",
        "Medium-term",
        "Until maturity",
        "Long-term",
    ]

    time_horizon = st.sidebar.selectbox(
        "Time horizon",
        time_horizon_options,
        index=time_horizon_options.index(selected["time_horizon"]),
    )

    confidence_options = [
        "High",
        "Medium",
        "Low",
    ]

    user_confidence = st.sidebar.selectbox(
        "User confidence",
        confidence_options,
        index=confidence_options.index(selected["user_confidence"]),
    )

    knowledge_options = ["Yes", "Partially", "No"]

    understands_pt = st.sidebar.selectbox(
        "Do you understand PT / maturity?",
        knowledge_options,
        index=knowledge_options.index(selected["understands_pt"]),
    )

    understands_lp = st.sidebar.selectbox(
        "Do you understand LP / impermanent loss?",
        knowledge_options,
        index=knowledge_options.index(selected["understands_lp"]),
    )

    understands_loop = st.sidebar.selectbox(
        "Do you understand loops / liquidation?",
        knowledge_options,
        index=knowledge_options.index(selected["understands_loop"]),
    )

    wants_infinit_first = st.sidebar.checkbox(
        "Use INFINIT as preferred orchestration layer",
        value=selected["wants_infinit_first"],
    )

    demo_mode_options = [
        "General RWA decision",
        "STRCx / Pendle demo",
    ]

    demo_mode = st.sidebar.selectbox(
        "Demo mode",
        demo_mode_options,
        index=demo_mode_options.index(selected["demo_mode"]),
    )

    show_advanced_route = st.sidebar.checkbox(
        "Show advanced pro route: Leverage Looping - PT apyUSD",
        value=selected["show_advanced_route"],
    )

    return UserInput(
        target_asset=target_asset,
        current_token=current_token,
        user_goal=user_goal,
        known_market=known_market,
        exit_plan=exit_plan,
        risk_profile=risk_profile,
        time_horizon=time_horizon,
        user_confidence=user_confidence,
        understands_pt=understands_pt,
        understands_lp=understands_lp,
        understands_loop=understands_loop,
        wants_infinit_first=wants_infinit_first,
        demo_mode=demo_mode,
        show_advanced_route=show_advanced_route,
    )


def render_recommendation(rec):
    status_icon = {
        "Ready to Explore": "🟢",
        "Needs Review": "🟡",
        "Do Not Force Entry": "🔴",
        "Blocked": "⛔",
        "Valid Option": "🔵",
    }.get(rec.decision_status, "⚪")

    with st.container(border=True):
        st.subheader(f"{status_icon} {rec.name}")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Decision status", rec.decision_status)

        with col2:
            st.metric("Risk", rec.risk_level)

        with col3:
            st.metric("Complexity", rec.complexity_level)

        st.write("### Simple explanation")
        st.write(rec.simple_description)

        st.write("### Execution / route")
        st.info(rec.route_message)

        with st.expander("Why this path may make sense", expanded=True):
            for item in rec.why_this_path:
                st.write(f"- {item}")

        with st.expander("Warnings"):
            for item in rec.warnings:
                st.write(f"- {item}")

        with st.expander("What to verify before action"):
            for item in rec.verification_steps:
                st.write(f"- {item}")

        st.write("### Next checkpoint")
        st.write(rec.next_checkpoint)


def main():
    st.title("🧭 Productive Capital Oracle V2")

    st.caption(
        "A continuous RWA decision layer. STRCx / Pendle is the committee demo case."
    )

    st.markdown(
        """
        **V1 asked:**  
        “So, you bought RWA. What next?”

        **V2 continues V1:**  
        It checks readiness, detects fake confidence, identifies weak market awareness,
        reviews missing exit plans, avoids forcing RWA exposure, compares strategy paths,
        validates risk, routes execution logic through INFINIT first, and creates review checkpoints.

        **Core principle:**  
        Productive Capital Oracle does not execute trades.  
        It acts as a decision layer before execution.

        **Preferred orchestration layer:** INFINIT  
        **Fallback examples:** Pendle, current-token routes, protocol-specific routes  
        **Committee demo:** STRCx / Pendle / PT / LP / 50/50  
        **Advanced demo route:** Leverage Looping - PT apyUSD via INFINIT
        """
    )

    user_input = build_user_input()

    oracle = ProductiveCapitalOracleV2()
    result = oracle.analyze(user_input)

    st.divider()

    st.header("Oracle Result")

    st.write("### Context")
    st.write(result.context_summary)

    st.write("### Final message")
    st.success(result.final_message)

    st.write("### Market Scout")
    st.info(result.market_report.summary)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Market status", result.market_report.market_status)

    with col2:
        st.metric("Confidence", result.market_report.confidence_level)

    with col3:
        st.metric(
            "Current-token fallback",
            "Yes" if result.market_report.use_current_token_fallback else "No",
        )

    with st.expander("Market red flags"):
        for item in result.market_report.red_flags:
            st.write(f"- {item}")

    with st.expander("Positive signals"):
        for item in result.market_report.positive_signals:
            st.write(f"- {item}")

    st.write("### Market Pulse")
    st.warning(result.pulse_report.summary)

    with st.expander("Watch items"):
        for item in result.pulse_report.watch_items:
            st.write(f"- {item}")

    with st.expander("Review signals"):
        for item in result.pulse_report.review_signals:
            st.write(f"- {item}")

    st.write("### Review & Retention Layer")
    st.info(result.review_plan.global_checkpoint)
    st.write(result.review_plan.review_reason)

    with st.expander("Strategy checkpoints"):
        for name, checkpoint in result.review_plan.strategy_checkpoints.items():
            st.write(f"**{name}:** {checkpoint}")

    st.divider()

    st.header("Strategy Recommendations")

    for rec in result.recommendations:
        render_recommendation(rec)

    st.divider()

    st.header("Current-Token Strategy Scanner")

    if result.current_token_routes:
        for route in result.current_token_routes:
            with st.container(border=True):
                st.subheader(route.name)
                st.write(route.simple_description)
                st.write(f"**Ecosystem:** {route.ecosystem}")
                st.write(f"**Risk:** {route.risk_level}")
                st.write(f"**Complexity:** {route.complexity_level}")

                st.write("**Possible protocol layers:**")
                for protocol in route.possible_protocols:
                    st.write(f"- {protocol}")

                st.write("**Verification required:**")
                for item in route.verification_required:
                    st.write(f"- {item}")
    else:
        st.write("Current-token fallback was not required in this scenario.")

    st.divider()

    st.header("MVP Transparency")
    st.warning(result.disclaimer)

    with st.expander("Metadata"):
        st.json(result.metadata)


if __name__ == "__main__":
    main()
