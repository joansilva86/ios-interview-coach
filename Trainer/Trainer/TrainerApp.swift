import SwiftUI
import Observation

@main
struct TrainerApp: App {
    var body: some Scene {
        WindowGroup {
            ContentView()
        }
    }
}

  struct Settings: Decodable {
      let theme: String
      let fontSize: Int
  }

  enum StorageError: Error {
      case fileMissing(name: String)
  }

  enum SettingsError: Error {
      case storage(StorageError)   // wraps the lower-level error
      case corruptData
  }

let disk: [String: Data] = [
    "settings.json": #"{"theme":"dark","fontSize":14}"#.data(using: .utf8)!,
    "broken.json":   #"{"theme":"dark""#.data(using: .utf8)!   // invalid JSON
]

final class ViewModel {
    func readFile(named name: String) throws(StorageError) -> Data {
        let data = disk[name]
        guard let data else {
            throw StorageError.fileMissing(name: name)
        }
        return data
    }
    
    func loadData(named name: String) -> Result<Data, SettingsError> {
        Result { try readFile(named: name) }
            .mapError { SettingsError.storage($0 as! StorageError) }
    }
    
    func decodeSettings(_ s: Data) -> Result<Settings,SettingsError> {
        return Result{ try JSONDecoder().decode(Settings.self, from: s) }
            .mapError{ _ in SettingsError.corruptData }
    }
    
    // TODO: implement this
//    func loadSettings(named name: String) -> Result<Settings, SettingsError> {
//        let json = loadData(named: name)
//            .map{ decodeSettings($0) }
//            
//    }
}
