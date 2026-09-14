"""SEMANTIC-BRIDGE-1.0 honesty: empty vs claimed, no hub resolve, not ICANN.

Author: Aziel Eliab only.
"""

from __future__ import annotations

import hashlib
from pathlib import Path

from miragegrid.az_generator import MeshDnsZone, PUBLIC_HOST_PAIR
from miragegrid.mesh import mesh_law_dict
from miragegrid.semantic_bridge import (
    CORPUS_HUB,
    CROSS_NETWORK_SURVIVAL,
    DESIGN_HUBS,
    FIRST_CLAIM_NAME,
    PERSON_ID,
    PREFERRED_PUBLIC_PAIR,
    SEMANTIC_BRIDGE_SPEC,
    build_bridge_registry,
    cap7_bridge_cite,
    design_pack_sha256,
    hosted_bridge_document,
    refuse_azg_icann_publish,
    refuse_fifth_product,
    refuse_hub_resolution,
    refuse_invent_first_flag_https,
    refuse_need_canonical_hub,
    refuse_need_tip,
    refuse_public_dns_claim,
    semantic_bridge_dict,
)


ROOT = Path(__file__).resolve().parents[1]
TIP = hashlib.sha256(b"mesh-tip-survival").hexdigest()
PACK = hashlib.sha256(b"design-pack-azieleliab").hexdigest()


def _assert_mesh_entry_law(row: dict) -> None:
    assert row["canonical_hub"] in {
        "https://www.azieleliab.com/",
        "https://www.azielcorpuslibrary.net/",
        "https://godlock.uk/",
        "https://hedidntjump.com/",
    }
    assert row["tip"] and len(row["tip"]) == 64
    assert row["tip"] == row["tip_sha256"]
    assert row["public_icann"] is False
    assert row["name_may_change"] is True
    assert row["fifth_product"] is False
    assert row["person"]["@id"] == PERSON_ID
    assert row["resolves_to_hub"] is False


def test_law_stamp_public_icann_false_and_person() -> None:
    law = semantic_bridge_dict()
    assert law["spec"] == SEMANTIC_BRIDGE_SPEC
    assert law["public_icann"] is False
    assert law["resolves_to_hub"] is False
    assert law["name_may_change"] is True
    assert law["first_flag"] == FIRST_CLAIM_NAME
    assert law["suffix_order"] == [".az", ".aziel", "pivot"]
    assert law["public_host_pair"] == PUBLIC_HOST_PAIR
    assert law["preferred_public_pair"] == list(PREFERRED_PUBLIC_PAIR)
    assert law["fifth_product"] is False
    assert law["person"]["@id"] == PERSON_ID
    assert law["cross_network_survival"] == CROSS_NETWORK_SURVIVAL
    assert law["growth"] == "Growth-ON"
    assert law["reexpand"] == "archive-not-index"
    cite = cap7_bridge_cite()
    assert cite["public_icann"] is False
    assert cite["resolves_to_hub"] is False
    assert cite["design_of"]["azcorpus"] == CORPUS_HUB
    assert cite["design_of"]["azlibrary"] == CORPUS_HUB
    assert all(row["design_of"] and row["resolves_to_hub"] is False for row in cite["designs"])
    assert cite["cite"].endswith("/v1/mesh/az-generator")
    assert cite["access"]["aznet"] is True
    assert cite["access"]["azbrowser"] is True
    mesh = mesh_law_dict()
    assert mesh["semantic_bridge"]["spec"] == SEMANTIC_BRIDGE_SPEC
    assert mesh["semantic_bridge"]["public_icann"] is False


