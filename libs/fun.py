from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search
from elasticsearch_dsl import Q
import json

def get_post_data():
    """
    从请求中获取参数
    :return:
    """
    data = {}
    try:
        if request.content_type.startswith('application/json'):
            data = request.get_data()
            data = json.loads(data)
        else:
            for key, value in request.form.items():
                if key.endswith('[]'):
                    data[key[:-2]] = request.form.getlist(key)
                else:
                    data[key] = value
    except :
        pass
    return data


def search_sent_plus(keyword):
    client = Elasticsearch()
    q = Q("multi_match", query=keyword, fields=['title', 'content'])
    s = Search(using=client)
    # s = Search(using=client, index="pet-index").query("match", content="金毛")
    s = Search(using=client, index="pet-sent-index").query(q)
    s=s[0:50]
    s=s.highlight_options(order='score')
    s = s.highlight('content')
    response = s.execute()
    return response
def search_content(keyword,limit=50):
    client = Elasticsearch()
    q = Q("multi_match", query=keyword, fields=['title', 'content'])
    s = Search(using=client)
    # s = Search(using=client, index="pet-index").query("match", content="金毛")
    s = Search(using=client, index="pet-index").query(q)
    s=s[0:limit]
    s=s.highlight_options(order='score')
    s = s.highlight('content')
    response = s.execute()
    return response
