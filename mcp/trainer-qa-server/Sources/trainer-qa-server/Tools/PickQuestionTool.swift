import MCP

struct PickQuestionTool {
    static let definition = Tool(
        name: ToolName.pickQuestion.rawValue,
        description: "Pick a review question from qa_bank.csv: only considers rows that already have an answer, a non-empty on_point_date, and no asked_flag set. Returns the one with the oldest on_point_date and sets its asked_flag so it won't be picked again until clearSession runs.",
        inputSchema: .object([
            "type": .string("object"),
            "properties": .object([:])
        ])
    )

    static func call() async throws -> CallTool.Result {
        do {
            var rows = try QABankStore.read()
            let eligible = rows.enumerated().dropFirst().filter { _, row in
                !row[2].isEmpty && !row[3].isEmpty && row[4].isEmpty
            }
            guard let (pickedIndex, picked) = eligible.min(by: { $0.element[3] < $1.element[3] }) else {
                return errorResult(
                    "No eligible questions in qa_bank.csv (need an answer, an on_point_date, and no asked_flag — run clearSession to reset).")
            }
            let category = picked[0]
            let question = picked[1]
            let answer = picked[2]
            let onPointDate = picked[3]

            rows[pickedIndex][4] = "1"
            try QABankStore.write(rows)

            let message = "[\(category)] \(question)\n(last On Point: \(onPointDate))\nModel answer: \(answer)"
            return .init(content: [.text(text: message, annotations: nil, _meta: nil)], isError: false)
        } catch {
            return errorResult("\(error)")
        }
    }

    private static func errorResult(_ message: String) -> CallTool.Result {
        .init(content: [.text(text: message, annotations: nil, _meta: nil)], isError: true)
    }
}
