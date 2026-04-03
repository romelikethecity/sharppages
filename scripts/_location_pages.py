"""Programmatic location pages for SharpPages.
Generates /locations/{slug}/ pages targeting local search."""

LOCATIONS = [
    ("Alabama", "Birmingham", "birmingham-al"), ("Alabama", "Huntsville", "huntsville-al"), ("Alabama", "Montgomery", "montgomery-al"),
    ("Alaska", "Anchorage", "anchorage-ak"), ("Alaska", "Juneau", "juneau-ak"),
    ("Arizona", "Phoenix", "phoenix-az"), ("Arizona", "Tucson", "tucson-az"), ("Arizona", "Scottsdale", "scottsdale-az"), ("Arizona", "Mesa", "mesa-az"),
    ("Arkansas", "Little Rock", "little-rock-ar"), ("Arkansas", "Fayetteville", "fayetteville-ar"),
    ("California", "Los Angeles", "los-angeles-ca"), ("California", "San Francisco", "san-francisco-ca"), ("California", "San Diego", "san-diego-ca"), ("California", "San Jose", "san-jose-ca"), ("California", "Sacramento", "sacramento-ca"), ("California", "Irvine", "irvine-ca"),
    ("Colorado", "Denver", "denver-co"), ("Colorado", "Colorado Springs", "colorado-springs-co"), ("Colorado", "Boulder", "boulder-co"),
    ("Connecticut", "Hartford", "hartford-ct"), ("Connecticut", "New Haven", "new-haven-ct"), ("Connecticut", "Stamford", "stamford-ct"),
    ("Delaware", "Wilmington", "wilmington-de"), ("Delaware", "Dover", "dover-de"),
    ("Florida", "Miami", "miami-fl"), ("Florida", "Tampa", "tampa-fl"), ("Florida", "Orlando", "orlando-fl"), ("Florida", "Jacksonville", "jacksonville-fl"), ("Florida", "Fort Lauderdale", "fort-lauderdale-fl"),
    ("Georgia", "Atlanta", "atlanta-ga"), ("Georgia", "Savannah", "savannah-ga"), ("Georgia", "Augusta", "augusta-ga"),
    ("Hawaii", "Honolulu", "honolulu-hi"),
    ("Idaho", "Boise", "boise-id"),
    ("Illinois", "Chicago", "chicago-il"), ("Illinois", "Springfield", "springfield-il"), ("Illinois", "Naperville", "naperville-il"),
    ("Indiana", "Indianapolis", "indianapolis-in"), ("Indiana", "Fort Wayne", "fort-wayne-in"),
    ("Iowa", "Des Moines", "des-moines-ia"), ("Iowa", "Cedar Rapids", "cedar-rapids-ia"),
    ("Kansas", "Wichita", "wichita-ks"), ("Kansas", "Overland Park", "overland-park-ks"),
    ("Kentucky", "Louisville", "louisville-ky"), ("Kentucky", "Lexington", "lexington-ky"),
    ("Louisiana", "New Orleans", "new-orleans-la"), ("Louisiana", "Baton Rouge", "baton-rouge-la"),
    ("Maine", "Portland", "portland-me"), ("Maine", "Augusta", "augusta-me"),
    ("Maryland", "Baltimore", "baltimore-md"), ("Maryland", "Bethesda", "bethesda-md"), ("Maryland", "Annapolis", "annapolis-md"),
    ("Massachusetts", "Boston", "boston-ma"), ("Massachusetts", "Cambridge", "cambridge-ma"), ("Massachusetts", "Worcester", "worcester-ma"),
    ("Michigan", "Detroit", "detroit-mi"), ("Michigan", "Grand Rapids", "grand-rapids-mi"), ("Michigan", "Ann Arbor", "ann-arbor-mi"),
    ("Minnesota", "Minneapolis", "minneapolis-mn"), ("Minnesota", "Saint Paul", "saint-paul-mn"),
    ("Mississippi", "Jackson", "jackson-ms"),
    ("Missouri", "Kansas City", "kansas-city-mo"), ("Missouri", "Saint Louis", "saint-louis-mo"),
    ("Montana", "Billings", "billings-mt"), ("Montana", "Helena", "helena-mt"),
    ("Nebraska", "Omaha", "omaha-ne"), ("Nebraska", "Lincoln", "lincoln-ne"),
    ("Nevada", "Las Vegas", "las-vegas-nv"), ("Nevada", "Reno", "reno-nv"),
    ("New Hampshire", "Manchester", "manchester-nh"), ("New Hampshire", "Concord", "concord-nh"),
    ("New Jersey", "Newark", "newark-nj"), ("New Jersey", "Jersey City", "jersey-city-nj"), ("New Jersey", "Princeton", "princeton-nj"),
    ("New Mexico", "Albuquerque", "albuquerque-nm"), ("New Mexico", "Santa Fe", "santa-fe-nm"),
    ("New York", "New York City", "new-york-city-ny"), ("New York", "Buffalo", "buffalo-ny"), ("New York", "Albany", "albany-ny"), ("New York", "Rochester", "rochester-ny"),
    ("North Carolina", "Charlotte", "charlotte-nc"), ("North Carolina", "Raleigh", "raleigh-nc"), ("North Carolina", "Durham", "durham-nc"),
    ("North Dakota", "Fargo", "fargo-nd"), ("North Dakota", "Bismarck", "bismarck-nd"),
    ("Ohio", "Columbus", "columbus-oh"), ("Ohio", "Cleveland", "cleveland-oh"), ("Ohio", "Cincinnati", "cincinnati-oh"),
    ("Oklahoma", "Oklahoma City", "oklahoma-city-ok"), ("Oklahoma", "Tulsa", "tulsa-ok"),
    ("Oregon", "Portland", "portland-or"), ("Oregon", "Salem", "salem-or"), ("Oregon", "Eugene", "eugene-or"),
    ("Pennsylvania", "Philadelphia", "philadelphia-pa"), ("Pennsylvania", "Pittsburgh", "pittsburgh-pa"), ("Pennsylvania", "Harrisburg", "harrisburg-pa"),
    ("Rhode Island", "Providence", "providence-ri"),
    ("South Carolina", "Charleston", "charleston-sc"), ("South Carolina", "Columbia", "columbia-sc"),
    ("South Dakota", "Sioux Falls", "sioux-falls-sd"),
    ("Tennessee", "Nashville", "nashville-tn"), ("Tennessee", "Memphis", "memphis-tn"), ("Tennessee", "Knoxville", "knoxville-tn"),
    ("Texas", "Houston", "houston-tx"), ("Texas", "Dallas", "dallas-tx"), ("Texas", "Austin", "austin-tx"), ("Texas", "San Antonio", "san-antonio-tx"), ("Texas", "Fort Worth", "fort-worth-tx"),
    ("Utah", "Salt Lake City", "salt-lake-city-ut"), ("Utah", "Provo", "provo-ut"),
    ("Vermont", "Burlington", "burlington-vt"),
    ("Virginia", "Richmond", "richmond-va"), ("Virginia", "Virginia Beach", "virginia-beach-va"), ("Virginia", "Arlington", "arlington-va"),
    ("Washington", "Seattle", "seattle-wa"), ("Washington", "Spokane", "spokane-wa"), ("Washington", "Tacoma", "tacoma-wa"),
    ("West Virginia", "Charleston", "charleston-wv"),
    ("Wisconsin", "Milwaukee", "milwaukee-wi"), ("Wisconsin", "Madison", "madison-wi"),
    ("Wyoming", "Cheyenne", "cheyenne-wy"),
]


