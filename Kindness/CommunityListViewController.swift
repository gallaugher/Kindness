//
//  CommunityListViewController.swift
//  Kindness
//
//  Created by John Gallaugher on 6/22/20.
//  Copyright © 2020 John Gallaugher. All rights reserved.
//

import UIKit
import CocoaMQTT

class CommunityListViewController: UIViewController {
    @IBOutlet weak var tableView: UITableView!
    
    var userID = ""
    
    var users: KindUsers!
    var mqttclient = CocoaMQTT(clientID: "kindness/itpcamp", host: "broker.shiftr.io", port: 1883)
    
    override func viewDidLoad() {
        super.viewDidLoad()
        users = KindUsers()
        tableView.delegate = self
        tableView.dataSource = self
        mqttclient.username = "kind-one"
        mqttclient.password = "8e0e6b8813973531"
        mqttclient.connect()
    }
    
    override func viewDidAppear(_ animated: Bool) {
        super.viewDidAppear(animated)        
        users.loadData {
            self.tableView.reloadData()
        }
    }
}

extension CommunityListViewController: UITableViewDelegate, UITableViewDataSource {
    func tableView(_ tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
        return users.kindUserArray.count
    }
    
    func tableView(_ tableView: UITableView, cellForRowAt indexPath: IndexPath) -> UITableViewCell {
        let cell = tableView.dequeueReusableCell(withIdentifier: "Cell", for: indexPath)
        cell.textLabel?.text = users.kindUserArray[indexPath.row].displayName
        return cell
    }
    
    func tableView(_ tableView: UITableView, didSelectRowAt indexPath: IndexPath) {
        let uID = users.kindUserArray[indexPath.row].documentID
        mqttclient.publish(uID, withString: "message from iOS app")
        let cell = tableView.cellForRow(at: indexPath)!
        cell.textLabel?.alpha = 0.0
        UIView.animate(withDuration: 1.0, animations: { cell.textLabel!.alpha = 1.0 })
    }
    
//    func tableView(_ tableView: UITableView, heightForRowAt indexPath: IndexPath) -> CGFloat {
//        return 50
//    }
}
