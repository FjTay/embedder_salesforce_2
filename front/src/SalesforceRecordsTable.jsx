import React from "react"

function SalesforceRecordsTable({ records }) {
  if (!records?.length) {
    return null
  }
  const columns = [...new Set(records.flatMap((row) => Object.keys(row)))]

  return (
    <div className="sf-table-wrap">
      <table className="sf-records-table">
        <thead>
          <tr>
            {columns.map((key) => (
              <th key={key}>{key}</th>
            ))}
          </tr>
        </thead>
        <tbody>
          {records.map((row, rowIndex) => (
            <tr key={row.Id ?? rowIndex}>
              {columns.map((col) => (
                <td key={col}>
                  {row[col] != null && row[col] !== "" ? String(row[col]) : "—"}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}

export default SalesforceRecordsTable
