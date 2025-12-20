"""Multi-step form demo.

Demonstrates all form elements: input, checkbox, radio, and select.
"""

from wry_py import UiWindow, div, text, button, input, checkbox, radio, select

# Form state
step = 1
form_data = {
    "name": "",
    "email": "",
    "notifications": False,
    "newsletter": False,
    "contact_method": "email",
    "experience": "",
    "country": "",
    "interests": [],
}

# Field-specific error messages for validation
form_errors = {
    "name": "",
    "email": "",
    "experience": "",
    "country": "",
}
window = UiWindow(title="Form Demo", width=500, height=500)

def validate_current_step():
    """Validates the current step's data."""
    errors = []
    if step == 1:
        # clear previous errors for step 1
        form_errors["name"] = ""
        form_errors["email"] = ""

        if not form_data["name"].strip():
            form_errors["name"] = "Name is required."
            errors.append("name")
        if "@" not in form_data["email"] or "." not in form_data["email"]:
            form_errors["email"] = "A valid email is required."
            errors.append("email")
    elif step == 3:
        # clear previous errors for step 3
        form_errors["experience"] = ""
        form_errors["country"] = ""

        if not form_data["experience"]:
            form_errors["experience"] = "Please select your experience level."
            errors.append("experience")
        if not form_data["country"]:
            form_errors["country"] = "Please select your country."
            errors.append("country")

    if errors:
        return {"message": "Please fix the highlighted errors."}

    return {"message": "valid"}

def next_step():
    global step
    if step < 4:
        validation_result = validate_current_step()
        if validation_result["message"] == "valid":
            step += 1
        render()


def prev_step():
    global step
    if step > 1:
        step -= 1
        render()


def submit_form():
    global step
    step = 5
    render()


def restart():
    global step, form_data, form_errors
    step = 1
    form_data = {
        "name": "",
        "email": "",
        "notifications": False,
        "newsletter": False,
        "contact_method": "email",
        "experience": "",
        "country": "",
        "interests": [],
    }
    # reset errors
    form_errors = {
        "name": "",
        "email": "",
        "experience": "",
        "country": "",
    }
    render()


def make_header():
    steps = ["Info", "Preferences", "Details", "Review"]

    step_indicators = div().h_flex().items_center().justify_center().gap(24)

    for i, label in enumerate(steps, 1):
        is_active = i == step
        is_done = i < step

        indicator = (
            div()
            .v_flex()
            .items_center()
            .gap(4)
            .child_builder(
                div()
                .width(32)
                .height(32)
                .rounded(16)
                .bg("#3b82f6" if is_active else "#22c55e" if is_done else "#404040")
                .v_flex()
                .items_center()
                .justify_center()
                .child_builder(
                    text(str(i) if not is_done else "✓")
                    .text_size(14)
                    .text_color("#fff")
                )
            )
            .child_builder(
                text(label)
                .text_size(11)
                .text_color("#fff" if is_active else "#888")
            )
        )
        step_indicators = step_indicators.child_builder(indicator)

    return (
        div()
        .padding(20)
        .border_bottom(1, "#333")
        .child_builder(step_indicators)
    )


def make_step_1():
    """Basic Information"""
    return (
        div()
        .v_flex()
        .gap(20)
        .child_builder(text("Basic Information").text_size(20).text_weight("bold"))
        .child_builder(
            div()
            .v_flex()
            .gap(6)
            .child_builder(text("Name").text_size(14).text_color("#aaa"))
            .child_builder(
                input()
                .placeholder("Enter your name")
                .value(form_data["name"])
                .full_width()
                .padding(12)
                .bg("#2a2a3a")
                .border(1, "#444")
                .rounded(6)
                .focus_border_color("#3b82f6")
                .transition_colors(0.15)
                .on_input(lambda v: update_field("name", v))
            )
            .child_builder(
                text(form_errors["name"]).text_color("#f87171").text_size(12)
            )
        )
        .child_builder(
            div()
            .v_flex()
            .gap(6)
            .child_builder(text("Email").text_size(14).text_color("#aaa"))
            .child_builder(
                input()
                .placeholder("Enter your email")
                .value(form_data["email"])
                .full_width()
                .padding(12)
                .bg("#2a2a3a")
                .border(1, "#444")
                .rounded(6)
                .focus_border_color("#3b82f6")
                .transition_colors(0.15)
                .on_input(lambda v: update_field("email", v))
            )
            .child_builder(
                text(form_errors["email"]).text_color("#f87171").text_size(12)
            )
        )
    )


