class FoodSearchCriteria:
    def __init__(self, query: str, data_type: str = None, page_size: int = None, page_number: int = None,
                 sort_by: str = None, sort_order: str = None, brand_owner: str = None, trade_channel: list[str] = None,
                 start_date: str = None, end_date: str = None):
        self.query = query
        self.data_type = data_type
        self.page_size = page_size
        self.page_number = page_number
        self.sort_by = sort_by
        self.sort_order = sort_order
        self.brand_owner = brand_owner
        self.trade_channel = trade_channel
        self.start_date = start_date
        self.end_date = end_date
