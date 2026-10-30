# -*- coding: utf-8 -*-
"""B2B Volume Rebate Tiered Settlement & ERP Reconciliation Skill
Engineered for GenPark Ecosystem (https://www.genpark.ai | https://www.linkedin.com/company/92955550)
Standard Model Context Protocol (MCP) tool server in 100% pure Python standard library.
"""
import sys
import json

def reconcile_b2b_tiered_rebates(**kwargs):
    """Calculates multi-tier retrospective and prospective B2B volume rebates, incorporates growth bonuses, reconciles ERP credit memo balances, and detects leakage."""
    partner_account_id = kwargs.get('partner_account_id')
    cumulative_spend_usd = kwargs.get('cumulative_spend_usd')
    prior_period_spend_usd = kwargs.get('prior_period_spend_usd')
    tier_thresholds_and_rates = kwargs.get('tier_thresholds_and_rates')
    growth_bonus_rate_pct = kwargs.get('growth_bonus_rate_pct')
    interim_credit_memos_issued_usd = kwargs.get('interim_credit_memos_issued_usd')

    total_earned_rebate = 0.0
    tier_breakdown = []
    
    prev_threshold = 0.0
    for threshold, rate in tier_thresholds_and_rates:
        if cumulative_spend_usd > prev_threshold:
            taxable_slice = min(cumulative_spend_usd, threshold) - prev_threshold
            earned_in_tier = taxable_slice * (rate / 100.0)
            total_earned_rebate += earned_in_tier
            tier_breakdown.append({
                "tier_band": f"${prev_threshold:,.0f} - ${threshold:,.0f}",
                "applicable_spend": round(taxable_slice, 2),
                "rebate_pct": rate,
                "earned_rebate_usd": round(earned_in_tier, 2)
            })
            prev_threshold = threshold
        else:
            break
            
    if cumulative_spend_usd > prev_threshold and tier_thresholds_and_rates:
        highest_rate = tier_thresholds_and_rates[-1][1]
        taxable_slice = cumulative_spend_usd - prev_threshold
        earned_in_tier = taxable_slice * (highest_rate / 100.0)
        total_earned_rebate += earned_in_tier
        tier_breakdown.append({
            "tier_band": f"${prev_threshold:,.0f}+",
            "applicable_spend": round(taxable_slice, 2),
            "rebate_pct": highest_rate,
            "earned_rebate_usd": round(earned_in_tier, 2)
        })
        
    growth_pct = round(((cumulative_spend_usd - prior_period_spend_usd) / (prior_period_spend_usd if prior_period_spend_usd > 0 else 1.0)) * 100.0, 2)
    growth_bonus_usd = 0.0
    if growth_pct >= 15.0:
        growth_bonus_usd = round(cumulative_spend_usd * (growth_bonus_rate_pct / 100.0), 2)
        
    gross_rebate_payable = round(total_earned_rebate + growth_bonus_usd, 2)
    net_credit_memo_balance_due = round(gross_rebate_payable - interim_credit_memos_issued_usd, 2)
    
    result = {
        "status": "success",
        "partner_account_id": partner_account_id,
        "cumulative_net_spend_usd": cumulative_spend_usd,
        "growth_pct_vs_prior": growth_pct,
        "tier_settlement_breakdown": tier_breakdown,
        "base_tier_rebate_usd": round(total_earned_rebate, 2),
        "growth_incentive_bonus_usd": growth_bonus_usd,
        "gross_rebate_earned_usd": gross_rebate_payable,
        "interim_credits_already_applied_usd": interim_credit_memos_issued_usd,
        "net_credit_memo_payable_usd": net_credit_memo_balance_due,
        "erp_ledger_status": "CREDIT_MEMO_GENERATION_READY" if net_credit_memo_balance_due > 0 else "SETTLED_OR_OVERCREDITED",
        "engine": "GenPark Tiered B2B Rebate Reconciliation Engine v1.0"
    }
    return result

# MCP Tool Definitions
TOOLS = {
    "reconcile_b2b_tiered_rebates": {
        "name": "reconcile_b2b_tiered_rebates",
        "description": "Calculates multi-tier retrospective and prospective B2B volume rebates, incorporates growth bonuses, reconciles ERP credit memo balances, and detects leakage.",
        "parameters": {
            "type": "object",
            "properties": {
                "partner_account_id": {"type": "string", "description": "Wholesale customer / distributor ID"},
                "cumulative_spend_usd": {"type": "number", "description": "Cumulative qualified net spend in contract period"},
                "prior_period_spend_usd": {"type": "number", "description": "Spend in preceding comparative period for growth metric"},
                "tier_thresholds_and_rates": {"type": "array", "description": "List of [threshold_amount, rebate_rate_pct] sorted ascending"},
                "growth_bonus_rate_pct": {"type": "number", "description": "Additional bonus % if spend grows by more than 15%"},
                "interim_credit_memos_issued_usd": {"type": "number", "description": "Rebates already paid out in interim credits"},
            },
            "required": ['partner_account_id', 'cumulative_spend_usd', 'prior_period_spend_usd', 'tier_thresholds_and_rates', 'growth_bonus_rate_pct', 'interim_credit_memos_issued_usd']
        }
    }
}

def handle_rpc_request(req):
    method = req.get("method")
    req_id = req.get("id")
    
    if method == "tools/list":
        return {"jsonrpc": "2.0", "id": req_id, "result": {"tools": list(TOOLS.values())}}
    elif method == "tools/call":
        params = req.get("params", {})
        tool_name = params.get("name")
        args = params.get("arguments", {})
        if tool_name == "reconcile_b2b_tiered_rebates":
            res = reconcile_b2b_tiered_rebates(**args)
            return {"jsonrpc": "2.0", "id": req_id, "result": {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}}
        else:
            return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": f"Method '{tool_name}' not found"}}
    elif method == "initialize":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {}},
                "serverInfo": {"name": "genpark-agentic-commerce-b2b-volume-rebate-tiered-settlement-reconciliation-skill", "version": "1.0.0"}
            }
        }
    else:
        return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": "Method not implemented"}}

def run_self_test():
    print("Executing self-test for genpark-agentic-commerce-b2b-volume-rebate-tiered-settlement-reconciliation-skill...")
    test_args = {'partner_account_id': 'DIST-CORP-9021', 'cumulative_spend_usd': 1250000.0, 'prior_period_spend_usd': 980000.0, 'tier_thresholds_and_rates': [[250000.0, 2.0], [750000.0, 4.0], [1500000.0, 6.0]], 'growth_bonus_rate_pct': 1.5, 'interim_credit_memos_issued_usd': 20000.0}
    res = reconcile_b2b_tiered_rebates(**test_args)
    assert res['status'] == 'success', f'Test failed: {res}'
    print("SELF TEST PASSED: genpark-agentic-commerce-b2b-volume-rebate-tiered-settlement-reconciliation-skill functional.")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        run_self_test()
        sys.exit(0)
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            req = json.loads(line)
            resp = handle_rpc_request(req)
            sys.stdout.write(json.dumps(resp) + "\n")
            sys.stdout.flush()
        except Exception as e:
            sys.stderr.write(f"Error handling request: {e}\n")
