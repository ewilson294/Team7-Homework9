""" 
Team#: 7
Team Member-1: Eric Wilson - Member’s Contribution 33%
Team Member-2: Ha Tran - Member’s Contribution 33%
Team Member-3: Quynh Tran - Member’s Contribution 33%
"""

import pandas as pd

# Read-in the data
tutor = pd.read_excel("Tutor.xlsx")
student = pd.read_excel("Student.xlsx")
mhist = pd.read_excel("Match_History.xlsx")

# review tutor data
tutor.info()

# covert TutorID to string
tutor['TutorID'] = tutor['TutorID'].astype(str)

# review student data type
student.info()

# covert StudentID, StudentGroup to string
student[['StudentID', "StudentGroup"]] = student[['StudentID', "StudentGroup"]].astype(str)

# review match_history data type
mhist.info()

# covert TutorID and StudentID to string
mhist[['TutorID', 'StudentID']] = mhist[['TutorID', 'StudentID']].astype(str)

print("\n")
print("########## Problem 1 ################")
# 1.Which tutors have a Dropped status and have achieved their certification after 4/01/2018?
students = tutor.loc[(tutor['TutorStatus'] == "Dropped") & (tutor["CertDate"] > "04/01/2018")]
print(students)

print("\n")
print("########## Problem 2 ################")
# 2.What is the average length of time a student stayed (or has stayed) in the program? Use the current date for ongoing tutoring.
# get current date - using normalize() to display the date only
cur_date = pd.to_datetime("today").normalize()
# copy match_history data
mhist_c = mhist.copy()
# fill in empty values at EndDate column
mhist_c['EndDate'].fillna(cur_date, inplace = True)
# define the average length of time per student
duration = mhist_c["EndDate"] - mhist_c['StartDate']
print("Average length of time a student stayed (or has stayed) in the program is", duration.mean().components.days, "days."  )

print("\n")
print("########## Problem 3 ################")
# merging match_hist data with tutor data
mhist_tutor = pd.merge(tutor, mhist, on = "TutorID", how = "left")
# mering match_list data with student data
mhist_std = pd.merge(student, mhist, on = "StudentID", how = "left")
# combining the 2 datasets
data = pd.merge(mhist_tutor, mhist_std, how = "outer")

# 3.Identify all students who have been matched in 2018 with a tutor whose status is Temp Stop.
students = data.loc[(data['StartDate'].dt.year == 2018) & (data['TutorStatus'] == "Temp Stop")]
print(students)

print("\n")
print("########## Problem 4 ################")
# 4.List the Read scores of students who were ever taught by tutors whose status is Dropped.
read_score = data[["StudentID", "ReadScore"]].loc[(data['TutorStatus'] == "Dropped") & (data['StudentID'].notnull())]
print(read_score)

print("\n")
print("########## Problem 5 ################")
# 5.List the tutors who taught two or more students
# Remove tutors who have never been matched
tutor_mat = mhist_tutor.loc[mhist_tutor['StudentID'].notnull()]
# crate summary table 
count_tutor = tutor_mat.groupby(["TutorID"])['StudentID'].agg('nunique')
# covert summary table to dataframe
count_tutor = pd.DataFrame(count_tutor)
# rename column
count_tutor.rename(columns = {'StudentID' : 'Number of Student'}, inplace = True)
# List the tutors who taught two or more students
tutor = count_tutor.loc[count_tutor['Number of Student'] >= 2]
print(tutor)

print("\n")
print("########## Problem 6 ################")
# 6.Display a list of all students, their read score, their tutors, and tutors status. 
student_tutor = data[["StudentID", "ReadScore", "TutorID", "TutorStatus"]].loc[data['StudentID'].notnull()]
print(student_tutor)

#Store this information in a file names Student_Tutor.xlsx
student_tutor.to_excel('Student_Tutor.xlsx',index=False)

print("\n")
print("########## Problem 7 ################")
# 7.For each student group, list the number of tutors who have been matched with that group.
# Remove students who have never been matched
std_tutor_mat = mhist_std.loc[mhist_std['TutorID'].notnull()]
# crate summary table 
count_tutor = std_tutor_mat.groupby(["StudentGroup"])['TutorID'].agg('nunique')
# covert summary table to dataframe
count_tutor = pd.DataFrame(count_tutor).rename(columns = {'TutorID' : 'Number of Tutor'})
# list the number of tutors who have been matched 
print(count_tutor)

print("\n")
print("########## Problem 8 ################")
# 8.List all active students who started in May and June. 
# Extract active students
act_std = mhist.loc[data['EndDate'].isnull()]
# List all active students who started in May and June
students = act_std.loc[(act_std['StartDate'].dt.month == 5)|(act_std['StartDate'].dt.month == 6)]
print(students)

print("\n")
print("########## Problem 9 ################")
# 9.Find students who have not been tutored yet.
no_tutor = mhist_std.loc[mhist_std['TutorID'].isnull()]
print(no_tutor)

print("\n")
print("########## Problem 10 ################")
# 10.Find tutors who did not tutor any students. 
no_std = mhist_tutor.loc[mhist_tutor['StudentID'].isnull()]
print(no_std)
