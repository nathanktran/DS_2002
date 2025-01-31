-- SQL Exercises (With Answers)

-- 1. Retrieve all students who enrolled in 2023.

SELECT * FROM Students WHERE YEAR(EnrollmentDate) = 2023;

-- 2. Find students whose email contains 'gmail.com'.

SELECT * FROM Students WHERE Email LIKE '%gmail.com%';

-- 3. Count how many students are enrolled in the database.

SELECT COUNT(*) AS TotalStudents FROM Students;

-- 4. Find students born between 2000 and 2005.

SELECT * FROM Students WHERE DateOfBirth BETWEEN '2000-01-01' AND '2005-12-31';

-- 5. List students sorted by last name in descending order.

SELECT * FROM Students ORDER BY LastName DESC;

-- 6. Find the names of students and the courses they are enrolled in.

SELECT s.StudentID, s.FirstName, s.LastName, c.CourseID, c.CourseName FROM Enrollments e
JOIN Students s ON e.StudentID = s.StudentID
JOIN Courses c ON e.CourseID = c.CourseID;

-- 7. List all students and their courses, ensuring students without courses are included (LEFT JOIN).

SELECT s.StudentID, s.FirstName, s.LastName, c.CourseID, c.CourseName FROM Students s
LEFT JOIN Enrollments e ON s.StudentID = e.StudentID
LEFT JOIN Courses c ON e.CourseID = c.CourseID;

-- 8. Find all courses with no students enrolled (LEFT JOIN).

SELECT c.CourseName FROM Courses c
LEFT JOIN Enrollments e ON c.CourseID = e.CourseID
WHERE e.EnrollmentID IS NULL;

-- 10. List courses and show the number of students enrolled in each course.

SELECT c.CourseName, COUNT(e.StudentID) AS TotalStudents FROM Courses c
LEFT JOIN Enrollments e ON c.CourseID = e.CourseID
GROUP BY c.CourseID, c.CourseName;

