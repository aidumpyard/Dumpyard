Dim macroRunning As Boolean

Sub RefreshAllPivotTables()
    If macroRunning Then
        MsgBox "The macro is already running."
        Exit Sub
    End If
    
    macroRunning = True
    Dim ws As Worksheet
    Dim dataWS As Worksheet
    Dim inputFilePath As String
    Dim inputFileName As String
    Dim inputSheetName As String
    Dim inputPivotTableName As String
    Dim dataFilePath As String
    Dim dataFileName As String
    Dim dataSheetName As String
    Dim dataColumns As String
    Dim inputCellNumber As String
    Dim inputWB As Workbook
    Dim dataWB As Workbook
    Dim pivotTable As PivotTable
    Dim pivotCache As PivotCache
    Dim lastRow As Long
    Dim i As Long
    Dim status As String
    Dim userInputSheetName As String
    Dim startTime As Double
    Dim endTime As Double
    Dim totalTime As Double
    Dim completedRows As Long
    Dim percentageComplete As Double
    Dim errorMessage As String
    
    ' Start timer
    startTime = Timer
    
    ' Read the input sheet name from the Summary sheet
    userInputSheetName = ThisWorkbook.Sheets("Summary").Range("D2").Value
    
    ' Get the last row with data in the UserInputs sheet
    lastRow = ThisWorkbook.Sheets(userInputSheetName).Cells(ThisWorkbook.Sheets(userInputSheetName).Rows.Count, "A").End(xlUp).Row
    
    ' Disable screen updating to keep the process in the background
    Application.ScreenUpdating = False
    Application.DisplayAlerts = False
    
    ' Initialize completed rows counter
    completedRows = 0
    
    ' Loop through each row in the UserInputs sheet
    For i = 2 To lastRow
        On Error GoTo ErrorHandler
        
        ' Check the status column
        status = ThisWorkbook.Sheets(userInputSheetName).Cells(i, 10).Value
        If status = "Successful" Then
            completedRows = completedRows + 1
            GoTo NextIteration
        End If
        
        ' Read user inputs from cells
        inputFilePath = ThisWorkbook.Sheets(userInputSheetName).Cells(i, 1).Value
        inputFileName = ThisWorkbook.Sheets(userInputSheetName).Cells(i, 2).Value
        inputSheetName = ThisWorkbook.Sheets(userInputSheetName).Cells(i, 3).Value
        inputPivotTableName = ThisWorkbook.Sheets(userInputSheetName).Cells(i, 4).Value
        dataFilePath = ThisWorkbook.Sheets(userInputSheetName).Cells(i, 5).Value
        dataFileName = ThisWorkbook.Sheets(userInputSheetName).Cells(i, 6).Value
        dataSheetName = ThisWorkbook.Sheets(userInputSheetName).Cells(i, 7).Value
        dataColumns = ThisWorkbook.Sheets(userInputSheetName).Cells(i, 8).Value
        inputCellNumber = ThisWorkbook.Sheets(userInputSheetName).Cells(i, 9).Value
        
        ' Open the data source file without updating links and keep it invisible
        Set dataWB = Workbooks.Open(Filename:=dataFilePath & "\" & dataFileName, UpdateLinks:=0)
        dataWB.Windows(1).Visible = False
        Set dataWS = dataWB.Sheets(dataSheetName)
        
        ' Open the input file without updating links and keep it invisible
        Set inputWB = Workbooks.Open(Filename:=inputFilePath & "\" & inputFileName, UpdateLinks:=0)
        inputWB.Windows(1).Visible = False
        Set ws = inputWB.Sheets(inputSheetName)
        
        ' Find the pivot table
        Set pivotTable = ws.PivotTables(inputPivotTableName)
        
        ' Update the pivot cache with the new data range
        Set pivotCache = inputWB.PivotCaches.Create( _
            SourceType:=xlDatabase, _
            SourceData:=dataWS.Range(dataColumns).Address(External:=True))
        
        ' Update the pivot table with the new cache
        pivotTable.ChangePivotCache pivotCache
        
        ' Refresh the pivot table
        pivotTable.RefreshTable
        
        ' Save the data file path and name in the specified cell
        ws.Range(inputCellNumber).Value = dataFilePath & "\" & dataFileName
        
        ' Save and close workbooks
        inputWB.Close SaveChanges:=True
        dataWB.Close SaveChanges:=False
        
        ' Update status to Successful
        ThisWorkbook.Sheets(userInputSheetName).Cells(i, 10).Value = "Successful"
        
        ' Increment completed rows counter
        completedRows = completedRows + 1
        
        ' Update percentage complete in the Summary sheet
        percentageComplete = (completedRows / (lastRow - 1)) * 100
        ThisWorkbook.Sheets("Summary").Range("C9").Value = percentageComplete & "%"
        
        ' Continue to the next iteration
        On Error GoTo 0
        GoTo NextIteration
        
ErrorHandler:
        ' Update status to Failed
        ThisWorkbook.Sheets(userInputSheetName).Cells(i, 10).Value = "Failed"
        ' Update error message
        errorMessage = Err.Description
        ThisWorkbook.Sheets(userInputSheetName).Cells(i, 11).Value = errorMessage
        ' Continue to the next iteration
        On Error GoTo 0
        
NextIteration:
    Next i
    
    ' End timer and calculate total time taken
    endTime = Timer
    totalTime = endTime - startTime
    ThisWorkbook.Sheets("Summary").Range("C10").Value = Format(totalTime, "0.00") & " seconds"
    
    ' Re-enable screen updating and display alerts
    Application.ScreenUpdating = True
    Application.DisplayAlerts = True
    
    MsgBox "All pivot tables processed."
    
    macroRunning = False
End Sub