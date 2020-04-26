STUDENT_ID_INDEX = 0
ACTION_TYPE_INDEX = 1
ACTION_ID_INDEX = 2
FACULTY_NAME_INDEX = 3
SUBJECT_NAME_INDEX = 4
SUBJECT_TYPE_INDEX = 5
SEASON_INDEX = 6


class Structure:
    inserted_actions = 0
    deleted_actions = 0
    actions_completed = 0
    student_count = 0
    subject_count = 0
    faculties_count = 0
    valid_faculties = []

    def __init__(self):
        self.faculties = {}

    def _add_new_faculty(self, parts):
        self.faculties[parts[FACULTY_NAME_INDEX]] = {}
        self._add_new_season(parts, self.faculties.get(parts[FACULTY_NAME_INDEX]))

    def _add_new_season(self, parts, faculty):
        faculty[parts[SEASON_INDEX]] = {}
        self._add_new_subject(parts, faculty[parts[SEASON_INDEX]])

    def _add_new_subject(self, parts, season):
        season[parts[SUBJECT_NAME_INDEX]] = {}
        self._add_new_subject_action(parts, season[parts[SUBJECT_NAME_INDEX]])

    def _add_new_subject_action(self, parts, subject):
        subject[parts[SUBJECT_TYPE_INDEX]] = {}
        self._add_new_action(parts, subject[parts[SUBJECT_TYPE_INDEX]])

    def _add_new_action(self, parts, subject_action):
        subject_action[parts[ACTION_ID_INDEX]] = []
        subject_action[parts[ACTION_ID_INDEX]].append(parts[STUDENT_ID_INDEX])

    def insert_record(self, parts):
        """
        Functions that insert passed record into created structure
        :param parts: list composite of [User number, action type, action id, faculty name, subject name, subject type,
                                         season name]
        """
        self.inserted_actions = self.inserted_actions + 1
        self.actions_completed = self.actions_completed + 1
        faculty = self.faculties.get(parts[FACULTY_NAME_INDEX])
        if faculty:
            season = faculty.get(parts[SEASON_INDEX])
            if season:
                subject = season.get(parts[SUBJECT_NAME_INDEX])
                if subject:
                    subject_action = subject.get(parts[SUBJECT_TYPE_INDEX])
                    if subject_action:
                        action_id = subject_action.get(parts[ACTION_ID_INDEX])
                        if action_id:
                            action_id.append(parts[STUDENT_ID_INDEX])
                        else:
                            self._add_new_action(parts, subject_action)
                    else:
                        self._add_new_subject_action(parts, subject)
                else:
                    self._add_new_subject(parts, season)
            else:
                self._add_new_season(parts, faculty)
        else:
            self._add_new_faculty(parts)

    def delete_record(self, parts):
        """
        Function that deletes specific record from the created structure
        :param parts: list composite of [User number, action type, action id, faculty name, subject name, subject type,
                                         season name]
        """
        self.deleted_actions = self.deleted_actions + 1
        self.inserted_actions = self.inserted_actions + 1
        self.actions_completed = self.actions_completed - 1
        self.faculties.get(parts[FACULTY_NAME_INDEX]).get(parts[SEASON_INDEX]).get(parts[SUBJECT_NAME_INDEX]) \
            .get(parts[SUBJECT_TYPE_INDEX]).get(parts[ACTION_ID_INDEX]).remove(parts[STUDENT_ID_INDEX])

    def get_needed_counts(self):
        """
        Function used to get remaining counts out of created structure
        """
        unique_students = set()

        for faculty_name, faculty in self.faculties.items():
            faculty_valid = False
            faculty_subject_count = 0
            for season in faculty.values():
                for subject in season.values():
                    subject_valid = False
                    subject_students = 0
                    if "Př" in subject:  # does subject contain lectures?
                        for lecture in subject["Př"].values():
                            for student in lecture:
                                subject_valid = True
                                subject_students = subject_students + 1
                                if student not in unique_students:
                                    unique_students.add(student)

                    elif "Cv" in subject:  # does subject contain practices?
                        for practice in subject["Cv"].values():
                            for student in practice:
                                subject_students = subject_students + 1
                                subject_valid = True
                                if student not in unique_students:
                                    unique_students.add(student)
                    else:
                        for seminar in subject["Se"].values():
                            for student in seminar:
                                subject_students = subject_students + 1
                                subject_valid = True
                                if student not in unique_students:
                                    unique_students.add(student)
                    if subject_valid:
                        faculty_valid = True
                        self.subject_count = self.subject_count + 1
                    faculty_subject_count = faculty_subject_count + subject_students  # can produce exception?
            if faculty_valid:
                self.faculties_count = self.faculties_count + 1
                self.valid_faculties.append([faculty_name, faculty_subject_count])

        self.student_count = len(unique_students)
