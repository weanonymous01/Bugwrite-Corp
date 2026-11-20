import re

# 1. Update scripts/build_seo.py cache string
with open('scripts/build_seo.py', 'r', encoding='utf-8') as f:
    seo = f.read()

seo_updated = seo.replace('?v=bit1', '?v=p2')
with open('scripts/build_seo.py', 'w', encoding='utf-8') as f:
    f.write(seo_updated)
print('Updated build_seo.py cache versions to ?v=p2')

# 2. Update slots in public/blog/articles-data.js
with open('public/blog/articles-data.js', 'r', encoding='utf-8') as f:
    data = f.read()

# Change when-is-gta-6-playable-release-times slot to recent
data = re.sub(r'(\"?id\"?:\s*\"when-is-gta-6-playable-release-times\",\s*\"?slot\"?:\s*)\"?featured\"?', r'\g<1>"recent"', data)

# Change gta-6-characters-jason-lucia-cast slot to featured
data = re.sub(r'(\"?id\"?:\s*\"gta-6-characters-jason-lucia-cast\",\s*\"?slot\"?:\s*)\"?recent\"?', r'\g<1>"featured"', data)

# Change new-zealand, metacritic, story-length, screenshots from gta6-hub to recent
for slug in ['new-zealand-gta-6-trick', 'gta-6-metacritic-score-review-embargo', 'how-long-is-gta-6-story-mode', 'gta-6-screenshots-gallery-weather']:
    data = re.sub(rf'(\"?id\"?:\s*\"{slug}\",\s*\"?slot\"?:\s*)\"?gta6-hub\"?', r'\g<1>"recent"', data)

# Change top 4 new trends to gta6-hub
for slug in ['lexie-shoaibi-mandy-gta-6-actress-house-location-scene', 'is-niko-bellic-in-gta-6-easter-eggs', 'gta-6-endings-how-many-choices-explained', 'has-anyone-finished-gta-6-how-much-made-gta-flu-online']:
    data = re.sub(rf'(\"?id\"?:\s*\"{slug}\",\s*\"?slot\"?:\s*)\"?recent\"?', r'\g<1>"gta6-hub"', data)

with open('public/blog/articles-data.js', 'w', encoding='utf-8') as f:
    f.write(data)
print('Updated article slots in articles-data.js')
