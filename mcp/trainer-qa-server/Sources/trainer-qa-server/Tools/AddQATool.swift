import MCP

struct AddQATool {
    static let definition = Tool(
        name: ToolName.addQa.rawValue,
        description: "Append a new question/answer pair to qa_bank.csv with an empty on_point_date. Refuses duplicate questions (case-insensitive).",
        inputSchema: .object([
            "type": .string("object"),
            "properties": .object([
                "category": .object([
                    "type": .string("string"),
                    "description": .string("Category, using the exact strings from topic_catalog.csv")
                ]),
                "question": .object([
                    "type": .string("string"),
                    "description": .string("The interview question")
                ]),
                "answer": .object([
                    "type": .string("string"),
                    "description": .string("Polished spoken-English model answer (empty if not written yet)")
                ])
            ]),
            "required": .array([.string("category"), .string("question")])
        ])
    )

    static func call(arguments: [String: Value]?) async throws -> CallTool.Result {
        guard let category = arguments?["category"]?.stringValue, !category.isEmpty else {
            return errorResult("Missing required argument: category")
        }
        guard let question = arguments?["question"]?.stringValue, !question.isEmpty else {
            return errorResult("Missing required argument: question")
        }
        let answer = arguments?["answer"]?.stringValue ?? ""

        do {
            var rows = try QABankStore.read()
            let folded = question.lowercased()
            if rows.dropFirst().contains(where: { $0[1].lowercased() == folded }) {
                return errorResult(
                    "Question already in qa_bank.csv: \(question). Edit the existing row instead of adding a duplicate.")
            }
            rows.append([category, question, answer, ""])
            try QABankStore.write(rows)
            let message = "Added to qa_bank.csv under \(category) (\(rows.count - 1) entries total)."
            return .init(content: [.text(text: message, annotations: nil, _meta: nil)], isError: false)
        } catch {
            return errorResult("\(error)")
        }
    }

    private static func errorResult(_ message: String) -> CallTool.Result {
        .init(content: [.text(text: message, annotations: nil, _meta: nil)], isError: true)
    }
}
