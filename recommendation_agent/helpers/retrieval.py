import weaviate.classes.query as wq

def retrieve_products(products, query, category=None):

    # Prevent empty BM25 searches
    if not query or not query.strip():
        return []

    if category:
        return products.query.bm25(
            query=query,
            limit=10,
            filters=wq.Filter.by_property("main_category").equal(category)
        ).objects

    return products.query.bm25(
        query=query,
        limit=10
    ).objects