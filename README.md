# Productive Capital Oracle V2

## Core idea

Productive Capital Oracle V2 continues V1.

V1 asked:

> So, you bought RWA. What next?

V2 expands this into a broader RWA decision layer.

It helps the user understand:

- whether they should enter an RWA / xStocks market at all
- whether market awareness is weak
- whether confidence is real or fake
- whether an exit plan exists
- whether the user understands PT / LP / loops
- whether current-token routes may be safer
- whether execution should go through INFINIT
- whether fallback routes need review
- when the user should return for a checkpoint

The tone can be light, but the purpose is serious:

- check readiness
- detect fake confidence
- identify weak market awareness
- identify missing exit plans
- avoid forcing RWA exposure

---

## Important positioning

Productive Capital Oracle V2 is not a live trading bot.

It does not execute transactions.

It does not connect to a wallet.

It does not provide financial advice.

It is an MVP decision-support prototype that models how a future wallet-aware and market-aware Oracle could work.

Current V2 is a static decision-logic MVP, not a live market scanner.

What works now:

- readiness checks
- fake-confidence detection
- exit-plan review
- strategy path comparison
- risk blocking
- current-token fallback
- INFINIT-first routing logic
- review checkpoints

---

## Product formula

> Productive Capital Oracle = decision layer  
> INFINIT = preferred orchestration layer  
> Fallback protocols = execution venues when INFINIT route is not available  
> User = final decision maker

---

## V1 → V2

### V1

V1 was a post-exposure decision MVP.

It asked:

> So, you bought RWA. What next?

It helped the user think about:

- what they are holding
- what can go wrong
- what paths exist
- whether to wait
- when to review

### V2

V2 continues V1.

It does not only ask what happens after RWA exposure.

It also checks whether the user should enter the RWA market at all.

If the market is unclear, the Oracle should not force RWA exposure.

Instead, it can review the current token the user already holds and compare safer strategy paths.

---

## Multi-Agent Architecture

Productive Capital Oracle V2 uses a simple internal multi-agent architecture.

### 1. RWA Market Scout Agent

Checks whether a usable RWA / xStocks market exists before the user buys.

It evaluates:

- what token the user currently holds
- what RWA exposure the user wants
- market availability
- liquidity clarity
- exit route clarity
- user readiness
- whether the current token can be used instead

If no suitable RWA market exists, the Oracle should not force RWA exposure.

---

### 2. Current-Token Strategy Scanner

If no usable RWA market exists, the Oracle does not force RWA exposure.

Instead, it analyzes the token the user already holds and checks whether safer strategy routes may exist.

Planned protocol layers:

#### Ethereum / Multi-chain

- Morpho
- Aave
- Pendle
- INFINIT

#### Solana

- Kamino

#### BNB Chain

- Venus
- Lista
- PancakeSwap
- Beefy
- Thena

#### Mantle

- Mantle ecosystem routes
- INFINIT-style orchestration
- future RWA / xStocks routes

The Oracle does not execute.

It only compares route logic, risks, and verification requirements.

---

### 3. Strategy Agent

Proposes a strategy path.

Possible paths:

- RWA market discovery
- current-token strategy
- PT / fixed-yield review
- experimental xStocks path
- Wait / No Action

Committee demo case:

- STRCx / Pendle
- PT
- LP
- 50/50 PT-LP
- Advanced Pro Route: Leverage Looping - PT apyUSD via INFINIT

Important:

> STRCx / Pendle / PT / LP / 50/50 is a demo case, not the full product boundary.

The Strategy Agent proposes.

It does not validate safety.

---

### 4. Market Pulse Agent

Observes market conditions.

Current V2 uses static demo assumptions.

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

---

### 5. Risk Guardian Agent

Validates safety.

It checks:

- weak market conditions
- unclear exit
- high volatility
- low confidence
- hidden leverage
- experimental xStocks risk
- too many red flags
- vault / curator risk for Morpho-style routes
- lending / liquidity / leverage risk for Kamino-style routes
- advanced looping / liquidation risk

