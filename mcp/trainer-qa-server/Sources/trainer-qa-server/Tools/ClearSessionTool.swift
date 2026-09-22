import MCP

struct ClearSessionTool {
    static let definition = Tool(
        name: ToolName.clearSession.rawValue,
        description: "Clear the asked_flag on every row in qa_bank.csv, making all questions eligible for pickQuestion again.",
        inputSchema: .object([
            "type": .string("object"),
            "properties": .object([:])
        ])
    )

    static func call() async throws -> CallTool.Result {
        do {
            var rows = try QABankStore.read()
            var cleared = 0
            for i in 1..<rows.count where !rows[i][4].isEmpty {
                rows[i][4] = ""
                cleared += 1
            }
            try QABankStore.write(rows)
            let message = "Session cleared: \(cleared) asked_flag(s) reset."
            return .init(content: [.text(text: message, annotations: nil, _meta: nil)], isError: false)
        } catch {
            return errorResult("\(error)")
        }
    }

    private static func errorResult(_ message: String) -> CallTool.Result {
        .init(content: [.text(text: message, annotations: nil, _meta: nil)], isError: true)
    }
}
