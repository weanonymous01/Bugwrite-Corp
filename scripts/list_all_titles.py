import json
import subprocess

node_code = (
    'const fs=require("fs"); const vm=require("vm"); const ctx={window:{}}; '
    'vm.runInNewContext(fs.readFileSync("public/blog/articles-data.js","utf8"), ctx); '
    'process.stdout.write(JSON.stringify(ctx.window.BUGWRITE_ARTICLES));'
)
res = subprocess.run(['node', '-e', node_code], capture_output=True, text=True, check=True)
arts = json.loads(res.stdout)

print(f"Total articles: {len(arts)}")
for cat in ['Big Tech', 'Security', 'Business', 'Gaming']:
    cat_arts = [a for a in arts if a.get('category') == cat]
    print(f"\n--- {cat} ({len(cat_arts)} articles) ---")
    for a in cat_arts:
        print(f"[{a['id']}] {a['title']}")
