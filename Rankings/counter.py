from common_functions import *


class CountClient:

    def __init__(self):
        self.authorCount = {}
        self.instiCount = {}
        self.countryCount = {}
        self.regionCount = {}

        self.tmp_author_count = {}
        self.tmp_insti_count = {}
        self.tmp_country_count = {}
        self.tmp_region_count = {}

    def reset_tmp_counts(self):
        self.tmp_author_count = {}
        self.tmp_insti_count = {}
        self.tmp_country_count = {}
        self.tmp_region_count = {}


