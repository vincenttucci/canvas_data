from bakery import assert_equal
from bakery_canvas import get_submissions
import matplotlib.pyplot as plt
from bakery_canvas import get_courses
from datetime import datetime

help_commands = """
exit > Exit the application
help > List all the commands
course > Change current course
points > Print total points in course
comments > Print how many comments in course
graded > Print ratio of ungraded/graded assignments
score_unweighted > Print average unweighted score
score > Print average weighted score
group > Print average of assignment group, by name
assignment > Print the details of a specific assignment, by ID
list > List all the assignments in the course
scores > Plot the distribution of grades in the course
earliness > Plot the distribution of the days assignments were submitted early
compare > Plot the relationship between assignments' points possible and their weighted points possible
predict > Plot the trends in grades over assignments, showing max ever possible, max still possible, and minimum still possible
"""
def count_courses(user_token: str) -> int:
    '''
    Consumes a user_token (a string value)
    and produces an integer representing
    the number of courses that the user is taking.
    
    Consumes:
    1. user_token (str): a string that represents the user's 
                         unique identifier.
    Returns: an integer representing the number
    of courses a student is taking.
    '''
    courses = get_courses(user_token)
    return len(courses)

assert_equal(count_courses('annie'), 6)
assert_equal(count_courses('jeff'), 6)
assert_equal(count_courses('pierce'), 0)
assert_equal(count_courses('troy'), 1)

def find_cs1(user_token: str) -> int:
    '''
    Consumes a user_token(a string) and produces an integer 
    representing the id of the first course that has the 
    text "CISC1" in their code field. If not Course can be found
    that satisfies this criteria, return 0 instead.
    
    Consumes:
    1. user_token (str): a string that represents the user's 
                         unique identifier.
    Returns: an integer representing the ID of the course
    that has "CISC1" in their code field
    '''
    courses = get_courses(user_token)
    id = 0
    for course in courses:
        if 'CISC1' in course.code:
            id = course.id
            break
    return id

assert_equal(find_cs1('annie'), 100167)
assert_equal(find_cs1('jeff'), 100167)
assert_equal(find_cs1('pierce'), 0)
assert_equal(find_cs1('troy'), 0)

def find_course(user_token: str, course_id: int) -> str:
    '''
    consumes a user_toke (a string) and a course_id (an integer),
    and produces a string representing the full name of the course 
    with the given id. If no sourse is found, then return
    "no course found" instead.
    
    Consumes:
    1. user_token (str): a string that represents the user's 
                         unique identifier.
    2. course_id (int): an integer representing the ID
                        of the course 
    Returns: a string representing the full name of a course
    with the given ID
    
    '''
    courses = get_courses(user_token)
    found = 'no course found'
    
    for course in courses:
        if course_id == course.id:
            found = course.name
    return found

assert_equal(find_course('annie', 394382), 'History of Ice Cream')
assert_equal(find_course('jeff', 600), 'no course found')
assert_equal(find_course('abed', 134088), 'Physical Education Education')

def render_courses (user_token: str) -> str:
    '''
    consumes a user_token (a string) and produces a single 
    string that combines all the available courses by joining together 
    their IDs and codes, ending each course with a newline.
    If the user has no courses, produce just the empty string.
    
    Consumes:
    1. user_token (str): a string that represents the user's 
                         unique identifier 
    Returns: a string that combines all the available
    courses by joining together their IDs and codes,
    ending each course with a newline.
    '''
    courses = get_courses(user_token)
    available_courses = ''
    
    for course in courses:
        available_courses += str(course.id) +': ' + str(course.code) + '\n'  
    return available_courses

assert_equal(render_courses('annie'), '679554: MATH101\n386814: ENGL101\n4182: SPAN101\n394382: ICRM304\n100167: CISC1\n134088: PHED201\n')
assert_equal(render_courses('troy'), '394382: ICRM304')
assert_equal(render_courses('pierce'), '')

