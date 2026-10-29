## PLAN
0. Initialize stale-pr-hygiene.md evidence file for q203 lane (r27 stale-PR hygiene audit)
1. Fetch origin and list all open PRs on mcpdev80/baseharbor
2. Audit PR #1188 (work/r27-producer-docs) - cherry diff + content analysis
3. Audit PR #1168 (work/shadow-probe3) - cherry diff + content analysis
4. Audit any other open PRs found beyond #1188 and #1168
5. Write RECOMMEND per PR with evidence hashes, finalize with END q203-DONE

## q203 stale-PR hygiene audit - t-20261029-r27
READ-ONLY lane. No commits, no gh close/merge. Recommendations only.

---

## Step 1: Fetch origin and enumerate open PRs

```
$ git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor fetch origin
```

```
$ gh pr list --repo mcpdev80/baseharbor --state open
```

---

## Step 2: PR #1188 (work/r27-producer-docs) audit

```
$ git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor fetch origin
$ git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor cherry origin/develop origin/work/r27-producer-docs
$ git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor diff --stat origin/develop...origin/work/r27-producer-docs
```

Content analysis: identify files in work/r27-producer-docs that exist nowhere on origin/develop.

RECOMMEND:

---

## Step 3: PR #1168 (work/shadow-probe3) audit

```
$ git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor fetch origin
$ git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor cherry origin/develop origin/work/shadow-probe3
$ git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor diff --stat origin/develop...origin/work/shadow-probe3
```

Content analysis: identify files in work/shadow-probe3 that exist nowhere on origin/develop.

RECOMMEND:

---

## Step 4: Other open PRs audit

For any additional open PRs discovered in Step 1, apply the same cherry/diff/content analysis and RECOMMEND.

---

END q203-DONE
