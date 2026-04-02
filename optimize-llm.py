#!/usr/bin/env python3
"""
Inject LLM/AI-search optimizations into all Character Engine pages:
- JSON-LD structured data (Organization, Service, FAQPage)
- Complete Open Graph + Twitter Card meta tags
- Canonical URLs
- Semantic HTML wrapper (<main>)
- Market-specific FAQ sections with schema markup
- robots meta allowing full indexing
"""

import os
import json
import re

BASE_DOMAIN = "https://characterengine.live"
ORG_NAME = "MiTL Studio"
BRAND_NAME = "Character Engine"

# Market page configs
MARKETS = {
    "index": {
        "path": "",
        "title": "Character Engine — AI Characters That Live",
        "description": "Build, manage, and deploy AI characters with memory, personality, and visual identity. Custom character IP creation, universe building, and character licensing by MiTL Studio.",
        "market_name": None,
        "faqs": [
            ("What is Character Engine?", "Character Engine is a full-service AI character IP platform by MiTL Studio. We build, manage, and deploy AI characters with memory, personality, backstory, visual identity, and the ability to interact in real time across live shows, social media, websites, and any digital touchpoint."),
            ("What can AI characters do for my brand?", "AI characters build memory (they remember every interaction), build brand authority (a consistent voice that never goes off-brand), and blur reality (audiences engage with them like real people). They can host live streams, produce social content, answer questions, onboard users, and represent your brand 24/7."),
            ("Can I build a custom character or do I have to license one?", "Both. You can build a fully custom character from scratch — we handle the architecture, visual identity, backstory, and deployment. Or you can license one of our 22+ existing characters from the MiTL universe for your campaigns and activations."),
            ("How does Character Engine work?", "We follow a four-step process: Discovery (understanding your brand and audience), Architecture (designing the character's personality, backstory, and visual identity), Build and Deploy (bringing the character to life across your platforms), and Manage and Grow (evolving the character over time with memory and new content)."),
            ("Who is behind Character Engine?", "Character Engine is built and operated by MiTL Studio, the team behind Mornings in the Lab — a daily live broadcast network with 1,000+ episodes and 22+ AI characters already deployed and active."),
        ]
    },
    "ecommerce": {
        "path": "ecommerce",
        "title": "Character Engine for E-Commerce — Your Brand Has Products. Not a Personality.",
        "description": "Your competitors sell products. You can sell a story. Character Engine builds AI characters that become the face of your e-commerce brand — with memory, personality, and presence that turns shoppers into fans.",
        "market_name": "E-Commerce & DTC Brands",
        "faqs": [
            ("How can AI characters help my e-commerce brand?", "AI characters become the personality behind your products. They host live product drops, create unboxing content, respond to customers on social media, and build a brand following that goes beyond individual products. They remember customer interactions and build relationships that drive repeat purchases."),
            ("Can a character host live shopping events?", "Yes. Characters can host live drops on Instagram Live, TikTok, YouTube, and other platforms. They know product specs, tell the backstory behind each item, interact with viewers in real time, and create urgency and excitement that drives conversions."),
            ("How is this different from hiring an influencer?", "Influencers leave, raise rates, and post for competitors. A Character Engine character is IP you own — it never leaves, never goes off-brand, and builds compounding recognition for your brand specifically. It's a permanent asset, not a rental."),
        ]
    },
    "realestate": {
        "path": "realestate",
        "title": "Character Engine for Real Estate — Every Agent Looks the Same Online.",
        "description": "Identical headshots, same scripts, zero differentiation. Character Engine builds an AI character that becomes your local market identity — producing daily neighborhood content with memory, personality, and presence.",
        "market_name": "Real Estate",
        "faqs": [
            ("How can AI characters help real estate agents?", "A character becomes your local market identity — producing daily content about your farm area, breaking down market data in an engaging voice, promoting listings, hosting virtual open houses, and building the kind of neighborhood recognition that generates referrals. It works your farm area 365 days a year."),
            ("Can the character produce neighborhood-specific content?", "Yes. Your character is built to know your farm area deeply — school ratings, new businesses, market trends, local events, community news. Every piece of content builds on the last, creating a local presence no competing agent can replicate."),
            ("Do I own the character?", "If you choose the Build Your Own path, the character is your IP. We build and manage it, but you own the brand identity. For licensing, you get usage rights to an existing character with flexible terms designed for real estate business models."),
        ]
    },
    "restaurants": {
        "path": "restaurants",
        "title": "Character Engine for Restaurants — Your Food Is Great. Your Brand Is Invisible.",
        "description": "You rely on Yelp reviews and UGC you don't control. Character Engine builds an AI character that becomes the face of your restaurant — telling the story behind every dish with memory, personality, and a social following.",
        "market_name": "Restaurants & Hospitality",
        "faqs": [
            ("How can a character help my restaurant's marketing?", "A character becomes the personality of your restaurant on social media and beyond. It tells the story behind every dish, introduces your team, promotes events, and builds a following that brings people through the door. It posts daily content while your kitchen focuses on food."),
            ("Can a character work for a restaurant group or franchise?", "Absolutely. We can build individual characters for each location with local personality, or a unifying brand character for the entire group. Licensing options work well for franchise models where consistency matters across locations."),
            ("What kind of content does the character produce?", "Menu storytelling, chef spotlights, behind-the-scenes content, event promotion and recaps, seasonal specials, neighborhood features, customer stories, and daily social posts. All in a consistent, engaging voice that captures your restaurant's personality."),
        ]
    },
    "fitness": {
        "path": "fitness",
        "title": "Character Engine for Fitness — Your Workouts Work. Your Marketing Doesn't.",
        "description": "You can't scale yourself. Character Engine builds an AI character that represents your training methodology, produces daily motivation and content, and builds community — while you train clients.",
        "market_name": "Fitness & Coaching",
        "faqs": [
            ("How can an AI character help fitness coaches?", "A character embodies your training philosophy and coaching style. It produces daily motivation, training tips, and mindset content. It manages your online community, responds to member questions, celebrates wins, and keeps engagement high between your live sessions — all while you focus on training clients."),
            ("Will the character sound like me?", "Yes. We build the character from your methodology, your voice patterns, and your coaching philosophy. It's not generic fitness tips — it's YOUR approach, delivered consistently. Think of it as an extension of you that never burns out."),
            ("Can the character help with member onboarding?", "Absolutely. The character walks new members through your programs, explains the philosophy behind the training, and adapts its messaging based on where each member is in their journey. Onboarding becomes a relationship, not a checklist."),
        ]
    },
    "podcasters": {
        "path": "podcasters",
        "title": "Character Engine for Podcasters — Your Show Needs a Cast, Not Just a Host.",
        "description": "Solo host fatigue is real. Character Engine builds AI characters that join your show as recurring co-hosts, commentators, and personalities — with memory, backstory, and audience following.",
        "market_name": "Podcasters & Show Hosts",
        "faqs": [
            ("Can AI characters actually co-host a podcast?", "Yes. Characters join your show with their own perspectives, opinions, and personality. They remember past episodes, have running bits, and build a relationship with your audience over time. We already run 22+ characters across daily live shows in the MiTL universe — this is proven, not theoretical."),
            ("How do characters add to a show format?", "Characters bring variety — a skeptic who challenges your takes, an analyst who brings data, a comedian who lightens the mood. Your show becomes a universe with multiple voices instead of one perspective. Audiences come back to hear what their favorite character thinks about the latest topic."),
            ("Can I license an existing character for my show?", "Yes. You can bring one of our existing MiTL universe characters onto your show. They come with personality, backstory, and audience recognition. We handle the integration into your format."),
        ]
    },
    "agencies": {
        "path": "agencies",
        "title": "Character Engine for Agencies — Your Clients Need Characters. You Need a Partner.",
        "description": "Your clients want differentiation. You can't build character IP in-house. Character Engine is your white-label partner for AI character creation, management, and deployment across your client roster.",
        "market_name": "Marketing & Creative Agencies",
        "faqs": [
            ("How does the white-label partnership work?", "We build characters for your clients behind the scenes. You present them, manage the client relationship, and take the credit. We handle the architecture, visual identity, deployment, and ongoing evolution. Your agency name on the deliverable, our engine under the hood."),
            ("Can we package this as a new service line?", "Yes. We train your team, provide the tools, and support every build. You add character IP as a premium offering to your pitch deck — a capability no competing agency has. We work with you on pricing models that work for agency margins."),
            ("What if we have multiple clients who need characters?", "That's exactly how this works best. One partnership gives you access to the full Character Engine platform for your entire client roster. Each client gets custom characters built to their brand, all managed through the same engine."),
        ]
    },
    "creators": {
        "path": "creators",
        "title": "Character Engine for Creators — You Can't Scale Yourself. But You Can Scale a Universe.",
        "description": "Creator burnout is real. Character Engine builds AI characters that extend your personal brand into a cast — producing content, engaging your audience, and building a universe while you focus on what you do best.",
        "market_name": "Creators & Influencers",
        "faqs": [
            ("How do AI characters extend a creator's brand?", "Characters represent different facets of your message. One might be the analyst, another the motivator, another the comedian. They produce content in their own voices, engage your community, and build followings within your universe — multiplying your output without multiplying your hours."),
            ("Will my audience accept AI characters?", "Our experience with 22+ characters across daily live shows says yes — overwhelmingly. Audiences pick favorites, debate takes, and share clips. The key is that characters are compelling and consistent, not that they're hidden. Transparency plus quality equals engagement."),
            ("Can a character manage my community?", "Yes. A Community Character can live in your Discord, respond to comments, host AMA-style conversations, and keep engagement high between your posts. It knows your members, references past interactions, and maintains the energy of your community spaces."),
        ]
    },
    "saas": {
        "path": "saas",
        "title": "Character Engine for SaaS — Your Product Has Features. It Needs a Face.",
        "description": "SaaS brands are faceless. Character Engine builds an AI character that becomes your product's personality — onboarding users, building brand affinity, and making your brand unforgettable across every touchpoint.",
        "market_name": "SaaS & Tech",
        "faqs": [
            ("How can an AI character help a SaaS product?", "A character becomes your product's personality. It onboards new users with warmth and context instead of a sterile product tour, announces features with excitement instead of corporate copy, manages community engagement, and creates consistent brand voice across marketing, support, social, and in-product messaging."),
            ("Is this just a chatbot with a name?", "No. A Character Engine character has a full personality architecture — backstory, voice patterns, emotional range, behavioral rules, visual identity, and memory. It remembers user journeys, adapts over time, and builds real brand affinity. A chatbot answers questions. A character builds relationships."),
            ("Can the character work inside our product?", "Yes. Through API integration, the character can appear in onboarding flows, help documentation, in-product messaging, and support interactions. The same personality that shows up on your social media shows up inside the product — consistent voice everywhere."),
        ]
    },
}


