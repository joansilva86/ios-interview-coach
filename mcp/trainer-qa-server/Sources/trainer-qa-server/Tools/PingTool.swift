import MCP

struct PingTool {
    static let definition = Tool(
        name: ToolName.ping.rawValue,
        description: "Connectivity check: replies with pong.",
        inputSchema: .object(["type": .string("object"), "properties": .object([:])])
    )

    static func call() -> CallTool.Result {
        .init(content: [.text(text: "pong", annotations: nil, _meta: nil)], isError: false)
    }
}
