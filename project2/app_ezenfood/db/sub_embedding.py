from sentence_transformers import SentenceTransformer
from sub_dao import SubDAO
import json

class SubEmbedding:
    
    def __init__(self):
        self.model = SentenceTransformer("snunlp/KR-SBERT-V40K-klueNLI-augSTS")

    def insert_sub_categories(self, categories):
        # 1) 문장 임베딩 일괄 처리
        sentences = [sentence for name, sentence, keys in categories]
        sentence_embeddings = self.model.encode(sentences, normalize_embeddings=True)

        # 2) 키워드 임베딩 일괄 처리
        all_key_embs = [
            self.model.encode(keys, normalize_embeddings=True)
            for name, sentence, keys in categories
        ]

        # 3) DB 넣을 튜플 준비
        data_list = []
        for (name, sentence, keys), sent_emb, key_embs in zip(categories, sentence_embeddings, all_key_embs):
            key_embs_list = [emb.tolist() for emb in key_embs]
            data_list.append((
                name,
                sentence,
                json.dumps(sent_emb.tolist()),
                json.dumps(keys),
                json.dumps(key_embs_list)
            ))

        # 4) DAO를 통해 DB 인서트
        SubDAO.insert_many(data_list)
        print(f"{len(data_list)}개 데이터 삽입 완료!")
