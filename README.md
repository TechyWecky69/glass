# 🪟 Glass

### Turn websites into real desktop applications on Linux

Glass transforms websites into native-feeling desktop applications.  
Create launchers, icons, isolated browser profiles, and manage your web apps directly from the terminal.

No Electron. No wrappers. No unnecessary bloat.

Just your browser, your website, and a clean desktop integration.

---

## ✨ Features

- 🚀 Install websites as desktop applications
- 🖥️ Creates native Linux `.desktop` launchers
- 🎨 Automatically downloads website icons
- 🔒 Optional isolated browser profiles
- 📦 Simple command-line interface
- 🗑️ Remove apps cleanly
- 📋 List and inspect installed web applications
- 🐧 Designed for Linux desktops (KDE Plasma friendly)

---

# 📦 Installation

## Option 1: Install from `.deb`

Download the latest `.deb` package from the Releases page.

Install:

```bash
sudo apt install ./python3-glass_VERSION_all.deb
```

Verify:

```bash
glass help
```

---

## Option 2: Install from source

Clone the repository:

```bash
git clone https://github.com/YOUR_USERNAME/glass.git
cd glass
```

Install:

```bash
pip install .
```

Test:

```bash
glass
```

---

# 🚀 Usage

## Install a website

```bash
glass install https://youtube.com
```

Glass will:

1. Detect the website name
2. Download an icon
3. Create a desktop launcher
4. Add it to your application menu

You can now launch it like any normal application.

---

## Custom app name

Override the detected name:

```bash
glass install https://youtube.com --name "YouTube Music"
```

---

## Create an isolated web app

By default Glass uses your normal browser profile.

To create a separate profile:

```bash
glass install https://youtube.com --isolated ~/Documents/GlassProfiles/youtube
```

This gives the application its own:

- 🍪 Cookies
- 💾 Local storage
- 🔐 Sessions
- ⚙️ Browser settings

Useful for:

- Multiple accounts
- Work/personal separation
- Apps that require independent sessions

---

# 📋 Managing Apps

## List installed apps

```bash
glass list
```

Example:

```
youtube-com
discord-com
github-com
```

---

## View app information

```bash
glass info youtube-com
```

---

## Remove an app

```bash
glass remove youtube-com
```

This removes:

- Desktop launcher
- Icon
- Glass database entry
- Associated profile (if applicable)

---

# 🛠️ How it works

Glass does not package websites into heavy applications.

Instead it creates lightweight browser application shortcuts.

Example:

```
Website
   |
   ↓
Glass
   |
   ├── Desktop launcher
   ├── Application icon
   ├── Browser app mode
   └── Optional isolated profile
```

Your browser handles:

- JavaScript
- Cookies
- Storage
- Authentication
- Updates

Glass simply integrates the website into your desktop.

---

# 🖥️ Supported Browsers

Currently supported:

- Chromium-based browsers

Examples:

- Chromium
- Google Chrome
- Ungoogled Chromium

Firefox support may come in the future.

---

# 🐧 Desktop Support

Designed for Linux desktops.

Tested on:

- ✅ Ubuntu
- ✅ KDE Plasma

Should work with any desktop environment supporting:

- `.desktop` files
- Linux application menus

---

# 📁 File Locations

Glass stores its data here:

```
~/.local/share/glass/
```

Icons:

```
~/.local/share/icons/glass/
```

Desktop launchers:

```
~/.local/share/applications/
```

---

# 🧑‍💻 Development

Clone the repository:

```bash
git clone https://github.com/YOUR_USERNAME/glass.git
cd glass
```

Install development version:

```bash
pip install -e .
```

Run:

```bash
glass
```

---

# 🗺️ Roadmap

Planned features:

- [ ] Firefox support
- [ ] GUI configuration tool
- [ ] Automatic updates
- [ ] Import/export applications
- [ ] Better icon extraction
- [ ] Flatpak package
- [ ] Official APT repository

---

# 🤝 Contributing

Contributions are welcome!

Ideas, bug reports, and improvements can be submitted through GitHub Issues.

---

# 📜 License

MIT License

You are free to use, modify, and distribute Glass.

---

# ❤️ Why Glass?

Modern websites are becoming applications.

Glass provides a simple way to bring them into your Linux desktop without installing huge application bundles.

Small. Fast. Native.

**See the web through Glass. 🪟**
