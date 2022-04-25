# -*- coding: utf-8 -*-


def jwt_response_payload_handler(token, user=None, request=None):
    """
    定义响应结果
    :param token:
    :param user:
    :param request:
    :return:
    """
    return {
        'user_id': user.id,
        'username': user.username,
        'token': token
    }
