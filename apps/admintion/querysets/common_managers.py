from django.db.models.query import QuerySet
from django.db.models import Manager
from django.contrib.postgres.aggregates import ArrayAgg

class CountriesQuerySet(QuerySet):
    def get_info(self):
        return self.all()

    def countries(self):
        return self.get_info().values(
            'id',
            'name',
        )

class CountriesManager(Manager):
    def get_query_set(self):
        return CountriesQuerySet(self.model)

    def countries(self):
        return self.get_query_set().countries()


class RegionsQuerySet(QuerySet):
    def get_info(self):
        return self.all()

    def regions(self):
        return self.get_info().values(
            'id',
            'name',
            'country__name',
        )
    
    def by_country(self, id: int):
        return self.get_info().values(
            'id',
            'name',
        ).filter(country_id=id)

class RegionsManager(Manager):
    def get_query_set(self):
        return RegionsQuerySet(self.model)

    def regions(self):
        return self.get_query_set().regions()

    def by_country(self, id: int):
        return self.get_query_set().by_country(id=id)

class DistrictsQuerySet(QuerySet):
    def get_info(self):
        return self.all()

    def districts(self):
        return self.get_info().values(
            'id',
            'name',
            'region_id',
            'region__name',
            'country__name',
        )
    def by_region(self, id: int):
        return self.get_info().values(
            'id',
            'name',
        ).filter(region_id=id)

    def by_country(self, id: int):
        return self.get_info().values(
            'id',
            'name',
        ).filter(country_id=id)

class DistrictsManager(Manager):
    def get_query_set(self):
        return DistrictsQuerySet(self.model)

    def districts(self):
        return self.get_query_set().districts()

    def by_region(self, id: int):
        return self.get_query_set().by_region(id=id)

    def by_country(self, id: int):
        return self.get_query_set().by_country(id=id)