The Risk Guardian Agent can downgrade confidence or block a strategy.

---

### 6. Review & Retention Layer

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

This makes the Oracle a continuous decision layer, not a one-time strategy generator.

---

## Execution model

The Oracle does not execute.

It only decides whether a path is reasonable, risky, unclear, or blocked.

Preferred orchestration layer:

> INFINIT

If an INFINIT route exists, the user should review and confirm the strategy there.

If no INFINIT route exists, the Oracle may suggest a fallback route.

Fallback examples:

- Pendle for PT / LP / 50/50 demo case
- Morpho / Aave-style vault or lending route
- Kamino-style lending or liquidity route
- BNB Chain routes such as Venus, Lista, PancakeSwap, Beefy or Thena
- Mantle ecosystem routes
- Wait / No Action

---

## Oracle × INFINIT relationship

Productive Capital Oracle does not compete with INFINIT.

It sits before execution.

The Oracle helps the user decide:

- should I enter this RWA strategy?
- do I understand the risks?
- is the market clear enough?
- do I have an exit plan?
- should I wait instead?

If the path is reasonable and an INFINIT route exists, INFINIT becomes the preferred orchestration layer.

If no INFINIT route exists, the Oracle explains fallback routes and marks them as requiring manual verification.

---

## Demo case: STRCx / Pendle

The demo case shows how the Oracle works.

Example user:

> I want to buy STRCx.  
> I saw a Pendle market.  
> I do not fully understand PT / LP / 50/50.  
> I am not sure whether there are better routes.  
> What should I do?

The Oracle can compare:

- STRCx PT
- STRCx LP
- STRCx 50/50 PT-LP
- INFINIT route if available
- Wait / No Action
- Current-token fallback if market awareness is weak

### PT

PT is a fixed-yield style path.

The user buys a discounted Principal Token that matures into the underlying asset later.

Main risks:

- maturity risk
- early-exit risk
- liquidity risk
- underlying asset risk

### LP

LP is a liquidity-provider path.

The user provides liquidity to a market and may earn fees or incentives.

Main risks:

- impermanent loss
- liquidity risk
- APY variability
- exit risk

### 50/50 PT-LP

A balanced allocation between PT and LP.

Important:

> 50/50 is balanced by allocation, but not simple by risk.

Main risks:

- combines PT maturity risk and LP risk
- requires understanding both mechanisms
- liquidity and exit conditions must be verified

---

## Committee demo: PT vs LP strategy comparison

One demo scenario shows how the Oracle compares PT and LP strategies.

The goal is not to recommend the highest APY.

The goal is to explain the trade-off.

### PT path

PT is treated as a fixed-yield core route.

It may offer lower APY, but it is usually easier to understand and more predictable if the user can hold until maturity.

Main review points:

- maturity date
- early-exit conditions
- liquidity
- underlying asset risk

### LP path

LP is treated as a growth / liquidity route.

It may offer higher APY, but it depends more on pool activity, incentives, liquidity depth and market conditions.

Main review points:

- impermanent loss
- liquidity depth
- pool activity
- APY sustainability
- exit conditions

### Oracle conclusion

PT is more stable.

LP is more profitable, but riskier.

The Oracle does not force the user into the higher APY path.

It explains the difference, checks readiness, validates risk, and creates a review checkpoint.

---

## Advanced pro route: Leverage Looping - PT apyUSD

The STRCx / Pendle example shows the basic PT vs LP decision.

If the user is advanced and wants a more aggressive fixed-yield route, the Oracle can also surface an INFINIT professional strategy:

> Leverage Looping - PT apyUSD

This route is part of the same committee demo ladder:

1. Basic route: PT
2. Growth route: LP
3. Balanced route: 50/50 PT-LP
4. Professional route: Leverage Looping - PT apyUSD through INFINIT

This route is not a default recommendation.

