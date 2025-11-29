from flask import Flask, render_template, request, redirect, url_for, flash, session
from backend.folder_locker import lock_folder, unlock_folder, list_locked_folders
from backend.notes_manager import count_notes
from backend.vault_manager import save_entry, list_entries, count_vault_entries, update_entry
from config import SECRET_KEY
from backend.login_manager import (
    is_master_set,
    create_master_passkey,
    verify_master_passkey,
    login_required,
)
from backend.notes_manager import (
    save_note,
    list_notes,
    load_note_content,
    update_note,
)



app = Flask(__name__, template_folder="templates", static_folder="static")
app.secret_key = SECRET_KEY
app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"


# ---------------------------
# Inject global master key flag
# ---------------------------
@app.context_processor
def inject_master_flag():
    return {"master_set": is_master_set()}


# ---------------------------
# Landing page
# ---------------------------
@app.route("/", endpoint="Landing")
def Landing():
    return render_template("Landing.html")


# ---------------------------
# Setup master key
# ---------------------------
@app.route("/setup", methods=["GET", "POST"], endpoint="CreatePasskey")
def CreatePasskey():
    if is_master_set():
        flash("Master passkey already created — please login.")
        return redirect(url_for("Login"))

    if request.method == "POST":
        p1 = request.form.get("pass1", "")
        p2 = request.form.get("pass2", "")
        if not p1 or p1 != p2:
            flash("Passkeys empty or do not match.")
            return redirect(url_for("CreatePasskey"))

        create_master_passkey(p1)
        flash("Master passkey created. Please log in.")
        return redirect(url_for("Login"))

    return render_template("CreatePasskey.html")


# ---------------------------
# Login
# ---------------------------
@app.route("/login", methods=["GET", "POST"], endpoint="Login")
def Login():
    if request.method == "POST":
        passphrase = request.form.get("pass", "")
        if verify_master_passkey(passphrase):
            session.clear()
            session["authenticated"] = True
            flash("Login successful.")
            return redirect(url_for("dashboard"))
        else:
            flash("Invalid passkey.")
            return redirect(url_for("Login"))
    return render_template("Login.html")


# ---------------------------
# Logout
# ---------------------------
@app.route("/logout", endpoint="Logout")
def Logout():
    session.clear()
    flash("Logged out.")
    return redirect(url_for("Landing"))


# ---------------------------
# Dashboard
# ---------------------------
@app.route("/dashboard")
@login_required
def dashboard():
    locked_folders = list_locked_folders()
    notes_count = count_notes()

    stats = {
        "locked_folders": sum(1 for f in locked_folders if f["status"] == "Locked"),
       "vault_entries": count_vault_entries(),
        "notes": notes_count,
    }

    return render_template("dashboard.html", stats=stats)

# ---------------------------
# Folder Locker
# ---------------------------
@app.route("/folder-locker", methods=["GET", "POST"], endpoint="FolderLocker")
@login_required
def FolderLocker():
    message = None
    if request.method == "POST":
        folder_path = request.form.get("folder_path", "").strip()
        action = request.form.get("action", "")

        if not folder_path:
            flash("Folder path is required.")
            return redirect(url_for("FolderLocker"))

        if action == "lock":
            success, message = lock_folder(folder_path)
        elif action == "unlock":
            success, message = unlock_folder(folder_path)
        else:
            message = "Invalid action."

        flash(message)

    folders = list_locked_folders()
    return render_template("FolderLocker.html", folders=folders, message=message)

# ---------------------------
# Notes Home
# ---------------------------
@app.route("/notes", methods=["GET"], endpoint="notes_home")
@login_required
def notes_home():
    notes = list_notes()
    return render_template(
        "NotesManager.html",
        notes=notes,
        active_note=None,
        title="",
        content="",
        new=False,
        show_key_prompt=False,
    )


# ---------------------------
# Open a note
# ---------------------------
@app.route("/notes/open/<filename>", methods=["GET", "POST"], endpoint="open_note")
@login_required
def open_note(filename):
    notes = list_notes()

    if request.method == "POST":
        key = request.form.get("key", "")
        title, content = load_note_content(filename, key)

        if title is None:
            flash("Invalid key or decryption failed.")
            return redirect(url_for("notes_home"))

        return render_template(
            "NotesManager.html",
            notes=notes,
            active_note=filename,
            title=title,
            content=content,
            editable=False,
            current_key=key,
            show_key_prompt=False,
        )
    return render_template(
        "NotesManager.html",
        notes=notes,
        active_note=filename,
        show_key_prompt=True,
        key_prompt_for=filename,
    )


