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
    @IBOutlet weak var tableView: UITableView!
    @IBOutlet weak var emailLabel: UILabel!
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
        if kindUser == nil {
            kindUser = KindUser(user: user)
        }
        kindUser.loadData {
            self.updateUserInterface()
        }
    }
    
    override func viewDidAppear(_ animated: Bool) {
        super.viewDidAppear(animated)
        self.navigationItem.title = "Profile"
        self.navigationItem.titleView?.largeContentTitle = "Profile"
    }
    
    func updateUserInterface() {
        emailLabel.text = kindUser.email
        profileTextField.text = kindUser.displayName
        descriptionTextView.text = kindUser.description
        topics.append(kindUser.documentID)
        tableView.reloadData()
    }
    
    func updateFromInterface() {
        kindUser.displayName = profileTextField.text!
        kindUser.description = descriptionTextView.text!
    }
    
    func leaveViewController() {
        let isPresentingInAddMode = presentingViewController is UINavigationController
        if isPresentingInAddMode {
            dismiss(animated: true, completion: nil)
        } else {
            navigationController?.popViewController(animated: true)
        }
    }
    
    @IBAction func saveButtonPressed(_ sender: UIBarButtonItem) {
        updateFromInterface()
        kindUser.saveData { (success) in
            if success {
                self.leaveViewController()
            } else {
                self.oneButtonAlert(title: "Save Failed", message: "For some reason, the data would not save to the cloud.")
            }
        }
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