It is shown only as an advanced alternative and must pass Risk Guardian checks.

### What this route means

Leverage Looping - PT apyUSD is an advanced INFINIT strategy.

It uses PT exposure together with lending / borrowing mechanics to amplify yield.

It may show higher APY, but it also adds:

- leverage risk
- liquidation risk
- lending protocol risk
- loop complexity
- APY instability
- exit complexity
- collateral risk

### Oracle behavior

For beginners:

> Blocked / Do Not Force Entry

For balanced users:

> Needs Review

For advanced users:

> Advanced Route Available, but live verification is required.

### Risk Guardian checks

The Oracle must not force this route.

Risk Guardian should block or downgrade it unless the user clearly understands:

- PT mechanics
- lending / borrowing
- loop structure
- liquidation risk
- collateral risk
- exit conditions
- APY instability

### Positioning

This route is shown only as a professional branch of the committee demo.

It is not the default recommendation.

The Oracle first checks simpler paths:

- PT
- LP
- 50/50 PT-LP
- Wait / No Action
- Current-token route

Only after that can it show advanced looping strategies.

---

## Why this matters

Many RWA users do not only need access to tokenized assets.

They need to understand:

- what strategies exist
- what PT / LP / loops actually mean
- where the risks are
- whether their confidence is real
- whether an exit plan exists
- whether a current-token strategy may be safer
- when to stop, wait, review, and return

---

## Positioning line

Yield tools tell users where to go.

Productive Capital Oracle tells users when to stop, wait, review, and return — not in panic, but with a plan.

---

## Current MVP limitations

This version does not use live market discovery.

This version does not connect to:

- INFINIT API
- Pendle API
- wallet data
- live liquidity data
- live APY data
- issuer / custodian / redemption data
- Morpho live vault data
- Kamino live lending / liquidity data

It is a static decision-logic prototype.

It demonstrates the logic of a future Oracle.

---

## Future upgrades

Future versions should add:

- wallet analysis
- live market discovery
- live INFINIT route availability
- live Pendle market checks
- liquidity and spread analysis
- asset risk database
- issuer / custodian / redemption checks
- Morpho vault data
- Kamino lending / liquidity data
- Aave / Venus / Lista route checks
- PancakeSwap / Beefy / Thena route checks
- Mantle xStocks / RWA route mapping
- review alerts
- maturity reminders
- APY change alerts
- price deviation monitoring
- advanced looping health monitoring
- collateral and liquidation monitoring

---

## AI-Agent Architecture

Productive Capital Oracle V2 is designed as an AI-agent decision architecture for RWA users.

The current hackathon MVP uses deterministic agents as a safety-first core.  
This allows the system to provide explainable decisions, structured risk checks, route comparison, and review checkpoints without relying on unstable AI-generated financial advice.

The agents in the current version include:

- **Market Scout Agent** — checks whether the market is mature enough to consider.
- **Risk Guardian Agent** — detects blockers, warnings, missing exit plans, and excessive complexity.
- **Strategy Agent** — compares possible routes such as PT, LP, 50/50, INFINIT routes, or waiting.
- **Route Orchestrator Agent** — maps the decision to possible execution paths.
- **Review & Retention Agent** — creates checkpoints after entry and helps users decide when to review, wait, return, or exit.

This version is not a fully autonomous financial AI.

It is a working MVP of a decision-agent system.

The next stage is to connect each agent to:

- LLM reasoning
- live market data
- protocol tools
- user memory
- execution availability
- stronger guardrails

The goal is not autonomous trading.

The goal is safer decision-making before DeFi execution.

## Current MVP vs Next Stage

**Current MVP:**  
A rule-based multi-agent decision system for RWA users.

**Next Stage:**  
AI-assisted agents with LLM reasoning, live market tools, memory, and INFINIT execution routing.

This approach keeps the current prototype stable and explainable, while showing a clear path toward real AI agents.

---


## Local run

Install dependencies:

```bash
pip install -r requirements.txt
