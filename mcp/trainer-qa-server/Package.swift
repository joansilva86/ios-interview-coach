// swift-tools-version: 6.0

import PackageDescription

let package = Package(
    name: "trainer-qa-server",
    platforms: [.macOS(.v13)],
    dependencies: [
        .package(url: "https://github.com/modelcontextprotocol/swift-sdk.git", from: "0.11.0")
    ],
    targets: [
        .executableTarget(
            name: "trainer-qa-server",
            dependencies: [.product(name: "MCP", package: "swift-sdk")]
        )
    ],
    swiftLanguageModes: [.v6]
)
