"""REDLINE-1.0 attack simulations. All four operator attacks REFUSE.

callable AZG · enable via GET · fake ICANN publish · Cap-7 resolve_to_hub true
Plus GET radio/plant, theater crypto, fielded 100.
Author: Aziel Eliab only.
"""

from __future__ import annotations

from pathlib import Path

from miragegrid.az_generator import AzGenerator, DeepNode, PaperVault, refuse_call_generator, synthetic_papers
from miragegrid.mesh import mesh_law_dict, refuse_get_enable_or_plant, refuse_radio_phy
from miragegrid.redline import (
    CALLABLE_AZG_ALIASES,
    PUBLIC_MESH_GET_DOORS,
    REDLINE_SPEC,
    foldlock_cite,
    lamb_lens_cite,
    redline_dict,
    refuse_callable_alias,
    refuse_fielded_100,
    refuse_theater_crypto,
    run_attack_sims,
)
from miragegrid.semantic_bridge import (
    CORPUS_HUB,
    WORKER_HOST,
    build_bridge_registry,
    cap7_bridge_cite,
    dead_named_worker,
    semantic_bridge_dict,
    shelves_cite,
)

ROOT = Path(__file__).resolve().parents[1]
MESH_JS = (ROOT / "workers/download-tracker/src/mesh.js").read_text(encoding="utf-8")
RUNTIME = (ROOT / "workers/download-tracker/src/runtime.js").read_text(encoding="utf-8")
INDEX = (ROOT / "workers/download-tracker/src/index.js").read_text(encoding="utf-8")
BRIDGE = (ROOT / "workers/download-tracker/src/bridge.js").read_text(encoding="utf-8")
HOME = (ROOT / "workers/download-tracker/src/homepage.js").read_text(encoding="utf-8")
SKILL = (ROOT / "SKILL.md").read_text(encoding="utf-8")
README = (ROOT / "README.md").read_text(encoding="utf-8")
REDLINE_DOC = (ROOT / "docs/REDLINE-1.0.md").read_text(encoding="utf-8")
MESH_LAW = (ROOT / "docs/mesh-law.md").read_text(encoding="utf-8")


def test_operator_attack_sims_all_refuse() -> None:
    bar = run_attack_sims()
    assert bar["code"] == "REDLINE-GREEN"
    assert bar["ok"] is True
    assert bar["yes"] is True
    assert bar["public_icann"] is False
    assert bar["resolves_to_hub"] is False
    assert bar["callable"] is False
    assert bar["get_never_enables"] is True
    assert bar["fielded_100"] is False
    assert bar["public_door_crypto"] == "cloudflare-tls"
    assert bar["foldlock"] == "cite-only"
    assert bar["lamb_lens"] is True
    assert bar["smaller_door"] is True
    names = {s["name"] for s in bar["sims"]}
    assert {
        "callable-azg",
        "enable-via-get",
        "get-radio-plant",
        "fake-icann-publish",
        "cap7-resolve-to-hub",
        "theater-crypto",
        "fielded-100",
    } <= names
    for sim in bar["sims"]:
        assert sim["ok"] is True, sim


def test_callable_azg_refuses() -> None:
    node = DeepNode("node-07", vault=PaperVault(synthetic_papers(49)))
    assert node.call_generator()["code"] == "AZG-NOT-CALLABLE"
    assert AzGenerator("node-08").call()["code"] == "AZG-NOT-CALLABLE"
    assert refuse_call_generator(path="/v1/mesh/az-generator")["callable"] is False
    for alias in CALLABLE_AZG_ALIASES:
        row = refuse_callable_alias(alias)
        assert row["code"] == "AZG-NOT-CALLABLE"
        assert row["ok"] is False


def test_get_never_enables_radios_or_plants() -> None:
    enable = refuse_get_enable_or_plant(method="GET", path="/v1/mesh/enable")
    assert enable is not None
    assert enable["code"] == "MESH-GET-NO-ENABLE"
    assert enable["enabled"] is False
    assert enable["claim_plant"] is False
    q = refuse_get_enable_or_plant(method="GET", path="/v1/mesh", search="enable=1")
    assert q is not None and q["code"] == "MESH-GET-NO-ENABLE"
    radio = refuse_get_enable_or_plant(method="GET", path="/v1/mesh", search="radio=on")
    assert radio is not None and radio["code"] == "MESH-GET-NO-ENABLE"
    plant = refuse_get_enable_or_plant(method="GET", path="/v1/mesh/az-generator", search="plant=1")
    assert plant is not None and plant["code"] == "MESH-GET-NO-ENABLE"
    claim = refuse_get_enable_or_plant(method="HEAD", path="/v1/mesh/az-generator", search="claim=true")
    assert claim is not None and claim["code"] == "MESH-GET-NO-ENABLE"
    clean = refuse_get_enable_or_plant(method="GET", path="/v1/mesh")
    assert clean is None
    cite = refuse_get_enable_or_plant(method="GET", path="/v1/mesh/az-generator")
    assert cite is None
    post = refuse_get_enable_or_plant(method="POST", path="/v1/mesh/enable")
    assert post is None
    phy = refuse_radio_phy(kind="rf")
    assert phy["hub_get_enables_mesh"] is False
    assert phy["radio_phy"] is False


def test_fake_icann_and_resolve_to_hub_refuse() -> None:
    assert build_bridge_registry([], icann_publish=True)["code"] == "BRIDGE-NO-ICANN-PUBLISH"
    assert build_bridge_registry([], public_icann=True)["code"] == "BRIDGE-NO-PUBLIC-DNS"
    assert build_bridge_registry([], resolve_to_hub=True)["code"] == "BRIDGE-NO-HUB-RESOLVE"
    law = semantic_bridge_dict()
    assert law["public_icann"] is False
    assert law["resolves_to_hub"] is False
    assert law["callable"] is False