def total_points(user_token: str, course_id: int) -> int:
    '''
    Consumes a user_token (a string) and a course_id (an integer), 
    and produces an integer representing the total number of points 
    possible in the course (NOT adjusted by group weights).
    
    Consumes:
    1. user_token (str): a string that represents the user's 
                         unique identifier
    2. course_id (int): an integer representing the ID
                        of the course 
    Returns: an integer representing the total number
    of points available in the course
    '''
    total = 0
    submissions = get_submissions(user_token, course_id)
    
    for submission in submissions:
        total += submission.assignment.points_possible
        
    return total

assert_equal(total_points('annie', 679554), 420)
assert_equal(total_points('annie', 386814), 700)
assert_equal(total_points('annie', 100167), 1060)
assert_equal(total_points('jeff', 679554), 420)
assert_equal(total_points('jeff', 386814), 700)
assert_equal(total_points('troy', 394382), 100)

def count_comments(user_token: str, course_id: int) -> int:
    '''
    Consumes a user_token (a string) and a course_id (an integer), 
    and produces an integer representing the number of comments across 
    all the submissions for that course.
    
    Consumes:
    1. user_token (str): a string that represents the user's 
                         unique identifier
    2. course_id (int): an integer representing the ID
                        of the course   
    Returns: an integer representing the total number
    of comments in the course
    '''
    submissions = get_submissions(user_token, course_id)
    total = 0
    for submission in submissions:
        if submission.comments:
            total += len(submission.comments)
            
    return total

assert_equal(count_comments('annie', 679554), 14)
assert_equal(count_comments('troy', 394382), 0)

def ratio_graded(user_token: str, course_id: int) -> str:
    '''
    consumes a user_token (a string) and a course_id 
    (an integer), and produces a string value representing the 
    number of assignments that have been graded compared to the 
    number of total assignments in the course.
    
    Consumes:
    1. user_token (str): a string that represents the user's 
                         unique identifier
    2. course_id (int): an integer representing the ID
                        of the course
    Returns: a string representing the ratio of
    assignmnets that have been graded vs ungraded
    '''
    submissions = get_submissions(user_token, course_id)
    denominator = len(submissions)
    
    numerator = 0
    for submission in submissions:
        if submission.status == 'graded':
            numerator += 1
            
    return (str(numerator) + '/' + str(denominator))

assert_equal(ratio_graded('annie', 679554), '10/10')
assert_equal(ratio_graded('annie', 134088), '6/11')
assert_equal(ratio_graded('shirley', 134088), '7/11')

def average_score (user_token: str, course_id: int) -> float:
    '''
    Consumes a user_token (a string) and a course_id (an integer), 
    and produces a float representing the average, unweighted 
    score of all the graded assignments in the course.
    
    Consumes:
    1. user_token (str): a string that represents the user's 
                         unique identifier
    2. course_id (int): an integer representing the ID
                        of the course
    Returns: a float representing the average, unweighted score
    of all graded assignments in the course
    '''
    
    points_possible = 0.0
    points_earned = 0.0
    submissions = get_submissions(user_token, course_id)
    
    for submission in submissions:
        if submission.status == 'graded':
            points_earned += submission.score 
            points_possible += submission.assignment.points_possible
    
    return points_earned/points_possible

assert_equal(average_score('annie', 679554), 0.95)
assert_equal(average_score('annie', 386814), 0.97)
assert_equal(average_score('jeff', 386814), 0.7)

def average_weighted (user_token: str, course_id: int) -> float:
    '''
    Consumes a user_token (a string) and a course_id (an integer), 
    and produces a float representing the average, weighted score 
    of all the graded assignments in the course.
    
    Consumes:
    1. user_token (str): a string that represents the user's 
                         unique identifier
    2. course_id (int): an integer representing the ID
                        of the course 
    Returns: a float representing the average, weighted score
    of all graded assignments in the course
    '''
    submissions = get_submissions(user_token, course_id)
    score_sum = 0
    points_possible = 0
    for submission in submissions:
        if submission.status == 'graded':
            score_sum += submission.score * submission.assignment.group.weight
            points_possible += submission.assignment.points_possible * submission.assignment.group.weight
    
    return score_sum/points_possible

assert_equal (average_weighted('annie', 679554), 0.9471153846153846)
assert_equal (average_weighted('annie', 386814), 0.97)
assert_equal (average_weighted('jeff', 386814), 0.7)

