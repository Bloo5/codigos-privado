class Character {
   constructor(Name, Race, Age, Gender, Main) {
      this.Name = Name
      this.Race = Race
      this.Age = Age
      this.Gender = Gender
      this.Main = Main
      this.Level = 1
   }
}

class Mage extends Character {
   constructor() {
      this.Class= 'Mage'
      this.Mana = 100
      this.Health = 80
      this.Barrier = 0
   }

   FireBall(target){
      this.Mana = this.Mana - 10
      target.Health = target.Health - 20      
   }

   IceBarrier() {
      this.Barrier = this.Barrier + 20
      this.Mana = this.Mana - 10      
   }

   Meditate() {
      this.Mana = this.Mana + 20
   }
}