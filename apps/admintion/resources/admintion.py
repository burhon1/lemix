from import_export import resources
from admintion.models import Countries, Regions, Districts

class CountriesResource(resources.ModelResource):

    class Meta:
        skip_unchanged = True
        report_skipped = False
        model = Countries
        fields = ('id', 'name')

class RegionsResource(resources.ModelResource):

    class Meta:
        skip_unchanged = True
        report_skipped = False
        model = Regions
        fields = ('id', 'name', 'country')

class DistrictsResource(resources.ModelResource):

    class Meta:
        skip_unchanged = True
        report_skipped = False
        model = Districts
        fields = ('id', 'name', 'country', 'region')