def build_jsonld(config):
    """Build JSON-LD structured data for a page."""
    canonical = f"{BASE_DOMAIN}/{config['path']}/" if config['path'] else f"{BASE_DOMAIN}/"
    
    schemas = []
    
    # Organization (on all pages)
    org = {
        "@context": "https://schema.org",
        "@type": "Organization",
        "@id": f"{BASE_DOMAIN}/#organization",
        "name": ORG_NAME,
        "brand": {"@type": "Brand", "name": BRAND_NAME},
        "url": BASE_DOMAIN,
        "sameAs": [
            "https://mitl.studio",
            "https://mornings.live",
            "https://universe.mitl.studio"
        ]
    }
    schemas.append(org)
    
    # Service
    service = {
        "@context": "https://schema.org",
        "@type": "Service",
        "name": f"{BRAND_NAME} for {config['market_name']}" if config['market_name'] else BRAND_NAME,
        "description": config['description'],
        "provider": {"@id": f"{BASE_DOMAIN}/#organization"},
        "url": canonical,
        "serviceType": "AI Character IP Creation and Management",
        "areaServed": "Worldwide",
    }
    if config['market_name']:
        service["audience"] = {
            "@type": "Audience",
            "audienceType": config['market_name']
        }
    schemas.append(service)
    
    # WebPage
    webpage = {
        "@context": "https://schema.org",
        "@type": "WebPage",
        "name": config['title'],
        "description": config['description'],
        "url": canonical,
        "isPartOf": {"@type": "WebSite", "name": BRAND_NAME, "url": BASE_DOMAIN},
        "publisher": {"@id": f"{BASE_DOMAIN}/#organization"},
    }
    if config['market_name']:
        webpage["about"] = {
            "@type": "Service",
            "name": f"AI Character Creation for {config['market_name']}"
        }
    schemas.append(webpage)
    
    # FAQPage
    if config['faqs']:
        faq = {
            "@context": "https://schema.org",
            "@type": "FAQPage",
            "mainEntity": [
                {
                    "@type": "Question",
                    "name": q,
                    "acceptedAnswer": {
                        "@type": "Answer",
                        "text": a
                    }
                }
                for q, a in config['faqs']
            ]
        }
        schemas.append(faq)
    
    return schemas


