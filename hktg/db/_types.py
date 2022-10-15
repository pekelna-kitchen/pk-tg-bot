
from typing import Optional
from dataclasses import dataclass

# DB tables names

class Tables:
    LOCATION = 'locations'
    ENTRIES = 'entries'
    PRODUCT = 'products'
    CONTAINER = 'containers'
    TG_USERS = 'tg_users'
    TG_ADMINS = 'tg_admins'
    TG_REQUESTS = 'tg_requests'

@dataclass()
class Product:
    id : Optional[int] = None
    symbol : Optional[str] = None
    name : Optional[str] = None
    limit_container : Optional[int] = None
    limit_amount : Optional[int] = None


    def desc(self):
        return '%s %s' % (self.symbol, self.name)


    def container(self, containers = None):

        if not self.limit_container:
            return None
        if containers:
            c =  _find_tuple_element(containers, {0: self.limit_container})
            return Container(*c)

        from ._postgresql import get_table
        containers = get_table(Tables.CONTAINER, {'id': self.limit_container})
        return Container(*containers[0])

    def is_valid(self):
        return self.symbol and self.name and self.limit_container and self.limit_amount

    def to_sql(self):
        return {
            "name": self.name,
            "symbol": self.symbol,
            "limit_container": self.limit_container,
            "limit_amount": self.limit_amount,
        }


@dataclass()
class Location:
    id : Optional[int] = None
    symbol : Optional[str] = None
    name : Optional[str] = None

    def desc(self):
        return '%s %s' % (self.symbol, self.name)

    def is_valid(self):
        return self.symbol and self.name

    def to_sql(self):
        return {
            "name": self.name,
            "symbol": self.symbol,
        }


@dataclass()
class Container:
    id : Optional[int] = None
    symbol : Optional[str] = None
    description : Optional[str] = None

    def desc(self):
        return '%s %s' % (self.symbol, self.description)

    def is_valid(self):
        return self.symbol and self.description

    def to_sql(self):
        return {
            "description": self.description,
            "symbol": self.symbol,
        }


@dataclass
class Entry:
    id: Optional[int] = None
    product_id: Optional[int] = None
    location_id: Optional[int] = None
    amount: Optional[int] = None
    container_id: Optional[int] = None
    date: Optional[str] = None
    editor: Optional[str] = None

    def is_valid(self):
        return self.product_id and self.location_id and self.amount and self.container_id

    def to_sql(self):
        return {
            "product_id": self.product_id,
            "location_id": self.location_id,
            "container_id": self.container_id,
            "amount": self.amount,
        }

    def container(self, containers = None):

        if not self.container_id:
            return None

        if containers:
            c = _find_tuple_element(containers, {0: self.container_id})
            return Container(*c)

        from ._postgresql import get_table
        containers = get_table(Tables.CONTAINER, {'id': self.container_id})
        return Container(*containers[0])

    def product(self, products = None) -> Product | None:
        if not self.product_id:
            return None

        if products:
            pr = _find_tuple_element(products, {0: self.product_id})
            return Product(*pr)

        from ._postgresql import get_table
        products = get_table(Tables.PRODUCT, {'id': self.product_id})
        return Product(*products[0])

    def location(self, locations = None):
        if not self.location_id:
            return None

        if locations:
            loc = _find_tuple_element(locations, {0: self.location_id})
            return Location(*loc)

        from ._postgresql import get_table
        locations = get_table(Tables.LOCATION, {'id': self.location_id})
        return Location(*locations[0])

# utilities

def _find_tuple_element(tuples, comparables: dict):
    def check_tuple_elem(t):
        for key in comparables:
            if t[key] != comparables[key]:
                return False
        return True

    return next((x for x in tuples if check_tuple_elem(x)), None)
