Sub RefreshAllPivotTables()
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
    
    ' Get the last row with data in the UserInputs sheet
    lastRow = ThisWorkbook.Sheets("UserInputs").Cells(ThisWorkbook.Sheets("UserInputs").Rows.Count, "A").End(xlUp).Row
    
    ' Loop through each row in the UserInputs sheet
    For i = 2 To lastRow
        On Error GoTo ErrorHandler
        
        ' Check the status column
        status = ThisWorkbook.Sheets("UserInputs").Cells(i, 10).Value
        If status = "Successful" Then GoTo NextIteration
        
        ' Read user inputs from cells
        inputFilePath = ThisWorkbook.Sheets("UserInputs").Cells(i, 1).Value
        inputFileName = ThisWorkbook.Sheets("UserInputs").Cells(i, 2).Value
        inputSheetName = ThisWorkbook.Sheets("UserInputs").Cells(i, 3).Value
        inputPivotTableName = ThisWorkbook.Sheets("UserInputs").Cells(i, 4).Value
        dataFilePath = ThisWorkbook.Sheets("UserInputs").Cells(i, 5).Value
        dataFileName = ThisWorkbook.Sheets("UserInputs").Cells(i, 6).Value
        dataSheetName = ThisWorkbook.Sheets("UserInputs").Cells(i, 7).Value
        dataColumns = ThisWorkbook.Sheets("UserInputs").Cells(i, 8).Value
        inputCellNumber = ThisWorkbook.Sheets("UserInputs").Cells(i, 9).Value
        
        ' Open the data source file without updating links
        Set dataWB = Workbooks.Open(Filename:=dataFilePath & "\" & dataFileName, UpdateLinks:=0)
        Set dataWS = dataWB.Sheets(dataSheetName)
        
        ' Open the input file without updating links
        Set inputWB = Workbooks.Open(Filename:=inputFilePath & "\" & inputFileName, UpdateLinks:=0)
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
        ThisWorkbook.Sheets("UserInputs").Cells(i, 10).Value = "Successful"
        
        ' Continue to the next iteration
        On Error GoTo 0
        GoTo NextIteration
        
ErrorHandler:
        ' Update status to Failed
        ThisWorkbook.Sheets("UserInputs").Cells(i, 10).Value = "Failed"
        ' Continue to the next iteration
        On Error GoTo 0
        
NextIteration:
    Next i
    
    MsgBox "All pivot tables processed."
End Sub