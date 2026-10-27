#!/usr/bin/env python3
"""capture-evidence.py — P3-Beweislauf Evidence-Capture (read-only, oeffentliche Felder).

Liest Run-/Job-/Commit-Referenzen ueber die oeffentliche GitHub-API (via gh CLI) und
die lokalen Git-Klone und schreibt ein maschinenlesbares JSON fuer Review und
Abnahme des v0.4.27 Receipt-Pilot (CODEMAN-START §5/§6, Task
t-20261027-r27-shadow-run).

Felder: run_id, run_attempt, workflow_id/workflow_name, head_sha, candidate_sha,
base_sha, receipt_path, plan_revision, introduction/approval/publication commits,
post-run/approval run-Referenzen und rc/Erwartungs-Abgleich je Check.

Secrets: es werden ausschliesslich oeffentliche Felder geschrieben. Kein Token, kein
Env-Dump, keine Artefakt-Inhalte aus Nicht-Oeffentlichkeit; `gh` nutzt die vorhandene
Authentifizierung der Session, dieses Skript lognt sie nie.

Grenzen: keine Actions-Ausloesung (kein dispatch/rerun/subscribe), keine Schreibzugriffe
auf Produkt- oder Planning-Repos; nur `gh ... view/list/get/download` und lokale
Git-Leseoperationen. DryRun-konform: dieses Skript DARF ausgefuehrt werden (read-only),
es veraendert ausser der --output-Datei nichts.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import subprocess
import sys
from pathlib import Path

PRODUCT = "mcpdev80/baseharbor"
PLANNING = "mcpdev80/baseharbor-plan"
GATE = "public-contracts"  # scripts/receipt_verifier.py GATE
EXPECTED_PROD_WORKFLOW_PATH = ".github/workflows/ci.yml"
EXPECTED_EVENT = "pull_request"


def gh(*args: str) -> object:
    result = subprocess.run(["gh", *args], capture_output=True, text=True)
    if result.returncode != 0:
        raise SystemExit(f"gh failed: gh {' '.join(args)}\n{result.stderr.strip()}")
    return json.loads(result.stdout) if result.stdout.strip() else None


def git_text(repo: str, *args: str) -> str:
    result = subprocess.run(["git", "-C", repo, *args], capture_output=True, text=True)
    if result.returncode != 0:
        raise SystemExit(f"git failed: git -C {repo} {' '.join(args)}\n{result.stderr.strip()}")
    return result.stdout.strip()


def git_ok(repo: str, *args: str) -> bool:
    return subprocess.run(["git", "-C", repo, *args], capture_output=True).returncode == 0


def run_facts(repo: str, run_id: int) -> dict:
    data = gh("run", "view", str(run_id), "-R", repo, "--json",
              "databaseId,attempt,displayTitle,headSha,headBranch,status,conclusion,"
              "workflowDatabaseId,workflowName,event,path,url")
    return {
        "run_id": data.get("databaseId"),
        "attempt": int(data.get("attempt", 1)),
        "workflow_id": data.get("workflowDatabaseId"),
        "workflow_name": data.get("workflowName"),
        "workflow_path": data.get("path"),
        "event": data.get("event"),
        "head_sha": data.get("headSha"),
        "head_branch": data.get("headBranch"),
        "status": data.get("status"),
        "conclusion": data.get("conclusion"),
        "url": data.get("url"),
    }


def job_rc(repo: str, run_id: int, job_name: str) -> int | None:
    """rc-Semantik fuer CI-Jobs: 0 success, 1 failure/sonstiges, None missing."""
    data = gh("run", "view", str(run_id), "-R", repo, "--json", "jobs")
    for job in data.get("jobs", []):
        if job.get("name") == job_name:
            return 0 if job.get("conclusion") == "success" else 1
    return None


def check(name: str, ok: bool | None, expected: str, actual: object) -> dict:
    return {"check": name, "expected": expected, "actual": actual,
            "pass": ok if ok is not None else None}


def plan_from_blob(planning: str, revision: str) -> dict:
    raw = git_text(planning, "show", f"{revision}:evidence/receipt-plans/{GATE}.json")
    return json.loads(raw)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--pr", type=int, required=True, help="contributor PR number")
    ap.add_argument("--run", type=int, help="producer CI run id (default: neuester Run fuer PR-head)")
    ap.add_argument("--post-run", type=int, help="receipt-post-run workflow_run id (optional)")
    ap.add_argument("--approval-run", type=int, help="receipt-approval dispatch run id (optional)")
    ap.add_argument("--planning", default=os.environ.get("PLANNING_LOCAL", ""),
                    help="lokaler baseharbor-plan checkout (Vollhistorie noetig)")
    ap.add_argument("--product", default=os.environ.get("PRODUCT_LOCAL", ""),
                    help="lokaler baseharbor checkout am Kandidaten")
    ap.add_argument("--verifier", help="Pfad zu scripts/receipt_verifier.py (fuer rc-Checks)")
    ap.add_argument("--output", type=Path, required=True)
    args = ap.parse_args()

    pr = gh("pr", "view", str(args.pr), "-R", PRODUCT, "--json",
            "number,headRefOid,baseRefOid,baseRefName,author,url,state")
    head_sha = pr["headRefOid"]
    run_id = args.run
    if run_id is None:
        rows = gh("run", "list", "-R", PRODUCT, "--branch", f"refs/pull/{args.pr}/merge",
                   "--workflow", EXPECTED_PROD_WORKFLOW_PATH, "--limit", "5",
                   "--json", "databaseId,headSha,attempt") or []
        fresh = [r for r in rows if r.get("headSha") == head_sha]
        if not fresh:
            raise SystemExit("kein producer-run fuer PR-head gefunden — STOP nach README")
        run_id = fresh[0]["databaseId"]

    prod = run_facts(PRODUCT, run_id)
    checks = []
    checks.append(check("run_event", prod["event"] == EXPECTED_EVENT,
                        EXPECTED_EVENT, prod["event"]))
    checks.append(check("run_workflow_path",
                        prod["workflow_path"] == EXPECTED_PROD_WORKFLOW_PATH,
                        EXPECTED_PROD_WORKFLOW_PATH, prod["workflow_path"]))
    checks.append(check("run_head_is_pr_head", prod["head_sha"] == head_sha,
                        "== PR headRefOid", prod["head_sha"]))
    checks.append(check("run_attempt_1", prod["attempt"] == 1, "1", prod["attempt"]))
    checks.append(check("run_success", prod["conclusion"] == "success",
                        "success", prod["conclusion"]))
    evidence = {"schema": "baseharbor.pr3-proof/v1",
                "captured_at": dt.datetime.now(dt.timezone.utc)
                .strftime("%Y-%m-%dT%H:%M:%SZ"),
                "repository": PRODUCT,
                "gate": GATE,
                "pr": {"number": pr["number"], "author": (pr.get("author") or {}).get("login"),
                       "state": pr.get("state"), "url": pr.get("url"),
                       "base_ref": pr.get("baseRefName")},
                "producer_run": prod,
                "head_sha": prod["head_sha"],
                "base_sha": pr["baseRefOid"],
                "candidate_sha": None,
                "receipt_path": None,
                "plan_revision": None,
                "introduction_commit": None,
                "approval_commit": None,
                "publication_commit": None,
                "post_run": None,
                "approval_run": None,
                "checks": checks}

    evidence["receipt_path"] = f"evidence/receipts/{GATE}/{prod['run_id']}-{prod['attempt']}.json"
    gate_job = job_rc(PRODUCT, run_id, "PR · Public Contracts")
    plan_job = job_rc(PRODUCT, run_id, "PR · Trusted Plan")
    checks.append(check("gate_job_rc", gate_job == 0 if gate_job is not None else None,
                            "0 (PR · Public Contracts success)", gate_job))
    checks.append(check("trusted_plan_job_rc", plan_job == 0 if plan_job is not None else None,
                            "0 (PR · Trusted Plan success)", plan_job))

    if args.planning:
        planning_head = git_text(args.planning, "rev-parse", "HEAD")
        plan = plan_from_blob(args.planning, planning_head)
        evidence["plan_revision"] = planning_head
        evidence["plan_fixture"] = {k: plan.get(k) for k in
                                    ("gate", "repository", "workflow_id", "head_sha",
                                     "candidate_sha", "base_sha", "task")}
        evidence["candidate_sha"] = plan.get("candidate_sha")
        checks.append(check("plan_candidate_is_pr_head",
                            plan.get("candidate_sha") == head_sha,
                            "== PR headRefOid", plan.get("candidate_sha")))
        checks.append(check("plan_workflow_id_matches_run",
                            plan.get("workflow_id") == prod["workflow_id"],
                            "== producer workflowDatabaseId", plan.get("workflow_id")))
        if git_ok(args.planning, "cat-file", "-e", f"HEAD:{evidence['receipt_path']}"):
            raw = git_text(args.planning, "show", f"HEAD:{evidence['receipt_path']}")
            try:
                value = json.loads(raw)
            except json.JSONDecodeError:
                value = None
                checks.append(check("receipt_canonical_json", False, "parseable canonical",
                                    "invalid"))
            if value:
                evidence["candidate_sha"] = value.get("sha")
                evidence["plan_revision"] = value.get("plan")
                evidence["approved_field"] = value.get("approved")
                first = git_text(args.planning, "log", "--format=%H", "--reverse",
                                 "--", evidence["receipt_path"]).splitlines()
                if first:
                    evidence["introduction_commit"] = first[0]
                    edits = git_text(args.planning, "log", "--format=%H",
                                     f"{first[0]}..HEAD",
                                     "--", evidence["receipt_path"]).splitlines()
                    if len(edits) == 1:
                        evidence["approval_commit"] = edits[0]
                    elif len(edits) > 1:
                        checks.append(check("receipt_single_approval_edit", False,
                                            "exactly 1 edit after introduction",
                                            {"edits": len(edits), "commits": edits}))
                    evidence["publication_commit"] = planning_head
        else:
            checks.append(check("receipt_published_in_planning", False,
                                "receipt path present at Planning HEAD",
                                evidence["receipt_path"]))
        if args.product and evidence["plan_revision"]:
            evidence["introduction_in_planning_history"] = git_ok(
                args.planning, "merge-base", "--is-ancestor",
                evidence.get("introduction_commit") or planning_head, "HEAD")

    if args.post_run:
        evidence["post_run"] = run_facts(PRODUCT, args.post_run)
    if args.approval_run:
        evidence["approval_run"] = run_facts(PRODUCT, args.approval_run)

    # rc je Check fuer die Verifier-Aufrufe (live erst vor, retained nach Approval).
    if args.verifier and evidence["receipt_path"] and args.planning:
        revision = git_text(args.planning, "rev-parse", "HEAD")
        mode = "retained" if evidence.get("approved_field") else "live"
        cmd = [sys.executable, args.verifier, mode, "--planning", args.planning,
               "--revision", revision, "--receipt", evidence["receipt_path"],
               "--candidate", evidence.get("candidate_sha") or "",
               "--plan", evidence.get("plan_revision") or revision]
        if mode == "live" and args.product:
            cmd += ["--product", args.product]
        proc = subprocess.run(cmd, capture_output=True, text=True)
        evidence["verifier_mode"] = mode
        checks.append(check(f"verifier_{mode}_rc", proc.returncode == 0, "0",
                            {"rc": proc.returncode,
                             "stderr_tail": proc.stderr.strip().splitlines()[-1:]}))

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(evidence, indent=2, sort_keys=True) + "\n")
    print(f"wrote {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
