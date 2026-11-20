# 0428-068 — three witness lines (run 44715140090, head bf923b52)

Exact-form witnesses for the Owner. Measured 2026-11-20.

## (a) ls-remote — branch head = PR head (same SHA)

```
$ git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/b-068-cli2-context-shell refs/pull/1710/head
bf923b52ba4340465ba28329773a2ec6b4ca1070	refs/heads/b-068-cli2-context-shell
bf923b52ba4340465ba28329773a2ec6b4ca1070	refs/pull/1710/head
```

Both refs resolve to `bf923b52ba4340465ba28329773a2ec6b4ca1070`.

## (b) merge-base — current develop IS ancestor of PR head

```
$ git fetch lane-origin refs/pull/1710/head
$ git merge-base --is-ancestor 681700ca66f3 <pr-head>; echo $?
```

Measured: the current develop tip is `dbe7fbc3905b4330acdcfbf3bfb5f4f3af34d0d2` (3 commits past `681700ca66f3`, which the Owner cited first). Against the actual current tip:

```
$ git merge-base --is-ancestor dbe7fbc3905b4330acdcfbf3bfb5f4f3af34d0d2 <pr-head>; echo $?
0   # exit 0 => develop IS ancestor of PR head
```

`git merge-base dbe7fbc3… bf923b52…` == `dbe7fbc3905b4330acdcfbf3bfb5f4f3af34d0d2` (exactly current develop). Rebase base = develop tip; 4 commits on top.

## (c) run-id + terminal status + conclusion

- Run **44715140090** (event `pull_request`, head `bf923b52`) → **completed | success**.
- 40 jobs total; all `PR · Go unit · cli-*` shards (cli-0, cli-1, cli-2, cli-3, packages, owner) ran and passed (not skipped). No non-success / non-skipped job.
- Conclusion: r2 is green at the delivered head `bf923b52` on current develop. The r1 head `eff023c0` / r2-1 head `d1ec4b72` runs (44700679422, 44712300731) are superseded by this terminal run.
