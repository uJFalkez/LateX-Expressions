# LaTeX Expressions Canvas

This is a simple and intuitive app for managing LaTeX expressions. You can organize them into folders, adjust their font size, preview, and export/import your data easily.

## 📂 Data

Internally, the data is stored in a compact and efficient structure: folders and expressions are indexed by their names, and JSON exports reflect this structure for easy readability and versioning.

Exported and imported data are handled as `.json` files. There's no restriction on the filename — only the content structure and file type matter.

One key feature is expression conflict handling on import — like a basic built-in Git system for resolving duplicates.

## Beta: 🎧 **Expression Listener**

The Listener allows integration between your symbolic development workflow and the app.

It's essentially a local socket at `http://localhost:8501/listener/<user_key>`. You can `POST` LaTeX expressions to this endpoint to render them inside the app in real-time.

For usage examples, refer to [this example](https://github.com/uJFalkez/LateX-Expressions/blob/main/Usage%20Examples/listener_example1.py). It’s pretty straightforward to use!

## 📢 Notes
Internally, it's quite difficult to lose data. In the worst-case scenario (e.g. a crash), restarting the app should restore all previously saved expressions.

The app is designed for fast access — ideal for study notes, report writing, or live demonstrations.

## ✨ Coming Soon (Ideas)
- Expression search/filter bar

- LaTeX syntax validation

- Dark mode toggle

- Integration with SymPy / PySR for symbolic development

## 📞 Contact
For questions, suggestions, or bug reports, contact: matubaramarcos@gmail.com
