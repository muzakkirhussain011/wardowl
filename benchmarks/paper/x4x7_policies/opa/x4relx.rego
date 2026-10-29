# X4 profile opa-rel-pe-excl: the x4rel rule with bans, which are kept in OPA data
# (data.x4rel_world.bans: document id -> banned users and groups).
#
# A ban is a negation. wardowl's filter language has none, so this package offers no filter
# document; partial evaluation keeps a `not` (or a `nin`) for a subject with bans in scope, and
# the harness's translator must then return no filter rather than drop it.

package x4relx

import rego.v1

world := data.x4rel_world

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

banned_by(b) if input.subject.id in b.users

banned_by(b) if {
	some g in b.groups
	g in my_groups
}

banned_docs contains d if {
	some d, b in world.bans
	banned_by(b)
}

shared_list := [d | some d in shared_docs]

folder_list := [f | some f in readable_folders]

banned_list := [d | some d in banned_docs]

levels := [sprintf("L%d", [i]) | some i in numbers.range(0, input.subject.attributes.clearance)]

default decision(_) := false

decision(m) if {
	m.tenant == input.subject.attributes.tenant
	m.classification in levels
	readable(m)
	not m.doc_id in banned_docs
}

readable(m) if m.owner == input.subject.id

readable(m) if m.doc_id in shared_docs

readable(m) if m.folder in readable_folders

decisions := [decision(r.metadata) | some r in input.resources]

allow if {
	input.doc.tenant == input.subject.attributes.tenant
	input.doc.classification in levels
	input.doc.owner == input.subject.id
	not input.doc.doc_id in banned_list
}

allow if {
	input.doc.tenant == input.subject.attributes.tenant
	input.doc.classification in levels
	input.doc.doc_id in shared_list
	not input.doc.doc_id in banned_list
}

allow if {
	input.doc.tenant == input.subject.attributes.tenant
	input.doc.classification in levels
	input.doc.folder in folder_list
	not input.doc.doc_id in banned_list
}
