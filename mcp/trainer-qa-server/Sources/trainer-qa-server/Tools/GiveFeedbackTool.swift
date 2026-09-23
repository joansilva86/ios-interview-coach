import MCP
import Foundation

struct GiveFeedbackTool {
    static let definition = Tool(
        name: ToolName.giveFeedback.rawValue,
        description: "Counts today's qa_bank.csv activity: how many rows have on_point_date set to today, and how many rows currently have asked_flag set (asked this session).",
        inputSchema: .object([
            "type": .string("object"),
            "properties": .object([:])
        ])
    )

    @QABankActor
    static func call() async throws -> CallTool.Result {
        do {
            let rows = try QABankStore.read()
            let dataRows = rows.dropFirst()

            let formatter = DateFormatter()
            formatter.dateFormat = "yyyy-MM-dd"
            formatter.timeZone = TimeZone.current
            let today = formatter.string(from: Date())

            let onPointToday = dataRows.filter { $0[3] == today }.count
            let asked = dataRows.filter { !$0[4].isEmpty }.count

            let message = "On Point today (\(today)): \(onPointToday)\nMarked as asked (asked_flag set): \(asked)"
            return .init(content: [.text(text: message, annotations: nil, _meta: nil)], isError: false)
        } catch {
            return errorResult("\(error)")
        }
    }

    private static func errorResult(_ message: String) -> CallTool.Result {
        .init(content: [.text(text: message, annotations: nil, _meta: nil)], isError: true)
    }
}
