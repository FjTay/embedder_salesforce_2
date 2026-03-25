import contexts.loader
import embedder.embedder
import embedder.embedder_util
import salesforce.client
import salesforce.salesforce_util


def run_data_query(user_nl_request):
    describe = salesforce.client.global_describe()
    sobjects = describe["sobjects"]
    sobjects_map = salesforce.salesforce_util.build_queryable_sobjects_map(sobjects)
    object_names = list(sobjects_map.keys())
    business_descriptions = contexts.loader.load_business_descriptions()
    business_objects = contexts.loader.load_business_objects()
    business_desc_lower = {k.lower(): v for k, v in business_descriptions.items()}
    embedding_texts = [
        f"{sobjects_map[name]} {business_desc_lower.get(name.lower(), '')}".strip() for name in object_names
    ]
    sobjects_shortlist = embedder.embedder.match_objects(
        user_nl_request,
        object_names,
        top_k=10,
        embedding_texts=embedding_texts,
        boost_objects=business_objects,
    )
    top5_sobjects = embedder.embedder_util.take_shortlist(sobjects_shortlist, 5)
    objects_by_sobject = {}
    for object_name in top5_sobjects:
        sobject_describe = salesforce.client.describe_sobject(object_name)
        sobject_fields_all = salesforce.salesforce_util.describe_sobject_fields(
            sobject_describe,
            custom_only=False,
        )
        lookups = {}
        for f in sobject_fields_all["fields"]:
            if f.get("type") != "reference" or not f.get("referenceTo"):
                continue
            target = f["referenceTo"][0]
            target_key = target.lower()
            lookups.setdefault(target_key, {})
            lookups[target_key][f["name"]] = {"label": f.get("label") or f["name"], "type": "reference"}
        sobject_fields_custom = salesforce.salesforce_util.describe_sobject_fields(
            sobject_describe,
            custom_only=True,
        )
        custom_non_lookup = []
        for f in sobject_fields_custom["fields"]:
            is_lookup = f.get("type") == "reference" and f.get("referenceTo")
            if not is_lookup:
                custom_non_lookup.append(f)
        custom_non_lookup_names = [f["name"] for f in custom_non_lookup]
        fields_map = salesforce.salesforce_util.build_fields_embedding_map(sobject_fields_custom)
        if not custom_non_lookup_names:
            top10_custom_non_lookup = []
        else:
            other_embedding_texts = [fields_map[n] for n in custom_non_lookup_names]
            top10_custom_non_lookup = embedder.embedder.match_objects(
                user_nl_request,
                custom_non_lookup_names,
                top_k=10,
                embedding_texts=other_embedding_texts,
                split_query_clauses=True,
            )
        custom_field_meta = {f["name"]: f for f in custom_non_lookup}
        fields = {}
        for f_name in top10_custom_non_lookup:
            meta = custom_field_meta.get(f_name)
            if meta:
                fields[f_name] = {"label": meta.get("label") or f_name, "type": meta.get("type")}
        objects_by_sobject[object_name] = {
            "label": sobject_describe.get("label") or object_name,
            "description": business_desc_lower.get(object_name.lower(), ""),
            "lookups": lookups,
            "fields": fields,
        }
    return {"objects": objects_by_sobject}
