from copy import deepcopy


class DataCollection:
    def __init__(self, data_retrieval_function, endpoint, url_params):
        self._data_retrieval_function = data_retrieval_function
        self._endpoint = endpoint
        self._url_params = url_params
        self._next_page_token = ''
        self._current_data_iterator = None

    def first_page(self):
        return self._data_retrieval_function(self._endpoint, self._url_params)['data']

    def __next__(self):
        try:
            if self._current_data_iterator is not None:
                return next(self._current_data_iterator)
        except StopIteration:
            if self._next_page_token is None:
                raise StopIteration

        url_params = deepcopy(self._url_params)
        if self._next_page_token:
            url_params['next_page_token'] = self._next_page_token
        api_response = self._data_retrieval_function(self._endpoint, url_params)
        self._next_page_token = api_response.get('next_page_token')
        self._current_data_iterator = iter(api_response['data'])
        return next(self._current_data_iterator)

    def __iter__(self):
        return self
