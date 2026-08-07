//
//  TrainerTests.swift
//  TrainerTests
//
//  Created by Erick Silva on 03/08/2026.
//

import Testing
@testable import Trainer

struct TrainerTests {

    @Test
    func example() async throws {
        var arrays = [1,2,3,4]
        var newArray = arrays.remove(at: 1)
        //#expect(arrays==newArray)
    }
}
