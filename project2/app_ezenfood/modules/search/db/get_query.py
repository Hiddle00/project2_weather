from cosine_similarity import cosine_similarity as cs
import numpy as np
import json

"""
    유사도 기준 정렬 후 반환하는 함수
"""

def get_query(query, rows, model):
    query_emb = model.encode([query], normalize_embeddings=True)[0]
    scored_rows = []

    for row in rows :
        sent_emb    = np.array(json.loads(row['sub_embedding']))
        kw_emb_list = [np.array(k) for k in json.loads(row['sub_keyword'])]

        sim_kw   = max([cs(query_emb, kw) for kw in kw_emb_list])
        sim_sent = cs(query_emb, sent_emb)
        
        sim = max(sim_sent, sim_kw)

        scored_rows.append((sim, row))

    # 유사도 기준 정렬
    scored_rows.sort(key=lambda x: x[0], reverse=True)

    # row만 추출해서 반환
    return [row for _, row in scored_rows]


