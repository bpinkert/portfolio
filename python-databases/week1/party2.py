class PartyAnimal:
  x = 0
  name = "" ""
  def __init__(self, z):
  	# call name argument into z variable
  	self.name = z
  	print self.name,"I am constructed"

  def party(self):
  	self.x = self.x + 1
  	print self.name,"party count",self.x

# an = PartyAnimal()

# # calling party method in an ob
# an.party()
# an.party()
# an.party()

s = PartyAnimal("Sally")
s.party()

j = PartyAnimal("Jim")
j.party()
s.party()