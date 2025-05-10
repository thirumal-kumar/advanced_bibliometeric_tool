def summarize_data(df):
    summary = {}
    summary['Total Records'] = len(df)
    if 'Journal' in df:
        summary['Unique Journals'] = df['Journal'].nunique()
    if 'Author' in df:
        summary['Unique Authors'] = len({a for s in df['Author'].dropna() for a in s.split(';')})
    return summary

def build_coauthorship_network(df, return_edges=False):
    # Returns list of (author1, author2, count)
    edges = {}
    for s in df['Author'].dropna():
        authors = [a.strip() for a in s.split(';') if a.strip()]
        for i in range(len(authors)):
            for j in range(i+1, len(authors)):
                pair = tuple(sorted((authors[i], authors[j])))
                edges[pair] = edges.get(pair, 0) + 1
    if return_edges:
        return [(a,b,c) for (a,b),c in edges.items()]
    return edges