def build_location_body(state, city, PRICING):
    return f'''
        <section class="page-header">
            <div class="container">
                <h1 class="page-header__title">Web Design &amp; SEO in <span class="text-accent">{city}, {state}</span></h1>
                <p class="page-header__subtitle">Fast static websites, WordPress migrations, programmatic SEO, and ad campaigns for businesses in {city}. Flat fees, 90+ PageSpeed scores, you own everything.</p>
            </div>
        </section>

        <section class="content-section">
            <div class="container">
                <div class="legal-content">
                    <h2>Web Design for {city} Businesses</h2>
                    <p>Most web agencies in {city} build on WordPress or Webflow. Those sites score 55-75 on mobile PageSpeed, cost $30-100/month in hosting, and need ongoing maintenance. SharpPages builds static HTML sites that score 90-98, host for $0, and require zero maintenance.</p>
                    <p>We work with service businesses, professional firms, healthcare practices, and SaaS companies in {city} and across {state}. Every project is flat fee with no hourly billing. You own all files when the project is done.</p>

                    <h2>Services We Offer in {city}</h2>
                    <ul>
                        <li><strong>Website design and build:</strong> Static HTML/CSS sites, mobile-first, sub-1-second load times. 90+ PageSpeed scores. Starts at ${PRICING["site_standard"]["low"]:,}.</li>
                        <li><strong>WordPress migration:</strong> Same design, 3-5x faster, $0 hosting. Starts at ${PRICING["redesign_wp_sq_wix"]["low"]:,}.</li>
                        <li><strong>Webflow migration:</strong> Escape vendor lock-in. 90+ PageSpeed. Starts at ${PRICING["redesign_webflow"]["low"]:,}.</li>
                        <li><strong>SEO and programmatic content:</strong> Hundreds of keyword-targeted pages. Monthly management from ${PRICING["seo_monthly"]["low"]:,}/month.</li>
                        <li><strong>Paid social ads:</strong> Facebook and Instagram campaigns. Setup from ${PRICING["ad_setup"]["low"]:,}, management from ${PRICING["ad_monthly"]["low"]:,}/month.</li>
                    </ul>

                    <h2>Why {city} Businesses Choose SharpPages</h2>
                    <p><strong>Speed:</strong> Our sites load in under 1 second. The average agency-built site in {city} takes 3-5 seconds on mobile. Google uses page speed as a ranking factor. Faster sites rank higher.</p>
                    <p><strong>Cost:</strong> Flat fees, no hourly billing. Static hosting is $0/month. Over 3 years, a SharpPages site costs ${PRICING["site_standard"]["low"]:,}-{PRICING["site_standard"]["high"]:,} total. A WordPress site costs $8,000-25,000+ including hosting and maintenance.</p>
                    <p><strong>Results:</strong> 322 programmatic SEO pages generated 363K impressions in 30 days. Ad campaigns deliver 2x industry average CTR.</p>

                    <h2>Get Started</h2>
                    <p>Run a <a href="/audit/">free site audit</a> to see how your current site scores. Or <a href="/contact/">tell us what you need</a> and get a fixed quote within two business days. See our <a href="/pricing/">pricing</a> for all options.</p>
                </div>
            </div>
        </section>

        <section class="faq-section">
            <div class="container" style="max-width: 720px;">
                <h2>Frequently Asked Questions</h2>
                <div class="faq-list">
                    <details class="faq-item">
                        <summary class="faq-item__question">Do you work with businesses in {city} remotely?</summary>
                        <div class="faq-item__answer"><p>Yes. All projects are handled remotely via email and video calls. We work with businesses across {state} and nationwide.</p></div>
                    </details>
                    <details class="faq-item">
                        <summary class="faq-item__question">How fast can you build a website for my {city} business?</summary>
                        <div class="faq-item__answer"><p>Standard sites: 2-4 weeks. Landing pages: 1-2 weeks. Programmatic SEO sites: 4-8 weeks. Fixed quote and timeline before the project starts.</p></div>
                    </details>
                    <details class="faq-item">
                        <summary class="faq-item__question">What makes SharpPages different from other {city} agencies?</summary>
                        <div class="faq-item__answer"><p>Speed (90+ PageSpeed vs 55-75), cost (flat fees, $0 hosting), and ownership (you get all source files, no platform lock-in).</p></div>
                    </details>
                </div>
            </div>
        </section>'''
