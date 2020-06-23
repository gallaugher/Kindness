//
//  UserViewController.swift
//  Kindness
//
//  Created by John Gallaugher on 6/22/20.
//  Copyright © 2020 John Gallaugher. All rights reserved.
//

import UIKit
import FirebaseUI

class ProfileViewController: UIViewController {
    @IBOutlet weak var aboutTextView: UITextView!
    @IBOutlet weak var tableView: UITableView!
    @IBOutlet weak var emailTextField: UITextField!
    @IBOutlet weak var profileTextField: UITextField!
    @IBOutlet weak var descriptionTextView: UITextView!
    @IBOutlet weak var photoImageView: UIImageView!
    
    var authUI: FUIAuth!
    var kindUser: KindUser!
    var topics: [String] = [] // user.uID, used to identify a device
    
    override func viewDidLoad() {
        super.viewDidLoad()
        authUI = FUIAuth.defaultAuthUI()
        tableView.delegate = self
        tableView.dataSource = self
        
        guard let user = authUI.auth?.currentUser else {
            print("😡 ERROR: No user!")
            return
        }
        configureUserInterface(user: user)
        self.navigationItem.title = "Profile"
    }
    
    override func viewDidAppear(_ animated: Bool) {
        super.viewDidAppear(animated)
        self.navigationItem.title = "Profile"
        self.navigationItem.titleView?.largeContentTitle = "Profile"
    }
    
    func configureUserInterface(user: User) {
        emailTextField.text = user.email
        profileTextField.text = user.displayName
        topics.append(user.uid)
        tableView.reloadData()
    }
    
}

extension ProfileViewController: UITableViewDelegate, UITableViewDataSource {
    func tableView(_ tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
        return topics.count
    }
    
    func tableView(_ tableView: UITableView, cellForRowAt indexPath: IndexPath) -> UITableViewCell {
        let cell = tableView.dequeueReusableCell(withIdentifier: "Cell", for: indexPath)
        cell.textLabel?.text = topics[indexPath.row]
        return cell
    }
    
    func tableView(_ tableView: UITableView, didSelectRowAt indexPath: IndexPath) {
        let pasteboard = UIPasteboard.general
        pasteboard.string = topics[indexPath.row]
        
        // animate selection
        let cell = tableView.cellForRow(at: indexPath)!
        cell.textLabel?.alpha = 0.0
        UIView.animate(withDuration: 1.0, animations: { cell.textLabel!.alpha = 1.0 })
    }
    
}
