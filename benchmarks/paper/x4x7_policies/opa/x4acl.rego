# X4 profile opa-acl-doc (and opa-acl-doc-drift): wardowl's metadata ACL policy, grown to the X4 model.
#
# Chunks carry their permissions in metadata: `allowed_users`, `allowed_groups` ("*" for everyone),
# `owner`, `tenant`, `classification` and `folder`. Group nesting and folders (their grants and their
# parents) live in OPA data, under data.x4acl_world, which the harness writes. The subject arrives
# as wardowl sends it: id, direct groups, and attributes `tenant` and `clearance`.
#
# `decisions` is the check (one boolean per chunk); `filter` is the same rule as a filter document,
# for wardowl's filter_path. There are no bans: wardowl's filter language has no negation.

package x4acl

import rego.v1

world := data.x4acl_world

# The subject's groups, direct and inherited through nesting. graph.reachable keeps only nodes that
# are keys of the graph, so the direct groups are added as they are.
my_groups := {g | some g in input.subject.groups} | graph.reachable(world.parents, input.subject.groups)

# Folders whose own grants admit the subject.
granted_folders contains f if {
	some f, info in world.folders
	folder_grants(info)
}

folder_grants(info) if input.subject.id in info.users

folder_grants(info) if {
	some g in info.groups
	g in my_groups
}

folder_grants(info) if info.wildcard == true

# A folder is readable when it or one of its ancestors grants the subject.
readable_folders contains f if {
	some f, _ in world.folders
	some a in graph.reachable(world.up, [f])
	a in granted_folders
}

levels := [sprintf("L%d", [i]) | some i in numbers.range(0, input.subject.attributes.clearance)]

# A permission field may hold one value or a list of values; a missing field holds none.
field_values(m, name) := v if {
	v := object.get(m, name, [])
	is_array(v)
} else := [object.get(m, name, null)]

default allowed(_) := false

allowed(m) if {
	m.tenant == input.subject.attributes.tenant
	m.classification in levels
	readable(m)
}

readable(m) if m.owner == input.subject.id

readable(m) if input.subject.id in field_values(m, "allowed_users")

readable(m) if {
	some g in field_values(m, "allowed_groups")
	g in my_groups
}

readable(m) if "*" in field_values(m, "allowed_groups")

readable(m) if m.folder in readable_folders

decisions := [allowed(r.metadata) | some r in input.resources]

filter := {"and": [
	{"in": {"field": "tenant", "values": [input.subject.attributes.tenant]}},
	{"in": {"field": "classification", "values": levels}},
	{"or": [
		{"in": {"field": "owner", "values": [input.subject.id]}},
		{"in": {"field": "allowed_users", "values": [input.subject.id]}},
		{"in": {"field": "allowed_groups", "values": array.concat([g | some g in my_groups], ["*"])}},
		{"in": {"field": "folder", "values": [f | some f in readable_folders]}},
	]},
]}