def test_empty_cap7_is_slot_empty_list() -> None:
    empty = build_bridge_registry([])
    assert empty["ok"] is True
    assert empty["code"] == "BRIDGE-EMPTY"
    assert empty["honesty"] == "empty-cap-7"
    assert empty["slots"] == []
    assert empty["claimed"] == 0
    assert empty["invented_first_flag_https"] is False
    assert empty["public_icann"] is False
    assert FIRST_CLAIM_NAME not in empty["names"]
    assert "azcorpus.az" in empty["names"]
    assert "azlibrary.az" in empty["names"]
    corpus = empty["names"]["azcorpus.az"]
    library = empty["names"]["azlibrary.az"]
    assert corpus["status"] == "named-mesh-site"
    assert corpus["public_icann"] is False
    assert corpus["download_open"] is True
    assert corpus["upload_auth"] == "none"
    assert corpus["canonical_hub"] == CORPUS_HUB
    assert corpus["design_of"] == CORPUS_HUB
    assert corpus["resolves_to_hub"] is False
    assert corpus["fifth_product"] is False
    assert corpus["name_may_change"] is True
    assert corpus["tip"] == design_pack_sha256("azcorpus")
    assert corpus["tip"] == corpus["tip_sha256"]
    _assert_mesh_entry_law(corpus)
    _assert_mesh_entry_law(library)
    assert corpus["design_pack"]["url"].endswith("/design-packs/azcorpus.json")
    assert corpus["design_pack"]["sha256"] == design_pack_sha256("azcorpus")
    assert library["upload_auth"] == "token"
    assert library["upload_plane"] == "plane-a"
    assert library["download_open"] is True
    assert library["canonical_hub"] == CORPUS_HUB
    assert library["fifth_product"] is False
    assert "https-gateway" not in {corpus["status"], library["status"]}
    hosted = hosted_bridge_document()
    assert hosted["claimed"] == 0
    assert hosted["slots"] == []
    assert hosted["code"] == "BRIDGE-EMPTY"
    assert set(hosted["names"]) == {"azcorpus.az", "azlibrary.az"}
    assert FIRST_CLAIM_NAME not in hosted["names"]
    assert hosted["design_packs"]["azcorpus"]["sha256"] == design_pack_sha256("azcorpus")
    assert hosted["design_packs"]["azlibrary"]["sha256"] == design_pack_sha256("azlibrary")


def test_inventing_first_flag_https_refuses() -> None:
    fake = build_bridge_registry([], invent_first_flag=True)
    assert fake["ok"] is False
    assert fake["code"] == "BRIDGE-NO-INVENT-HTTPS"
    assert refuse_invent_first_flag_https()["code"] == "BRIDGE-NO-INVENT-HTTPS"
    unhosted_https = build_bridge_registry(
        [
            {
                "name": FIRST_CLAIM_NAME,
                "public_host": True,
                "status": "https-gateway",
                "tip_sha256": TIP,
                "design_of": "https://www.azieleliab.com/",
            }
        ]
    )
    # public pair without a real gateway URL is claimed-unhosted, not live HTTPS
    assert unhosted_https["ok"] is True
    row = unhosted_https["names"][FIRST_CLAIM_NAME]
    assert row["status"] == "claimed-unhosted"
    assert "public_gateway_url" not in row
    assert row["icann"] is False
    assert row["resolves_to_hub"] is False
    _assert_mesh_entry_law(row)
    assert build_bridge_registry([{"name": "orphan.az", "tip_sha256": TIP}])["code"] == "BRIDGE-NEED-CANONICAL-HUB"
    assert build_bridge_registry(
        [{"name": "orphan.az", "design_of": "https://godlock.uk/"}]
    )["code"] == "BRIDGE-NEED-TIP"
    assert build_bridge_registry(
        [
            {
                "name": "orphan.az",
                "tip_sha256": TIP,
                "design_of": "https://godlock.uk/",
                "fifth_product": True,
            }
        ]
    )["code"] == "BRIDGE-NO-FIFTH-PRODUCT"
    assert refuse_need_canonical_hub()["code"] == "BRIDGE-NEED-CANONICAL-HUB"
    assert refuse_need_tip()["code"] == "BRIDGE-NEED-TIP"
    assert refuse_fifth_product()["code"] == "BRIDGE-NO-FIFTH-PRODUCT"


