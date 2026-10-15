"""Positive and negative fixtures for scripts/plan.py.

Each test builds a small vault in a temporary directory, so no fixture files
with checkboxes live in the real vault.
"""
import contextlib
import hashlib
import io
import json
import pathlib
import shutil
import sys
import tempfile
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
import plan  # noqa: E402

REPO = pathlib.Path(__file__).resolve().parents[2]


def task_note(tid, title, status="planned", release="v1.0", extra="", deps="[]", done=False, tags=None):
    box = "x" if done else " "
    tag = tags if tags is not None else (f" #status/{status}" if status else "")
    return f"""---
id: {tid}
type: task
release: {release}
parent: ""
owner: {extra or '""'}
depends_on: {deps}
repos: [mcpdev80/baseharbor]
prs: []
sources: ["mcpdev80/baseharbor#{tid.split('-')[1]}"]
blocker: ""
resolution: ""
evidence: []
---

- [{box}] {tid} · {title} #task #release/{release.replace('.', '-')}{tag}

## Goal

Something.
"""


class Fixture:
    def __init__(self):
        self.dir = pathlib.Path(tempfile.mkdtemp())
        for d in ("tasks", "releases", "epics", "decisions", "views", "templates"):
            (self.dir / d).mkdir()
        (self.dir / "releases" / "v1.0.md").write_text(
            "---\nid: v1.0\nkind: release\ntitle: Test\nstatus: active\norder: 1\nsources: []\nevidence: []\n---\n\n# v1.0\n")
        (self.dir / "releases" / "v2.0.md").write_text(
            "---\nid: v2.0\nkind: release\ntitle: Later\nstatus: planned\norder: 2\nsources: []\nevidence: []\n---\n\n# v2.0\n")
        shutil.copy(REPO / "templates" / "task.md", self.dir / "templates" / "task.md")
        cb = self.dir / ".obsidian" / "plugins" / "card-board"
        cb.mkdir(parents=True)
        cfg = json.loads((REPO / ".obsidian/plugins/card-board/data.json").read_text())
        cfg["data"]["boardConfigs"] = [{
            "columns": [{"tag": "namedTag", "data": {"collapsed": False, "name": "Planned", "tag": "status/planned"}},
                        {"tag": "completed", "data": {"collapsed": False, "index": 1, "limit": 5, "name": "Closed"}}],
            "filters": [{"tag": "tagFilter", "data": "task"}], "filterPolarity": "Allow",
            "filterScope": "TopLevelOnly", "name": "All", "showColumnTags": False, "showFilteredTags": False}]
        (cb / "data.json").write_text(json.dumps(cfg))
        og = self.dir / ".obsidian" / "plugins" / "obsidian-git"
        og.mkdir(parents=True)
        shutil.copy(REPO / ".obsidian/plugins/obsidian-git/data.json", og / "data.json")
        self.sources = []

    def add_task(self, tid, text):
        (self.dir / "tasks" / f"{tid}-x.md").write_text(text)
        self.sources.append(f"mcpdev80/baseharbor#{tid.split('-')[1]}")

    def finish(self, extra_sources=()):
        snap = self.dir / "migration" / "source-snapshot"
        (snap / "baseharbor").mkdir(parents=True)
        entries = []
        for src in list(self.sources) + list(extra_sources):
            num = src.split("#")[1]
            f = snap / "baseharbor" / f"{num}.json"
            f.write_text(json.dumps({"source": src}))
            entries.append({"source": src, "title": "t", "updated_at": "2026-01-01T00:00:00Z", "comments": 0,
                            "file": str(f.relative_to(self.dir)),
                            "sha256": hashlib.sha256(f.read_bytes()).hexdigest()})
        (snap / "inventory.json").write_text(json.dumps({
            "captured_at": "2026-01-01T00:00:00Z", "repositories": ["mcpdev80/baseharbor"],
            "open_issues": entries, "open_pull_requests": []}))
        return self

    def run(self, *args):
        out = io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(out):
            code = plan.main(["--root", str(self.dir)] + list(args))
        return code, out.getvalue()

    def checked(self):
        self.run("render")
        return self.run("check")


