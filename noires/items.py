from datetime import datetime

from itemloaders.processors import MapCompose, TakeFirst, Compose
from scrapy import Item, Field
from scrapy.loader import ItemLoader


class NoiresItem(Item):
    name = Field()
    website = Field()
    category = Field()
    date = Field()
    source = Field()


def format_date(input_format):
    def format_string_date(raw_date: str):
        if raw_date is None:
            return None
        assert isinstance(raw_date, str)
        date_object = datetime.strptime(raw_date.strip(), input_format)
        return date_object.strftime('%Y-%m-%d')

    return format_string_date


def sec_clean_category(raw_category: str):
    return raw_category.replace("[", "").replace("]", "")


def sec_website(all_text_list: list):
    text = ' '.join(all_text_list)
    return text.split('Website')[1].replace(':', '').strip().split()[0]


class SfcLoader(ItemLoader):
    default_item_class = NoiresItem
    default_input_processor = MapCompose(str.strip)
    default_output_processor = TakeFirst()

    date_in = MapCompose(format_date('%d %b %Y'))


class SecLoader(ItemLoader):
    default_item_class = NoiresItem
    default_input_processor = MapCompose(str.strip)
    default_output_processor = TakeFirst()

    category_in = MapCompose(str.strip, sec_clean_category)
    website_in = Compose(sec_website)


class FcaLoader(ItemLoader):
    default_item_class = NoiresItem
    default_input_processor = MapCompose(str.strip)
    default_output_processor = TakeFirst()

    date_in = MapCompose(format_date('%d/%m/%Y'))
