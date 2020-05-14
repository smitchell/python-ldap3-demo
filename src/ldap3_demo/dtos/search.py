from ldap3 import SUBTREE, DEREF_ALWAYS, BASE, LEVEL, SUBTREE, DEREF_NEVER, DEREF_SEARCH, DEREF_BASE, ALL_ATTRIBUTES, \
    ALL_OPERATIONAL_ATTRIBUTES

search_base_types = dict(BASE=BASE, LEVEL=LEVEL, SUBTREE=SUBTREE)

dereference_aliases_types = dict(
    DEREF_NEVER=DEREF_NEVER,
    DEREF_SEARCH=DEREF_SEARCH,
    DEREF_BASE=DEREF_BASE,
    DEREF_ALWAYS=DEREF_ALWAYS
)


class Search:

    def __init__(self, search_base,
                 search_filter,
                 search_scope=SUBTREE,
                 dereference_aliases=DEREF_ALWAYS,
                 attributes=None,
                 size_limit=0,
                 time_limit=0,
                 types_only=False,
                 get_operational_attributes=False,
                 controls=None,
                 paged_size=None,
                 paged_criticality=False,
                 paged_cookie=None):
        self.search_base = search_base_types[search_base]
        self.search_filter = search_filter
        self.search_scope = search_scope
        self.dereference_aliases = dereference_aliases_types[dereference_aliases]
        if attributes == 'ALL_ATTRIBUTES':
            self.attributes = ALL_ATTRIBUTES
        elif attributes == 'ALL_OPERATIONAL_ATTRIBUTES':
            self.attributes = ALL_OPERATIONAL_ATTRIBUTES
        else:
            self.attributes = attributes
        self.attributes = attributes
        self.size_limit = size_limit
        self.time_limit = time_limit
        self.types_only = types_only
        self.get_operational_attributes = get_operational_attributes
        self.controls = controls
        self.paged_size = paged_size
        self.paged_criticality = paged_criticality
        self.paged_cookie = paged_cookie