class PlanTests(unittest.TestCase):
    def fixture(self):
        f = Fixture()
        self.addCleanup(shutil.rmtree, f.dir)
        return f

    def assertCheckFails(self, f, needle):
        code, out = f.checked()
        self.assertEqual(code, 1, out)
        self.assertIn(needle, out)

    def test_valid_vault_passes_and_derives_ready(self):
        f = self.fixture()
        f.add_task("core-1", task_note("core-1", "Area: first"))
        f.add_task("core-2", task_note("core-2", "Area: second", deps="[core-1]"))
        f.finish()
        code, out = f.checked()
        self.assertEqual(code, 0, out)
        _, listing = f.run("list", "--ready")
        self.assertIn("core-1", listing)
        self.assertNotIn("core-2", listing)

    def test_task_in_unstarted_release_is_queued_unless_early(self):
        f = self.fixture()
        f.add_task("core-1", task_note("core-1", "A: later", release="v2.0"))
        f.add_task("core-2", task_note("core-2", "B: pulled ahead", release="v2.0").replace("blocker:", "early: true\nblocker:"))
        f.finish()
        code, out = f.checked()
        self.assertEqual(code, 0, out)
        _, queued = f.run("list", "--status", "queued")
        _, ready = f.run("list", "--ready")
        self.assertIn("core-1", queued)
        self.assertIn("core-2", ready)
        self.assertNotIn("core-1", ready)

    def test_render_is_stable(self):
        f = self.fixture()
        f.add_task("core-1", task_note("core-1", "Area: first"))
        f.finish()
        f.run("render")
        before = {p: p.read_text() for p in f.dir.rglob("*.md")}
        _, out = f.run("render")
        self.assertEqual(out.strip(), "")
        self.assertEqual(before, {p: p.read_text() for p in f.dir.rglob("*.md")})

    def test_duplicate_id_is_rejected(self):
        f = self.fixture()
        f.add_task("core-1", task_note("core-1", "Area: first"))
        (f.dir / "tasks" / "core-1-y.md").write_text(task_note("core-1", "Area: copy"))
        f.finish()
        self.assertCheckFails(f, "duplicate id core-1")

    def test_cycle_is_rejected(self):
        f = self.fixture()
        f.add_task("core-1", task_note("core-1", "A: a", deps="[core-2]"))
        f.add_task("core-2", task_note("core-2", "B: b", deps="[core-1]"))
        f.finish()
        self.assertCheckFails(f, "dependency cycle")

    def test_unknown_dependency_is_rejected(self):
        f = self.fixture()
        f.add_task("core-1", task_note("core-1", "A: a", deps="[core-9]"))
        f.finish()
        self.assertCheckFails(f, "unknown dependency 'core-9'")

    def test_checked_card_needs_evidence_and_no_status_tag(self):
        f = self.fixture()
        f.add_task("core-1", task_note("core-1", "A: a", done=True, tags=" #status/review"))
        f.finish()
        code, out = f.checked()
        self.assertEqual(code, 1)
        self.assertIn("conflicting lifecycle markers", out)
        self.assertIn("requires evidence", out)

    def test_checked_card_with_resolution_and_evidence_passes(self):
        f = self.fixture()
        text = task_note("core-1", "A: a", done=True, tags=" #status/closed").replace('resolution: ""', "resolution: accepted").replace(
            "evidence: []", 'evidence: ["https://example.org/run/1"]')
        text = text.replace("#status/closed\n", "#status/closed @completed(2026-10-15T10:00:00)\n")
        f.add_task("core-1", text)
        f.add_task("core-2", task_note("core-2", "B: b", deps="[core-1]"))
        f.finish()
        code, out = f.checked()
        self.assertEqual(code, 0, out)
        _, listing = f.run("list", "--ready")
        self.assertIn("core-2", listing)

    def test_closed_tag_on_unchecked_card_is_rejected(self):
        f = self.fixture()
        f.add_task("core-1", task_note("core-1", "A: a", status="closed"))
        f.finish()
        self.assertCheckFails(f, "#status/closed on an unchecked card")

    def test_two_status_tags_are_rejected(self):
        f = self.fixture()
        f.add_task("core-1", task_note("core-1", "A: a", tags=" #status/planned #status/active"))
        f.finish()
        self.assertCheckFails(f, "exactly one #status tag")

    def test_active_requires_owner(self):
        f = self.fixture()
        f.add_task("core-1", task_note("core-1", "A: a", status="active"))
        f.finish()
        self.assertCheckFails(f, "status active requires an owner")

    def test_extra_checkbox_in_task_note_is_rejected(self):
        f = self.fixture()
        f.add_task("core-1", task_note("core-1", "A: a") + "\n## Acceptance\n\n- [ ] accidental card\n")
        f.finish()
        self.assertCheckFails(f, "exactly one checkbox")

    def test_checkbox_outside_tasks_is_rejected(self):
        f = self.fixture()
        f.add_task("core-1", task_note("core-1", "A: a"))
        f.finish()
        (f.dir / "HOME.md").write_text("# Home\n\n- [ ] stray card\n")
        self.assertCheckFails(f, "would become a CardBoard card")

    def test_release_tag_must_match_release(self):
        f = self.fixture()
        f.add_task("core-1", task_note("core-1", "A: a").replace("#release/v1-0", "#release/v2-0"))
        f.finish()
        self.assertCheckFails(f, "does not match release")

    def test_unmapped_inventory_issue_is_rejected(self):
        f = self.fixture()
        f.add_task("core-1", task_note("core-1", "A: a"))
        f.finish(extra_sources=["mcpdev80/baseharbor#99"])
        self.assertCheckFails(f, "mcpdev80/baseharbor#99 is not accounted for")

    def test_duplicate_alias_maps_source(self):
        f = self.fixture()
        f.add_task("core-1", task_note("core-1", "A: a").replace("blocker:", 'aliases: ["mcpdev80/baseharbor#7"]\nblocker:'))
        f.finish(extra_sources=["mcpdev80/baseharbor#7"])
        code, out = f.checked()
        self.assertEqual(code, 0, out)
        manifest = json.loads((f.dir / "migration" / "manifest.json").read_text())
        entry = next(e for e in manifest["issues"] if e["source"] == "mcpdev80/baseharbor#7")
        self.assertEqual(entry["disposition"], "duplicate")

    def test_tampered_snapshot_is_rejected(self):
        f = self.fixture()
        f.add_task("core-1", task_note("core-1", "A: a"))
        f.finish()
        (f.dir / "migration/source-snapshot/baseharbor/1.json").write_text("{}")
        self.assertCheckFails(f, "does not match its inventory digest")

    def test_stale_generated_view_is_rejected(self):
        f = self.fixture()
        f.add_task("core-1", task_note("core-1", "A: a"))
        f.finish()
        f.run("render")
        (f.dir / "views" / "overview.md").write_text("edited by hand\n")
        code, out = f.run("check")
        self.assertEqual(code, 1)
        self.assertIn("generated file is stale", out)

    def test_broken_link_is_rejected(self):
        f = self.fixture()
        f.add_task("core-1", task_note("core-1", "A: a") + "\nSee [missing](nope.md).\n")
        f.finish()
        self.assertCheckFails(f, "broken link 'nope.md'")

    def test_unsupported_cardboard_config_is_rejected(self):
        f = self.fixture()
        f.add_task("core-1", task_note("core-1", "A: a"))
        f.finish()
        path = f.dir / ".obsidian/plugins/card-board/data.json"
        cfg = json.loads(path.read_text())
        cfg["data"]["boardConfigs"][0]["columns"][0]["data"]["tag"] = "status/doing"
        cfg["data"]["globalSettings"]["filters"] = []
        path.write_text(json.dumps(cfg))
        code, out = f.checked()
        self.assertEqual(code, 1)
        self.assertIn("not a known status or release tag", out)
        self.assertIn("must ignore templates/", out)

    def test_automatic_git_sync_is_rejected(self):
        f = self.fixture()
        f.add_task("core-1", task_note("core-1", "A: a"))
        f.finish()
        path = f.dir / ".obsidian/plugins/obsidian-git/data.json"
        cfg = json.loads(path.read_text())
        cfg["autoPushInterval"] = 10
        path.write_text(json.dumps(cfg))
        self.assertCheckFails(f, "autoPushInterval must be 0")

    def test_claim_sets_owner_and_active(self):
        f = self.fixture()
        f.add_task("core-1", task_note("core-1", "A: a"))
        f.finish()
        f.run("render")
        code, out = f.run("claim", "core-1", "--owner", "tester (s1)")
        self.assertEqual(code, 0, out)
        text = (f.dir / "tasks" / "core-1-x.md").read_text()
        self.assertIn('owner: tester (s1)', text)
        self.assertIn("#status/active", text)
        code, out = f.run("check")
        self.assertEqual(code, 0, out)
        code, out = f.run("claim", "core-1", "--owner", "someone else")
        self.assertEqual(code, 1)

    def test_new_creates_valid_task(self):
        f = self.fixture()
        f.add_task("core-1", task_note("core-1", "A: a"))
        f.finish()
        code, out = f.run("new", "--repo", "core", "--slug", "try-it", "--title", "Area: try", "--release", "v1.0")
        self.assertEqual(code, 0, out)
        code, out = f.checked()
        self.assertEqual(code, 0, out)


    def test_topic_badges_follow_frontmatter_and_preserve_state(self):
        f = self.fixture()
        note = task_note("core-1", "CI: readable").replace("type: task", "type: bug\nareas: [ci, security]")
        f.add_task("core-1", note)
        f.finish()
        self.assertEqual(f.checked()[0], 0)
        path = f.dir / "tasks/core-1-x.md"
        self.assertIn("#area/ci #area/security #kind/bug", path.read_text())
        path.write_text(path.read_text().replace("#area/ci", "#area/wrong"))
        self.assertEqual(f.run("check")[0], 1)
        f.run("render")
        self.assertNotIn("#area/wrong", path.read_text())
        self.assertIn("#status/planned", path.read_text())

    def test_invalid_or_duplicate_topic_slugs_are_rejected(self):
        for areas in ("[CI]", "[ci, ci]", "[ci/other]"):
            f = self.fixture()
            f.add_task("core-1", task_note("core-1", "CI: bad").replace("type: task", "type: task\nareas: " + areas))
            f.finish()
            self.assertCheckFails(f, "areas must contain unique lowercase tag slugs")

    def test_roadmap_counts_acceptance_not_review_and_keeps_release_status(self):
        f = self.fixture()
        note = task_note("core-1", "A: review", status="review", extra="tester").replace("prs: []", 'prs: ["mcpdev80/baseharbor#1"]')
        f.add_task("core-1", note)
        f.finish()
        f.run("render")
        roadmap = f.dir / "roadmap/cards.md"
        self.assertIn("**Accepted tasks:** 0/1", roadmap.read_text())
        path = f.dir / "tasks/core-1-x.md"
        path.write_text(path.read_text().replace("- [ ]", "- [x]").replace("#status/review", "#status/closed")
                        .replace('resolution: ""', 'resolution: accepted').replace("evidence: []", '[REPLACE]'))
        path.write_text(path.read_text().replace('[REPLACE]', 'evidence: ["https://example.org/proof"]'))
        f.run("render")
        self.assertIn("**Accepted tasks:** 1/1", roadmap.read_text())
        self.assertIn("**Release:** active", roadmap.read_text())
        self.assertIn("#roadmap-state/next", roadmap.read_text())
        self.assertIn("no executable tasks cut yet", roadmap.read_text())
        self.assertEqual(f.run("check")[0], 0)

    def test_roadmap_ui_edits_are_rejected_not_task_acceptance(self):
        f = self.fixture().finish()
        f.run("render")
        path = f.dir / "roadmap/cards.md"
        path.write_text(path.read_text().replace("- [ ]", "- [x]", 1))
        code, out = f.run("check")
        self.assertEqual(code, 1)
        self.assertIn("generated file is stale", out)
        self.assertEqual(len(plan.Vault(f.dir).load().tasks), 0)

    def test_topic_css_hides_routing_not_topic_badges(self):
        css = (REPO / ".obsidian/snippets/baseharbor-board.css").read_text()
        self.assertIn('[href^="#area/"]', css)
        self.assertIn('[href^="#kind/"]', css)
        cfg = json.loads((REPO / ".obsidian/plugins/card-board/data.json").read_text())
        roadmap = next(b for b in cfg['data']['boardConfigs'] if b['name'] == 'Roadmap')
        self.assertEqual(roadmap['filters'], [{'tag': 'tagFilter', 'data': 'roadmap'}])
        self.assertEqual(plan.validate_cardboard(cfg, {plan.release_tag(x.stem) for x in (REPO / 'releases').glob('*.md')}), [])

    def test_current_board_shows_every_planned_task_without_duplicates(self):
        cfg = json.loads((REPO / ".obsidian/plugins/card-board/data.json").read_text())
        board = next(b for b in cfg["data"]["boardConfigs"] if b["name"] == "Current · v0.4.26")
        tags = [col["data"].get("tag") for col in board["columns"]]
        self.assertEqual(board["columns"][0]["data"]["name"], "Planned")
        self.assertEqual(tags.count("status/planned"), 1)
        self.assertNotIn("view/waiting", tags)
        self.assertNotIn("view/ready", tags)
        self.assertNotIn("view/queued", tags)
        f = self.fixture()
        f.add_task("core-1", task_note("core-1", "A: ready"))
        f.add_task("core-2", task_note("core-2", "B: waiting", deps="[core-1]"))
        f.finish()
        f.run("render")
        ready = (f.dir / "tasks/core-1-x.md").read_text()
        waiting = (f.dir / "tasks/core-2-x.md").read_text()
        self.assertIn("**Ready to assign**", ready)
        self.assertIn("**Waiting for prerequisites**", waiting)
        self.assertIn("**Needs:** [core-1]", waiting)
        for text in (ready, waiting):
            self.assertIn("#status/planned", text)
        self.assertEqual(f.run("check")[0], 0)

    def test_generated_card_has_actual_owner_priority_and_pr(self):
        f = self.fixture()
        note = task_note("core-1", "Area: readable", extra="tester (session 2)")
        note = note.replace("blocker:", "priority: high\nblocker:").replace("prs: []", 'prs: ["mcpdev80/baseharbor#930"]')
        f.add_task("core-1", note)
        f.finish()
        code, out = f.checked()
        self.assertEqual(code, 0, out)
        text = (f.dir / "tasks/core-1-x.md").read_text()
        self.assertIn("**Owner:** tester (session 2) · **Priority:** high", text)
        self.assertIn("[baseharbor#930](https://github.com/mcpdev80/baseharbor/pull/930)", text)
        self.assertEqual(sum(bool(plan.CHECKBOX.match(line)) for line in text.splitlines()), 1)

    def test_card_readiness_changes_only_when_prerequisite_is_accepted(self):
        f = self.fixture()
        f.add_task("core-1", task_note("core-1", "A: prerequisite"))
        f.add_task("core-2", task_note("core-2", "B: consumer", deps="[core-1]"))
        f.finish()
        f.run("render")
        consumer = f.dir / "tasks/core-2-x.md"
        self.assertIn("#status/planned #view/waiting", consumer.read_text())
        self.assertIn("**Needs:** [core-1]", consumer.read_text())
        prerequisite = f.dir / "tasks/core-1-x.md"
        # A merged PR alone does not accept the prerequisite.
        prerequisite.write_text(prerequisite.read_text().replace("prs: []", 'prs: ["mcpdev80/baseharbor#9"]'))
        f.run("render")
        self.assertIn("#view/waiting", consumer.read_text())
        prerequisite.write_text(prerequisite.read_text().replace("- [ ]", "- [x]").replace("#status/planned", "#status/closed")
                               .replace('resolution: ""', 'resolution: accepted')
                               .replace("evidence: []", 'evidence: ["https://example.org/proof"]'))
        f.run("render")
        self.assertIn("#status/planned #view/ready", consumer.read_text())
        self.assertNotIn("**Needs:**", consumer.read_text())
        code, out = f.run("check")
        self.assertEqual(code, 0, out)

    def test_false_or_duplicate_readiness_tag_is_rejected(self):
        f = self.fixture()
        f.add_task("core-1", task_note("core-1", "A: prerequisite"))
        f.add_task("core-2", task_note("core-2", "B: consumer", deps="[core-1]"))
        f.finish()
        f.run("render")
        path = f.dir / "tasks/core-2-x.md"
        path.write_text(path.read_text().replace("#view/waiting", "#view/ready #view/waiting"))
        code, out = f.run("check")
        self.assertEqual(code, 1)
        self.assertIn("generated readiness tag is stale", out)

    def test_card_preview_cannot_be_edited_as_a_second_record(self):
        f = self.fixture()
        f.add_task("core-1", task_note("core-1", "A: a", extra="real owner"))
        f.finish()
        f.run("render")
        path = f.dir / "tasks/core-1-x.md"
        path.write_text(path.read_text().replace("**Owner:** real owner", "**Owner:** fabricated owner"))
        code, out = f.run("check")
        self.assertEqual(code, 1)
        self.assertIn("generated card preview is stale", out)

    def test_status_change_refreshes_one_view_tag_and_preserves_handoff(self):
        f = self.fixture()
        f.add_task("core-1", task_note("core-1", "A: a", extra="tester") + "\n## Handoff\n\nKeep exact source SHA and original failure here.\n")
        f.finish()
        f.run("render")
        path = f.dir / "tasks/core-1-x.md"
        path.write_text(path.read_text().replace("#status/planned", "#status/active"))
        code, out = f.run("check")
        self.assertEqual(code, 1)  # Obsidian edits do not silently refresh derived data.
        f.run("render")
        text = path.read_text()
        self.assertIn("#status/active #view/active", text)
        self.assertNotIn("#view/ready", text)
        self.assertEqual(text.count("#view/"), 1)
        self.assertIn("Keep exact source SHA and original failure here.", text)
        self.assertEqual(f.run("check")[0], 0)

    def test_queued_card_does_not_claim_it_is_startable(self):
        f = self.fixture()
        f.add_task("core-1", task_note("core-1", "A: later", release="v2.0"))
        f.finish()
        f.run("render")
        text = (f.dir / "tasks/core-1-x.md").read_text()
        self.assertIn("#view/queued", text)
        self.assertIn("**Later release**", text)
        self.assertNotIn("**Ready to assign**", text)
        self.assertNotIn("core-1", (f.dir / "views/ready.md").read_text())

    def test_invalid_priority_is_rejected_and_missing_is_not_invented(self):
        f = self.fixture()
        f.add_task("core-1", task_note("core-1", "A: a"))
        f.finish()
        f.run("render")
        path = f.dir / "tasks/core-1-x.md"
        self.assertIn("**Priority:** not set", path.read_text())
        path.write_text(path.read_text().replace("blocker:", "priority: imaginary\nblocker:"))
        self.assertCheckFails(f, "priority must be empty")

    def test_card_text_cannot_inject_a_checkbox_or_status_tag(self):
        value = "owner\n- [ ] forged #status/closed <script>"
        rendered = plan.card_text(value)
        self.assertNotIn("\n", rendered)
        self.assertIn("\\#status/closed", rendered)
        self.assertIn("\\<script\\>", rendered)



class RealVaultTest(unittest.TestCase):
    def test_repository_vault_is_valid(self):
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            code = plan.main(["--root", str(REPO), "check"])
        self.assertEqual(code, 0, out.getvalue())


if __name__ == "__main__":
    unittest.main()
