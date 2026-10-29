# X4 profiles opa-rel-doc and opa-rel-pe, and X7's opa-data and opa-policy paths.
#
# Chunks carry scalar columns in their metadata: `doc_id`, `tenant`, `owner`, `folder` and
# `classification`. Who each document is shared with, group nesting and folders live in OPA data,
# under data.x4rel_world, which the harness writes. The same rule is offered three ways:
#
# * `decisions`: one boolean per chunk, for wardowl's check;
# * `filter`: a filter document, for wardowl's filter_path;
# * `allow`: the rule over `input.doc`, for OPA's Compile API with `input.doc` unknown. Each body is
#   one way to read, so partial evaluation gives one query per way.

package x4rel

import rego.v1

world := data.x4rel_world

# Users this version of the policy denies outright. X7's opa-policy path uploads new versions of
# this module with users added on the next line; X4 leaves it empty.
deny_users := set() # x7: deny_users

permitted if not input.subject.id in deny_users

my_groups := {g | some g in input.subject.groups} | graph.reachable(world.parents, input.subject.groups)

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

readable_folders contains f if {
	some f, _ in world.folders
	some a in graph.reachable(world.up, [f])
	a in granted_folders
}

shared(s) if input.subject.id in s.users

shared(s) if {
	some g in s.groups
	g in my_groups
}

shared(s) if s.wildcard == true

shared_docs contains d if {
	some d, s in world.shares
	shared(s)
}

shared_list := [d | some d in shared_docs]

folder_list := [f | some f in readable_folders]

levels := [sprintf("L%d", [i]) | some i in numbers.range(0, input.subject.attributes.clearance)]

tenants := [input.subject.attributes.tenant] if {
	permitted
} else := []

# ---- the check ----

default decision(_) := false

decision(m) if {
	permitted
	m.tenant == input.subject.attributes.tenant
	m.classification in levels
	readable(m)
}

readable(m) if m.owner == input.subject.id

readable(m) if m.doc_id in shared_docs

readable(m) if m.folder in readable_folders

decisions := [decision(r.metadata) | some r in input.resources]

# ---- the filter document ----

filter := {"and": [
	{"in": {"field": "tenant", "values": tenants}},
	{"in": {"field": "classification", "values": levels}},
	{"or": [
		{"in": {"field": "owner", "values": [input.subject.id]}},
		{"in": {"field": "doc_id", "values": shared_list}},
		{"in": {"field": "folder", "values": folder_list}},
	]},
]}

# ---- the rule for partial evaluation ----

allow if {
	permitted
	input.doc.tenant == input.subject.attributes.tenant
	input.doc.classification in levels
	input.doc.owner == input.subject.id
}

allow if {
	permitted
	input.doc.tenant == input.subject.attributes.tenant
	input.doc.classification in levels
	input.doc.doc_id in shared_list
}

allow if {
	permitted
	input.doc.tenant == input.subject.attributes.tenant
	input.doc.classification in levels
	input.doc.folder in folder_list
}
