from sqlalchemy import ForeignKey, Column, Table, Integer, String, MetaData
from sqlalchemy.orm import relationship, backref,session
from sqlalchemy.orm import declarative_base

convention = {
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
}
metadata = MetaData(naming_convention=convention)

Base = declarative_base(metadata=metadata)

freebie_dev = Table(
    'freebie_devs',
    Base.metadata,
    Column('company_id', ForeignKey('companies.id'), primary_key=True),
    Column('dev_id', ForeignKey('devs.id'), primary_key=True),
    extend_existing=True,
)


class Company(Base):
    __tablename__ = 'companies'

    id = Column(Integer(), primary_key=True)
    name = Column(String())
    founding_year = Column(Integer())
    
    devs = relationship('Dev', secondary=freebie_dev, back_populates='companies')
    freebies = relationship('Freebie', backref=backref('company'))

    def __repr__(self):
        return f'<Company {self.name}>'
    
    def give_freebie(self, dev, item_name, value):
        freebie = Freebie(item_name=item_name, value=value, dev=dev, company=self)
        session.add(freebie)
        session.commit()
        return freebie

    @classmethod
    def oldest_company(cls):
        return session.query(cls).order_by(cls.founding_year).first()

class Dev(Base):
    __tablename__ = 'devs'

    id = Column(Integer(), primary_key=True)
    name= Column(String())

    companies = relationship('Company', secondary=freebie_dev, back_populates='devs')
    freebies = relationship('Freebie', backref=backref('dev'))

    def __repr__(self):
        return f'<Dev {self.name}>'
    

    def received_one(self, item_name):
        return any(freebie.item_name == item_name for freebie in self.freebies)

    def give_away(self, dev, freebie):
        if freebie in self.freebies:
            freebie.dev = dev
            session.commit()
    
class Freebie(Base):
    __tablename__ = 'freebies'

    id = Column(Integer(), primary_key=True)
    item_name = Column(String())
    value = Column (Integer())

    dev_id = Column(Integer(), ForeignKey('devs.id'))
    company_id = Column(Integer(), ForeignKey('companies.id'))

    def __repr__(self):
        return f'Freebie(id={self.id}, ' +\
            f'item_name={self.item_name}, ' + \
            f'company_id={self.company_id})'
    
    def print_details(self):
        return f'{self.dev.name} owns a {self.item_name} from {self.company.name}'
    
    

