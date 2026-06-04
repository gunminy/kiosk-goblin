# Contributing to Kiosk Goblin

Thank you for your interest in contributing to Kiosk Goblin! We love contributions from the community.

## Code of Conduct

Please be respectful and welcoming to other contributors.

## How to Contribute

### 1. Reporting Bugs or Requesting Features
- Please search open issues before creating a new one.
- Use the templates available when opening a new issue.

### 2. Local Setup
1. Clone the repository.
2. Create a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Copy the environment template:
   ```bash
   cp .env.example .env
   ```
5. Run the application locally:
   ```bash
   streamlit run app.py
   ```

### 3. Writing Plugins
If you wish to add a new plugin:
1. Create a directory under `kiosk_goblin/plugins/<your_plugin_name>/`.
2. Implement a subclass of `BasePlugin` inside `kiosk_goblin/plugins/<your_plugin_name>/__init__.py`.
3. Export the class as `PluginClass`.

### 4. Pull Requests
- Keep PRs focused on a single change.
- Make sure code passes syntax and linting checks.
- Document any new features or configurations in the layout example.
