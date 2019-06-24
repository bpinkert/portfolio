class PartyAnimal:
  # object w/ bit of data
  x = 0

  # method
  def party(self):
  	self.x = self.x + 1
  	print "So far",self.x

# create PartyAnimal object in an obect
an = PartyAnimal()

# calling party method in an ob
an.party()
an.party()
an.party()