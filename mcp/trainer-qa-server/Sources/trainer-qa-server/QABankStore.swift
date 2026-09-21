import Foundation

enum QABankError: Error, CustomStringConvertible {
    case malformedFile(String)
    case questionNotFound(String)

    var description: String {
        switch self {
        case .malformedFile(let message):
            return message
        case .questionNotFound(let question):
            return "Question not found in qa_bank.csv: \(question)"
        }
    }
}

struct QABankStore {
    static let header = ["category", "question", "answer", "on_point_date"]
    static let fileURL = URL(fileURLWithPath: "qa_bank.csv")

    static func read() throws -> [[String]] {
        guard FileManager.default.fileExists(atPath: fileURL.path) else {
            return [header]
        }
        let content = try String(contentsOf: fileURL, encoding: .utf8)
        let rows = parseCSV(content)
        guard let first = rows.first, first == header else {
            throw QABankError.malformedFile(
                "qa_bank.csv is malformed (expected header: \(header.joined(separator: ","))).")
        }
        return rows
    }

    static func write(_ rows: [[String]]) throws {
        let content = rows.map { row in row.map(escapeField).joined(separator: ",") }
            .joined(separator: "\n") + "\n"
        let tmpURL = fileURL.deletingLastPathComponent()
            .appendingPathComponent(".qa_bank.csv.\(UUID().uuidString).tmp")
        try content.write(to: tmpURL, atomically: false, encoding: .utf8)
        _ = try FileManager.default.replaceItemAt(fileURL, withItemAt: tmpURL)
    }

    static func findQuestionIndex(_ rows: [[String]], question: String) throws -> Int {
        let dataRows = rows.dropFirst()
        if let index = dataRows.firstIndex(where: { $0[1] == question }) {
            return index
        }
        let folded = question.lowercased()
        if let index = dataRows.firstIndex(where: { $0[1].lowercased() == folded }) {
            return index
        }
        throw QABankError.questionNotFound(question)
    }
}

private func escapeField(_ field: String) -> String {
    if field.contains(",") || field.contains("\"") || field.contains("\n") {
        return "\"" + field.replacingOccurrences(of: "\"", with: "\"\"") + "\""
    }
    return field
}

private func parseCSV(_ content: String) -> [[String]] {
    var rows: [[String]] = []
    var currentRow: [String] = []
    var currentField = ""
    var insideQuotes = false
    let chars = Array(content)
    var i = 0
    while i < chars.count {
        let c = chars[i]
        if insideQuotes {
            if c == "\"" {
                if i + 1 < chars.count, chars[i + 1] == "\"" {
                    currentField.append("\"")
                    i += 1
                } else {
                    insideQuotes = false
                }
            } else {
                currentField.append(c)
            }
        } else if c == "\"" {
            insideQuotes = true
        } else if c == "," {
            currentRow.append(currentField)
            currentField = ""
        } else if c == "\n" {
            currentRow.append(currentField)
            rows.append(currentRow)
            currentRow = []
            currentField = ""
        } else if c != "\r" {
            currentField.append(c)
        }
        i += 1
    }
    if !currentField.isEmpty || !currentRow.isEmpty {
        currentRow.append(currentField)
        rows.append(currentRow)
    }
    return rows
}
