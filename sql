Here are 10 commonly asked SQL interview questions with clear examples and answers. These cover basic to intermediate levels, helpful for most data and developer roles:

⸻

🟢 1. What is the difference between WHERE and HAVING?

Answer:
	•	WHERE is used to filter rows before aggregation.
	•	HAVING is used to filter groups after aggregation.

Example:

-- WHERE filters individual rows
SELECT * FROM Employees WHERE Salary > 50000;

-- HAVING filters groups after GROUP BY
SELECT Department, AVG(Salary)
FROM Employees
GROUP BY Department
HAVING AVG(Salary) > 50000;


⸻

🟢 2. Find the second highest salary from the Employee table.

Solution 1: Using LIMIT (MySQL):

SELECT DISTINCT Salary
FROM Employees
ORDER BY Salary DESC
LIMIT 1 OFFSET 1;

Solution 2: Using subquery (Standard SQL):

SELECT MAX(Salary) AS SecondHighest
FROM Employees
WHERE Salary < (SELECT MAX(Salary) FROM Employees);


⸻

🟢 3. What is a JOIN? List types of joins.

Answer:
A JOIN combines rows from two or more tables based on a related column.

Types:
	•	INNER JOIN: Matching rows only
	•	LEFT JOIN: All from left + matches from right
	•	RIGHT JOIN: All from right + matches from left
	•	FULL OUTER JOIN: All rows from both tables

Example:

SELECT a.Name, b.DepartmentName
FROM Employees a
INNER JOIN Departments b ON a.DepartmentID = b.ID;


⸻

🟢 4. Get the count of employees in each department.

SELECT DepartmentID, COUNT(*) AS EmployeeCount
FROM Employees
GROUP BY DepartmentID;


⸻

🟡 5. What is the difference between RANK(), DENSE_RANK(), and ROW_NUMBER()?

Answer:
	•	RANK() gives gaps in ranking if duplicates exist
	•	DENSE_RANK() gives continuous ranks without gaps
	•	ROW_NUMBER() gives unique row index regardless of duplicates

Example:

SELECT Name, Salary,
       RANK() OVER (ORDER BY Salary DESC) AS Rank,
       DENSE_RANK() OVER (ORDER BY Salary DESC) AS DenseRank,
       ROW_NUMBER() OVER (ORDER BY Salary DESC) AS RowNum
FROM Employees;


⸻

🟡 6. Find duplicate records in a table.

SELECT Name, COUNT(*)
FROM Employees
GROUP BY Name
HAVING COUNT(*) > 1;


⸻

🟡 7. Write a query to find the employees with salaries higher than the department average.

SELECT Name, Salary, DepartmentID
FROM Employees e
WHERE Salary > (
    SELECT AVG(Salary)
    FROM Employees
    WHERE DepartmentID = e.DepartmentID
);


⸻

🟡 8. Difference between DELETE, TRUNCATE, and DROP?

Answer:

Operation	Removes Rows	Can Rollback	Resets Identity	Removes Structure
DELETE	Yes	Yes	No	No
TRUNCATE	Yes (All)	No	Yes	No
DROP	Yes (All)	No	Yes	Yes (Table gone)


⸻

🔴 9. Find the cumulative (running) total of sales.

SELECT OrderID, CustomerID, Amount,
       SUM(Amount) OVER (PARTITION BY CustomerID ORDER BY OrderID) AS RunningTotal
FROM Sales;


⸻

🔴 10. What is a CTE? How is it useful?

Answer:
A CTE (Common Table Expression) provides a temporary result set that can be referenced within a SELECT, INSERT, UPDATE, or DELETE.

Example:
Get employees with above-average salary using CTE:

WITH AvgSalary AS (
    SELECT DepartmentID, AVG(Salary) AS DeptAvg
    FROM Employees
    GROUP BY DepartmentID
)
SELECT e.Name, e.Salary
FROM Employees e
JOIN AvgSalary a ON e.DepartmentID = a.DepartmentID
WHERE e.Salary > a.DeptAvg;


⸻

Let me know if you want advanced SQL case studies, window functions practice, or real-time project scenarios next!