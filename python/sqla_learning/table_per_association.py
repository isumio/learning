"""

Adapted from sqlalchemy source tree: table_per_association.py
https://github.com/zzzeek/sqlalchemy/tree/master/examples/generic_associations

Illustrates a mixin which provides a generic association
via a individually generated association tables for each parent class.
The associated objects themselves are persisted in a single table
shared among all parents.

This configuration has the advantage that all Address
rows are in one table, so that the definition of "Address"
can be maintained in one place.   The association table
contains the foreign key to Address so that Address
has no dependency on the system.


"""
from sqlalchemy.ext.declarative import as_declarative, declared_attr
from sqlalchemy import create_engine, Integer, Column, \
                    String, ForeignKey, Table
from sqlalchemy.orm import Session, relationship

@as_declarative()
class Base(object):
    """Base class which provides automated table name
    and surrogate primary key column.

    """
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()
    id = Column(Integer, primary_key=True)

class Address(Base):
    """The Address class.

    This represents all address records in a
    single table.

    """
    street = Column(String)
    city = Column(String)
    zip = Column(String)

    def __repr__(self):
        return "%s(street=%r, city=%r, zip=%r)" % \
            (self.__class__.__name__, self.street,
            self.city, self.zip)

class HasAddresses(object):
    """HasAddresses mixin, creates a new address_association
    table for each parent.

    """
    @declared_attr
    def addresses(cls):
        address_association = Table(
            "%s_addresses" % cls.__tablename__,
            cls.metadata,
            Column("address_id", ForeignKey("address.id"),
                                primary_key=True),
            Column("%s_id" % cls.__tablename__,
                                ForeignKey("%s.id" % cls.__tablename__),
                                primary_key=True),
        )
        return relationship(Address, secondary=address_association)

class Customer(HasAddresses, Base):
    name = Column(String)

class Supplier(HasAddresses, Base):
    company_name = Column(String)

engine = create_engine('sqlite://', echo=True)
Base.metadata.create_all(engine)

session = Session(engine)

session.add_all([
    Customer(
        name='customer 1',
        addresses=[
            Address(
                    street='123 anywhere street',
                    city="New York",
                    zip="10110"),
            Address(
                    street='40 main street',
                    city="San Francisco",
                    zip="95732")
        ]
    ),
    Supplier(
        company_name="Ace Hammers",
        addresses=[
            Address(
                    street='2569 west elm',
                    city="Detroit",
                    zip="56785")
        ]
    ),
])

session.commit()

for customer in session.query(Customer):
    for address in customer.addresses:
        print(address)

for supplier in session.query(Supplier):
    for address in supplier.addresses:
        print(address)
