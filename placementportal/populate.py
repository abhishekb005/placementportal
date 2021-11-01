
from django_faker import Faker
# this Populator is only a function thats return a django_faker.populator.Populator instance
# correctly initialized with a faker.generator.Generator instance, configured as above
populator = Faker.getPopulator()

from placementapp.models import User,School,Degree
populator.addEntity(User,5)
populator.addEntity(School,10)
populator.addEntity(Degree,10)

insertedPks = populator.execute()