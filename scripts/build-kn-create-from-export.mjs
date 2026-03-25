/**
 * Build a knowledge-network POST body from `kweaver bkn get <id> --export` JSON.
 * Strips server-managed fields. Use: kweaver bkn create --body-file <out.json>
 */
import { readFileSync, writeFileSync } from "node:fs";

const [, , exportPath, outPath, newId, newName] = process.argv;
if (!exportPath || !outPath || !newId) {
  console.error(
    "Usage: node scripts/build-kn-create-from-export.mjs <export.json> <out.json> <new_kn_id> [new_name]",
  );
  process.exit(1);
}

const j = JSON.parse(readFileSync(exportPath, "utf8"));

function stripOt(ot) {
  return {
    id: ot.id,
    name: ot.name,
    data_source: ot.data_source,
    data_properties: ot.data_properties,
    primary_keys: ot.primary_keys,
    display_key: ot.display_key,
    incremental_key: ot.incremental_key,
    tags: ot.tags ?? [],
    comment: ot.comment ?? "",
    icon: ot.icon ?? "",
    color: ot.color ?? "",
  };
}

function stripRt(rt) {
  return {
    id: rt.id,
    name: rt.name,
    source_object_type_id: rt.source_object_type_id,
    target_object_type_id: rt.target_object_type_id,
    type: rt.type,
    mapping_rules: rt.mapping_rules ?? [],
    tags: rt.tags ?? [],
    comment: rt.comment ?? "",
    icon: rt.icon ?? "",
    color: rt.color ?? "",
  };
}

const payload = {
  id: newId,
  name: newName ?? `${j.name}_json导入`,
  tags: j.tags ?? [],
  comment: j.comment ?? "",
  icon: j.icon ?? "",
  color: j.color ?? "",
  detail: j.detail ?? "",
  branch: j.branch ?? "main",
  object_types: (j.object_types ?? []).map(stripOt),
  relation_types: (j.relation_types ?? []).map(stripRt),
  // Export action shapes differ from ontology create schema; add via UI/CLI later.
  action_types: [],
};

writeFileSync(outPath, JSON.stringify(payload, null, 2), "utf8");
console.error(`Wrote ${outPath} (${payload.object_types.length} OT, ${payload.relation_types.length} RT)`);
