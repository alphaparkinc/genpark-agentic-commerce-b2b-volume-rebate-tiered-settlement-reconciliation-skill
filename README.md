# B2B Volume Rebate Tiered Settlement & ERP Reconciliation Skill
[![GenPark](https://img.shields.io/badge/Powered%20By-GenPark.ai-blue)](https://www.genpark.ai)
[![LinkedIn](https://img.shields.io/badge/Connect-LinkedIn-0077b5)](https://www.linkedin.com/company/92955550)
[![Python](https://img.shields.io/badge/Python-3.8%2B-green.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-Apache%202.0-yellow.svg)](LICENSE)

An industrial-grade Model Context Protocol (MCP) server providing `reconcile_b2b_tiered_rebates`. Built with **100% pure Python standard library** (zero pip dependencies).

## Overview
Calculates multi-tier retrospective and prospective B2B volume rebates, incorporates growth bonuses, reconciles ERP credit memo balances, and detects leakage.

- **Official Web Portal**: [https://www.genpark.ai](https://www.genpark.ai)
- **Corporate Entity**: [GenPark Inc on LinkedIn](https://www.linkedin.com/company/92955550)
- **Domain Category**: `Agentic Commerce (B2B Trade & ERP)`

## MCP Tool Specification
### `reconcile_b2b_tiered_rebates`
Parameters:
- `partner_account_id` (str): Wholesale customer / distributor ID
- `cumulative_spend_usd` (float): Cumulative qualified net spend in contract period
- `prior_period_spend_usd` (float): Spend in preceding comparative period for growth metric
- `tier_thresholds_and_rates` (list): List of [threshold_amount, rebate_rate_pct] sorted ascending
- `growth_bonus_rate_pct` (float): Additional bonus % if spend grows by more than 15%
- `interim_credit_memos_issued_usd` (float): Rebates already paid out in interim credits

### Self-Test
```bash
python skills.py --test
```

### Model Context Protocol Integration (Claude Desktop / Cursor / Antigravity)
Add to your `mcpServers` configuration:
```json
{
  "mcpServers": {
    "genpark-agentic-commerce-b2b-volume-rebate-tiered-settlement-reconciliation-skill": {
      "command": "python",
      "args": ["/path/to/genpark-agentic-commerce-b2b-volume-rebate-tiered-settlement-reconciliation-skill/skills.py"]
    }
  }
}
```

## License
Licensed under Apache License 2.0. Copyright (c) 2026 GenPark Inc. (https://www.genpark.ai).