def build_faq_html(faqs):
    """Build a visible FAQ section with proper semantic markup."""
    html = '\n  <!-- FAQ Section -->\n'
    html += '  <section class="services" id="faq">\n'
    html += '    <div class="container container--narrow">\n'
    html += '      <div class="section-header fade-in" style="text-align: center; margin-bottom: var(--space-8);">\n'
    html += '        <span class="section-label">FAQ</span>\n'
    html += '        <h2 class="section-title">Frequently Asked Questions</h2>\n'
    html += '      </div>\n'
    html += '      <div class="fade-in" style="display: flex; flex-direction: column; gap: var(--space-4);">\n'
    
    for q, a in faqs:
        html += f'        <details style="background: var(--color-surface); border: 1px solid var(--color-border); border-radius: var(--radius-lg); overflow: hidden;">\n'
        html += f'          <summary style="padding: var(--space-5) var(--space-6); cursor: pointer; font-weight: 600; font-size: var(--text-base); list-style: none; display: flex; align-items: center; justify-content: space-between;">\n'
        html += f'            {q}\n'
        html += f'            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="var(--color-text-muted)" stroke-width="2" style="flex-shrink: 0; margin-left: var(--space-4); transition: transform 0.2s ease;"><path d="M6 9l6 6 6-6"/></svg>\n'
        html += f'          </summary>\n'
        html += f'          <div style="padding: 0 var(--space-6) var(--space-6); color: var(--color-text-muted); line-height: 1.7;">\n'
        html += f'            <p>{a}</p>\n'
        html += f'          </div>\n'
        html += f'        </details>\n'
    
    html += '      </div>\n'
    html += '    </div>\n'
    html += '  </section>\n'
    return html


