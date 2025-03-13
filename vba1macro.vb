Sub EmbedMsgFiles()
    Dim ws As Worksheet
    Dim cell As Range
    Dim objOLE As OLEObject
    Dim lastRow As Integer
    Dim filePath As String
    
    ' Set the worksheet
    Set ws = ThisWorkbook.Sheets("Sheet2")
    
    ' Find the last row in the Approval column (assuming it's column G)
    lastRow = ws.Cells(ws.Rows.Count, "G").End(xlUp).Row
    
    ' Loop through each cell in the Approval column
    For Each cell In ws.Range("G2:G" & lastRow) ' Assuming G is the Approval column
        filePath = cell.Value
        
        ' Check if the file exists
        If Dir(filePath) <> "" Then
            ' Insert the file as an embedded object
            Set objOLE = ws.OLEObjects.Add(ClassType:="Package", _
                                           FileName:=filePath, _
                                           Link:=False, _
                                           DisplayAsIcon:=True)
            
            ' Move the embedded object to the cell
            objOLE.Top = cell.Top
            objOLE.Left = cell.Left
            objOLE.Width = cell.Width
            objOLE.Height = cell.Height
        End If
    Next cell
    
    MsgBox "All .msg files embedded successfully!", vbInformation
End Sub