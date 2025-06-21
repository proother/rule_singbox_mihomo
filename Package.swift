// swift-tools-version: 5.7

import PackageDescription

let package = Package(
  name: "Libbox",
  platforms: [.iOS(.v12), .macOS(.v11)],
  products: [
    .library(name: "Libbox", targets: ["Libbox"])
  ],
  targets: [
    .binaryTarget(
      name: "Libbox",
      url: "https://github.com/proother/sing-box-lib/releases/download/v1.11.14/Libbox-ios.xcframework.zip",
      checksum: "56e6627cde6060ff54f953fbffc12230ea5e5e34e514a2c24895ef7c3f98b876"
    )
  ]
)
