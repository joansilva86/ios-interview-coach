import MCP

enum ToolName: String {
    case ping
    case herramientaMagica
    case markOnPoint
    case addQa
}

@main
struct TrainerQAServer {
    static func main() async throws {
        let server = Server(
            name: "trainer-qa-swift",
            version: "0.1.0",
            title: "soyPepitoServer",
            instructions: "hint para la LLM",
            capabilities: .init(tools: .init(listChanged: false)),
            configuration: .default
        )

        await server.withMethodHandler(ListTools.self) { _ in
            .init(tools: [
                PingTool.definition,
                HerramientaMagicaTool.definition,
                MarkOnPointTool.definition,
                AddQATool.definition
            ])
        }

        await server.withMethodHandler(CallTool.self) { params in
            switch ToolName(rawValue: params.name) {
            case .ping: return PingTool.call()
            case .herramientaMagica: return HerramientaMagicaTool.call()
            case .markOnPoint: return try await MarkOnPointTool.call(arguments: params.arguments)
            case .addQa: return try await AddQATool.call(arguments: params.arguments)
            case nil:
                return .init(content: [.text(text: "Unknown tool: \(params.name)", annotations: nil, _meta: nil)], isError: true)
            }
        }

        try await server.start(transport: StdioTransport())
        await server.waitUntilCompleted()
    }
}
