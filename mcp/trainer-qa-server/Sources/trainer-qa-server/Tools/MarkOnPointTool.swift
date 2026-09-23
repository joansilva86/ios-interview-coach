import MCP

struct MarkOnPointTool {
    static let definition = Tool(
        name: ToolName.markOnPoint.rawValue,
        description: "marca una respuesta que esta bien.",
        inputSchema: .object([
            "type": .string("object"),
            "properties": .object([
                "question": .object([
                    "type": .string("string"),
                    "description": .string("The question exactly as it appears in qa_bank.csv")
                ]),
                "date": .object([
                    "type": .string("string"),
                    "description": .string("Date of the On Point answer, YYYY-MM-DD")
                ])
            ]),
            "required": .array([.string("question"), .string("date")])
        ])
    )

    @QABankActor
    static func call(arguments: [String: Value]?) async throws -> CallTool.Result {
        guard let question = arguments?["question"]?.stringValue, !question.isEmpty else {
            return errorResult("Missing required argument: question")
        }
        guard let date = arguments?["date"]?.stringValue, !date.isEmpty else {
            return errorResult("Missing required argument: date")
        }

        do {
            var rows = try QABankStore.read()
            let index = try QABankStore.findQuestionIndex(rows, question: question)
            let previous = rows[index][3]
            rows[index][3] = date
            try QABankStore.write(rows)

            let previousText = previous.isEmpty ? "first On Point" : "previous: \(previous)"
            let message = "on_point_date set to \(date) for \(rows[index][1]) (\(previousText))"
            return .init(content: [.text(text: message, annotations: nil, _meta: nil)], isError: false)
        } catch {
            return errorResult("\(error)")
        }
    }

    private static func errorResult(_ message: String) -> CallTool.Result {
        .init(content: [.text(text: message, annotations: nil, _meta: nil)], isError: true)
    }
}
