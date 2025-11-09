'''
You will define four classes in this project.
1. Wedding: This class represents the Wedding and handles sending out invitations, keeping track of all confirmed guests and allowing general management of the wedding operations.
2. Invitation: This class creates all the details needed for an invitation and informs us whether it has been responded to.
3. Guest: This class represents a guest being invited and enables guests to accept or decline invitations.
4. SpecialGuest: This class represents a guest who has the bonus feature of being able to invite a plus-one guest to the Wedding.

These classes will handle the management of a wedding guest system, including:
- Managing the wedding guest list and invitations (Wedding)
- Tracking invitation status and responses (Invitation)
- Handling basic guest attendance (Guest)
- Managing special guest privileges like plus-ones (SpecialGuest)

The system uses inheritance and object composition to maintain guest lists and track RSVPs. 
The Wedding class is the central coordinator, using Invitation objects to track guest status. 
In contrast, the Guest and SpecialGuest classes handle individual guest behaviors, with SpecialGuest extending Guest functionality to 
include plus-one management.
'''

from typing import List, Optional

class Wedding:
    def __init__(self, bride_name: str, groom_name: str) -> None:
        # The __init__ method initializes a new instance of the Wedding class.
        # It sets the bride's and groom's names, as well as creates empty lists
        # for confirmed guests and invitations.
        self.bride_name: str = bride_name  # Instance variable to store the bride's name.
        self.groom_name: str = groom_name  # Instance variable to store the groom's name.
        self.confirmed_guest_list: List['Guest'] = []  # List to store guests who have confirmed attendance.
        self.invitation_list: List['Invitation'] = []  # List to store all invitations sent for the wedding.
    
    def send_invitation(self, name: str, email: str, is_special: bool = False) -> None:
        # Method to send an invitation to a guest.
        # Parameters:
        # - name: The name of the guest.
        # - email: The email address of the guest.
        # - is_special: A boolean indicating if the guest is a special guest (default is False).

        if self.get_guest_by_email(email):  # Check if a guest with the same email already exists.
            return
        
        # Create a special guest or a regular guest instance based on the is_special flag.
        if is_special:
            guest: Guest = SpecialGuest(name, email, self)
        else:
            guest: Guest = Guest(name, email, self)
        
        # Create an invitation for the guest and add it to the invitation list.
        invitation: Invitation = Invitation(guest)
        self.invitation_list.append(invitation)

    def retrieve_invitation(self, email: str) -> Optional['Invitation']:
        # Method to retrieve an invitation using the guest's email address.
        # Parameters:
        # - email: The email address of the guest.
        # Returns: The Invitation object if found, otherwise None.

        for invitation in self.invitation_list:  # Iterate through all invitations.
            if invitation.guest.email == email:  # Check if the email matches.
                return invitation  # Return the matching invitation.
        return None  # Return None if no matching invitation is found.

    def get_guest_by_email(self, email: str) -> Optional['Guest']:
        # Method to retrieve a guest using their email address.
        # Parameters:
        # - email: The email address of the guest.
        # Returns: The Guest object if found, otherwise None.

        for invitation in self.invitation_list:  # Iterate through all invitations.
            if invitation.guest.email == email:  # Check if the email matches.
                return invitation.guest  # Return the matching guest.
        return None  # Return None if no matching guest is found.

class Invitation:
    def __init__(self, guest: 'Guest') -> None:
        # The __init__ method initializes a new instance of the Invitation class.
        # Parameters:
        # - guest: The Guest object for whom the invitation is created.

        self.guest: Guest = guest  # Instance variable to store the guest associated with this invitation.
        self.status: str = "pending"  # Instance variable to store the status of the invitation (default is "pending").

    def accept(self) -> None:
        # Method to mark the invitation as accepted.
        self.status = "accepted"  # Update the status to "accepted".

    def decline(self) -> None:
        # Method to mark the invitation as declined.
        self.status = "declined"  # Update the status to "declined".

class Guest:
    def __init__(self, name: str, email: str, wedding: Wedding, inviting_guest_email: Optional[str] = None) -> None:
        # The __init__ method initializes a new instance of the Guest class.
        # Parameters:
        # - name: The name of the guest.
        # - email: The email address of the guest.
        # - wedding: The Wedding object to which the guest is invited.
        # - inviting_guest_email: The email address of the guest who invited this guest (for plus-ones, default is None).

        self.name: str = name  # Instance variable to store the guest's name.
        self.email: str = email  # Instance variable to store the guest's email address.
        self.wedding: Wedding = wedding  # Instance variable to store the associated Wedding object.
        self.inviting_guest_email: Optional[str] = inviting_guest_email  # Email of the guest who invited this guest, if any.

    def accept_invitation(self) -> None:
        # Method for the guest to accept their invitation.
        invitation = self.wedding.retrieve_invitation(self.email)  # Retrieve the guest's invitation.
        if invitation:  # Check if an invitation exists.
            invitation.accept()  # Mark the invitation as accepted.
            if self not in self.wedding.confirmed_guest_list:  # If the guest is not already confirmed:
                self.wedding.confirmed_guest_list.append(self)  # Add the guest to the confirmed guest list.

    def decline_invitation(self) -> None:
        # Method for the guest to decline their invitation.
        invitation = self.wedding.retrieve_invitation(self.email)  # Retrieve the guest's invitation.
        if invitation:  # Check if an invitation exists.
            invitation.decline()  # Mark the invitation as declined.
            if self in self.wedding.confirmed_guest_list:  # If the guest is already confirmed:
                self.wedding.confirmed_guest_list.remove(self)  # Remove the guest from the confirmed guest list.

class SpecialGuest(Guest):
    def __init__(self, name: str, email: str, wedding: Wedding) -> None:
        # The __init__ method initializes a new instance of the SpecialGuest class.
        # Inherits from the Guest class and adds functionality for a plus-one.
        # Parameters:
        # - name: The name of the special guest.
        # - email: The email address of the special guest.
        # - wedding: The Wedding object to which the special guest is invited.

        super().__init__(name, email, wedding)  # Call the superclass constructor.
        self.plus_one: Optional[Guest] = None  # Instance variable to store the special guest's plus-one (default is None).

    def invite_plus_one(self, name: str, email: str) -> None:
        # Method for the special guest to invite a plus-one.
        # Parameters:
        # - name: The name of the plus-one.
        # - email: The email address of the plus-one.

        if self.plus_one:  # Check if a plus-one is already invited.
            return  # Return early if plus-one already exists
        
        if not self.wedding.get_guest_by_email(email):  # Check if the plus-one's email is not already in the wedding.
            self.plus_one = Guest(name, email, self.wedding, self.email)  # Create a new Guest object for the plus-one.
            self.wedding.send_invitation(name, email)  # Send an invitation to the plus-one.

    def uninvite_plus_one(self) -> None:
        # Method to uninvite the special guest's plus-one.
        # Parameters:
        # - self: The SpecialGuest instance.

        if self.plus_one:  # Check if a plus-one exists.
            invitation = self.wedding.retrieve_invitation(self.plus_one.email)  # Retrieve plus-one's invitation.
            self.wedding.invitation_list.remove(invitation)  # Remove invitation from wedding list.

            if self.plus_one in self.wedding.confirmed_guest_list:  # If plus-one is in confirmed list.
                self.wedding.confirmed_guest_list.remove(self.plus_one)  # Remove plus-one from confirmed list.

            self.plus_one = None  # Reset plus-one reference to None.
