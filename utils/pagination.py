from rest_framework.pagination import PageNumberPagination as _PageNumberPagination


class PageNumberPagination(_PageNumberPagination):
    page_size = 10  # 默认页面数据条数
    page_query_param = 'page'  # 指定页码
    page_size_query_param = 'size'  # 指定每页条数
    max_page_size = 20  # 指定每页最大条数
    invalid_page_message = '页码无效'
    page_query_description = "第几页"
    page_size_query_description = "每页几条"

    def get_paginated_response(self, data):
        response = super().get_paginated_response(data)
        response.data["current_page_num"] = self.page.number
        response.data["total_pages"] = self.page.paginator.num_pages
        return response
