# LaTeX Expression Canvas

A minimalistic and powerful web app to manage and preview LaTeX expressions. Ideal for students, engineers, researchers, and anyone who frequently works with mathematical notation. The interface is clean, focused, and avoids bloat — designed for speed and usability.

## 🚀 Features

- 📁 **Folder-based organization**: Save LaTeX expressions grouped in named folders.
- 📋 **Copy to clipboard**: Quickly copy expressions with one click.
- 🗑️ **Delete expressions**: Remove entries easily, with safety in mind.
- 🧩 **Open in new tab**: Launch any expression in a separate fullscreen tab for printing or screenshot.
- 🔠 **Font size control**: Adjust the rendered LaTeX font size dynamically.
- 🔒 **Delete lock**: Prevent accidental deletions by locking the delete button.
- 🧼 **Clear-on-save toggle**: Optionally clear the canvas after saving a new expression.
- 📤 **Export folders**: Export an entire folder as a JSON file.
- 📦 **Export all data**: Download your entire expression library at once.
- 📥 **Import with conflict resolution**: Import expressions from JSON, with per-expression override control if naming conflicts occur.
- 👁️ **Toggle preview rendering**: Disable expression preview on canvas for lightweight use or focus mode.
- 🧪 **Load example expressions**: Populate the app with sample LaTeX expressions to get started or test.

## 🧠 Data Structure

Internally, the data is stored in a compact and efficient structure:

All folders and expressions are indexed by their names, and JSON exports reflect this structure for easy readability and versioning.

## 🛠️ Tech Stack

- **Frontend**: [Streamlit](https://streamlit.io/)
- **Rendering**: MathJax for LaTeX preview
- **Clipboard / File Handling**: Native browser APIs
- **Data format**: JSON

## 💻 Running the App

```bash
pip install streamlit
streamlit run app.py
```

Exported data is saved as .json, with the following format:
{
  "Algebra": {
    "Quadratic Formula": "\\frac{-b \\pm \\sqrt{b^2 - 4ac}}{2a}"
  },
  "Calculus": {
    "Euler's Identity": "e^{i\\pi} + 1 = 0"
  }
}