def build_meta_tags(config):
    """Build complete meta tag block."""
    canonical = f"{BASE_DOMAIN}/{config['path']}/" if config['path'] else f"{BASE_DOMAIN}/"
    
    tags = f'''  <meta name="description" content="{config["description"]}">
  <meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large">
  <link rel="canonical" href="{canonical}">

  <!-- Open Graph -->
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="{BRAND_NAME}">
  <meta property="og:title" content="{config["title"]}">
  <meta property="og:description" content="{config["description"]}">
  <meta property="og:url" content="{canonical}">

  <!-- Twitter -->
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{config["title"]}">
  <meta name="twitter:description" content="{config["description"]}">'''
    return tags


def process_page(page_key, config):
    """Process a single page file."""
    if page_key == "index":
        filepath = "/home/user/workspace/character-engine/index.html"
    else:
        filepath = f"/home/user/workspace/character-engine/{config['path']}/index.html"
    
    with open(filepath, 'r') as f:
        html = f.read()
    
    # 1. Replace existing meta description and OG tags with comprehensive block
    # Remove old meta tags
    html = re.sub(r'  <meta name="description"[^>]*>\n', '', html)
    html = re.sub(r'  <meta property="og:title"[^>]*>\n', '', html)
    html = re.sub(r'  <meta property="og:description"[^>]*>\n', '', html)
    html = re.sub(r'  <meta property="og:type"[^>]*>\n', '', html)
    
    # Insert new meta tags after <title>
    meta_block = build_meta_tags(config)
    html = html.replace(
        f'<title>{config["title"]}</title>\n',
        f'<title>{config["title"]}</title>\n{meta_block}\n'
    )
    
    # If title doesn't match exactly, try a more flexible approach
    if meta_block not in html:
        # Find the title tag and insert after it
        title_match = re.search(r'<title>[^<]+</title>\n', html)
        if title_match:
            insert_pos = title_match.end()
            html = html[:insert_pos] + meta_block + '\n' + html[insert_pos:]
    
    # 2. Add JSON-LD structured data before </head>
    schemas = build_jsonld(config)
    jsonld_block = '\n'
    for schema in schemas:
        jsonld_block += f'  <script type="application/ld+json">\n{json.dumps(schema, indent=2, ensure_ascii=False)}\n  </script>\n'
    
    html = html.replace('</head>', f'{jsonld_block}</head>')
    
    # 3. Wrap body content in <main> if not already
    if '<main' not in html:
        html = html.replace('<body>\n', '<body>\n<main>\n')
        html = html.replace('  <footer', '</main>\n\n  <footer')
    
    # 4. Add FAQ section before Final CTA
    faq_html = build_faq_html(config['faqs'])
    html = html.replace('  <!-- Final CTA -->', f'{faq_html}\n  <!-- Final CTA -->')
    
    # 5. Add details/summary toggle CSS
    details_css = '''
  <style>
    details summary::-webkit-details-marker { display: none; }
    details[open] summary svg { transform: rotate(180deg); }
    details summary:hover { color: var(--color-gold); }
  </style>'''
    html = html.replace('</head>', f'{details_css}\n</head>')
    
    with open(filepath, 'w') as f:
        f.write(html)
    
    print(f"  ✓ {filepath}")


def main():
    print("Optimizing Character Engine pages for LLM/AI search...\n")
    
    for key, config in MARKETS.items():
        print(f"Processing: {key}")
        process_page(key, config)
    
    print(f"\nDone. {len(MARKETS)} pages optimized.")


if __name__ == "__main__":
    main()
