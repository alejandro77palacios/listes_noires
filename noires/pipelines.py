from pathlib import Path

from scrapy.exporters import CsvItemExporter, JsonItemExporter

class MultiExporterPipeline:
    def __init__(self):
        self.files = {}
        self.data_directory = Path('data')

    def open_spider(self, spider):
        csv_file = open(self.data_directory /f'{spider.name}.csv', 'w+b')
        json_file = open(self.data_directory /f'{spider.name}.json', 'w+b')
        self.files[spider] = {'csv': csv_file, 'json': json_file}

        # Y del mismo modo para los exporters
        self.exporters = {
            'csv': CsvItemExporter(csv_file),
            'json': JsonItemExporter(json_file),
        }
        self.exporters['csv'].start_exporting()
        self.exporters['json'].start_exporting()

    def close_spider(self, spider):
        self.exporters['csv'].finish_exporting()
        self.exporters['json'].finish_exporting()
        self.files[spider]['csv'].close()
        self.files[spider]['json'].close()

        # Retira los archivos del diccionario
        del self.files[spider]

    def process_item(self, item, spider):
        self.exporters['csv'].export_item(item)
        self.exporters['json'].export_item(item)
        return item