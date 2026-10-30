"""Simple Contact Manager (list + dict + JSON file)."""

import json
import os

FILE = "contacts.json"


# ---------- Storage ----------

def load_contacts():
    """Read contacts from the JSON file. Return [] if missing or broken."""
    if not os.path.exists(FILE):
        return []
    try:
        with open(FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data if isinstance(data, list) else []
    except json.JSONDecodeError:
        print("Warning: contacts file is corrupted. Starting with an empty list.")
        return []


def save_contacts(contacts):
    """Write all contacts to the JSON file."""
    with open(FILE, "w", encoding="utf-8") as f:
        json.dump(contacts, f, ensure_ascii=False, indent=2)


# ---------- Helpers ----------

def print_contact(c, index=None):
    prefix = f"{index}. " if index is not None else ""
    print(f"{prefix}{c['name']} | {c['phone']} | {c['email']}")


def ask_number(prompt, max_value):
    """Ask for a number between 1 and max_value. Return index (0-based) or None."""
    try:
        n = int(input(prompt))
    except ValueError:
        print("Please enter a number.")
        return None
    if not 1 <= n <= max_value:
        print("Number out of range.")
        return None
    return n - 1


def is_valid_phone(phone):
    cleaned = phone.replace(" ", "").replace("-", "").replace("+", "")
    return cleaned.isdigit() and len(cleaned) >= 8


def phone_exists(contacts, phone, skip=None):
    return any(c["phone"] == phone and c is not skip for c in contacts)


# ---------- Features ----------

def add_contact(contacts):
    name = input("Name: ").strip()
    if not name:
        print("Name cannot be empty.")
        return

    phone = input("Phone: ").strip()
    if not is_valid_phone(phone):
        print("Invalid phone number (digits only, at least 8).")
        return
    if phone_exists(contacts, phone):
        print("A contact with this phone number already exists.")
        return

    email = input("Email (optional): ").strip()

    contacts.append({"name": name, "phone": phone, "email": email})
    save_contacts(contacts)
    print("Contact added!")


def list_contacts(contacts):
    if not contacts:
        print("No contacts yet.")
        return
    print("\n--- All contacts ---")
    for i, c in enumerate(sorted_view(contacts), start=1):
        print_contact(c, i)


def sorted_view(contacts):
    """Keep the stored order stable; just return the list as is."""
    return contacts


def search_contacts(contacts):
    keyword = input("Search by name or phone: ").strip().lower()
    if not keyword:
        print("Please type something to search.")
        return
    found = [
        c for c in contacts
        if keyword in c["name"].lower() or keyword in c["phone"]
    ]
    if not found:
        print("Not found.")
        return
    print(f"\nFound {len(found)} result(s):")
    for c in found:
        print_contact(c)


def edit_contact(contacts):
    if not contacts:
        print("No contacts to edit.")
        return
    list_contacts(contacts)
    idx = ask_number("Number to edit: ", len(contacts))
    if idx is None:
        return

    c = contacts[idx]
    print("Press Enter to keep the current value.")

    new_name = input(f"Name [{c['name']}]: ").strip()
    new_phone = input(f"Phone [{c['phone']}]: ").strip()
    new_email = input(f"Email [{c['email']}]: ").strip()

    if new_phone:
        if not is_valid_phone(new_phone):
            print("Invalid phone number. Nothing changed.")
            return
        if phone_exists(contacts, new_phone, skip=c):
            print("Another contact already uses this phone. Nothing changed.")
            return
        c["phone"] = new_phone
    if new_name:
        c["name"] = new_name
    if new_email:
        c["email"] = new_email

    save_contacts(contacts)
    print("Contact updated!")


def delete_contact(contacts):
    if not contacts:
        print("No contacts to delete.")
        return
    list_contacts(contacts)
    idx = ask_number("Number to delete: ", len(contacts))
    if idx is None:
        return

    confirm = input(f"Delete '{contacts[idx]['name']}'? (y/n): ").strip().lower()
    if confirm != "y":
        print("Cancelled.")
        return

    removed = contacts.pop(idx)
    save_contacts(contacts)
    print(f"Deleted {removed['name']}.")


def sort_contacts(contacts):
    contacts.sort(key=lambda c: c["name"].lower())
    save_contacts(contacts)
    print("Contacts sorted by name.")


# ---------- Main ----------

MENU = """
===== CONTACT MANAGER =====
1. Add contact
2. List contacts
3. Search
4. Edit
5. Delete
6. Sort by name
0. Exit"""


def main():
    contacts = load_contacts()
    actions = {
        "1": add_contact,
        "2": list_contacts,
        "3": search_contacts,
        "4": edit_contact,
        "5": delete_contact,
        "6": sort_contacts,
    }

    while True:
        print(MENU)
        choice = input("Choose: ").strip()
        if choice == "0":
            print("Goodbye!")
            break
        action = actions.get(choice)
        if action:
            action(contacts)
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()
