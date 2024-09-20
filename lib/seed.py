#!/usr/bin/env python3

# Script goes here!
from faker import Faker
import random
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Dev, Company, Freebie

fake = Faker()

if __name__ == '__main__':
    
    engine = create_engine('sqlite:///freebies.db')
    Session = sessionmaker(bind=engine)
    session = Session()
    # delete existing data
    session.query(Dev).delete()
    session.query(Company).delete()
    session.query(Freebie).delete()
    session.commit()

    devs = [
        Dev(
            name=fake.name(),
    )for i in range(50)]

    session.bulk_save_objects(devs)
    session.commit()
    devs = session.query(Dev).all()

    companies = [
        Company(
        name=fake.company(),
        founding_year=random.randint(1900, 2023)
    )
    for _ in range(50)]

    session.bulk_save_objects(companies)
    session.commit()
    companies = session.query(Company).all()

    freebie_items = [
        "T-shirt", "Mug", "Sticker Pack", "Notebook", "USB Drive", 
        "Pen", "Water Bottle", "Backpack", "Keychain", "Headphones"
    ]

    freebies = [
        Freebie(
            item_name=random.choice(freebie_items),
            value=random.randint(5, 100),  # Random value between 5 and 100
            dev_id=random.choice(devs).id,
            company_id=random.choice(companies).id
        ) for _ in range(100)
    ]
    
    session.bulk_save_objects(freebies)
    session.commit()