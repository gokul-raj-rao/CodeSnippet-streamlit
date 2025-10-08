import streamlit as st
import json
import os


SNIPPETS_FILE = "snippets.json"


# ----------------- Utility Functions -----------------
def load_snippets():
    if os.path.exists(SNIPPETS_FILE):
        with open(SNIPPETS_FILE, "r") as f:
            return json.load(f)
    return []


def save_snippets(snippets):
    with open(SNIPPETS_FILE, "w") as f:
        json.dump(snippets, f, indent=4)


# ----------------- Main App -----------------
def main():
    st.set_page_config(page_title="Code Snippet Manager", layout="wide")
    st.title("📂 Code Snippet Manager")

    # Load existing snippets
    snippets = load_snippets()

    menu = ["Add Snippet", "View Snippets", "Search Snippets"]
    choice = st.sidebar.selectbox("Choose", menu)

    if choice == "Add Snippet":
        st.subheader("➕ Add New Code Snippet")
        title = st.text_input("Snippet Title")
        description = st.text_area("Description")
        language = st.selectbox("Programming Language", ["Python", "JavaScript", "Java", "C++", "Other"])
        code = st.text_area("Paste your code here", height=200)

        if st.button("Save Snippet"):
            if title and code:
                new_snippet = {
                    "title": title,
                    "description": description,
                    "language": language,
                    "code": code
                }
                snippets.append(new_snippet)
                save_snippets(snippets)
                st.success("✅ Snippet saved successfully!")
            else:
                st.warning("⚠️ Title and code are required!")

    elif choice == "View Snippets":
        st.subheader("📜 All Saved Snippets")
        if snippets:
            for i, snip in enumerate(snippets):
                with st.expander(f"{i+1}. {snip['title']} ({snip['language']})"):
                    st.write(f"**Description:** {snip['description']}")
                    st.code(snip["code"], language=snip["language"].lower())
        else:
            st.info("No snippets saved yet.")

    elif choice == "Search Snippets":
        st.subheader("🔍 Search Snippets")
        query = st.text_input("Enter keyword (title, description, language)")
        if query:
            results = [snip for snip in snippets if query.lower() in snip['title'].lower() 
                       or query.lower() in snip['description'].lower() 
                       or query.lower() in snip['language'].lower()]
            if results:
                for snip in results:
                    with st.expander(f"{snip['title']} ({snip['language']})"):
                        st.write(f"**Description:** {snip['description']}")
                        st.code(snip["code"], language=snip["language"].lower())
            else:
                st.warning("No matching snippets found.")


if __name__ == "__main__":
    main()
