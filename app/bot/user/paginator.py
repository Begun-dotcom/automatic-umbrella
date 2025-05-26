import math


class Paginator:
    def __init__(self, array : list, page : int = 1, rep_page : int = 1):
        self.array = array
        self.page = page
        self.rep_page = rep_page
        self.len = len(array)
        self.pages = math.ceil(self.len / self.rep_page)

    def __get_slice(self):
        start = (self.page - 1) * self.rep_page
        stop = start + self.rep_page
        return self.array[start:stop]

    def get_page(self):
        page_items = self.__get_slice()
        return page_items

    def has_next(self):
        if self.page < self.pages:
           return self.page + 1
        return False

    def has_previous(self):
        if self.page > 1:
            return self.page - 1
        return False

    def get_next(self):
        if self.page < self.pages:
            self.page += 1
            return self.get_page()
        raise IndexError(f'Next page does not exist. Use has_next() to check before.')

    def get_previous(self):
        if self.page > 1:
            self.page -= 1
            return self.__get_slice()
        raise IndexError(f'Previous page does not exist. Use has_previous() to check before.')