def test_claimed_names_listed_honestly_with_design_provenance() -> None:
    claimed = build_bridge_registry(
        [
            {
                "name": "www.survivalnetwork.az",
                "public_host": True,
                "public_gateway_url": "https://gateway.example.workers.dev/sn",
                "tip_sha256": TIP,
                "design_pack_sha256": PACK,
                "design_of": "https://www.azieleliab.com/",
                "access": "https-gateway",
            },
            {
                "name": "mesh-only-three.az",
                "public_host": False,
                "tip_hash": hashlib.sha256(b"mesh-only").hexdigest(),
                "design_of": "godlock.uk",
                "access": "azbrowser",
            },
        ]
    )
    assert claimed["ok"] is True
    assert claimed["code"] == "BRIDGE-OK"
    assert claimed["honesty"] == "claimed"
    assert claimed["claimed"] == 2
    first = claimed["names"]["www.survivalnetwork.az"]
    assert first["status"] == "https-gateway"
    assert first["tip_sha256"] == TIP
    assert first["design_pack_sha256"] == PACK
    assert first["public_gateway_url"] == "https://gateway.example.workers.dev/sn"
    assert first["access"] == "https-gateway"
    assert first["icann"] is False
    assert first["design_of"] == "https://www.azieleliab.com/"
    assert first["canonical_hub"] == "https://www.azieleliab.com/"
    assert first["resolves_to_hub"] is False
    assert first["name_may_change"] is True
    assert first["tip"] == TIP
    _assert_mesh_entry_law(first)
    mesh = claimed["names"]["mesh-only-three.az"]
    assert mesh["status"] == "mesh-only"
    assert mesh["access"] == "azbrowser"
    assert mesh["design_of"] == "https://godlock.uk/"
    assert mesh["canonical_hub"] == "https://godlock.uk/"
    assert "public_gateway_url" not in mesh
    assert mesh["resolves_to_hub"] is False
    _assert_mesh_entry_law(mesh)
    for row in claimed["names"].values():
        _assert_mesh_entry_law(row)


def test_refuse_hub_resolution_and_icann_publish() -> None:
    assert refuse_public_dns_claim()["code"] == "BRIDGE-NO-PUBLIC-DNS"
    assert refuse_azg_icann_publish()["code"] == "BRIDGE-NO-ICANN-PUBLISH"
    assert refuse_hub_resolution()["resolves_to_hub"] is False
    assert build_bridge_registry([], public_icann=True)["code"] == "BRIDGE-NO-PUBLIC-DNS"
    assert build_bridge_registry([], icann_publish=True)["code"] == "BRIDGE-NO-ICANN-PUBLISH"
    assert build_bridge_registry([], resolve_to_hub=True)["code"] == "BRIDGE-NO-HUB-RESOLVE"
    cname = build_bridge_registry(
        [
            {
                "name": "www.survivalnetwork.az",
                "public_gateway_url": "https://www.azieleliab.com/",
                "public_host": True,
            }
        ]
    )
    assert cname["code"] == "BRIDGE-NO-HUB-RESOLVE"
    flag = build_bridge_registry(
        [{"name": "www.survivalnetwork.az", "resolves_to_hub": True, "design_of": "https://godlock.uk/"}]
    )
    assert flag["code"] == "BRIDGE-NO-HUB-RESOLVE"
    hub_name = build_bridge_registry([{"name": "azieleliab.com"}])
    assert hub_name["code"] == "BRIDGE-NO-HUB-RESOLVE"


