class Course:
    def __init__(self, name, number, level, prev_courses):
        self.name = name
        self.number = number
        self.level = level
        self.prev_courses = prev_courses

    def __str__(self):
        return "(" + str(self.number) + ") " + self.name + \
            "   lvl(" + str(self.level) + ")     needed_crs=" +\
               str([str(i) for i in self.prev_courses]) + ""

    def __repr__(self):
        return self.__str__()


class Department:
    def __init__(self, table, priority_2, musthave_3, musthave_5):
        self.table = table
        self.priority_2 = priority_2
        self.musthave_3 = musthave_3
        self.musthave_5 = musthave_5

    def count_courses(self, current_lvl_course):
        need = dict()
        need_choose = set()
        for course in current_lvl_course:
            for courses in course.prev_courses:
                if type(courses) == type(tuple()):
                    lst = list()
                    for i in courses:
                        lst.append(i)
                        if i not in need:
                            need[i] = 1
                        else:
                            need[i] += 1
                    need_choose.add(tuple(lst))
                    for i in courses:
                        for crs in i.prev_courses:
                            if crs not in need:
                                need[crs] = 1
                            else:
                                need[crs] += 1
                else:
                    if courses not in need:
                        need[courses] = 1
                    else:
                        need[courses] += 1

        for choose in need_choose:
            min = len(choose) * 10
            min_crs = []
            for crs in choose:
                if crs in need:
                    if min > need[crs]:
                        min = need[crs]
                        min_crs = [crs]
                    elif min == need[crs]:
                        min_crs.append(crs)

            if len(min_crs) == 1:
                if min_crs[0] in need and need[min_crs[0]] == 1:
                    need.pop(min_crs[0])
            else:
                copy = min_crs.copy()
                for same in copy:
                    if same in need and need[same] == 1:
                        min_crs.remove(same)
                if len(min_crs) == 1:
                    need.pop(min_crs[0])
                elif len(min_crs) > 1:
                    copy = min_crs.copy()
                    for i in self.priority_2:
                        if i in min_crs:
                            min_crs.remove(i)
                    if len(min_crs) >= 1:
                        need.pop(min_crs[0])
                    else:
                        need.pop(copy[0])

        list_courses = [(i, j) for i, j in need.items()]
        list_courses.sort(key=lambda i: i[1], reverse=True)
        courses_needed = [i[0] for i in list_courses]
        return courses_needed

    def return_courses_3(self):
        need_2 = self.count_courses(self.musthave_3)
        need_1 = self.count_courses(need_2)
        need_0 = self.count_courses(need_1)

        all_courses = set(need_1).union(set(need_2).union(set(self.musthave_3).union(set(need_0))))
        for courses in all_courses:
            print(courses, end='\n\n')


table = [set() for i in range(6)]
level = set()
cpp = Course("C++", 1, 1, [])
pyth = Course("Python", 2, 1, [])
algo = Course("Algo", 3, 1, [])
level.add(cpp)
level.add(pyth)
level.add(algo)
table[1] = level
level.clear()

cpp2 = Course("C++2", 4, 2, [cpp])
pyth2 = Course("Python2", 5, 2, [pyth])
temp = Course("Temp", 6, 2, [cpp, algo])

level.add(cpp2)
level.add(pyth2)
level.add(temp)
table[2] = level
level.clear()

var = Course("Var", 7, 3, [temp, (pyth, cpp)])
level.add(var)
table[3] = level

dep = Department(table, [], [var], [])

dep.return_courses_3()
