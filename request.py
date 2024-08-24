
from collections import defaultdict
from email.policy import default
from urllib.request import Request

    # {
    #     'id':123,
    #     'name':rivaan
    # }

class Request:
    def __init__(self,environ) -> None:
        self.queries=defaultdict()

        for key, val in environ.items():
            setattr(self,key.replace(".","_").lower(),val)

        if self.query_string:
            req_queries=self.query_string.split("&")

            for query in req_queries:
                query_key , query_val= query.split("=")

                self.queries[query_key]=query_val
