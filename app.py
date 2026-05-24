from flask import Flask, render_template, request, jsonify
from reviewer import run_review

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/review", methods=["POST"])
def review():
    data = request.get_json()
    pr_url = data.get("pr_url", "").strip()
    post_to_github = data.get("post_to_github", False)

    if not pr_url:
        return jsonify({"error": "Please provide a GitHub PR URL."}), 400

    if "github.com" not in pr_url or "/pull/" not in pr_url:
        return jsonify({"error": "Invalid GitHub PR URL. Format: https://github.com/owner/repo/pull/123"}), 400

    try:
        result = run_review(pr_url, post_to_github)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    import os
port = int(os.environ.get("PORT", 5000))
app.run(debug=False, host="0.0.0.0", port=port)