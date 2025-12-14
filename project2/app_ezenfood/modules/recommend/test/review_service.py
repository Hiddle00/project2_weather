from app_ezenfood.modules.recommend.test.review_dao import ReviewDAO
from app_ezenfood.modules.utils.get_conn import get_root_conn
import pandas as pd

class ReviewService:

    def __init__(self) :
        self.review_dao = ReviewDAO(get_root_conn)

    def attach_rest_id(
        self,
        review_df : pd.DataFrame
    ) -> pd.DataFrame:
        
        # 리뷰 DF에 rest_id 추가
        # 1. DB 음식점 정보
        rest_rows = self.review_dao.rest_id_map()
        rest_df   = pd.DataFrame(rest_rows)
        
        print(rest_df.columns)
        
        # 2. nplace_id 기준 merge (최우선)
        if 'rest_code' in review_df.columns and 'nplace_id' in rest_df.columns :
            merged = review_df.merge(
                rest_df[['rest_id', 'nplace_id']],
                left_on  = 'rest_code',
                right_on = 'nplace_id',
                how      = 'left'
            )
        else :
            # fallback: 상호명 기준
            merged = review_df.merge(
                rest_df[['rest_id', 'rest_name']],
                left_on  = 'rest_name',
                right_on = 'rest_name',
                how      = 'left'
            )

        return merged
