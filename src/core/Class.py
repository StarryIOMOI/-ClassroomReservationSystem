class Buildings:
        def __init__(self, building_id, building_name, status):
             self.id = building_id
             self.name = building_name
             self.status = status
             
class Areas:
     def __init__(self, area_id, area_name, building_id, status):
          self.id = area_id
          self.name = area_name
          self.building_id = building_id
          self.status = status

class Floors:
     def __init__(self, floor_id, floor_name, area_id, status):
          self.id = floor_id
          self.name = floor_name
          self.area_id = area_id
          self.status = status

class Classrooms:
     def __init__(self, classroom_id, classroom_name, floor_id, status):
          self.id = classroom_id
          self.name = classroom_name
          self.floor_id = floor_id
          self.status = status