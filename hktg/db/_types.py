
from typing import Optional
from dataclasses import dataclass

# DB tables names

class Tables:
    LOCATION = 'locations'
    ENTRIES = 'entries'
    PRODUCT = 'products'
    CONTAINER = 'containers'

    ROLES = 'roles'
    USERS = 'users'
    PROMOTIONS = 'promotions'

    DISTRICTS = 'districts'
    COORDS = 'coords'
    CIVILS = 'civils'

# WAREHOUSE TYPES

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
        return _get_by_foreign_key(self.limit_container, Tables.CONTAINER, Container, containers)

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
        return _get_by_foreign_key(self.container_id, Tables.CONTAINER, Container, containers)

    def product(self, products = None) -> Product | None:
        return _get_by_foreign_key(self.product_id, Tables.PRODUCT, Product, products)

    def location(self, locations = None):
        return _get_by_foreign_key(self.location_id, Tables.LOCATION, Location, locations)

# USER MANAGEMENT TYPES

@dataclass
class Role:
    id: Optional[int] = None
    name: Optional[str] = None

@dataclass
class User:
    id: Optional[int] = None
    name: Optional[str] = None
    tg_id: Optional[str] = None
    viber_id: Optional[str] = None
    phone: Optional[str] = None

    def is_valid(self):
        return self.name and ( self.tg_id or self.viber_id or self.phone )

    def to_sql(self):
        return {
            "name": self.name,
            "tg_id": self.tg_id,
            "viber_id": self.viber_id,
            "phone": self.phone,
        }

@dataclass
class Promotion:
    id: Optional[int] = None
    users_id: Optional[int] = None
    role_id: Optional[int] = None
    date: Optional[str] = None
    promoter: Optional[int] = None

# DRIVER TYPES

@dataclass
class District:
    id: Optional[int] = None
    name: Optional[str] = None

@dataclass
class Coord:
    id: Optional[int] = None
    longitude: Optional[str] = None
    latitude: Optional[str] = None

@dataclass
class Civil:
    id: Optional[int] = None
    district_id: Optional[int] = None
    address: Optional[str] = None
    phone_number: Optional[str] = None
    notes: Optional[str] = None
    coords_id: Optional[int] = None

    def coords(self, coords = None):
        return _get_by_foreign_key(self.coords_id, Tables.COORDS, Coord, coords)

    def district(self, districts = None):
        return _get_by_foreign_key(self.district_id, Tables.DISTRICTS, District, districts)

# utilities

def _find_tuple_element(tuples, comparables: dict):
    def check_tuple_elem(t):
        for key in comparables:
            if t[key] != comparables[key]:
                return False
        return True

    return next((x for x in tuples if check_tuple_elem(x)), None)

def _get_by_foreign_key(fkey, table_name, type_of, collection, key = 'id' ):
    if not fkey:
        return None

    if collection:
        c = _find_tuple_element(collection, {0: fkey})
        return type_of(*c)

    from ._postgresql import get_table
    tuples_list = get_table(table_name, {key: fkey})
    return type_of(*tuples_list[0])