def average_group (user_token: str, course_id: int, group_name: str) -> float:
    '''
    Consumes a user_token (a string), a course_id (an integer), 
    and a group_name (a string). The function returns a float
    representing the average, unweighted score for all the
    graded submissions that have that group_name
    
    Consumes:
    1. user_token (str): a string that represents the user's 
                         unique identifier
    2. course_id (int): an integer representing the ID
                        of the course
    3. group_name (str): a string representing the name of a group
                        of assignments
    Returns: a float representing the average, unweighted
    grade ratio of all assignments with that group_name
    '''
    submissions = get_submissions(user_token, course_id)
    
    total_score = 0
    points_earned = 0
    
    for submission in submissions:
        if group_name.lower() == submission.assignment.group.name.lower():
            if submission.status == 'graded':
                total_score += submission.assignment.points_possible
                points_earned += submission.score 
            
    if total_score == 0.0:
        return 0.0
    
assert_equal(average_group('annie', 679554, 'Homework'), 0.9636363636363636)
assert_equal(average_group('troy', 394382, 'Assignments'), 0.8)

def render_assignment(user_token: str, course_id: int, assignment_id: int) -> str:
    '''
    consumes a user_token (a string), a course_id (an integer), and an assignment_id 
    (an integer). The function produces a string representing the assignment and its 
    submission details. If the assignment cannot be found in the user's submissions, 
    then return the string "Assignment not found: " followed by the assignment_id.
    
    Consumes:
    1. user_token (str): a string that represents the user's 
                         unique identifier.
    2. course_id (int): an integer representing the ID
                        of the course
    3. assignment_id (int): an integer representing
                            an assignment's ID
    Returns: a string representing an assignment
    and its submission details
    '''
    submissions = get_submissions(user_token, course_id)
    
    printed = "Assignment not found: " + str(assignment_id)
    
    for submission in submissions:
        if submission.assignment.id == assignment_id:
            printed = str(submission.assignment.id) + ": " + submission.assignment.name + "\nGroup: " + submission.assignment.group.name + "\nModule: " + submission.assignment.module + "\nGrade: "  
            if submission.status == "graded":
                g = str(submission.score) + "/" + str(submission.assignment.points_possible) + " (" + submission.grade + ")"
                printed += g
            else:
                printed += "(missing)"
    return printed

assert_equal(render_assignment('annie', 679554, 7), 'Assignment not found: 7')
assert_equal(render_assignment('annie', 679554, 299650), '299650: Introduction\nGroup: Homework\nModule: Module 1\nGrade: 10.0/10 (A)')
assert_equal(render_assignment('annie', 679554, 553716), '553716: Basic Addition\nGroup: Homework\nModule: Module 2\nGrade: 14.0/15 (A)')
assert_equal(render_assignment('annie', 679554, 805499), '805499: Basic Subtraction\nGroup: Homework\nModule: Module 2\nGrade: 19.0/20 (A)')
assert_equal(render_assignment('annie', 134088, 937202), '937202: Technology in the outdoor classroom\nGroup: Homework\nModule: Module 2\nGrade: (missing)')
assert_equal(render_assignment('jeff', 386814, 24048), '24048: HOMEWORK 3\nGroup: Assignments\nModule: MODULE 1\nGrade: 58.0/100 (F)')

def render_all(user_token: str, course_id: int) -> str:
    '''
    consumes a user_token (a string) and a course_id 
    (an integer), and produces a single string that describes all 
    of the submissions in the course.
    
    Consumes:
    1. user_token (str): a string that represents the user's 
                         unique identifier.
    2. course_id (int): an integer representing the ID
                        of the course
    Returns: a string representing all submissions
    in the course
    '''
    submissions = get_submissions(user_token, course_id)
    string = ''
    x = False
    for submission in submissions:
        if submission.grade:
            string += (str(submission.assignment.id) + ": " + submission.assignment.name + " (Graded)\n")
        else:
            string += (str(submission.assignment.id) + ": " + submission.assignment.name + " (Ungraded)\n")
    return string

