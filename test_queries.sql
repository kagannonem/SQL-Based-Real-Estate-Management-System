SELECT 
    subordinate.AgentName AS [Employee Name],
    subordinate.Level AS [Employee Level],
    manager.AgentName AS [Reports To Manager],
    manager.Level AS [Manager Level]
FROM Agents subordinate
LEFT JOIN Agents manager ON subordinate.ManagerID = manager.AgentID;