def make_step_2():
    """Preferences"""
    return (
        div()
        .v_flex()
        .gap(20)
        .child_builder(text("Preferences").text_size(20).text_weight("bold"))
        .child_builder(
            div()
            .v_flex()
            .gap(12)
            .child_builder(text("Notifications").text_size(14).text_color("#aaa"))
            .child_builder(
                checkbox("Enable push notifications")
                .checked(form_data["notifications"])
                .on_change(lambda v: update_field("notifications", v == "true"))
            )
            .child_builder(
                checkbox("Subscribe to newsletter")
                .checked(form_data["newsletter"])
                .on_change(lambda v: update_field("newsletter", v == "true"))
            )
        )
        .child_builder(
            div()
            .v_flex()
            .gap(12)
            .child_builder(text("Preferred contact method").text_size(14).text_color("#aaa"))
            .child_builder(
                radio("Email")
                .group("contact")
                .value("email")
                .checked(form_data["contact_method"] == "email")
                .on_change(lambda v: update_field("contact_method", v))
            )
            .child_builder(
                radio("Phone")
                .group("contact")
                .value("phone")
                .checked(form_data["contact_method"] == "phone")
                .on_change(lambda v: update_field("contact_method", v))
            )
            .child_builder(
                radio("SMS")
                .group("contact")
                .value("sms")
                .checked(form_data["contact_method"] == "sms")
                .on_change(lambda v: update_field("contact_method", v))
            )
        )
    )


def make_step_3():
    """Additional Details"""
    return (
        div()
        .v_flex()
        .gap(20)
        .child_builder(text("Additional Details").text_size(20).text_weight("bold"))
        .child_builder(
            div()
            .v_flex()
            .gap(6)
            .child_builder(text("Experience Level").text_size(14).text_color("#aaa"))
            .child_builder(
                select()
                .option("", "Select your experience...")
                .option("beginner", "Beginner (0-1 years)")
                .option("intermediate", "Intermediate (2-4 years)")
                .option("advanced", "Advanced (5-9 years)")
                .option("expert", "Expert (10+ years)")
                .selected(form_data["experience"])
                .full_width()
                .bg("#2a2a3a")
                .text_color("#fff")
                .border(1, "#444")
                .rounded(6)
                .on_change(lambda v: update_field("experience", v))
            )
            .child_builder(
                text(form_errors["experience"]).text_color("#f87171").text_size(12)
            )
        )
        .child_builder(
            div()
            .v_flex()
            .gap(6)
            .child_builder(text("Country").text_size(14).text_color("#aaa"))
            .child_builder(
                select()
                .option("", "Select your country...")
                .option("us", "United States")
                .option("uk", "United Kingdom")
                .option("ca", "Canada")
                .option("au", "Australia")
                .option("de", "Germany")
                .option("fr", "France")
                .option("jp", "Japan")
                .option("other", "Other")
                .selected(form_data["country"])
                .full_width()
                .bg("#2a2a3a")
                .text_color("#fff")
                .border(1, "#444")
                .rounded(6)
                .on_change(lambda v: update_field("country", v))
            )
            .child_builder(
                text(form_errors["country"]).text_color("#f87171").text_size(12)
            )
        )
        .child_builder(
            div()
            .v_flex()
            .gap(12)
            .child_builder(text("Areas of Interest").text_size(14).text_color("#aaa"))
            .child_builder(
                div()
                .v_flex()
                .gap(8)
                .child_builder(
                    checkbox("Web Development")
                    .checked("web" in form_data["interests"])
                    .on_change(lambda v: toggle_interest("web", v == "true"))
                )
                .child_builder(
                    checkbox("Mobile Development")
                    .checked("mobile" in form_data["interests"])
                    .on_change(lambda v: toggle_interest("mobile", v == "true"))
                )
                .child_builder(
                    checkbox("Data Science")
                    .checked("data" in form_data["interests"])
                    .on_change(lambda v: toggle_interest("data", v == "true"))
                )
                .child_builder(
                    checkbox("DevOps")
                    .checked("devops" in form_data["interests"])
                    .on_change(lambda v: toggle_interest("devops", v == "true"))
                )
            )
        )
    )