# ---------------------------
# Edit and save note
# ---------------------------
@app.route("/notes/edit/<filename>", methods=["POST"], endpoint="edit_note")
@login_required
def edit_note(filename):
    current_key = request.form.get("current_key", "")
    new_title = request.form.get("title", "")
    new_content = request.form.get("content", "")

    try:
        new_key = update_note(filename, current_key, new_title, new_content)
    except ValueError:
        flash("Current key incorrect. Could not save.")
        return redirect(url_for("open_note", filename=filename))
    except Exception as e:
        flash(f"Error saving note: {e}")
        return redirect(url_for("open_note", filename=filename))

    flash(f"Note updated and re-encrypted with a new key: {new_key}")
    return redirect(url_for("notes_home"))


# ---------------------------
# Create new note
# ---------------------------
@app.route("/notes/new", methods=["GET", "POST"], endpoint="create_new_note")
@login_required
def create_new_note():
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        content = request.form.get("content", "").strip()

        if not title or not content:
            flash("Title and content required.")
            return redirect(url_for("create_new_note"))

        file_name, key = save_note(title, content)
        flash(f"Note created and encrypted successfully. File: {file_name}, Key: {key}")
        return redirect(url_for("notes_home"))

    notes = list_notes()
    return render_template(
        "NotesManager.html",
        notes=notes,
        new=True,
        active_note=None,
        title="",
        content="",
        editable=True,
        show_key_prompt=False,
    )
# ---------------------------
# Password Vault Page
# ---------------------------
@app.route("/password-vault", methods=["GET", "POST"])
@login_required
def password_vault():
    """Password Vault — Add and View Passwords."""
    if request.method == "POST":
        website = request.form.get("website", "").strip()
        name = request.form.get("name", "").strip()
        contact = request.form.get("contact", "").strip()
        password = request.form.get("password", "").strip()
        category = request.form.get("category", "Other")

        if not website or not password:
            flash("⚠️ Website and Password fields are required.")
            return redirect(url_for("password_vault"))

        success, message = save_entry(website, name, contact, password, category)
        flash(message)
        return redirect(url_for("password_vault"))

    # GET — list all vault entries
    vault_entries = list_entries()
    return render_template("PasswordVault.html", vault_entries=vault_entries)


@app.route("/vault", methods=["GET"], endpoint="PasswordVault")
@login_required
def PasswordVault():
    """Display all saved encrypted passwords."""
    entries = list_entries()
    return render_template("PasswordVault.html", vault_entries=entries)


@app.route("/vault/add", methods=["POST"], endpoint="AddVaultEntry")
@login_required
def AddVaultEntry():
    """Handle new password form submission."""
    website = request.form.get("website", "").strip()
    name = request.form.get("name", "").strip()
    contact = request.form.get("contact", "").strip()
    password = request.form.get("password", "").strip()
    category = request.form.get("category", "Other")

    if not (website and name and password):
        flash("Website, Name, and Password are required.")
        return redirect(url_for("PasswordVault"))

    success, msg = save_entry(website, name, contact, password, category)
    flash(msg)
    return redirect(url_for("PasswordVault"))

# ---------------------------
# Edit Vault Entry
# ---------------------------
@app.route("/password-vault/edit/<int:entry_id>", methods=["POST"])
@login_required
def edit_vault_entry(entry_id):
    """Update an existing password entry."""
    website = request.form.get("website", "").strip()
    name = request.form.get("name", "").strip()
    contact = request.form.get("contact", "").strip()
    password = request.form.get("password", "").strip()
    category = request.form.get("category", "Other")

    success, msg = update_entry(entry_id, website, name, contact, password, category)
    flash(msg)
    return redirect(url_for("password_vault"))

# ---------------------------
# Debug route list
# ---------------------------
@app.cli.command("routes")
def list_routes():
    """List all registered routes — run with `flask routes`."""
    import urllib
    output = []
    for rule in app.url_map.iter_rules():
        methods = ",".join(rule.methods)
        url = urllib.parse.unquote(f"{rule}")
        output.append(f"{rule.endpoint:20s} {methods:25s} {url}")
    for line in sorted(output):
        print(line)


# ---------------------------
# Run the app
# ---------------------------
if __name__ == "__main__":
    app.run(debug=True)
