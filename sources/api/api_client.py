class APIClient:
    def search(self, query):
        raise NotImplementedError

    def retrieve_item(self, item_id):
       raise NotImplementedError

    def get_metadata(self, item_id):
        raise NotImplementedError
