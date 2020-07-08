
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