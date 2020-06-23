//
//  KindUsers.swift
//  Kindness
//
//  Created by John Gallaugher on 6/22/20.
//  Copyright © 2020 John Gallaugher. All rights reserved.
//

import Foundation
import Firebase

class KindUsers {
    var kindUserArray = [KindUser]()
    var db: Firestore!
    
    init() {
        db = Firestore.firestore()
    }
    
    func loadData(completed: @escaping () -> ())  {
        db.collection("users").addSnapshotListener { (querySnapshot, error) in
            guard error == nil else {
                print("*** ERROR: adding the snapshot listener \(error!.localizedDescription)")
                return completed()
            }
            self.kindUserArray = []
            // there are querySnapshot!.documents.count documents in teh spots snapshot
            for document in querySnapshot!.documents {
                let kindUser = KindUser(dictionary: document.data())
                kindUser.documentID = document.documentID
                self.kindUserArray.append(kindUser)
            }
            completed()
        }
    }
}
