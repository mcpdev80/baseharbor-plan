# BF-03 fix — round-2 witness (CI gate re-run)

- Mission: `/tmp/opencode/mission-bf03-fix.md` (card `t-20261115-bughunt-d28-tmp-selection` = 0427-187)
- Lane branch: `lane-0428-fix-bf03`, head `c678cdd0a7385504be76d4acf927e47080e3db81`
- Coordinator-run observation: run `43667577512` on `829d75bc` terminal FAILED
- Fix: `gofmt` reformat of `internal/orgconfig/store.go` (my own code)
- Re-run: `43668270812` on `c678cdd0` terminal SUCCESS

## Gate investigation

Run `43667577512` failed on job "PR · Draft source and routing" (ID `132670279399`).
Job log:

```
$ gh run view 43667577512 --repo mcpdev80/baseharbor --log-failed --job 132670279399
...
PR · Draft source and routing	Validate changed Go formatting and CI routes
...
Unformatted Go source: internal/orgconfig/store.go
PR · Draft source and routing	... ##[error]Process completed with exit code 1.
```

The "source and routing" gate's failing assertion was the `gofmt -l` check on my
own source (`internal/orgconfig/store.go`), NOT a PR-object metadata requirement
(title/body/labels/source-verweis on card 0427-187). No PR metadata change needed.

## Fix

```
$ cd /tmp/opencode/bf03-fix-wt
$ gofmt -d internal/orgconfig/store.go   # doc-comment bullet reindent
$ gofmt -w internal/orgconfig/store.go internal/orgconfig/orgconfig_test.go
$ gofmt -l internal/orgconfig/           # empty -> all formatted
$ go build ./... && go vet ./internal/orgconfig/ && go test ./internal/orgconfig/ -count=1
ok  	github.com/mcpdev80/baseharbor/internal/orgconfig  0.082s
$ git add internal/orgconfig/store.go internal/orgconfig/orgconfig_test.go
$ git commit -m "chore(BF-03): gofmt internal/orgconfig after world-writable fix"
[c678cdd0]
$ git push   # 829d75bc..c678cdd0
```

## Re-run witness

```
$ gh run view 43668270812 --repo mcpdev80/baseharbor --json status,conclusion
{"conclusion":"success","status":"completed"}
```

Run `43668270812` (trigger `pull_request`, head `c678cdd0`) terminal:
**completed / success**. Job "PR · Draft source and routing" (ID `132672405686`)
now ✓; all 6 Go jobs pass (cli-0/1/2/3, packages). Remaining matrix jobs pending,
not failed.

## END

END_DONE mission-bf03-fix.md: routing gate `43667577512` was a gofmt violation in
my own `internal/orgconfig/store.go` — fixed with `gofmt -w`, committed
`c678cdd0`, re-run `43668270812` terminal SUCCESS. PR #1582 DRAFT base develop head
`c678cdd0`; no PR metadata / `.github/**` change; CI for `internal/orgconfig` runs
under normal `pull_request`.
