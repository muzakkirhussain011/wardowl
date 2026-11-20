# The company's reading rule for the knowledge assistant, in Rego, for wardowl's OPAAuthorizer.
#
# Who a document is shared with lives in OPA's data, pushed there by the document system, one entry
# per tenant and path. Both tenants file documents under the same paths, so a path names a document
# only together with its tenant:
#
#   {"northwind": {"hr/salary-bands-1": {"tenant": "northwind", "users": ["carol"], "groups": ["hr"]}}}
#
# A person may read a document of their own tenant that is shared with them by name, with one of
# their groups, or with everyone ("*" among the groups). The tenant and the groups come from the
# subject wardowl sends (from authentication); the chunk says which tenant it belongs to and the
# path of its document there, in its `tenant` and `path` metadata.
#
# The scenario uploads this file with PUT /v1/policies/<id> and the sharing with PUT /v1/data/...,
# after giving the package and the data root a name unique to the run.

package acme_s02.documents

import rego.v1

sharing := data.acme_s02_data.sharing

# One decision per chunk, in the order wardowl sent them (OPAAuthorizer's decisions_path).
decisions := [allowed(r) | some r in input.resources]

default allowed(_) := false

allowed(r) if {
	tenant := r.metadata.tenant
	path := r.metadata.path
	is_string(tenant)
	is_string(path)
	readable(sharing[tenant][path])
}

readable(entry) if {
	entry.tenant == input.subject.attributes.tenant
	shared_with_subject(entry)
}

shared_with_subject(entry) if input.subject.id in entry.users

shared_with_subject(entry) if {
	some group in entry.groups
	group in input.subject.groups
}

shared_with_subject(entry) if "*" in entry.groups

# The same rule as a filter for pre-filtering (OPAAuthorizer's filter_path): the subject's tenant,
# and every path of it the subject may read. The tenant is needed: the other tenant has documents
# at the same paths. Both lists are empty for a subject of no tenant this data knows.
filter := {"and": [
	{"in": {"field": "tenant", "values": [tenant | some tenant, _ in sharing; tenant == input.subject.attributes.tenant]}},
	{"in": {"field": "path", "values": [path | some path, entry in sharing[input.subject.attributes.tenant]; readable(entry)]}}
]}