def test_zone_bridge_registry_does_not_map_to_hubs() -> None:
    zone = MeshDnsZone("node-03")
    zone.publish(
        name="www.survivalnetwork.az",
        tip_hash=TIP,
        design_of="https://www.azielcorpuslibrary.net/",
        design_pack_sha256=PACK,
        public_gateway_url="https://pair.example.workers.dev/a",
    )
    zone.publish(
        name="mesh-only-three.az",
        tip_hash=hashlib.sha256(b"m3").hexdigest(),
        design_of="https://godlock.uk/",
    )
    doc = zone.bridge_registry()
    assert doc["ok"] is True
    assert doc["public_icann"] is False
    assert "www.survivalnetwork.az" in doc["names"]
    first = doc["names"]["www.survivalnetwork.az"]
    assert first["resolves_to_hub"] is False
    assert first["design_of"] == "https://www.azielcorpuslibrary.net/"
    assert first["canonical_hub"] == "https://www.azielcorpuslibrary.net/"
    assert first["tip"] == TIP
    assert first["public_gateway_url"].startswith("https://pair.example.workers.dev/")
    assert first["public_gateway_url"] != "https://www.azielcorpuslibrary.net/"
    _assert_mesh_entry_law(first)
    _assert_mesh_entry_law(doc["names"]["mesh-only-three.az"])
    labels = {row["label"] for row in DESIGN_HUBS}
    assert labels == {"azieleliab", "azielcorpuslibrary", "godlock", "hedidntjump"}
    assert "azcorpus.az" in doc["names"]
    assert doc["names"]["azcorpus.az"]["fifth_product"] is False
    assert doc["fifth_product"] is False


def test_preferred_pair_bumps_generic_public_hosts() -> None:
    zone = MeshDnsZone("node-pref")
    zone.publish(name="a.az")
    zone.publish(name="b.az")
    assert zone.public_hosts() == ["a.az", "b.az"]
    zone.publish(
        name="azcorpus.az",
        tip_hash=TIP,
        design_of=CORPUS_HUB,
        public_gateway_url="https://pair.example.workers.dev/corpus",
    )
    assert "azcorpus.az" in zone.public_hosts()
    assert len(zone.public_hosts()) == PUBLIC_HOST_PAIR
    zone.publish(
        name="azlibrary.az",
        tip_hash=PACK,
        design_of=CORPUS_HUB,
        public_gateway_url="https://pair.example.workers.dev/library",
    )
    assert set(zone.public_hosts()) == {"azcorpus.az", "azlibrary.az"}
    preferred = MeshDnsZone("node-pref-first")
    preferred.publish(name="azcorpus.az")
    preferred.publish(name="azlibrary.az")
    assert preferred.public_hosts() == ["azcorpus.az", "azlibrary.az"]
    doc = preferred.bridge_registry()
    assert doc["claimed"] == 2
    assert doc["names"]["azcorpus.az"]["upload_auth"] == "none"
    assert doc["names"]["azlibrary.az"]["upload_auth"] == "token"
    assert doc["names"]["azcorpus.az"]["canonical_hub"] == CORPUS_HUB


def test_docs_and_worker_surfaces_exist() -> None:
    law = (ROOT / "docs" / "SEMANTIC-BRIDGE-1.0.md").read_text(encoding="utf-8")
    assert "SEMANTIC-BRIDGE-1.0" in law
    assert "public_icann" in law
    assert "resolves_to_hub" in law
    assert "design_of" in law
    assert "canonical_hub" in law
    assert "azcorpus" in law
    assert "azlibrary" in law
    assert "design-packs" in law
    assert "fifth public product" in law or "fifth product" in law
    assert "relocatable" in law
    assert "https://www.azieleliab.com/" in law
    assert "https://hedidntjump.com/" in law
    assert "Growth-ON" in law
    assert "CROSS-NETWORK-SURVIVAL" in law
    assert "Visible 15:20 identity-lock HTML" in law
    assert "opens azieleliab.com" in law
    home = (ROOT / "workers" / "download-tracker" / "src" / "homepage.js").read_text(encoding="utf-8")
    assert "15:20" not in home
    js = (ROOT / "workers" / "download-tracker" / "src" / "bridge.js").read_text(encoding="utf-8")
    assert "SEMANTIC-BRIDGE-1.0" in js
    assert "resolves_to_hub: false" in js
    index = (ROOT / "workers" / "download-tracker" / "src" / "index.js").read_text(encoding="utf-8")
    assert "/llms.txt" in index
    assert "/ai.txt" in index
    assert "/v1/bridge" in index
    assert "design-packs" in index
    toml = (ROOT / "workers" / "download-tracker" / "wrangler.toml").read_text(encoding="utf-8")
    assert "/llms.txt" in toml
    assert "/bridge.json" in toml
    assert "/design-packs" in toml