assert_equal(render_all('troy', 394382), '711675: Practical (graded)')
assert_equal(render_all('shirley', 679554), '299650: Introduction (graded)\n553716: Basic Addition (graded)\n805499: Basic Subtraction (graded)\n749969: Basic Multiplication (graded)\n763866: Basic Division (graded)\n979025: Midterm 1 (graded)\n870878: Logarithms (graded)\n126393: Antiderivatives (graded)\n122494: Actual Sorcery (graded)\n683132: Final Exam (graded)\n')

def plot_scores(user_token: str, course_id: int):
    '''
    consumes a user_token (a string) and a course_id 
    (an integer) and returns nothing but creates a graph 
    representing the distribution of the fractional 
    scores in the course. 
    
    Consumes:
    1. user_token (str): a string that represents the user's 
                   unique identifier.
    2. course_id (int): an integer representing the unique identifier 
                  of the course.
    Returns: nothing but creates a histogram
             representing submission scores in a course.
    '''
    
    submissions = get_submissions(user_token, course_id)
    data = []
    for submission in submissions:
        if submission.grade:
            if submission.assignment.points_possible > 0:
                data.append(submission.score/submission.assignment.points_possible*100)
    plt.hist(data)
    plt.title('Distribution of Fractional Scores in the Course')
    plt.xlabel('Score Received')
    plt.ylabel('Number of Assignments')
    plt.show()
    
def days_apart(first_date: str, second_date: str) -> int:
    """
    Determines the days between `first` and `second` date.
    
    Consumes:
    1. first_date (str): a string representing the date
                         that an assignment was due at.
    
    2. second_date (str): a string representing the date
                          that an assignment was submitted
                          at.
    Returns: an integer representing the days between those
    two dates
    """
    first_date = datetime.strptime(first_date, "%Y-%m-%dT%H:%M:%S%z")
    second_date = datetime.strptime(second_date, "%Y-%m-%dT%H:%M:%S%z")
    difference = second_date - first_date
    
    return difference.days

def plot_earliness(user_token: str, course_id: int):
    '''
    consumes two strings (representing two dates in ISO format)
    and produces an integer indicating how many days are between
    the two dates.
    
    Consumes:
    1. user_token (str): a string that represents the user's 
                   unique identifier.
    2. course_id (int): an integer representing the unique identifier 
                  of the course.      
    Returns: nothing but creates a graph representing the
    lateness of each submission
    '''
    submissions = get_submissions(user_token, course_id)
    
    data = []
    for submission in submissions:
        if submission.submitted_at and submission.assignment.due_at:
            data.append(days_apart(submission.submitted_at, submission.assignment.due_at))
    
    plt.hist(data)
    plt.title('Lateness')
    plt.xlabel('Due Dates')
    plt.ylabel('Number of Assignments')
    plt.show()
    
def plot_points(user_token: str, course_id: int):
    '''
    consumes a user_token (a string) and a course_id 
    (an integer) and returns nothing but creates a 
    graph comparing the points possible for each 
    assignment with the weighted points possible 
    for that assignment
    
    Consumes:
    1. user_token (str): a string that represents the user's 
                   unique identifier.
    2. course_id (int): an integer representing the unique identifier 
                  of the course.
    Returns: nothing but creates a graph comparing the points possible
    for each assignment with the weighted points possible for that assignment
    '''
    submissions = get_submissions(user_token, course_id)
    possible_points = []
    weighted_points = []
    
    total_weighted = 0
    for submission in submissions:
        total_weighted += (submission.assignment.points_possible * submission.assignment.group.weight) / 100
        if total_weighted == 0:
            return
        
    compared_points = 0
    points = 0
    for submission in submissions:
        points = (submission.assignment.points_possible)
        compared_points = (submission.assignment.points_possible * submission.assignment.group.weight / total_weighted)
        possible_points.append(points)
        weighted_points.append(compared_points)
        
    plt.scatter(possible_points, weighted_points)
    plt.title('Points Possible vs Weighted Points')
    plt.xlabel('Points Possible')
    plt.ylabel('Weighted Points Possible')
    plt.show()
    