def make_step_4():
    """Review"""
    experience_labels = {
        "beginner": "Beginner (0-1 years)",
        "intermediate": "Intermediate (2-4 years)",
        "advanced": "Advanced (5-9 years)",
        "expert": "Expert (10+ years)",
    }

    country_labels = {
        "us": "United States",
        "uk": "United Kingdom",
        "ca": "Canada",
        "au": "Australia",
        "de": "Germany",
        "fr": "France",
        "jp": "Japan",
        "other": "Other",
    }

    interest_labels = {
        "web": "Web Development",
        "mobile": "Mobile Development",
        "data": "Data Science",
        "devops": "DevOps",
    }

    def info_row(label, value):
        return (
            div()
            .h_flex()
            .justify_between()
            .padding(8, 0)
            .border_bottom(1, "#333")
            .child_builder(text(label).text_color("#888"))
            .child_builder(text(value or "Not provided").text_color("#fff"))
        )

    interests_str = ", ".join(
        interest_labels.get(i, str(i)) for i in form_data["interests"]
    ) or "None selected"

    return (
        div()
        .v_flex()
        .gap(16)
        .child_builder(text("Review Your Information").text_size(20).text_weight("bold"))
        .child_builder(
            div()
            .v_flex()
            .bg("#1f1f2e")
            .rounded(8)
            .padding(16)
            .child_builder(info_row("Name", form_data["name"]))
            .child_builder(info_row("Email", form_data["email"]))
            .child_builder(info_row("Notifications", "Enabled" if form_data["notifications"] else "Disabled"))
            .child_builder(info_row("Newsletter", "Subscribed" if form_data["newsletter"] else "Not subscribed"))
            .child_builder(info_row("Contact Method", form_data["contact_method"].title()))
            .child_builder(info_row("Experience", experience_labels.get(form_data["experience"], "Not selected")))
            .child_builder(info_row("Country", country_labels.get(form_data["country"], "Not selected")))
            .child_builder(info_row("Interests", interests_str))
        )
    )


def make_success():
    """Success message"""
    return (
        div()
        .v_flex()
        .items_center()
        .justify_center()
        .gap(20)
        .flex_1()
        .child_builder(
            div()
            .width(64)
            .height(64)
            .rounded(32)
            .bg("#22c55e")
            .v_flex()
            .items_center()
            .justify_center()
            .child_builder(text("✓").text_size(32).text_color("#fff"))
        )
        .child_builder(text("Form Submitted!").text_size(24).text_weight("bold"))
        .child_builder(
            text("Thank you for completing the form.")
            .text_color("#888")
            .text_center()
        )
        .child_builder(
            button("Start Over")
            .padding(12, 24)
            .bg("#3b82f6")
            .rounded(6)
            .cursor("pointer")
            .transition_colors(0.15)
            .hover_bg("#2563eb")
            .on_click(restart)
        )
    )


def make_nav_buttons():
    buttons = div().h_flex().gap(12).justify_between()

    if step > 1:
        buttons = buttons.child_builder(
            button("Back")
            .padding(12, 24)
            .bg("#404040")
            .rounded(6)
            .cursor("pointer")
            .transition_colors(0.15)
            .hover_bg("#525252")
            .on_click(prev_step)
        )
    else:
        buttons = buttons.child_builder(div())

    if step < 4:
        buttons = buttons.child_builder(
            button("Next")
            .padding(12, 24)
            .bg("#3b82f6")
            .rounded(6)
            .cursor("pointer")
            .transition_colors(0.15)
            .hover_bg("#2563eb")
            .on_click(next_step)
        )
    else:
        buttons = buttons.child_builder(
            button("Submit")
            .padding(12, 24)
            .bg("#22c55e")
            .rounded(6)
            .cursor("pointer")
            .transition_colors(0.15)
            .hover_bg("#16a34a")
            .on_click(submit_form)
        )

    return buttons


def update_field(field, value):
    form_data[field] = value
    # clear any existing error for this field when the user updates it
    if field in form_errors:
        form_errors[field] = ""


def toggle_interest(interest, checked):
    if checked and interest not in form_data["interests"]:
        form_data["interests"].append(interest)
    elif not checked and interest in form_data["interests"]:
        form_data["interests"].remove(interest)


def render():
    if step == 5:
        content = make_success()
        root = (
            div()
            .size_full()
            .v_flex()
            .bg("#171717")
            .child_builder(content)
            .build()
        )
    else:
        step_content = {
            1: make_step_1,
            2: make_step_2,
            3: make_step_3,
            4: make_step_4,
        }

        root = (
            div()
            .size_full()
            .v_flex()
            .bg("#171717")
            .child_builder(make_header())
            .child_builder(
                div()
                .flex_1()
                .v_flex()
                .padding(24)
                .overflow("auto")
                .child_builder(step_content[step]())
            )
            .child_builder(
                div()
                .padding(20)
                .border_top(1, "#333")
                .child_builder(make_nav_buttons())
            )
            .build()
        )

    window.set_root(root)


render()
window.run()
