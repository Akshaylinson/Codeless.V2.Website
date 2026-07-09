from pathlib import Path
import re


BASE = Path(__file__).resolve().parent
REFERENCE = BASE / "career-details.html"


def extract(pattern: str, text: str, label: str) -> str:
    match = re.search(pattern, text, flags=re.DOTALL)
    if not match:
        raise RuntimeError(f"Could not find {label} in reference header")
    return match.group(1)


def page_active(filename: str) -> str:
    name = filename.lower()
    if name == "index.html":
        return "home"
    if name == "about.html":
        return "about"
    if name in {"service.html", "service-details.html", "ai-marketing.html", "ai-chatbot.html"}:
        return "services"
    if name == "contact.html":
        return "contact"
    if name in {"career.html", "career-details.html", "project.html", "project-details.html", "team.html"}:
        return "about"
    return ""


def li_class(base: str, active: bool) -> str:
    return f'class="active {base}"' if active else f'class="{base}"'


def build_desktop_nav(active: str, about_submenu: str, services_submenu: str) -> str:
    return f"""                            <ul>
                                <li {li_class("", active == "home") if False else ""}>"""


def desktop_nav(active: str, about_submenu: str, services_submenu: str) -> str:
    home_class = 'class="menu-item-has-children active"' if active == "home" else 'class="menu-item-has-children"'
    about_class = li_class("menu-item-has-children megamenu", active == "about")
    services_class = li_class("menu-item-has-children megamenu", active == "services")
    contact_class = 'class="active"' if active == "contact" else 'class=""'

    return f"""                            <ul>
                                <li {home_class}><a href="index.html"><span>Home</span></a></li>
                                <li {about_class}>
                                    <a href="about.html"><span>About Us</span></a>
{about_submenu}
                                </li>
                                <li {services_class}>
                                    <a href="service.html"><span>Services</span></a>
{services_submenu}
                                </li>
                                <li {contact_class}><a href="contact.html"><span>Contact Us</span></a></li>
                            </ul>"""


def mobile_nav(active: str) -> str:
    home_class = "menu-item active" if active == "home" else "menu-item"
    about_class = "menu-item active menu-item-has-children" if active == "about" else "menu-item menu-item-has-children"
    services_class = "menu-item active menu-item-has-children" if active == "services" else "menu-item menu-item-has-children"
    contact_class = "menu-item active" if active == "contact" else "menu-item"

    return f"""                                <ul class="xb-menu-primary clearfix">
                                    <li class="{home_class}"><a href="index.html"><span>Home</span></a></li>
                                    <li class="{about_class}">
                                        <a href="about.html"><span>About Us</span></a>
                                        <ul class="sub-menu">
                                            <li><a href="about.html"><span>About Us</span></a></li>
                                            <li><a href="team.html"><span>Team</span></a></li>
                                            <li><a href="project.html"><span>Project</span></a></li>
                                            <li><a href="project-details.html"><span>Project Details</span></a></li>
                                            <li><a href="career.html"><span>Career</span></a></li>
                                            <li><a href="career-details.html"><span>Career Details</span></a></li>
                                        </ul>
                                    </li>
                                    <li class="{services_class}">
                                        <a href="service.html"><span>Services</span></a>
                                        <ul class="sub-menu">
                                            <li><a href="service.html"><span>Services</span></a></li>
                                            <li><a href="service-details.html"><span>Service Details</span></a></li>
                                            <li><a href="ai-marketing.html"><span>AI Marketing</span></a></li>
                                            <li><a href="ai-chatbot.html"><span>AI Chatbot</span></a></li>
                                        </ul>
                                    </li>
                                    <li class="{contact_class}"><a href="contact.html"><span>Contact Us</span></a></li>
                                </ul>"""


def main() -> None:
    reference_text = REFERENCE.read_text(encoding="utf-8")
    about_submenu = extract(
        r'<li class="menu-item-has-children active megamenu">\s*<a href="#!"><span>Pages</span></a>\s*(<ul class="submenu">.*?</ul>)\s*</li>',
        reference_text,
        "about mega menu",
    )
    services_submenu = extract(
        r'<li class="menu-item-has-children megamenu">\s*<a href="#!"><span>Services</span></a>\s*(<ul class="submenu">.*?</ul>)\s*</li>',
        reference_text,
        "services mega menu",
    )

    for path in sorted(BASE.glob("*.html")):
        content = path.read_text(encoding="utf-8")
        active = page_active(path.name)

        desktop = desktop_nav(active, about_submenu, services_submenu)
        mobile = mobile_nav(active)

        content, desktop_count = re.subn(
            r'(<nav class="main-menu collapse navbar-collapse">\s*)<ul>.*?</ul>(\s*</nav>)',
            lambda m: m.group(1) + desktop + m.group(2),
            content,
            flags=re.DOTALL,
        )
        content, mobile_count = re.subn(
            r'(<nav class="xb-header-nav">\s*)<ul class="xb-menu-primary clearfix">.*?</ul>(\s*</nav>)',
            lambda m: m.group(1) + mobile + m.group(2),
            content,
            flags=re.DOTALL,
        )

        if desktop_count != 1 or mobile_count != 1:
            raise RuntimeError(f"Header replacement failed in {path.name}")

        path.write_text(content, encoding="utf-8")
        print(f"Updated {path.name}")


if __name__ == "__main__":
    main()
