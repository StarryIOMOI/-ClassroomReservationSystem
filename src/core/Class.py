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
          self.course = []

class Courses:
     def __init__(self, course_id, course_name, class_id, class_name,classroom_id, classroom_name,
     teacher_id, teacher_name, week_start, week_end, timeslot_id, semester_id):
          self.id = course_id
          self.name = course_name
          self.class_id = class_id
          self.class_name = class_name
          self.classroom_id = classroom_id
          self.classroom_name = classroom_name
          self.teacher_id = teacher_id
          self.teacher_name = teacher_name
          self.week_start = week_start
          self.week_end = week_end
          self.timeslot_id = timeslot_id
          self.semester_id = semester_id
     
class Semesters:
     def __init__(self, semester_id, semester_name, start, end, total_week):
          self.id = semester_id
          self.name = semester_name
          self.start = start
          self.end = end
          self.week = total_week

class Timenow:
     def __init__(self, id, name, week):
          self.id = id
          self.name = name
          self.week = week