def predict_grades(user_token: str, course_id: int):
    '''
    consumes a user_token (a string) 
    and a course_id (an integer) and returns 
    nothing but creates a graph with three running sums
    
    Consumes:
    1. user_token (str): a string that represents the user's 
                         unique identifier.
    2. course_id (int): an integer representing the unique identifier 
                            of the course.
    Returns: nothing but creates a graph comparing the points possible
    for each assignment with three running sum lines representing:
        1. the maximum weughted points possible in the course
        2. the maximum weighted score in the course
        3. the minimum possible weited score in the course
    '''
    submissions = get_submissions(user_token, course_id)
    total_max_points = 0
    total_max_score = 0
    total_min_score = 0
    max_points = []
    max_score = []
    min_score = []
    total_weighted = 0
    for submission in submissions:
        total_weighted += (submission.assignment.points_possible * submission.assignment.group.weight) / 100
    
    for submission in submissions:
        total_max_points += submission.assignment.points_possible * submission.assignment.group.weight / total_weighted
        if submission.graded_at:
            total_min_score += submission.score * submission.assignment.group.weight / total_weighted
            total_max_score += submission.score * submission.assignment.group.weight / total_weighted
        else:
            total_max_score += submission.assignment.points_possible * submission.assignment.group.weight / total_weighted
        
        max_points.append(total_max_points)
        max_score.append(total_max_score)
        min_score.append(total_min_score)
        
    plt.plot(max_points, label = 'Max Points')
    plt.plot(max_score, label = 'Max Score')
    plt.plot(min_score, label = 'Min Score')
    plt.title('What Grade Will I Earn?')
    plt.xlabel('Weighted Points')
    plt.ylabel('Course Percentage')
    plt.legend()
    plt.show()

def execute(command: str, user_token: str, course_id: int) -> int:
    '''
    Consumes a command, user_token, ans course_id to return
    an integer representing the ID of the course the user
    is working with, and also prints results calling the previous
    functions, depending on the user's command

    Consumes:
    1. Command (str): a string representing a command of
                      the user's desired action
    2. user_token (str): a string that represents the user's 
                         unique identifier.
    3. course_id (int): an integer representing the unique identifier 
                            of the course.
    Returns: an integer representing the ID of the current course
    '''
    if command == 'exit':
        return 0
    elif command == 'course':
        print (render_courses(user_token))
        course_id = int(input('enter your course ID: '))
        print (find_course(user_token, course_id)) 
    elif command == 'points':
        print (total_points(user_token, course_id))
    elif command == 'comments':
        print (count_comments(user_token, course_id))
    elif command == 'graded':
        print (ratio_graded(user_token, course_id))
    elif command == 'score_unweighted':
        print (average_score(user_token, course_id))
    elif command == 'score':
        print (average_weighted(user_token, course_id))
    elif command == 'group':
        group_name = input('Enter a Group Name: ')
        print (average_group(user_token, course_id, group_name))
    elif command == 'assignment':
        assignment_id = int(input('Enter an Assignment ID: '))
        print(render_assignment(user_token, course_id, assignment_id))
    elif command == 'list': 
        print (render_all(user_token, course_id))
    elif command == 'scores':
        print (plot_scores(user_token, course_id))
    elif command == 'earliness':
        print (plot_earliness(user_token, course_id))
    elif command == 'compare':
        print (plot_points(user_token, course_id))
    elif command == 'predict':
        print (predict_grades(user_token, course_id))
    elif command == 'help':
        print (help_commands)
    return course_id      
    
def main(user_token: str):
    '''
    Consumes a user_token and calls the execute function
    to display the results of the user's desired actions.
    
    Consumes:
    1. Command (str): a string representing a command of
                      the user's desired action
    Returns: nothing but calls the execute function to
    display results
    '''
    cs1 = 0
    list_of_courses = get_courses(user_token)
    if count_courses(user_token) == 0:
        print ('No courses available')
        return
    else:
        cs1 = find_cs1(user_token)
        if cs1 == 0:
            first_course = list_of_courses[0]
            cs1 = first_course.id
            
    while cs1 > 0:
        what_to_do = input('Enter Your Command or type "help": ')
        print (cs1)
        cs1 = (execute(what_to_do, user_token, cs1))
        
main('annie')