import MCP

struct HerramientaMagicaTool {
    static let definition = Tool(
        name: ToolName.herramientaMagica.rawValue,
        description: "Devuelve un resultado mágico de prueba.",
        inputSchema: .object(["type": .string("object"), "properties": .object([:])])
    )

    static func call() -> CallTool.Result {
        .init(content: [.text(text: "✨ magia ✨", annotations: nil, _meta: nil)], isError: false)
    }
}