def test_tls_foldlock_lamb_lens_no_fielded_100() -> None:
    tls = refuse_theater_crypto(layer="cloudflare-tls")
    assert tls["code"] == "REDLINE-TLS-OK"
    assert refuse_theater_crypto(layer="xor")["code"] == "REDLINE-NO-THEATER-CRYPTO"
    assert refuse_theater_crypto(foldlock_as_crypto=True)["code"] == "REDLINE-NO-THEATER-CRYPTO"
    fold = foldlock_cite()
    assert fold["cite_only"] is True
    assert fold["theater_crypto"] is False
    assert fold["not_zip"] is True
    lens = lamb_lens_cite()
    assert lens["harvest"] is False
    assert lens["fielded_100"] is False
    assert refuse_fielded_100(fielded=100)["code"] == "AZG-NO-FIELDED-100"
    assert refuse_fielded_100(claimed=7)["code"] == "AZG-FIELDED-OK"
    stamp = redline_dict()
    assert stamp["spec"] == REDLINE_SPEC
    assert stamp["fielded_100"] is False
    assert stamp["public_door_crypto"]["layer"] == "cloudflare-tls"
    law = mesh_law_dict()
    assert law["redline"]["spec"] == REDLINE_SPEC
    assert law["get_never_enables"] is True
    assert law["fielded_100"] is False


def test_smaller_door_surface_in_worker_and_docs() -> None:
    assert "MESH-GET-NO-ENABLE" in MESH_JS
    assert "refuseGetEnableOrPlant" in MESH_JS
    assert "GET_ENABLE_PLANT_INTENTS" in MESH_JS
    assert "CALLABLE_AZG_ALIASES" in MESH_JS
    assert "PUBLIC_MESH_GET_DOORS" in MESH_JS
    assert "REDLINE-1.0" in MESH_JS
    assert "cloudflare-tls" in MESH_JS
    assert "cite-only" in MESH_JS
    assert "fielded_100: false" in MESH_JS
    assert "LAMB LENS" in MESH_JS or "lamb_lens" in MESH_JS
    assert "FOLDLOCK" in MESH_JS
    assert "AZG-NOT-CALLABLE" in RUNTIME
    assert "/v1/call-generator" in RUNTIME or "call-generator" in RUNTIME
    assert "AZG-NOT-CALLABLE" in INDEX
    assert "public_icann: false" in BRIDGE
    assert "resolves_to_hub: false" in BRIDGE
    assert "GET never enables" in HOME
    assert "REDLINE-1.0" in HOME
    assert "fielded 100" not in HOME.lower() or "no fielded 100" in HOME.lower()
    assert REDLINE_SPEC in REDLINE_DOC
    assert "MESH-GET-NO-ENABLE" in REDLINE_DOC
    assert "AZG-NOT-CALLABLE" in REDLINE_DOC
    assert "BRIDGE-NO-HUB-RESOLVE" in REDLINE_DOC
    assert "cloudflare-tls" in REDLINE_DOC.lower() or "Cloudflare TLS" in REDLINE_DOC
    assert "FoldLock" in REDLINE_DOC
    assert "Lamb Lens" in REDLINE_DOC
    assert "no fielded 100" in REDLINE_DOC.lower()
    assert "REDLINE-1.0" in MESH_LAW
    assert "REDLINE-1.0" in README
    assert "REDLINE-1.0" in SKILL
    for door in PUBLIC_MESH_GET_DOORS:
        assert f'"{door}"' in MESH_JS
    assert "/v1/mesh/call-generator" in MESH_JS
    assert "queryHasEnableOrPlant" in MESH_JS
    planted = refuse_get_enable_or_plant(method="GET", path="/v1/shuffle/ping", search="prev=p&lockset=l")
    assert planted is not None and planted["code"] == "MESH-GET-NO-ENABLE"
    upd = refuse_get_enable_or_plant(method="GET", path="/v1/shuffle/update")
    assert upd is not None and upd["code"] == "MESH-GET-NO-ENABLE"


def test_g6_live_host_cite_design_of_and_shelves() -> None:
    from miragegrid.semantic_bridge import app_worker

    live = dead_named_worker()
    assert live["cite"] is True
    assert live["status"] == "live-app"
    assert live["url"] == "https://miragegrid.vibelock.workers.dev"
    assert live["download_plane"] == WORKER_HOST
    assert "download-tracker" not in live["host"]
    assert app_worker()["historical_cf_1042"] == "closed-by-creating-worker-miragegrid"
    cite = cap7_bridge_cite()
    assert cite["design_of"]["azcorpus"] == CORPUS_HUB
    assert cite["design_of"]["azlibrary"] == CORPUS_HUB
    assert cite["resolves_to_hub"] is False
    assert cite["public_icann"] is False
    shelves = shelves_cite()
    assert shelves["code"] == "SHELVES-CITE"
    assert shelves["canonical"] == "https://www.azielcorpuslibrary.net/shelves"
    assert shelves["framagit"] is None
    assert shelves["framagit_url"] is None
    assert shelves["invented_framagit"] is False
    assert shelves["resolves_to_hub"] is False
    assert "shelvesCite" in BRIDGE
    assert "/shelves" in INDEX
    assert "live-app" in BRIDGE
    assert "closed-by-creating-worker-miragegrid" in BRIDGE
    assert "https://miragegrid.vibelock.workers.dev" in README
    assert "https://miragegrid.vibelock.workers.dev" in SKILL
